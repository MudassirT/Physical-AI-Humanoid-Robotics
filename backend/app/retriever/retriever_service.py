from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client import models as qmodels

from app.core.config import settings
from app.core.logging import get_logger
from app.services.embedding import EmbeddingGenerator

from ..schemas.chat_models import ContentChunk

logger = get_logger(__name__)


class RetrieverService:
    """
    Handles semantic retrieval of content chunks from the Qdrant vector database.

    Given a natural-language query, the service:
    1. Embeds the query with Cohere (``search_query`` input type).
    2. Performs an approximate-nearest-neighbour search in Qdrant, optionally
       filtered by curriculum module.
    3. Returns the top-k results as ``ContentChunk`` objects.
    """

    def __init__(self):
        self.qdrant_client = self._initialize_qdrant_client()
        self.embedding_generator = EmbeddingGenerator()
        self.collection_name = settings.COLLECTION_NAME

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _initialize_qdrant_client(self) -> QdrantClient:
        """
        Initialises and returns a Qdrant client using credentials from settings.

        Raises:
            ValueError: If ``QDRANT_URL`` or ``QDRANT_API_KEY`` are not set.
        """
        qdrant_url = settings.QDRANT_URL
        qdrant_api_key = settings.QDRANT_API_KEY

        if not qdrant_url or not qdrant_api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY must be configured in settings.")

        return QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            check_compatibility=False,
        )

    def _get_query_embedding(self, text: str) -> list[float] | None:
        """
        Generates a *query* embedding for the given text.

        Uses ``input_type="search_query"`` (Cohere best practice) so that the
        vector is optimised for retrieval against document embeddings.

        Args:
            text: The raw query string.

        Returns:
            A list of floats (embedding vector) or ``None`` on failure.
        """
        embeddings = self.embedding_generator.generate_embeddings(
            [text], input_type="search_query"
        )
        if embeddings:
            return embeddings[0]
        return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def retrieve_chunks(
        self,
        query_text: str,
        top_k: int = 5,
        module_filter: Optional[str] = None,
    ) -> list[ContentChunk]:
        """
        Retrieves the most relevant content chunks for a given query from Qdrant.

        Args:
            query_text: The natural-language query to search for.
            top_k: Maximum number of chunks to return (default: 5).
            module_filter: Optional curriculum module identifier (e.g. "module1",
                "module6-bipedal-locomotion"). If None or "all", performs global search.

        Returns:
            A list of :class:`ContentChunk` objects, ordered by descending
            similarity score. Returns an empty list when embedding fails or
            no results are found.
        """
        logger.info(
            f"RetrieverService: querying Qdrant for '{query_text[:80]}...' "
            f"(top_k={top_k}, module_filter={module_filter})"
        )

        query_embedding = self._get_query_embedding(query_text)
        if query_embedding is None:
            logger.warning("RetrieverService: embedding generation failed — returning empty result.")
            return []

        query_filter = None
        if module_filter and module_filter.strip().lower() not in ("", "all", "none"):
            clean_filter = module_filter.strip()
            norm_module = clean_filter.split("-")[0] if "-" in clean_filter else clean_filter
            # Normalize standard curriculum module identifiers to lowercase for Qdrant keyword matching
            if norm_module.isalnum() or norm_module.replace("_", "").isalnum():
                norm_module = norm_module.lower()
                clean_filter = clean_filter.lower()
            query_filter = qmodels.Filter(
                must=[
                    qmodels.FieldCondition(
                        key="module",
                        match=qmodels.MatchValue(value=norm_module),
                    )
                ]
            )

        try:
            search_result = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                query_filter=query_filter,
                limit=top_k,
                with_payload=True,
            )
        except Exception as exc:
            logger.error(f"RetrieverService: Qdrant query failed — {exc}", exc_info=True)
            return []

        retrieved_chunks: list[ContentChunk] = []
        points = getattr(search_result, "points", search_result)
        for hit in points:
            payload = hit.payload or {}
            chunk = ContentChunk(
                chunk_id=str(hit.id),
                source_url=payload.get("source_url", "unknown"),
                original_text=payload.get("text", "unknown"),
                score=hit.score,
                module=payload.get("module"),
                chapter=payload.get("chapter"),
                content_hash=payload.get("content_hash"),
            )
            retrieved_chunks.append(chunk)

        logger.info(
            f"RetrieverService: retrieved {len(retrieved_chunks)} chunks "
            f"(IDs: {[c.chunk_id for c in retrieved_chunks]})"
        )
        return retrieved_chunks


# ---------------------------------------------------------------------------
# Manual smoke test — run with:  cd backend && uv run python -m app.retriever.retriever_service
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    retriever = RetrieverService()
    test_query = "What is a digital twin in the context of robotics?"
    try:
        chunks = retriever.retrieve_chunks(test_query)
        if chunks:
            print(f"Found {len(chunks)} chunks for query: '{test_query}'")
            for i, chunk in enumerate(chunks):
                print(f"  {i + 1}. Score: {chunk.score:.4f}, Source: {chunk.source_url}")
                print(f"     Text: {chunk.original_text[:120]}...")
        else:
            print(f"No chunks found for query: '{test_query}'")
    except Exception as e:
        print(f"An error occurred: {e}")
