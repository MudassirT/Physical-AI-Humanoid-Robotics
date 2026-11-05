"""
Unit tests for app.routes.chat

All external services (AgentService, RetrieverService) are mocked so these
tests run without any network calls or API keys.
"""

from contextlib import contextmanager
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Helpers — build a TestClient with fully mocked service singletons
# ---------------------------------------------------------------------------

@contextmanager
def _mock_client(agent_response=None, retriever_response=None):
    """
    Context manager that yields a TestClient where the route-level singletons
    are replaced with mocks for the entire duration of the ``with`` block.

    Usage::

        with _mock_client() as (client, mock_agent, mock_retriever):
            response = client.post("/ask", json={"query_text": "..."})
    """
    from app.schemas.chat_models import ChatResponse, ContentChunk

    default_agent_response = agent_response or ChatResponse(
        answer_text="ROS 2 nodes are the building blocks of ROS 2 applications.",
        retrieved_sources=["https://example.com/ai-book/ros2-nodes"],
    )
    default_retriever_response = retriever_response or [
        ContentChunk(
            chunk_id="1",
            source_url="https://example.com/ai-book/ros2-nodes",
            original_text="A ROS 2 node is a process that performs computation.",
            score=0.91,
        )
    ]

    mock_agent = MagicMock()
    mock_agent.ask_agent.return_value = default_agent_response

    mock_retriever = MagicMock()
    mock_retriever.retrieve_chunks.return_value = default_retriever_response

    with patch("app.routes.chat.agent_service", mock_agent), \
         patch("app.routes.chat.retriever_service", mock_retriever):
        from app.main import app
        client = TestClient(app)
        yield client, mock_agent, mock_retriever


# ---------------------------------------------------------------------------
# Tests — POST /ask
# ---------------------------------------------------------------------------

class TestAskEndpoint:
    """Tests for POST /ask."""

    def test_ask_returns_200_with_valid_query(self):
        with _mock_client() as (client, mock_agent, _):
            response = client.post("/ask", json={"query_text": "What are ROS 2 nodes?"})

        assert response.status_code == 200
        body = response.json()
        assert "answer_text" in body
        assert "retrieved_sources" in body
        assert isinstance(body["answer_text"], str)
        assert len(body["answer_text"]) > 0

    def test_ask_calls_agent_with_correct_query(self):
        query = "What is a digital twin?"
        with _mock_client() as (client, mock_agent, _):
            client.post("/ask", json={"query_text": query})
            mock_agent.ask_agent.assert_called_once_with(query)

    def test_ask_returns_422_for_empty_query(self):
        with _mock_client() as (client, _, __):
            response = client.post("/ask", json={"query_text": ""})

        # Pydantic min_length=1 should trigger validation error
        assert response.status_code == 422

    def test_ask_returns_422_for_missing_query_field(self):
        with _mock_client() as (client, _, __):
            response = client.post("/ask", json={})

        assert response.status_code == 422

    def test_ask_returns_500_when_agent_raises_exception(self):
        mock_agent = MagicMock()
        mock_agent.ask_agent.side_effect = RuntimeError("Gemini is down")
        mock_retriever = MagicMock()
        mock_retriever.retrieve_chunks.return_value = []

        with patch("app.routes.chat.agent_service", mock_agent), \
             patch("app.routes.chat.retriever_service", mock_retriever):
            from app.main import app
            client = TestClient(app, raise_server_exceptions=False)
            response = client.post("/ask", json={"query_text": "What are ROS 2 nodes?"})

        assert response.status_code == 500
        assert "detail" in response.json()

    def test_ask_response_includes_sources(self):
        from app.schemas.chat_models import ChatResponse
        agent_resp = ChatResponse(
            answer_text="Nodes are processes.",
            retrieved_sources=["https://example.com/source1", "https://example.com/source2"],
        )
        with _mock_client(agent_response=agent_resp) as (client, _, __):
            response = client.post("/ask", json={"query_text": "Tell me about nodes"})

        body = response.json()
        assert len(body["retrieved_sources"]) == 2


# ---------------------------------------------------------------------------
# Tests — GET /health
# ---------------------------------------------------------------------------

class TestHealthEndpoint:
    """Tests for GET /health."""

    def test_health_returns_200(self):
        with _mock_client() as (client, _, __):
            response = client.get("/health")

        assert response.status_code == 200

    def test_health_returns_ok_status(self):
        with _mock_client() as (client, _, __):
            response = client.get("/health")

        assert response.json() == {"status": "ok"}

    def test_health_responds_quickly(self):
        """Health endpoint must respond within 500 ms (SC-004)."""
        import time
        with _mock_client() as (client, _, __):
            start = time.monotonic()
            response = client.get("/health")
            elapsed_ms = (time.monotonic() - start) * 1000

        assert response.status_code == 200
        assert elapsed_ms < 500, f"Health check took {elapsed_ms:.0f}ms (> 500ms)"


# ---------------------------------------------------------------------------
# Tests — POST /retrieval-test
# ---------------------------------------------------------------------------

class TestRetrievalTestEndpoint:
    """Tests for POST /retrieval-test."""

    def test_retrieval_test_returns_200(self):
        with _mock_client() as (client, _, __):
            response = client.post("/retrieval-test", json={"query_text": "What is Isaac Sim?"})

        assert response.status_code == 200

    def test_retrieval_test_returns_chunks(self):
        with _mock_client() as (client, _, mock_retriever):
            response = client.post("/retrieval-test", json={"query_text": "Isaac Sim"})

        body = response.json()
        assert "chunks" in body
        assert isinstance(body["chunks"], list)
        assert len(body["chunks"]) >= 1

    def test_retrieval_test_calls_retriever_with_correct_query(self):
        query = "What is Gazebo?"
        with _mock_client() as (client, _, mock_retriever):
            client.post("/retrieval-test", json={"query_text": query})
            mock_retriever.retrieve_chunks.assert_called_once_with(query_text=query, top_k=5)

    def test_retrieval_test_returns_422_for_empty_query(self):
        with _mock_client() as (client, _, __):
            response = client.post("/retrieval-test", json={"query_text": ""})

        assert response.status_code == 422

    def test_retrieval_test_returns_500_when_retriever_raises(self):
        mock_agent = MagicMock()
        mock_retriever = MagicMock()
        mock_retriever.retrieve_chunks.side_effect = ConnectionError("Qdrant unreachable")

        with patch("app.routes.chat.agent_service", mock_agent), \
             patch("app.routes.chat.retriever_service", mock_retriever):
            from app.main import app
            client = TestClient(app, raise_server_exceptions=False)
            response = client.post("/retrieval-test", json={"query_text": "Isaac Sim"})

        assert response.status_code == 500


# ---------------------------------------------------------------------------
# Tests — GET /heartbeat
# ---------------------------------------------------------------------------

class TestHeartbeatEndpoint:
    """Tests for GET /heartbeat."""

    def test_heartbeat_returns_200(self):
        with _mock_client() as (client, _, __):
            response = client.get("/heartbeat")

        assert response.status_code == 200

    def test_heartbeat_returns_alive_status(self):
        with _mock_client() as (client, _, __):
            response = client.get("/heartbeat")

        assert response.json() == {"status": "alive"}
