"""
Ingestion script for the Physical AI & Humanoid Robotics book.

Reads all .mdx documents from ai-book-docs/, chunks them, generates Cohere
embeddings (using embed-english-v3.0 with input_type='search_document'),
and uploads them to the Qdrant Cloud collection.

Supports:
- --incremental: SHA-256 change-detection manifest (skips unchanged files)
- --force: Re-ingests all documents and recreates the collection
- --dry-run: Analyzes changes without calling embedding/Qdrant APIs
"""

import argparse
import glob
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from qdrant_client import models

from app.core.logging import get_logger
from app.models.models import Document
from app.services.embedding import EmbeddingGenerator
from app.services.text_processor import TextProcessor
from app.services.vector_store import VectorStore

logger = get_logger(__name__)

DEFAULT_MANIFEST_PATH = backend_dir / ".ingest_manifest.json"


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


def compute_file_hash(file_path: Path | str) -> str:
    """Compute the SHA-256 hash of a file's binary content."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def generate_point_id(rel_path: str, chunk_index: int) -> str:
    """Generate a deterministic UUID5 point ID for a document chunk."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{rel_path}:{chunk_index}"))


def extract_metadata_from_path(rel_path: str) -> tuple[str, str]:
    """
    Extract (module, chapter) from a relative MDX file path.
    Example: 'module1-ros2/1-1-intro.mdx' -> ('module1', '1-1-intro')
    """
    path_obj = Path(rel_path)
    parent_name = path_obj.parent.name
    module = parent_name.split("-")[0] if "-" in parent_name else parent_name
    chapter = path_obj.stem
    return module, chapter


def plan_ingestion(
    docs_dir: Path,
    manifest: dict,
    force: bool = False,
) -> tuple[dict, list[str], list[str], list[str], list[str]]:
    """
    Scans docs_dir, compares against manifest, and categorises files into:
    (new_files, modified_files, unchanged_files, deleted_files).

    Returns:
        (file_hashes, new_files, modified_files, unchanged_files, deleted_files)
    """
    mdx_files = sorted(glob.glob(str(docs_dir / "**" / "*.mdx"), recursive=True))
    current_files: dict[str, str] = {}
    file_hashes: dict[str, str] = {}

    for file_path in mdx_files:
        rel_path = os.path.relpath(file_path, str(docs_dir)).replace("\\", "/")
        file_hash = compute_file_hash(file_path)
        current_files[rel_path] = file_path
        file_hashes[rel_path] = file_hash

    new_files: list[str] = []
    modified_files: list[str] = []
    unchanged_files: list[str] = []

    if force:
        new_files = list(current_files.keys())
        deleted_files = list(manifest.keys())
        return file_hashes, new_files, modified_files, unchanged_files, deleted_files

    for rel_path, file_hash in file_hashes.items():
        if rel_path not in manifest:
            new_files.append(rel_path)
        elif manifest[rel_path].get("sha256") != file_hash:
            modified_files.append(rel_path)
        else:
            unchanged_files.append(rel_path)

    deleted_files = [rel_path for rel_path in manifest if rel_path not in current_files]

    return file_hashes, new_files, modified_files, unchanged_files, deleted_files


