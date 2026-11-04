from markdownify import markdownify as md
import tiktoken
from app.core.logging import get_logger

logger = get_logger(__name__)

class TextProcessor:
    def __init__(self, model_name="cl100k_base", chunk_size=400, chunk_overlap=50):
        self.tokenizer = tiktoken.get_encoding(model_name)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        logger.info(f"TextProcessor initialized with model: {model_name}, chunk_size: {chunk_size}")

    def clean_text(self, html_content):
        return md(html_content)

    def chunk_text(self, text):
        tokens = self.tokenizer.encode(text)
        chunks = []
        for i in range(0, len(tokens), self.chunk_size - self.chunk_overlap):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunks.append(self.tokenizer.decode(chunk_tokens))
        return chunks
