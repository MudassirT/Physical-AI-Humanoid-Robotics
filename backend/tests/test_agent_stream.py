"""
Unit tests for SSE streaming in AgentService and POST /ask.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.chat_models import ContentChunk


@pytest.fixture
def streaming_agent():
    """
    Returns an AgentService configured for streaming tests with mocked dependencies.
    """
    from app.agent.agent_service import AgentService

    fake_chunk = ContentChunk(
        chunk_id="chunk-101",
        source_url="/ai-book/module6-bipedal-locomotion/6-2-zero-moment-point",
        original_text="The Zero-Moment Point is a criterion for dynamic balance.",
        score=0.94,
        module="module6",
        chapter="6-2-zero-moment-point",
    )

    with patch("app.agent.agent_service.genai") as mock_genai, \
         patch("app.agent.agent_service.RetrieverService") as mock_retriever_cls:

        mock_retriever = MagicMock()
        mock_retriever.retrieve_chunks.return_value = [fake_chunk]
        mock_retriever_cls.return_value = mock_retriever

        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client

        # Mock generate_content_stream to yield tokens
        def fake_stream(*args, **kwargs):
            for t in ["The ", "ZMP ", "ensures ", "stability."]:
                m = MagicMock()
                m.text = t
                yield m

        mock_client.models.generate_content_stream = MagicMock(side_effect=fake_stream)

        service = AgentService()
        service._retriever_mock = mock_retriever
        service._client_mock = mock_client
        yield service


class TestAgentStream:
    """Tests for AgentService.ask_agent_stream."""

    def test_ask_agent_stream_full_sequence(self, streaming_agent):
        events = list(streaming_agent.ask_agent_stream("What is ZMP?", module_filter="module6"))

        event_names = [e[0] for e in events]
        assert event_names == ["sources", "token", "token", "token", "token", "done"]

        # Check sources event
        sources_data = events[0][1]
        assert "sources" in sources_data
        assert "/ai-book/module6-bipedal-locomotion/6-2-zero-moment-point" in sources_data["sources"]

        # Check tokens
        tokens = [e[1]["token"] for e in events if e[0] == "token"]
        assert "".join(tokens) == "The ZMP ensures stability."

        # Check done event
        done_data = events[-1][1]
        assert done_data["done"] is True
        assert done_data["total_sources"] == 1

        # Check that retriever was called with module_filter
        streaming_agent._retriever_mock.retrieve_chunks.assert_called_once_with(
            query_text="What is ZMP?",
            top_k=5,
            module_filter="module6",
        )

    def test_ask_agent_stream_no_chunks_found(self, streaming_agent):
        streaming_agent._retriever_mock.retrieve_chunks.return_value = []

        events = list(streaming_agent.ask_agent_stream("Unknown topic"))
        event_names = [e[0] for e in events]
        assert event_names == ["sources", "token", "done"]

        # Sources empty
        assert events[0][1]["sources"] == []
        # Fallback token
        assert "could not find relevant information" in events[1][1]["token"].lower()
        # Done event
        assert events[2][1]["done"] is True
        assert events[2][1]["total_sources"] == 0

    def test_ask_agent_stream_error_handling(self, streaming_agent):
        streaming_agent._retriever_mock.retrieve_chunks.side_effect = RuntimeError("Database offline")

        events = list(streaming_agent.ask_agent_stream("Query triggering error"))
        assert len(events) == 1
        assert events[0][0] == "error"
        assert "Database offline" in events[0][1]["error"]


class TestChatRouteStreaming:
    """Tests for POST /ask streaming behavior."""

    def test_ask_with_stream_flag_returns_sse_stream(self):
        fake_events = [
            ("sources", {"sources": ["/ai-book/module1-ros2/1-1-intro"]}),
            ("token", {"token": "Hello "}),
            ("token", {"token": "Robotics"}),
            ("done", {"done": True, "total_sources": 1}),
        ]

        with patch("app.routes.chat.agent_service.ask_agent_stream", return_value=iter(fake_events)):
            client = TestClient(app)
            response = client.post("/ask", json={"query_text": "Hello", "stream": True})

            assert response.status_code == 200
            assert "text/event-stream" in response.headers.get("content-type", "")

            body = response.text
            assert "event: sources" in body
            assert 'data: {"sources": ["/ai-book/module1-ros2/1-1-intro"]}' in body
            assert "event: token" in body
            assert 'data: {"token": "Hello "}' in body
            assert 'data: {"token": "Robotics"}' in body
            assert "event: done" in body
            assert 'data: {"done": true, "total_sources": 1}' in body

    def test_ask_with_accept_header_returns_sse_stream(self):
        fake_events = [
            ("sources", {"sources": []}),
            ("token", {"token": "Test"}),
            ("done", {"done": True, "total_sources": 0}),
        ]

        with patch("app.routes.chat.agent_service.ask_agent_stream", return_value=iter(fake_events)):
            client = TestClient(app)
            response = client.post(
                "/ask",
                json={"query_text": "Hello"},
                headers={"Accept": "text/event-stream"},
            )

            assert response.status_code == 200
            assert "text/event-stream" in response.headers.get("content-type", "")
            assert "event: sources" in response.text
            assert "event: token" in response.text
            assert "event: done" in response.text
