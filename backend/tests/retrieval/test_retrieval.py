import logging
import os
from datetime import datetime, timezone

import pytest

from .models import Query, RetrievalLog
from .retrieval_logic import retrieve_chunks

# --- Logger Setup ---
# Console logger
console_logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
console_logger.addHandler(console_handler)
console_logger.setLevel(logging.INFO)

# JSON File logger
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)  # Ensure the logs directory exists
log_file_path = os.path.join(log_dir, 'retrieval_verification.log')
file_logger = logging.getLogger('retrieval_logger')
file_handler = logging.FileHandler(log_file_path, mode='w')
# No formatter needed, we will log pre-formatted JSON strings
file_logger.addHandler(file_handler)
file_logger.setLevel(logging.INFO)
# --- End Logger Setup ---


@pytest.fixture(autouse=True)
def hermetic_retrieval_double(monkeypatch):
    """
    Hermetic test double ensuring retrieval tests run 100% offline
    without external network calls or live API credentials.
    """
    if os.getenv("RUN_LIVE_API_TESTS", "").lower() in ("1", "true", "yes"):
        yield
        return

    from . import retrieval_logic as rl
    from .mocks import MockEmbeddingGenerator, get_mock_qdrant_client

    monkeypatch.setattr(rl, "get_qdrant_client", get_mock_qdrant_client)
    monkeypatch.setattr(rl, "EmbeddingGenerator", MockEmbeddingGenerator)
    yield


# Placeholder for the sample queries.
SAMPLE_QUERIES: list[Query] = [
    Query(query_text="What are the core concepts of ROS 2?", expected_id="1-2-ros2-core-concepts.mdx"),
    Query(query_text="How do I create a ROS 2 workspace?", expected_id="1-3-ros2-workspace.mdx"),
    Query(query_text="What is a digital twin?", expected_id="2-1-introduction-to-digital-twins.mdx"),
    # Add more queries here...
]


@pytest.mark.parametrize("query", SAMPLE_QUERIES)
def test_retrieval_accuracy(query: Query):
    """
    Tests the accuracy of the RAG retrieval pipeline for a single query.
    """
    console_logger.info(f"Testing query: '{query.query_text}'")

    retrieved_chunks = retrieve_chunks(query.query_text, top_k=5)

    passed = False
    matching_chunks = [c for c in retrieved_chunks if query.expected_id in c.source_url]
    if matching_chunks and matching_chunks[0].score >= 0.45:
        passed = True

    # Log the result to the JSON file
    log_entry = RetrievalLog(
        timestamp=datetime.now(timezone.utc).isoformat(),
        query_text=query.query_text,
        passed=passed,
        retrieved_chunks=retrieved_chunks,
    )
    file_logger.info(log_entry.model_dump_json())

    # Assertions
    assert retrieved_chunks, f"No chunks were retrieved for query: '{query.query_text}'"
    assert matching_chunks, (
        f"Expected source '{query.expected_id}' not found in retrieved chunks: {[c.source_url for c in retrieved_chunks]}"
    )
    assert matching_chunks[0].score >= 0.45, f"Score {matching_chunks[0].score} is below threshold"

    console_logger.info(f"Query test PASSED for: '{query.query_text}'")


def test_retriever_module_filter_case_insensitivity():
    """Verify RetrieverService normalizes mixed-case module filters to lowercase."""
    from unittest.mock import MagicMock, patch

    from app.retriever.retriever_service import RetrieverService

    with patch("app.retriever.retriever_service.QdrantClient") as mock_qdrant_cls, \
         patch("app.retriever.retriever_service.EmbeddingGenerator") as mock_emb_cls:

        mock_qdrant = MagicMock()
        mock_qdrant_cls.return_value = mock_qdrant
        mock_emb = MagicMock()
        mock_emb.return_value.generate_embeddings.return_value = [[0.1] * 1024]
        mock_emb_cls.return_value = mock_emb

        service = RetrieverService()

        # Mixed-case full module name
        service.retrieve_chunks("test query", module_filter="Module1-ros2")
        call_kwargs = mock_qdrant.query_points.call_args.kwargs
        q_filter = call_kwargs.get("query_filter")
        assert q_filter is not None
        assert q_filter.must[0].match.value == "module1"

        # Uppercase module key
        service.retrieve_chunks("test query", module_filter="MODULE2")
        call_kwargs = mock_qdrant.query_points.call_args.kwargs
        q_filter = call_kwargs.get("query_filter")
        assert q_filter is not None
        assert q_filter.must[0].match.value == "module2"

        # Mixed-case with whitespace
        service.retrieve_chunks("test query", module_filter="  MoDuLe3-Ai-RoBoT  ")
        call_kwargs = mock_qdrant.query_points.call_args.kwargs
        q_filter = call_kwargs.get("query_filter")
        assert q_filter is not None
        assert q_filter.must[0].match.value == "module3"
