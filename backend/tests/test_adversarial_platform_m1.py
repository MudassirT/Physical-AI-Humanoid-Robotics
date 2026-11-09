"""
Adversarial Stress Test Suite for Backend Platform Upgrades (Milestone M1).

Covers:
1. SSE streaming protocol robustness (framing, double-newlines, error events, early disconnect, unary fallback).
2. /analytics telemetry endpoint (high-concurrency rapid fire, line corruption immunity, validation edge cases, aggregate metrics resilience).
3. Qdrant module filtering (non-existent module, 'all', None, dash normalization) & Incremental Ingestion lifecycle (new, modified, untouched, deleted files).
"""

import concurrent.futures
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.retriever.retriever_service import RetrieverService
from ingest_docs import (
    compute_file_hash,
    plan_ingestion,
    run_ingestion,
)

# ===========================================================================
# 1. SSE Streaming Protocol Robustness
# ===========================================================================

class TestSSEStreamingAdversarial:
    """Adversarial challenge tests for SSE streaming protocol."""

    def test_sse_wire_format_exact_compliance(self):
        """
        Verify that the SSE stream strictly adheres to the SSE specification:
        - Content-Type is text/event-stream
        - Framing is exact: 'event: <type>\ndata: <json>\n\n' with double newlines
        - Sequence: sources -> token* -> done
        """
        fake_events = [
            ("sources", {"sources": ["/ai-book/module1-ros2/1-1-intro", "/ai-book/module2-digital-twin/2-1-intro"]}),
            ("token", {"token": "Alpha "}),
            ("token", {"token": "Beta "}),
            ("token", {"token": "Gamma."}),
            ("done", {"done": True, "total_sources": 2}),
        ]

        with patch("app.routes.chat.agent_service.ask_agent_stream", return_value=iter(fake_events)):
            client = TestClient(app)
            response = client.post("/ask", json={"query_text": "Stream test", "stream": True})

            assert response.status_code == 200
            assert "text/event-stream" in response.headers.get("content-type", "")
            assert response.headers.get("cache-control") == "no-cache"
            assert response.headers.get("connection") == "keep-alive"
            assert response.headers.get("x-accel-buffering") == "no"

            raw_text = response.text
            # Verify double-newline separation
            blocks = [b for b in raw_text.split("\n\n") if b.strip()]
            assert len(blocks) == 5, f"Expected 5 event blocks separated by double newlines, got {len(blocks)}"

            # Inspect individual block structure
            parsed_events = []
            for block in blocks:
                lines = block.strip().split("\n")
                assert len(lines) == 2, f"Each SSE block must have event and data line: {lines}"
                assert lines[0].startswith("event: "), f"Missing event header: {lines[0]}"
                assert lines[1].startswith("data: "), f"Missing data header: {lines[1]}"

                event_type = lines[0].replace("event: ", "").strip()
                event_data = json.loads(lines[1].replace("data: ", "").strip())
                parsed_events.append((event_type, event_data))

            assert parsed_events[0][0] == "sources"
            assert parsed_events[0][1]["sources"] == ["/ai-book/module1-ros2/1-1-intro", "/ai-book/module2-digital-twin/2-1-intro"]

            tokens = [data["token"] for ev, data in parsed_events if ev == "token"]
            assert "".join(tokens) == "Alpha Beta Gamma."

            assert parsed_events[-1][0] == "done"
            assert parsed_events[-1][1]["done"] is True
            assert parsed_events[-1][1]["total_sources"] == 2

    def test_sse_error_event_formatting_on_stream_failure(self):
        """
        Verify that if generator fails mid-stream, an 'event: error\ndata: {"error": "..."}\n\n'
        frame is cleanly formatted without crashing the HTTP server.
        """
        def faulty_stream(*args, **kwargs):
            yield ("sources", {"sources": []})
            yield ("token", {"token": "Partial output before crash"})
            raise RuntimeError("Gemini API connection abruptly severed")

        with patch("app.routes.chat.agent_service.ask_agent_stream", side_effect=faulty_stream):
            client = TestClient(app)
            response = client.post("/ask", json={"query_text": "Error test", "stream": True})

            assert response.status_code == 200
            raw_text = response.text
            assert "event: error" in raw_text
            assert "Gemini API connection abruptly severed" in raw_text

            # Verify the error block ends with double newlines
            error_part = raw_text.split("event: error")[1]
            assert "\ndata: " in error_part
            assert error_part.endswith("\n\n")

    def test_sse_client_early_disconnect_resilience(self):
        """
        Simulate a client that abruptly terminates reading after the first chunk.
        Verify that the server does not deadlock, hang, or raise unhandled exceptions.
        """
        fake_events = (
            [("sources", {"sources": ["/ai-book/module1/1-1"]})]
            + [("token", {"token": f"Token-{i} "}) for i in range(50)]
            + [("done", {"done": True, "total_sources": 1})]
        )

        with patch("app.routes.chat.agent_service.ask_agent_stream", return_value=iter(fake_events)):
            client = TestClient(app)
            # Use stream() context manager to consume only part of the stream and abort
            with client.stream("POST", "/ask", json={"query_text": "Disconnect test", "stream": True}) as stream_resp:
                assert stream_resp.status_code == 200
                chunks_read = 0
                for line in stream_resp.iter_lines():
                    if line:
                        chunks_read += 1
                    if chunks_read >= 2:
                        break  # Client disconnects abruptly

            # Client disconnected cleanly, subsequent requests should still function normally
            health_res = client.get("/health")
            assert health_res.status_code == 200
            assert health_res.json()["status"] == "ok"

    def test_unary_mode_fallback_stream_false(self):
        """
        Verify that when stream=False (or stream not requested), a standard ChatResponse JSON
        is returned with answer_text and retrieved_sources.
        """
        from app.schemas.chat_models import ChatResponse

        fake_chat_response = ChatResponse(
            answer_text="ROS 2 uses DDS as its middleware layer.",
            retrieved_sources=["/ai-book/module1-ros2/1-1-intro"],
        )

        with patch("app.routes.chat.agent_service.ask_agent", return_value=fake_chat_response):
            client = TestClient(app)

            # 1. Explicit stream=False
            res1 = client.post(
                "/ask",
                json={"query_text": "What does ROS 2 use?", "stream": False},
                headers={"Accept": "application/json"},
            )
            assert res1.status_code == 200
            assert res1.headers.get("content-type", "").startswith("application/json")
            data1 = res1.json()
            assert data1["answer_text"] == "ROS 2 uses DDS as its middleware layer."
            assert data1["retrieved_sources"] == ["/ai-book/module1-ros2/1-1-intro"]

            # 2. Omitted stream field (defaults to False)
            res2 = client.post(
                "/ask",
                json={"query_text": "What does ROS 2 use?"},
                headers={"Accept": "application/json"},
            )
            assert res2.status_code == 200
            assert res2.headers.get("content-type", "").startswith("application/json")

    def test_sse_tokens_with_newlines_and_special_characters(self):
        """
        Verify that tokens containing newlines, markdown code blocks, or unicode
        do not break the SSE event/data framing due to JSON payload serialization.
        """
        multiline_tokens = [
            ("sources", {"sources": []}),
            ("token", {"token": "```python\ndef test():\n    return 42\n```\n\n"}),
            ("token", {"token": "Unicode test: 🤖 🦾 🚀\nLine 2\n"}),
            ("done", {"done": True, "total_sources": 0}),
        ]

        with patch("app.routes.chat.agent_service.ask_agent_stream", return_value=iter(multiline_tokens)):
            client = TestClient(app)
            response = client.post("/ask", json={"query_text": "Code snippet", "stream": True})

            assert response.status_code == 200
            raw_text = response.text

            # Split by double newline delimiter
            blocks = [b for b in raw_text.split("\n\n") if b.strip()]
            assert len(blocks) == 4

            # Verify each block has exactly 2 lines (event and data)
            for block in blocks:
                lines = block.strip().split("\n")
                assert len(lines) == 2
                assert lines[0].startswith("event: ")
                assert lines[1].startswith("data: ")
                # Data must be valid JSON
                payload = json.loads(lines[1][6:])
                assert isinstance(payload, dict)


