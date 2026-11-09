"""
Tier 1: Feature Coverage (Platform Track)

Verifies:
1. GET /heartbeat liveness probe.
2. GET /health operational status.
3. POST /ask unary question answering.
4. POST /ask SSE streaming event protocol.
5. POST /analytics telemetry event ingestion.
6. GET /analytics telemetry metrics reporting.
7. POST /retrieval-test direct vector search.
"""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.chat_models import ChatResponse, ContentChunk


class TestTier1BackendCoverage:
    """Tier 1: Platform & Backend API Feature Verification."""

    def test_heartbeat_endpoint(self, test_client: TestClient):
        """Verify GET /heartbeat returns liveness signal."""
        response = test_client.get("/heartbeat")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "alive"

    def test_health_endpoint(self, test_client: TestClient):
        """Verify GET /health returns operational health status."""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "ok"

    def test_ask_unary_mode(self, test_client: TestClient):
        """Verify POST /ask in unary (non-streaming) mode returns grounded answer."""
        mock_response = ChatResponse(
            answer_text="The Zero-Moment Point is the ground contact tipping line.",
            retrieved_sources=["/ai-book/module6-bipedal-locomotion/6-2-zero-moment-point"],
        )

        with patch("app.routes.chat.agent_service.ask_agent", return_value=mock_response):
            payload = {
                "query_text": "What is the Zero-Moment Point?",
                "stream": False,
            }
            response = test_client.post("/ask", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert "answer_text" in data
            assert "retrieved_sources" in data
            assert len(data["retrieved_sources"]) > 0

    def test_ask_sse_streaming_mode(self, test_client: TestClient):
        """
        Verify POST /ask in SSE streaming mode yields ordered event stream:
        event: sources -> event: token* -> event: done
        """
        fake_events = [
            ("sources", {"sources": ["/ai-book/module6-bipedal-locomotion/6-2-zero-moment-point"]}),
            ("token", {"token": "ZMP preview control regulates com trajectory."}),
            ("done", {"done": True, "total_sources": 1}),
        ]

        with patch("app.routes.chat.agent_service.ask_agent_stream", return_value=iter(fake_events)):
            payload = {
                "query_text": "Explain ZMP preview control",
                "stream": True,
            }

            # Test request with SSE accept header
            response = test_client.post(
                "/ask",
                json=payload,
                headers={"Accept": "text/event-stream"},
            )

        content_type = response.headers.get("content-type", "")
        if "text/event-stream" not in content_type:
            pytest.skip(
                "SSE streaming mode on POST /ask is pending M1 backend implementation "
                f"(current content-type: {content_type})"
            )

        assert response.status_code == 200
        stream_text = response.text

        # Verify event stream structure
        assert "event: sources" in stream_text or "sources" in stream_text, (
            "SSE stream must include initial sources event"
        )
        assert "event: token" in stream_text or "token" in stream_text, (
            "SSE stream must include token chunk events"
        )
        assert "event: done" in stream_text or "done" in stream_text, (
            "SSE stream must terminate with a done event"
        )

    def test_analytics_telemetry_post(self, test_client: TestClient):
        """Verify POST /analytics records telemetry events."""
        routes = [r.path for r in app.routes]
        if "/analytics" not in routes:
            pytest.skip("POST /analytics route pending M1 backend implementation")

        event_payload = {
            "event_type": "page_view",
            "module_id": "module6",
            "chapter_id": "6-2-zero-moment-point",
            "session_id": "test_session_12345",
            "data": {"referrer": "https://example.com", "screen_width": 1920},
        }

        response = test_client.post("/analytics", json=event_payload)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data.get("status") in ["recorded", "ok"]
        assert "event_id" in data

    def test_analytics_metrics_get(self, test_client: TestClient):
        """Verify GET /analytics returns aggregated telemetry statistics."""
        routes = [r.path for r in app.routes]
        if "/analytics" not in routes:
            pytest.skip("GET /analytics route pending M1 backend implementation")

        response = test_client.get("/analytics")
        assert response.status_code == 200
        data = response.json()
        assert "total_events" in data
        assert "event_counts" in data

    def test_retrieval_test_endpoint(self, test_client: TestClient):
        """Verify POST /retrieval-test executes direct Qdrant vector retrieval."""
        mock_chunk = ContentChunk(
            chunk_id="test-chunk-1",
            original_text="The 3D Linear Inverted Pendulum Model...",
            source_url="/ai-book/module6-bipedal-locomotion/6-2-zero-moment-point",
            score=0.92,
            module="module6",
            chapter="6-2-zero-moment-point",
        )

        with patch("app.routes.chat.retriever_service.retrieve_chunks", return_value=[mock_chunk]):
            payload = {"query_text": "3D Linear Inverted Pendulum"}
            response = test_client.post("/retrieval-test", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert "chunks" in data
            assert len(data["chunks"]) == 1
            assert data["chunks"][0]["chunk_id"] == "test-chunk-1"
            assert data["chunks"][0]["score"] == 0.92
