import cohere

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class EmbeddingGenerator:
    """
    Generates text embeddings using the Cohere API.

    Uses ``embed-english-v3.0`` (1 024-dimensional vectors).
    Two ``input_type`` modes are supported:

    - ``"search_document"``  — for indexing content into the vector store.
    - ``"search_query"``     — for embedding user queries at retrieval time.
    """

    MODEL = "embed-english-v3.0"

    def __init__(self):
        self.co = cohere.Client(settings.COHERE_API_KEY)

    def generate_embeddings(self, texts: list[str], input_type: str = "search_document") -> list[list[float]] | None:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of strings to embed.
            input_type: Cohere input_type — ``"search_document"`` (default) or
                        ``"search_query"`` (use for query-time embeddings).

        Returns:
            A list of embedding vectors, or ``None`` on error.
        """
        try:
            response = self.co.embed(
                texts=texts,
                model=self.MODEL,
                input_type=input_type,
            )
            return response.embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return None