# ===========================================================================
# 2. /analytics Telemetry Endpoint Robustness & Concurrency
# ===========================================================================

class TestAnalyticsAdversarial:
    """Adversarial challenge tests for /analytics telemetry endpoint."""

    @pytest.fixture
    def isolated_analytics_log(self, tmp_path: Path):
        log_file = tmp_path / "adversarial_analytics.jsonl"
        with patch("app.routes.analytics.ANALYTICS_LOG_PATH", log_file), \
             patch("app.routes.analytics.get_analytics_file_path", return_value=log_file):
            yield log_file

    def test_analytics_high_concurrency_rapid_fire(self, isolated_analytics_log: Path):
        """
        Stress test: Rapid-fire 200 concurrent POST requests from multiple threads.
        Verify that no JSONL lines are interleaved or corrupted.
        """
        client = TestClient(app)
        num_requests = 200
        concurrency = 25

        def send_request(idx: int) -> int:
            payload = {
                "event_type": "query" if idx % 2 == 0 else "page_view",
                "session_id": f"sess-{idx:04d}",
                "module_id": f"module{(idx % 12) + 1}",
                "chapter_id": f"ch-{(idx % 5) + 1}",
                "data": {"payload_id": idx, "filler": "X" * 100},
            }
            res = client.post("/analytics", json=payload)
            return res.status_code

        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            status_codes = list(executor.map(send_request, range(num_requests)))

        # All requests must succeed with 200
        assert all(code == 200 for code in status_codes), f"Some requests failed: {set(status_codes)}"

        # Validate file integrity
        assert isolated_analytics_log.exists()
        raw_content = isolated_analytics_log.read_text(encoding="utf-8")
        lines = [ln for ln in raw_content.splitlines() if ln.strip()]

        assert len(lines) == num_requests, f"Expected {num_requests} lines, got {len(lines)}"

        # Parse every line to verify zero line corruption or interleaving
        seen_event_ids = set()
        seen_payload_ids = set()
        for idx, line in enumerate(lines):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as err:
                pytest.fail(f"Line {idx} corrupted by thread race condition: '{line}' — {err}")

            assert "event_id" in record
            assert record["event_id"] not in seen_event_ids, f"Duplicate event_id detected: {record['event_id']}"
            seen_event_ids.add(record["event_id"])

            payload_id = record["data"]["payload_id"]
            seen_payload_ids.add(payload_id)

        assert len(seen_payload_ids) == num_requests

    def test_analytics_validation_oversized_payloads(self, isolated_analytics_log: Path):
        """
        Verify validation rules reject oversized payload fields (max_length constraints).
        """
        client = TestClient(app)

        # 1. session_id > 128 chars
        res = client.post("/analytics", json={
            "event_type": "page_view",
            "session_id": "s" * 129,
        })
        assert res.status_code == 422

        # 2. module_id > 64 chars
        res = client.post("/analytics", json={
            "event_type": "page_view",
            "module_id": "m" * 65,
        })
        assert res.status_code == 422

        # 3. chapter_id > 128 chars
        res = client.post("/analytics", json={
            "event_type": "page_view",
            "chapter_id": "c" * 129,
        })
        assert res.status_code == 422

    def test_analytics_validation_missing_and_malformed(self, isolated_analytics_log: Path):
        """
        Verify validation rules reject missing required fields and malformed payloads.
        """
        client = TestClient(app)

        # 1. Missing event_type
        res = client.post("/analytics", json={"module_id": "module1"})
        assert res.status_code == 422

        # 2. Empty JSON body
        res = client.post("/analytics", json={})
        assert res.status_code == 422

        # 3. Non-dict data field
        res = client.post("/analytics", json={
            "event_type": "page_view",
            "data": "should_be_a_dict_not_a_string",
        })
        assert res.status_code == 422

    def test_analytics_unknown_event_types_handled(self, isolated_analytics_log: Path):
        """
        Verify arbitrary string event types are accepted and counted properly in GET /analytics.
        """
        client = TestClient(app)

        res = client.post("/analytics", json={
            "event_type": "custom_gesture_event",
            "module_id": "module7",
            "data": {"gesture": "pinch"},
        })
        assert res.status_code == 200

        summary_res = client.get("/analytics")
        assert summary_res.status_code == 200
        summary = summary_res.json()
        assert summary["total_events"] == 1
        assert summary["event_counts"]["custom_gesture_event"] == 1

    def test_analytics_summary_corrupted_lines_resilience(self, isolated_analytics_log: Path):
        """
        Verify that GET /analytics gracefully skips corrupted lines (e.g. from partial disk write)
        without returning a 500 internal server error.
        """
        client = TestClient(app)

        # Write valid line, corrupted lines, empty lines, and valid line
        isolated_analytics_log.parent.mkdir(parents=True, exist_ok=True)
        with open(isolated_analytics_log, "w", encoding="utf-8") as f:
            f.write(json.dumps({"event_type": "page_view", "module_id": "module1"}) + "\n")
            f.write("{this is broken non json garbage line\n")
            f.write("\n\n")
            f.write('{"truncated_json": \n')
            f.write(json.dumps({"event_type": "query", "module_id": "module1"}) + "\n")

        res = client.get("/analytics")
        assert res.status_code == 200
        summary = res.json()
        assert summary["total_events"] == 2
        assert summary["total_queries"] == 1
        assert summary["event_counts"]["page_view"] == 1
        assert summary["event_counts"]["query"] == 1

    def test_analytics_summary_non_numeric_and_null_quiz_scores(self, isolated_analytics_log: Path):
        """
        Verify that GET /analytics calculates average_quiz_scores robustly even when
        data contains non-numeric, None, or missing scores.
        """
        client = TestClient(app)

        events = [
            {"event_type": "quiz_score", "chapter_id": "ch-1", "data": {"score": 80.0}},
            {"event_type": "quiz_score", "chapter_id": "ch-1", "data": {"score": 100.0}},
            {"event_type": "quiz_score", "chapter_id": "ch-1", "data": {"score": "not_a_float"}},
            {"event_type": "quiz_score", "chapter_id": "ch-1", "data": {"score": None}},
            {"event_type": "quiz_score", "chapter_id": "ch-1", "data": {}},
            {"event_type": "quiz_score", "chapter_id": "ch-2", "data": {"score": 75}},
        ]

        for ev in events:
            res = client.post("/analytics", json=ev)
            assert res.status_code == 200

        summary = client.get("/analytics").json()
        # ch-1 average should be (80 + 100) / 2 = 90.0 (non-numeric ignored)
        assert summary["average_quiz_scores"]["ch-1"] == 90.0
        assert summary["average_quiz_scores"]["ch-2"] == 75.0