def run_ingestion(
    incremental: bool = True,
    force: bool = False,
    dry_run: bool = False,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
):
    repo_root = backend_dir.parent
    docs_dir = repo_root / "ai-book-docs"

    if not docs_dir.exists():
        logger.error(f"Documentation directory not found: {docs_dir}")
        return

    logger.info(
        f"Starting documentation ingestion (incremental={incremental}, "
        f"force={force}, dry_run={dry_run})"
    )

    # 1. Load manifest
    manifest: dict = {}
    if manifest_path.exists() and not force:
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            logger.info(f"Loaded existing ingestion manifest with {len(manifest)} entries.")
        except Exception as exc:
            logger.warning(f"Could not load manifest, starting fresh: {exc}")
            manifest = {}

    # 2. Plan changes
    file_hashes, new_files, modified_files, unchanged_files, deleted_files = plan_ingestion(
        docs_dir=docs_dir,
        manifest=manifest,
        force=force,
    )

    logger.info(
        f"Ingestion Plan: {len(new_files)} new, {len(modified_files)} modified, "
        f"{len(unchanged_files)} unchanged, {len(deleted_files)} deleted."
    )

    if dry_run:
        logger.info("DRY-RUN mode enabled. No changes will be applied.")
        for f in new_files:
            logger.info(f"  [+] New: {f}")
        for f in modified_files:
            logger.info(f"  [*] Modified: {f}")
        for f in deleted_files:
            logger.info(f"  [-] Deleted: {f}")
        return

    vector_store = VectorStore()

    # 3. Handle force / collection setup
    if force:
        logger.info(f"Force re-ingestion: recreating collection '{vector_store.collection_name}'...")
        vector_store.create_collection()
        manifest.clear()
    else:
        # Ensure collection exists without dropping existing vectors
        try:
            existing = [c.name for c in vector_store.client.get_collections().collections]
            if vector_store.collection_name not in existing:
                vector_store.client.create_collection(
                    collection_name=vector_store.collection_name,
                    vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
                )
                logger.info(f"Created collection '{vector_store.collection_name}'.")
        except Exception as exc:
            logger.warning(f"Collection check notice: {exc}")

    # 4. Handle deleted files: remove points from Qdrant and manifest
    for del_path in deleted_files:
        old_ids = manifest.get(del_path, {}).get("chunk_ids", [])
        if old_ids:
            try:
                vector_store.client.delete(
                    collection_name=vector_store.collection_name,
                    points_selector=models.PointIdsList(points=old_ids),
                )
                logger.info(f"Deleted {len(old_ids)} obsolete points for {del_path}")
            except Exception as exc:
                logger.error(f"Failed to delete points for {del_path}: {exc}")
        manifest.pop(del_path, None)

    # 5. Handle modified files: delete old points first
    for mod_path in modified_files:
        old_ids = manifest.get(mod_path, {}).get("chunk_ids", [])
        if old_ids:
            try:
                vector_store.client.delete(
                    collection_name=vector_store.collection_name,
                    points_selector=models.PointIdsList(points=old_ids),
                )
                logger.info(f"Removed {len(old_ids)} old points for modified file {mod_path}")
            except Exception as exc:
                logger.error(f"Failed to delete old points for {mod_path}: {exc}")

    # 6. Process new and modified files
    files_to_process = new_files + modified_files
    if not files_to_process and not deleted_files:
        logger.info("Knowledge base is already up to date. No vectorization needed.")
        return

    text_processor = TextProcessor(chunk_size=350, chunk_overlap=50)
    embedding_gen = EmbeddingGenerator()
    batch_size = 64

    for rel_path in files_to_process:
        full_path = docs_dir / rel_path
        if not full_path.exists():
            continue

        with open(full_path, "r", encoding="utf-8") as f:
            raw_content = f.read()

        title = extract_title(raw_content, default=Path(full_path).stem)
        cleaned_text = clean_markdown(raw_content)
        chunks = text_processor.chunk_text(cleaned_text)
        module, chapter = extract_metadata_from_path(rel_path)
        content_hash = file_hashes.get(rel_path, compute_file_hash(full_path))
        source_url = f"/ai-book/{rel_path}"

        file_docs: list[Document] = []
        point_ids: list[str] = []

        for idx, chunk in enumerate(chunks):
            pid = generate_point_id(rel_path, idx)
            point_ids.append(pid)
            doc = Document(
                text=chunk,
                source_url=source_url,
                title=title,
                chunk_index=idx,
                module=module,
                chapter=chapter,
                content_hash=content_hash,
            )
            file_docs.append(doc)

        # Generate embeddings in batches for this file
        file_embeddings: list[list[float]] = []
        for i in range(0, len(file_docs), batch_size):
            batch = [d.text for d in file_docs[i : i + batch_size]]
            embeddings = embedding_gen.generate_embeddings(batch, input_type="search_document")
            if not embeddings:
                logger.error(f"Failed to generate embeddings for {rel_path} batch {i}")
                break
            file_embeddings.extend(embeddings)

        if len(file_embeddings) == len(file_docs):
            points = [
                models.PointStruct(
                    id=pid,
                    vector=emb,
                    payload=doc.model_dump(),
                )
                for pid, emb, doc in zip(point_ids, file_embeddings, file_docs)
            ]

            try:
                vector_store.client.upsert(
                    collection_name=vector_store.collection_name,
                    points=points,
                    wait=True,
                )
                manifest[rel_path] = {
                    "sha256": content_hash,
                    "chunk_ids": point_ids,
                    "count": len(point_ids),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
                logger.info(f"Upserted {len(points)} points for {rel_path}")
            except Exception as exc:
                logger.error(f"Failed to upsert points for {rel_path}: {exc}")
        else:
            logger.error(f"Embedding count mismatch for {rel_path}, skipping manifest update.")

    # 7. Persist updated manifest atomically
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_manifest = manifest_path.with_suffix(".tmp")
    with open(temp_manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    temp_manifest.replace(manifest_path)
    logger.info(f"Ingestion complete. Updated manifest written to {manifest_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Ingest documentation into Qdrant vector database with incremental hashing."
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        default=True,
        help="Use SHA-256 change detection manifest (default: True).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-ingest all documents and reset collection.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Display planned actions without modifying Qdrant or manifest.",
    )
    args = parser.parse_args()

    run_ingestion(
        incremental=args.incremental,
        force=args.force,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
