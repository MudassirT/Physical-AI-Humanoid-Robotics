"""
Global Pytest Fixtures for End-to-End (E2E) Test Suite.

Provides hermetic test doubles (Qdrant, Gemini, Cohere) ensuring all tests
execute with zero reliance on external live API credentials.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Resolve workspace project root directory."""
    # From backend/tests/e2e -> up 3 levels to project root
    current = Path(__file__).resolve().parent
    for parent in [current, current.parent, current.parent.parent, current.parent.parent.parent]:
        if (parent / "package.json").exists() and (parent / "ai-book-docs").exists():
            return parent
    return current.parent.parent.parent


@pytest.fixture(scope="session")
def docs_dir(project_root: Path) -> Path:
    """Path to ai-book-docs directory."""
    return project_root / "ai-book-docs"


@pytest.fixture
def temp_analytics_dir():
    """Create an isolated temporary directory for analytics log testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_cohere_client():
    """Deterministic mock of Cohere client returning 1024-dim float embeddings."""
    mock_client = MagicMock()
    # 1024-dimension float vector
    fake_vector = [0.01 * (i % 100) for i in range(1024)]

    mock_response = MagicMock()
    mock_response.embeddings = [fake_vector]
    mock_client.embed.return_value = mock_response
    return mock_client


@pytest.fixture
def mock_qdrant_client():
    """Deterministic mock of Qdrant client."""
    mock_client = MagicMock()

    # Fake scored points returned by vector search
    fake_point = MagicMock()
    fake_point.id = "c81d4e2e-bcf2-11e6-869b-7fa663f21000"
    fake_point.score = 0.95
    fake_point.payload = {
        "text": "The Zero-Moment Point (ZMP) is a fundamental criterion for bipedal gait stability.",
        "source_url": "/ai-book/module6-bipedal-locomotion/6-2-zero-moment-point",
        "title": "Zero-Moment Point (ZMP)",
        "chunk_index": 0,
        "module": "module6",
        "chapter": "6-2-zero-moment-point",
    }

    mock_response = MagicMock()
    mock_response.points = [fake_point]
    mock_client.query_points.return_value = mock_response
    mock_client.delete.return_value = MagicMock()
    mock_client.upsert.return_value = MagicMock()
    return mock_client


@pytest.fixture
def mock_gemini_client():
    """Deterministic mock of Google GenAI Client with unary and streaming capabilities."""
    mock_client = MagicMock()

    # Unary response
    mock_unary_res = MagicMock()
    mock_unary_res.text = (
        "The Zero-Moment Point (ZMP) specifies the point on the ground where the net "
        "tipping moment is zero. Grounding source: /ai-book/module6-bipedal-locomotion/6-2-zero-moment-point"
    )
    mock_unary_res.candidates = [MagicMock()]
    mock_client.models.generate_content.return_value = mock_unary_res

    # Streaming response generator
    def fake_stream(*args, **kwargs):
        chunks = [
            "The ",
            "Zero-Moment ",
            "Point ",
            "(ZMP) ",
            "specifies the ",
            "tipping ",
            "boundary.",
        ]
        for c in chunks:
            chunk_mock = MagicMock()
            chunk_mock.text = c
            yield chunk_mock

    mock_client.models.generate_content_stream = MagicMock(side_effect=fake_stream)
    return mock_client


@pytest.fixture
def test_client() -> TestClient:
    """FastAPI TestClient with isolated lifespan."""
    with TestClient(app) as client:
        yield client
