"""
Pytest configuration and shared fixtures for the backend test suite.

Fixtures defined here are available to all tests without explicit import.
"""

import os
from unittest.mock import patch

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

load_dotenv()

FAKE_ENV = {
    "COHERE_API_KEY": os.getenv("COHERE_API_KEY", "test-cohere-key"),
    "QDRANT_API_KEY": os.getenv("QDRANT_API_KEY", "test-qdrant-key"),
    "QDRANT_URL": os.getenv("QDRANT_URL", "https://test.qdrant.io:6333"),
    "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "test-gemini-key"),
    "COLLECTION_NAME": os.getenv("COLLECTION_NAME", "test_collection"),
}


@pytest.fixture(scope="session", autouse=True)
def patch_env_vars(tmp_path_factory):
    """
    Session-scoped fixture that patches all required env vars before any
    module-level Settings() instantiation occurs.
    """
    with patch.dict("os.environ", FAKE_ENV, clear=False):
        yield


@pytest.fixture(scope="session")
def test_client():
    """
    Returns a FastAPI TestClient for the main application.

    Uses ``patch.dict`` to ensure Settings() validation passes without a real
    ``.env`` file.
    """
    with patch.dict("os.environ", FAKE_ENV, clear=False):
        # Delay imports until env is patched
        with patch("app.agent.agent_service.AgentService.__init__", return_value=None), \
             patch("app.retriever.retriever_service.RetrieverService.__init__", return_value=None):
            from app.main import app
            client = TestClient(app, raise_server_exceptions=False)
            yield client


# ---------------------------------------------------------------------------
# Reusable mock objects
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_content_chunk():
    """Returns a fake ContentChunk Pydantic model."""
    from app.schemas.chat_models import ContentChunk
    return ContentChunk(
        chunk_id="chunk-001",
        source_url="https://example.com/ai-book/1-2-ros2-core-concepts",
        original_text="ROS 2 nodes are the basic computational units in the ROS 2 framework.",
        score=0.92,
    )


@pytest.fixture
def mock_chat_response():
    """Returns a fake ChatResponse Pydantic model."""
    from app.schemas.chat_models import ChatResponse
    return ChatResponse(
        answer_text="ROS 2 nodes are the fundamental building blocks of ROS 2 applications.",
        retrieved_sources=["https://example.com/ai-book/1-2-ros2-core-concepts"],
    )
