"""
Ingestion script for the Physical AI & Humanoid Robotics book.

Reads all .mdx documents from ai-book-docs/, chunks them, generates Cohere
embeddings (using embed-english-v3.0 with input_type='search_document'),
and uploads them to the Qdrant Cloud collection.
"""

import glob
import os
import re
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from qdrant_client import models

from app.core.config import settings
from app.core.logging import get_logger
from app.models.models import Document
from app.services.embedding import EmbeddingGenerator
from app.services.text_processor import TextProcessor
from app.services.vector_store import VectorStore

logger = get_logger(__name__)


def extract_title(content: str, default: str) -> str:
    """Extract title from frontmatter or first # header."""
    fm_match = re.search(r"^title:\s*['\"]?(.*?)['\"]?\s*$", content, re.MULTILINE)
    if fm_match:
        return fm_match.group(1).strip()
    h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    return default


def clean_markdown(content: str) -> str:
    """Remove frontmatter and clean up markdown for embedding."""
    # Remove YAML frontmatter
    cleaned = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)
    # Remove HTML-like tags if any
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    # Normalize excessive newlines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def run_ingestion():
    repo_root = backend_dir.parent
    docs_dir = repo_root / "ai-book-docs"

    if not docs_dir.exists():
        logger.error(f"Documentation directory not found: {docs_dir}")
        return

    mdx_files = sorted(glob.glob(str(docs_dir / "**" / "*.mdx"), recursive=True))
    logger.info(f"Found {len(mdx_files)} MDX documents in {docs_dir}")

    text_processor = TextProcessor(chunk_size=350, chunk_overlap=50)
    all_documents: list[Document] = []

    for file_path in mdx_files:
        rel_path = os.path.relpath(file_path, str(docs_dir)).replace("\\", "/")
        with open(file_path, "r", encoding="utf-8") as f:
            raw_content = f.read()

        title = extract_title(raw_content, default=Path(file_path).stem)
        cleaned_text = clean_markdown(raw_content)
        chunks = text_processor.chunk_text(cleaned_text)

        source_url = f"/ai-book/{rel_path}"

        for idx, chunk in enumerate(chunks):
            doc = Document(
                text=chunk,
                source_url=source_url,
                title=title,
                chunk_index=idx,
            )
            all_documents.append(doc)

    logger.info(f"Total chunks created: {len(all_documents)}")

    # Generate embeddings in batches (Cohere max batch size is 96)
    embedding_gen = EmbeddingGenerator()
    batch_size = 64
    all_embeddings: list[list[float]] = []

    for i in range(0, len(all_documents), batch_size):
        batch = [doc.text for doc in all_documents[i : i + batch_size]]
        logger.info(f"Generating embeddings for batch {i // batch_size + 1} ({len(batch)} texts)...")
        embeddings = embedding_gen.generate_embeddings(batch, input_type="search_document")
        if not embeddings:
            logger.error(f"Failed to generate embeddings for batch starting at index {i}")
            return
        all_embeddings.extend(embeddings)

    logger.info(f"Generated {len(all_embeddings)} embeddings total.")

    # Upload to Qdrant
    vector_store = VectorStore()
    vector_store.create_collection()

    points = [
        models.PointStruct(
            id=i,
            vector=emb,
            payload=doc.model_dump(),
        )
        for i, (emb, doc) in enumerate(zip(all_embeddings, all_documents))
    ]

    vector_store.client.upsert(
        collection_name=vector_store.collection_name,
        points=points,
        wait=True,
    )
    logger.info(
        f"Successfully ingested {len(points)} points into Qdrant collection '{vector_store.collection_name}'!"
    )


if __name__ == "__main__":
    run_ingestion()
