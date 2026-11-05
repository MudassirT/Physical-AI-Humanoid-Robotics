"""
TextProcessor — converts raw HTML to clean Markdown and chunks it into
overlapping segments suitable for embedding.

Chunking is word-based (instead of BPE-token-based) so that there is no
dependency on the ``tiktoken`` package.  For the typical chunk sizes used in
this project (400 words ≈ 500–600 tokens) the difference in granularity is
negligible.
"""

from markdownify import markdownify as md

from app.core.logging import get_logger

logger = get_logger(__name__)


class TextProcessor:
    """Cleans HTML and splits text into overlapping word-based chunks."""

    def __init__(self, model_name: str = "word", chunk_size: int = 400, chunk_overlap: int = 50):
        """
        Args:
            model_name: Unused; kept for API compatibility with the previous
                        ``tiktoken``-based implementation.
            chunk_size: Maximum number of words per chunk.
            chunk_overlap: Number of words shared between consecutive chunks.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        logger.info(
            f"TextProcessor initialized with chunk_size={chunk_size}, "
            f"chunk_overlap={chunk_overlap} (word-based)"
        )

    def clean_text(self, html_content: str) -> str:
        """Convert HTML to clean Markdown text.

        Args:
            html_content: Raw HTML string.

        Returns:
            Markdown-formatted plain text.
        """
        return md(html_content)

    def chunk_text(self, text: str) -> list[str]:
        """Split *text* into overlapping word-based chunks.

        Args:
            text: Plain text to chunk (should be pre-cleaned).

        Returns:
            A list of string chunks.  The last chunk may be shorter than
            ``chunk_size``.
        """
        words = text.split()
        if not words:
            return []

        step = max(1, self.chunk_size - self.chunk_overlap)
        chunks: list[str] = []
        for i in range(0, len(words), step):
            chunk_words = words[i : i + self.chunk_size]
            chunks.append(" ".join(chunk_words))
        return chunks