# ===========================================================================
# 3. Qdrant Module Filtering and Incremental Ingestion
# ===========================================================================

class TestQdrantFilteringAndIngestionAdversarial:
    """Adversarial challenge tests for Qdrant module filtering and incremental ingestion."""

    @pytest.fixture
    def mock_retriever(self):
        with patch("app.retriever.retriever_service.QdrantClient") as mock_qdrant_cls, \
             patch("app.retriever.retriever_service.EmbeddingGenerator") as mock_embed_cls:

            mock_qdrant = MagicMock()
            mock_qdrant_cls.return_value = mock_qdrant

            mock_embed = MagicMock()
            mock_embed.generate_embeddings.return_value = [[0.05] * 1024]
            mock_embed_cls.return_value = mock_embed

            retriever = RetrieverService()
            retriever.qdrant_client = mock_qdrant
            retriever.embedding_generator = mock_embed
            yield retriever, mock_qdrant

    def test_qdrant_module_filter_nonexistent_module(self, mock_retriever):
        """
        Query with non-existent module filter (e.g. module99).
        Qdrant should receive the module filter and return empty list cleanly.
        """
        retriever, mock_qdrant = mock_retriever
        mock_qdrant.query_points.return_value = []

        chunks = retriever.retrieve_chunks("What is kinematics?", module_filter="module99")

        assert chunks == []
        call_kwargs = mock_qdrant.query_points.call_args.kwargs
        q_filter = call_kwargs.get("query_filter")
        assert q_filter is not None
        assert len(q_filter.must) == 1
        assert q_filter.must[0].key == "module"
        assert q_filter.must[0].match.value == "module99"

    def test_qdrant_module_filter_all_and_none_variations(self, mock_retriever):
        """
        Verify that module_filter='all', 'ALL', 'none', '', and None all result in query_filter=None (global search).
        """
        retriever, mock_qdrant = mock_retriever
        mock_qdrant.query_points.return_value = []

        for f_val in [None, "all", "ALL", "None", "", "   "]:
            retriever.retrieve_chunks("Test query", module_filter=f_val)
            call_kwargs = mock_qdrant.query_points.call_args.kwargs
            assert call_kwargs.get("query_filter") is None, f"Expected None filter for module_filter='{f_val}'"

    def test_qdrant_module_filter_dash_and_whitespace_normalization(self, mock_retriever):
        """
        Verify module_filter strings like '  module6-bipedal-locomotion  ' normalize to 'module6'.
        """
        retriever, mock_qdrant = mock_retriever
        mock_qdrant.query_points.return_value = []

        retriever.retrieve_chunks("Bipedal balance", module_filter="  module6-bipedal-locomotion  ")
        call_kwargs = mock_qdrant.query_points.call_args.kwargs
        q_filter = call_kwargs.get("query_filter")
        assert q_filter is not None
        assert q_filter.must[0].match.value == "module6"

    def test_incremental_ingestion_lifecycle_simulation(self, tmp_path: Path):
        """
        Adversarial test for incremental ingestion change-detection:
        - 1 untouched file (hash unchanged) -> MUST NOT trigger embedding generation
        - 1 modified file (hash changed) -> MUST delete old points and generate new embeddings
        - 1 new file (not in manifest) -> MUST generate new embeddings
        - 1 deleted file (in manifest but gone from disk) -> MUST delete old points
        """
        repo_root = tmp_path / "repo"
        backend_dir = repo_root / "backend"
        docs_dir = repo_root / "ai-book-docs"
        mod1 = docs_dir / "module1-ros2"
        mod1.mkdir(parents=True)
        backend_dir.mkdir(parents=True)

        # File 1: Untouched
        f_untouched = mod1 / "1-1-untouched.mdx"
        f_untouched.write_text("# Untouched Chapter\nUnchanged text content.", encoding="utf-8")
        untouched_hash = compute_file_hash(f_untouched)

        # File 2: Modified
        f_modified = mod1 / "1-2-modified.mdx"
        f_modified.write_text("# Modified Chapter\nBrand new updated text content.", encoding="utf-8")
        modified_hash = compute_file_hash(f_modified)

        # File 3: New
        f_new = mod1 / "1-3-new.mdx"
        f_new.write_text("# New Chapter\nFresh newly created chapter.", encoding="utf-8")

        # Initial manifest contains: untouched, modified (with old hash), and deleted
        initial_manifest = {
            "module1-ros2/1-1-untouched.mdx": {
                "sha256": untouched_hash,
                "chunk_ids": ["point-untouched-1"],
                "count": 1,
            },
            "module1-ros2/1-2-modified.mdx": {
                "sha256": "old_obsolete_sha256_hash",
                "chunk_ids": ["point-modified-old-1", "point-modified-old-2"],
                "count": 2,
            },
            "module1-ros2/1-4-deleted.mdx": {
                "sha256": "deleted_file_hash",
                "chunk_ids": ["point-deleted-1"],
                "count": 1,
            },
        }

        # 1. Verify plan_ingestion classification
        _, new_files, mod_files, unchanged_files, del_files = plan_ingestion(
            docs_dir=docs_dir,
            manifest=initial_manifest,
        )

        assert new_files == ["module1-ros2/1-3-new.mdx"]
        assert mod_files == ["module1-ros2/1-2-modified.mdx"]
        assert unchanged_files == ["module1-ros2/1-1-untouched.mdx"]
        assert del_files == ["module1-ros2/1-4-deleted.mdx"]

        # 2. Run run_ingestion with mocks and inspect vector store and embedding calls
        manifest_file = backend_dir / ".ingest_manifest.json"
        manifest_file.write_text(json.dumps(initial_manifest), encoding="utf-8")

        with patch("ingest_docs.VectorStore") as mock_vs_cls, \
             patch("ingest_docs.EmbeddingGenerator") as mock_embed_cls, \
             patch("ingest_docs.backend_dir", backend_dir):

            mock_vs = MagicMock()
            mock_client = MagicMock()
            mock_client.get_collections.return_value.collections = [MagicMock(name="rag_agent_docs")]
            mock_vs.client = mock_client
            mock_vs.collection_name = "rag_agent_docs"
            mock_vs_cls.return_value = mock_vs

            mock_embed = MagicMock()
            mock_embed.generate_embeddings.return_value = [[0.123] * 1024]
            mock_embed_cls.return_value = mock_embed

            run_ingestion(
                incremental=True,
                force=False,
                dry_run=False,
                manifest_path=manifest_file,
            )

            # Check deletions: deleted file points and modified file old points must be removed
            deleted_point_calls = mock_client.delete.call_args_list
            deleted_ids_flattened = []
            for call in deleted_point_calls:
                points_selector = call.kwargs.get("points_selector")
                if points_selector:
                    deleted_ids_flattened.extend(points_selector.points)

            assert "point-deleted-1" in deleted_ids_flattened, "Obsolete points for deleted file must be deleted"
            assert "point-modified-old-1" in deleted_ids_flattened, "Old points for modified file must be deleted"
            assert "point-modified-old-2" in deleted_ids_flattened, "Old points for modified file must be deleted"
            assert "point-untouched-1" not in deleted_ids_flattened, "Points for untouched file must NEVER be deleted"

            # Check embeddings: EmbeddingGenerator called only for new and modified
            embedded_texts = []
            for call in mock_embed.generate_embeddings.call_args_list:
                batch = call.args[0] if call.args else call.kwargs.get("texts", [])
                embedded_texts.extend(batch)

            # Verify untouched text was NOT passed to embedding generator
            for text in embedded_texts:
                assert "Unchanged text content" not in text, "Untouched file content was recomputed for embeddings!"

            # Verify new and modified text WAS passed to embedding generator
            assert any("Brand new updated text content" in t for t in embedded_texts), "Modified content was not embedded"
            assert any("Fresh newly created chapter" in t for t in embedded_texts), "New content was not embedded"

            # Verify final manifest state on disk
            final_manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
            assert "module1-ros2/1-4-deleted.mdx" not in final_manifest, "Deleted file still in manifest"
            assert "module1-ros2/1-1-untouched.mdx" in final_manifest, "Untouched file missing from manifest"
            assert "module1-ros2/1-2-modified.mdx" in final_manifest
            assert final_manifest["module1-ros2/1-2-modified.mdx"]["sha256"] == modified_hash
            assert "module1-ros2/1-3-new.mdx" in final_manifest

    def test_incremental_ingestion_corrupted_manifest_resilience(self, tmp_path: Path):
        """
        Verify that a corrupted or truncated manifest file is handled gracefully
        by starting fresh instead of crashing with JSONDecodeError.
        """
        repo_root = tmp_path / "repo2"
        backend_dir = repo_root / "backend"
        docs_dir = repo_root / "ai-book-docs"
        mod = docs_dir / "module1"
        mod.mkdir(parents=True)
        backend_dir.mkdir(parents=True)

        f = mod / "doc.mdx"
        f.write_text("# Doc\nContent", encoding="utf-8")

        corrupt_manifest = backend_dir / ".ingest_manifest.json"
        corrupt_manifest.write_text("{this is corrupted invalid json", encoding="utf-8")

        with patch("ingest_docs.VectorStore") as mock_vs_cls, \
             patch("ingest_docs.EmbeddingGenerator") as mock_embed_cls, \
             patch("ingest_docs.backend_dir", backend_dir):

            mock_vs = MagicMock()
            mock_client = MagicMock()
            mock_client.get_collections.return_value.collections = [MagicMock(name="rag_agent_docs")]
            mock_vs.client = mock_client
            mock_vs.collection_name = "rag_agent_docs"
            mock_vs_cls.return_value = mock_vs

            mock_embed = MagicMock()
            mock_embed.generate_embeddings.return_value = [[0.1] * 1024]
            mock_embed_cls.return_value = mock_embed

            # Should not raise exception
            run_ingestion(incremental=True, manifest_path=corrupt_manifest)

            # Updated manifest must now be valid JSON
            new_manifest_data = json.loads(corrupt_manifest.read_text(encoding="utf-8"))
            assert "module1/doc.mdx" in new_manifest_data

    def test_qdrant_module_filter_injection_safety(self, mock_retriever):
        """
        Verify that arbitrary strings with SQL or shell syntax are treated as exact string matches
        and do not cause injection or crash. Also confirms hyphen splitting behavior.
        """
        retriever, mock_qdrant = mock_retriever
        mock_qdrant.query_points.return_value = []

        # 1. Without hyphen
        injection_attempt_1 = "module1' OR '1'='1"
        retriever.retrieve_chunks("Test", module_filter=injection_attempt_1)
        call_kwargs1 = mock_qdrant.query_points.call_args.kwargs
        q_filter1 = call_kwargs1.get("query_filter")
        assert q_filter1 is not None
        assert q_filter1.must[0].match.value == injection_attempt_1

        # 2. With hyphen: splits at first hyphen per normalization rule
        injection_attempt_2 = "module1' OR 1=1; --"
        retriever.retrieve_chunks("Test", module_filter=injection_attempt_2)
        call_kwargs2 = mock_qdrant.query_points.call_args.kwargs
        q_filter2 = call_kwargs2.get("query_filter")
        assert q_filter2 is not None
        assert q_filter2.must[0].match.value == "module1' OR 1=1; "
