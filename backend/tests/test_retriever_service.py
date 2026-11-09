"""
Unit tests for app.retriever.retriever_service.RetrieverService

All Qdrant and EmbeddingGenerator calls are mocked.
"""

from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def retriever_service():
    """
    Returns a RetrieverService with Qdrant client and EmbeddingGenerator mocked.
    """
    with patch("app.retriever.retriever_service.QdrantClient") as mock_qdrant_cls, \
         patch("app.retriever.retriever_service.EmbeddingGenerator") as mock_emb_cls:

        mock_qdrant_instance = MagicMock()
        mock_qdrant_cls.return_value = mock_qdrant_instance

        mock_emb_instance = MagicMock()
        mock_emb_cls.return_value = mock_emb_instance

        from app.retriever.retriever_service import RetrieverService
        service = RetrieverService()
        service._qdrant_mock = mock_qdrant_instance
        service._emb_mock = mock_emb_instance
        yield service


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_qdrant_hit(chunk_id="1", source_url="https://example.com/page", text="Some text.", score=0.9):
    hit = MagicMock()
    hit.id = chunk_id
    hit.score = score
    hit.payload = {"source_url": source_url, "text": text}
    return hit


# ---------------------------------------------------------------------------
# Tests — RetrieverService.retrieve_chunks
# ---------------------------------------------------------------------------

class TestRetrieveChunks:
    """Tests for RetrieverService.retrieve_chunks."""

    def test_returns_content_chunks_on_success(self, retriever_service):
        # Mock embedding generation
        retriever_service.embedding_generator.generate_embeddings.return_value = [[0.1] * 1024]

        # Mock Qdrant search
        hit = _make_qdrant_hit(chunk_id="42", source_url="https://example.com/ros2", text="ROS 2 intro.", score=0.88)
        retriever_service.qdrant_client.query_points.return_value = [hit]

        from app.schemas.chat_models import ContentChunk
        chunks = retriever_service.retrieve_chunks("What is ROS 2?", top_k=1)

        assert len(chunks) == 1
        assert isinstance(chunks[0], ContentChunk)
        assert chunks[0].chunk_id == "42"
        assert chunks[0].score == 0.88

    def test_returns_empty_list_when_embedding_fails(self, retriever_service):
        retriever_service.embedding_generator.generate_embeddings.return_value = None

        chunks = retriever_service.retrieve_chunks("Some query")

        assert chunks == []
        retriever_service.qdrant_client.query_points.assert_not_called()

    def test_returns_empty_list_when_qdrant_raises(self, retriever_service):
        retriever_service.embedding_generator.generate_embeddings.return_value = [[0.1] * 1024]
        retriever_service.qdrant_client.query_points.side_effect = Exception("Connection refused")

        chunks = retriever_service.retrieve_chunks("Query that fails")

        assert chunks == []

    def test_uses_search_query_input_type_for_embedding(self, retriever_service):
        """Embedding for queries must use ``input_type='search_query'`` (not 'search_document')."""
        retriever_service.embedding_generator.generate_embeddings.return_value = [[0.1] * 1024]
        retriever_service.qdrant_client.query_points.return_value = []

        retriever_service.retrieve_chunks("What is a digital twin?")

        call_kwargs = retriever_service.embedding_generator.generate_embeddings.call_args
        # Either positional or keyword
        args, kwargs = call_kwargs
        input_type = kwargs.get("input_type") or (args[1] if len(args) > 1 else None)
        assert input_type == "search_query", (
            f"Expected input_type='search_query' but got '{input_type}'. "
            "Query embeddings must use 'search_query' for correct Cohere retrieval."
        )

    def test_top_k_is_passed_to_qdrant(self, retriever_service):
        retriever_service.embedding_generator.generate_embeddings.return_value = [[0.1] * 1024]
        retriever_service.qdrant_client.query_points.return_value = []

        retriever_service.retrieve_chunks("What is ROS 2?", top_k=3)

        call_kwargs = retriever_service.qdrant_client.query_points.call_args.kwargs
        assert call_kwargs.get("limit") == 3

    def test_source_url_falls_back_to_unknown_when_missing(self, retriever_service):
        retriever_service.embedding_generator.generate_embeddings.return_value = [[0.1] * 1024]

        hit = MagicMock()
        hit.id = "5"
        hit.score = 0.75
        hit.payload = {}   # no source_url in payload

        retriever_service.qdrant_client.query_points.return_value = [hit]

        chunks = retriever_service.retrieve_chunks("Query with missing payload")
        # Should not raise; fallback should be "unknown"
        assert chunks[0].source_url == "unknown"

    def test_multiple_chunks_returned_in_order(self, retriever_service):
        retriever_service.embedding_generator.generate_embeddings.return_value = [[0.1] * 1024]

        hits = [
            _make_qdrant_hit(chunk_id=str(i), score=0.9 - i * 0.05) for i in range(3)
        ]
        retriever_service.qdrant_client.query_points.return_value = hits

        chunks = retriever_service.retrieve_chunks("Multi-result query", top_k=3)

        assert len(chunks) == 3
        assert chunks[0].chunk_id == "0"
        assert chunks[1].chunk_id == "1"
        assert chunks[2].chunk_id == "2"

    def test_retrieve_chunks_with_module_filter_builds_qdrant_filter(self, retriever_service):
        retriever_service.embedding_generator.generate_embeddings.return_value = [[0.1] * 1024]
        retriever_service.qdrant_client.query_points.return_value = []

        retriever_service.retrieve_chunks("What is ZMP?", module_filter="module6-bipedal-locomotion")

        call_kwargs = retriever_service.qdrant_client.query_points.call_args.kwargs
        q_filter = call_kwargs.get("query_filter")
        assert q_filter is not None
        assert len(q_filter.must) == 1
        condition = q_filter.must[0]
        assert condition.key == "module"
        assert condition.match.value == "module6"

    def test_retrieve_chunks_with_none_or_all_filter_passes_none(self, retriever_service):
        retriever_service.embedding_generator.generate_embeddings.return_value = [[0.1] * 1024]
        retriever_service.qdrant_client.query_points.return_value = []

        # Test None
        retriever_service.retrieve_chunks("What is ROS 2?", module_filter=None)
        assert retriever_service.qdrant_client.query_points.call_args.kwargs.get("query_filter") is None

        # Test "all"
        retriever_service.retrieve_chunks("What is ROS 2?", module_filter="all")
        assert retriever_service.qdrant_client.query_points.call_args.kwargs.get("query_filter") is None

    def test_retrieve_chunks_populates_payload_metadata(self, retriever_service):
        retriever_service.embedding_generator.generate_embeddings.return_value = [[0.1] * 1024]

        hit = MagicMock()
        hit.id = "chunk-xyz"
        hit.score = 0.96
        hit.payload = {
            "source_url": "/ai-book/module1-ros2/1-1-intro",
            "text": "Intro to ROS 2",
            "module": "module1",
            "chapter": "1-1-intro",
            "content_hash": "hash_abc_123",
        }
        retriever_service.qdrant_client.query_points.return_value = [hit]

        chunks = retriever_service.retrieve_chunks("ROS 2")
        assert len(chunks) == 1
        assert chunks[0].chunk_id == "chunk-xyz"
        assert chunks[0].module == "module1"
        assert chunks[0].chapter == "1-1-intro"
        assert chunks[0].content_hash == "hash_abc_123"

