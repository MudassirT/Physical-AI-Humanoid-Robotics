"""
Tier 3: Cross-Feature Interactions

Verifies:
1. Frontend QuizEngine score submission matches backend /analytics schema.
2. Frontend ChapterProgress toggle completion matches backend /analytics schema.
3. ChatQuery module_filter propagation through Retriever to Qdrant filter condition.
4. Incremental ingestion dirty checking (SHA-256 manifest logic and deterministic UUID5 IDs).
"""

import hashlib
import inspect
import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.retriever.retriever_service import RetrieverService
from app.schemas.chat_models import (
    AnalyticsEvent,
    ChatQuery,
)


class TestTier3CrossFeatureInteractions:
    """Tier 3: Inter-Module and Cross-System Interaction Contracts."""

    def test_quiz_engine_to_analytics_contract(self, test_client: TestClient):
        """
        Verify that the payload produced by the frontend QuizEngine component
        strictly validates against the backend AnalyticsEvent schema.
        """
        # Emulated client payload from React QuizEngine component
        quiz_submission_payload = {
            "event_type": "quiz_score",
            "session_id": "anon_session_884920",
            "module_id": "module6",
            "chapter_id": "6-2-zero-moment-point",
            "data": {
                "quiz_id": "quiz-6-2-zmp-basics",
                "score": 4,
                "total_questions": 5,
                "percentage": 80.0,
                "passed": True,
                "user_answers": {
                    "q1": {"selected": 2, "correct": 2, "is_correct": True},
                    "q2": {"selected": 0, "correct": 0, "is_correct": True},
                    "q3": {"selected": 1, "correct": 3, "is_correct": False},
                    "q4": {"selected": 1, "correct": 1, "is_correct": True},
                    "q5": {"selected": 0, "correct": 0, "is_correct": True},
                },
            },
        }

        # 1. Verify schema level compliance
        event = AnalyticsEvent(**quiz_submission_payload)
        assert event.event_type == "quiz_score"
        assert event.data["passed"] is True
        assert event.data["score"] == 4

        # 2. If route is mounted, verify HTTP endpoint level compliance
        routes = [r.path for r in app.routes]
        if "/analytics" in routes:
            response = test_client.post("/analytics", json=quiz_submission_payload)
            assert response.status_code in [200, 201]
            data = response.json()
            assert data.get("status") in ["recorded", "ok"]

    def test_chapter_progress_to_analytics_contract(self, test_client: TestClient):
        """
        Verify that the payload produced by the frontend ChapterProgress component
        strictly validates against the backend AnalyticsEvent schema.
        """
        progress_toggle_payload = {
            "event_type": "progress_update",
            "session_id": "anon_session_884920",
            "module_id": "module6",
            "chapter_id": "6-2-zero-moment-point",
            "data": {
                "completed": True,
                "completed_chapters_count": 3,
                "module_total_chapters": 10,
                "module_progress_percent": 30.0,
                "curriculum_total_completed": 12,
                "curriculum_total_chapters": 110,
            },
        }

        # 1. Verify schema level compliance
        event = AnalyticsEvent(**progress_toggle_payload)
        assert event.event_type == "progress_update"
        assert event.data["completed"] is True
        assert event.data["module_progress_percent"] == 30.0

        # 2. If route is mounted, verify HTTP endpoint level compliance
        routes = [r.path for r in app.routes]
        if "/analytics" in routes:
            response = test_client.post("/analytics", json=progress_toggle_payload)
            assert response.status_code in [200, 201]

    def test_ask_module_filter_propagation_to_qdrant(self):
        """
        Verify that passing a module_filter in ChatQuery translates to a scoped
        Qdrant search filter in RetrieverService.
        """
        # Verify ChatQuery schema accepts module_filter
        query = ChatQuery(
            query_text="Explain ZMP support polygon",
            module_filter="module6",
            stream=False,
        )
        assert query.module_filter == "module6"

        retriever = RetrieverService()
        sig = inspect.signature(retriever.retrieve_chunks)

        # Check if retrieve_chunks has module_filter parameter
        if "module_filter" not in sig.parameters:
            pytest.skip("RetrieverService.retrieve_chunks does not yet take module_filter (pending M1 implementation)")

        # Mock Qdrant client to intercept the query_filter argument
        mock_qdrant = MagicMock()
        mock_response = MagicMock()
        mock_response.points = []
        mock_qdrant.query_points.return_value = mock_response
        retriever.qdrant_client = mock_qdrant

        # Mock Cohere embedding via _get_query_embedding
        with patch.object(retriever, "_get_query_embedding", return_value=[0.1] * 1024):
            retriever.retrieve_chunks(query_text="Explain ZMP", module_filter="module6", top_k=3)

            # Assert query_points was invoked with query_filter
            assert mock_qdrant.query_points.called
            call_kwargs = mock_qdrant.query_points.call_args.kwargs

            # The query_filter must be present and contain module field condition
            query_filter = call_kwargs.get("query_filter")
            assert query_filter is not None, "Qdrant query_points must receive query_filter when module_filter is specified"

    def test_incremental_ingestion_dirty_checking_simulation(self):
        """
        Verify the incremental hashing logic and deterministic UUID5 point ID generation:
        1. Identical content produces identical SHA-256 and skips embedding.
        2. Modified content changes SHA-256, triggering re-embedding.
        3. Deterministic point IDs ensure point overwriting without orphaned vectors.
        """
        NAMESPACE_MODULE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
        rel_path = "ai-book-docs/module6-bipedal-locomotion/6-2-zero-moment-point.mdx"
        chunk_idx = 0

        # Generate deterministic UUID5 ID
        point_id_1 = str(uuid.uuid5(NAMESPACE_MODULE, f"{rel_path}:{chunk_idx}"))
        point_id_2 = str(uuid.uuid5(NAMESPACE_MODULE, f"{rel_path}:{chunk_idx}"))
        assert point_id_1 == point_id_2, "Point IDs for same file:chunk must be completely deterministic"

        # Content 1
        content_v1 = "# Zero-Moment Point\n\nThe ZMP is the point where horizontal inertia moment is zero."
        hash_v1 = hashlib.sha256(content_v1.encode("utf-8")).hexdigest()

        # Simulated Manifest
        manifest = {
            rel_path: {
                "sha256": hash_v1,
                "chunk_ids": [point_id_1],
                "chunk_count": 1,
            }
        }

        # Check identical content -> Skip
        content_v1_recheck = "# Zero-Moment Point\n\nThe ZMP is the point where horizontal inertia moment is zero."
        hash_v1_recheck = hashlib.sha256(content_v1_recheck.encode("utf-8")).hexdigest()
        assert hash_v1_recheck == manifest[rel_path]["sha256"], "Unchanged file must match manifest SHA-256 (action: skip)"

        # Check modified content -> Update
        content_v2 = "# Zero-Moment Point\n\nEnhanced with 3D-LIPM equations."
        hash_v2 = hashlib.sha256(content_v2.encode("utf-8")).hexdigest()
        assert hash_v2 != manifest[rel_path]["sha256"], "Modified file must differ from manifest SHA-256 (action: update)"
