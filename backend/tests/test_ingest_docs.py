"""
Unit tests for incremental hash-based auto-ingestion pipeline (ingest_docs.py).
"""

import hashlib
import uuid
from pathlib import Path
from unittest.mock import patch

import pytest

from ingest_docs import (
    clean_markdown,
    compute_file_hash,
    extract_metadata_from_path,
    extract_title,
    generate_point_id,
    plan_ingestion,
    run_ingestion,
)


class TestIngestionHelpers:
    """Tests for individual utility functions in ingest_docs.py."""

    def test_compute_file_hash(self, tmp_path: Path):
        test_file = tmp_path / "sample.mdx"
        content = b"# Sample Content for Hashing\n\nSome text."
        test_file.write_bytes(content)

        expected_hash = hashlib.sha256(content).hexdigest()
        assert compute_file_hash(test_file) == expected_hash

    def test_generate_point_id_deterministic(self):
        rel_path = "module6-bipedal-locomotion/6-2-zero-moment-point.mdx"
        idx = 3
        expected = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{rel_path}:{idx}"))

        assert generate_point_id(rel_path, idx) == expected
        assert generate_point_id(rel_path, idx) == generate_point_id(rel_path, idx)

    def test_extract_metadata_from_path(self):
        m1, c1 = extract_metadata_from_path("module1-ros2/1-1-intro.mdx")
        assert m1 == "module1"
        assert c1 == "1-1-intro"

        m6, c6 = extract_metadata_from_path("module6-bipedal-locomotion/6-2-zero-moment-point.mdx")
        assert m6 == "module6"
        assert c6 == "6-2-zero-moment-point"

    def test_extract_title_from_frontmatter(self):
        content = "---\ntitle: 'Zero-Moment Point Analysis'\n---\n# Ignored H1"
        assert extract_title(content, "default") == "Zero-Moment Point Analysis"

    def test_clean_markdown_removes_frontmatter_and_html(self):
        content = "---\ntitle: Foo\n---\n<CustomBadge text='test'/>\n\nActual paragraph."
        cleaned = clean_markdown(content)
        assert "title: Foo" not in cleaned
        assert "<CustomBadge" not in cleaned
        assert "Actual paragraph." in cleaned


class TestIngestionPlanning:
    """Tests for change detection and manifest reconciliation."""

    @pytest.fixture
    def mock_docs_dir(self, tmp_path: Path):
        docs = tmp_path / "ai-book-docs"
        mod1 = docs / "module1-ros2"
        mod1.mkdir(parents=True)

        f1 = mod1 / "1-1-intro.mdx"
        f1.write_text("# Chapter 1\nIntro text", encoding="utf-8")

        f2 = mod1 / "1-2-nodes.mdx"
        f2.write_text("# Chapter 2\nNodes text", encoding="utf-8")

        return docs

    def test_plan_ingestion_identifies_new_files(self, mock_docs_dir: Path):
        manifest = {}
        _, new_files, modified, unchanged, deleted = plan_ingestion(
            docs_dir=mock_docs_dir,
            manifest=manifest,
        )

        assert len(new_files) == 2
        assert "module1-ros2/1-1-intro.mdx" in new_files
        assert "module1-ros2/1-2-nodes.mdx" in new_files
        assert modified == []
        assert unchanged == []
        assert deleted == []

    def test_plan_ingestion_identifies_modified_and_unchanged(self, mock_docs_dir: Path):
        f1_path = mock_docs_dir / "module1-ros2" / "1-1-intro.mdx"
        f1_hash = compute_file_hash(f1_path)

        manifest = {
            "module1-ros2/1-1-intro.mdx": {
                "sha256": f1_hash,
                "chunk_ids": ["id-1"],
            },
            "module1-ros2/1-2-nodes.mdx": {
                "sha256": "outdated_hash_123",
                "chunk_ids": ["id-2"],
            },
            "module1-ros2/1-3-deleted.mdx": {
                "sha256": "deleted_hash",
                "chunk_ids": ["id-3"],
            },
        }

        _, new_files, modified, unchanged, deleted = plan_ingestion(
            docs_dir=mock_docs_dir,
            manifest=manifest,
        )

        assert new_files == []
        assert modified == ["module1-ros2/1-2-nodes.mdx"]
        assert unchanged == ["module1-ros2/1-1-intro.mdx"]
        assert deleted == ["module1-ros2/1-3-deleted.mdx"]

    def test_run_ingestion_dry_run_makes_no_mutations(self, mock_docs_dir: Path, tmp_path: Path):
        manifest_file = tmp_path / ".ingest_manifest.json"

        with patch("ingest_docs.VectorStore") as mock_vs_cls:
            run_ingestion(
                incremental=True,
                force=False,
                dry_run=True,
                manifest_path=manifest_file,
            )

            # VectorStore should not have been initialized or called in dry-run
            mock_vs_cls.assert_not_called()
            # Manifest file should not have been created
            assert not manifest_file.exists()
