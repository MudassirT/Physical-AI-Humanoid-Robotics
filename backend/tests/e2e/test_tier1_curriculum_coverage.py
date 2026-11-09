"""
Tier 1: Feature Coverage (Curriculum Track)

Verifies:
1. Valid YAML frontmatter across all existing MDX chapters.
2. Mandatory `title` and `sidebar_position` fields.
3. KaTeX math delimiter balancing ($...$ and $$...$$).
4. Code block syntax and unclosed fence detection.
5. Directory `_category_.json` files for proper sidebar ordering.
6. Master plan 110-chapter presence matrix audit.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

import pytest
import yaml

from .curriculum_manifest import ChapterSpec, get_all_chapters


def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """Extract YAML frontmatter and remaining markdown body."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except Exception as exc:
        pytest.fail(f"Invalid YAML frontmatter: {exc}")

    body = parts[2]
    return frontmatter, body


def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks to prevent false positives in math/JSX checks."""
    # Remove triple-backtick code blocks
    text_no_code = re.sub(r"```[\s\S]*?```", "", text)
    # Remove inline code
    text_no_code = re.sub(r"`[^`\n]+`", "", text_no_code)
    return text_no_code


class TestTier1CurriculumCoverage:
    """Tier 1: Comprehensive Curriculum Verification."""

    def test_existing_chapters_frontmatter(self, docs_dir: Path):
        """Verify frontmatter on all currently authored MDX chapters."""
        mdx_files = list(docs_dir.rglob("*.mdx"))
        assert len(mdx_files) > 0, "No MDX files found in ai-book-docs/"

        for file_path in mdx_files:
            content = file_path.read_text(encoding="utf-8")
            frontmatter, body = parse_frontmatter(content)

            # Assert frontmatter exists
            assert frontmatter, f"{file_path.name} missing or empty frontmatter"

            # Assert title exists and is non-empty string
            assert "title" in frontmatter, f"{file_path.name} missing 'title' in frontmatter"
            assert isinstance(frontmatter["title"], str) and len(frontmatter["title"].strip()) > 0, (
                f"{file_path.name} has empty or non-string 'title'"
            )

            # Assert sidebar_position exists and is integer (except intro if configured separately)
            if file_path.name != "intro.mdx":
                assert "sidebar_position" in frontmatter, (
                    f"{file_path.name} missing 'sidebar_position' in frontmatter"
                )
                assert isinstance(frontmatter["sidebar_position"], int), (
                    f"{file_path.name} 'sidebar_position' must be an integer"
                )

    def test_existing_chapters_katex_math_delimiters(self, docs_dir: Path):
        """Verify KaTeX math delimiters ($ and $$) are properly paired."""
        mdx_files = list(docs_dir.rglob("*.mdx"))

        for file_path in mdx_files:
            content = file_path.read_text(encoding="utf-8")
            _, body = parse_frontmatter(content)

            # Strip fenced code blocks
            clean_body = strip_code_blocks(body)

            # Check block math $$...$$
            # Replace escaped \$$ with nothing first
            block_matches = re.findall(r"\$\$", clean_body)
            assert len(block_matches) % 2 == 0, (
                f"{file_path.name} has unbalanced block math ($$) delimiters (count={len(block_matches)})"
            )

            # Remove balanced block math before checking inline math
            clean_body_no_blocks = re.sub(r"\$\$[\s\S]*?\$\$", "", clean_body)

            # Check inline math $...$
            # Ignore escaped \$
            clean_body_no_escapes = clean_body_no_blocks.replace(r"\$", "")
            inline_matches = re.findall(r"(?<!\$)\$(?!\$)", clean_body_no_escapes)
            assert len(inline_matches) % 2 == 0, (
                f"{file_path.name} has unbalanced inline math ($) delimiters (count={len(inline_matches)})"
            )

    def test_code_blocks_closure(self, docs_dir: Path):
        """Verify that all triple-backtick code blocks are properly terminated."""
        mdx_files = list(docs_dir.rglob("*.mdx"))

        for file_path in mdx_files:
            content = file_path.read_text(encoding="utf-8")
            # Count triple backticks
            matches = re.findall(r"```", content)
            assert len(matches) % 2 == 0, (
                f"{file_path.name} has unclosed code fence (total ``` count={len(matches)})"
            )

    def test_module_category_json_presence(self, docs_dir: Path):
        """Verify that existing module directories possess valid _category_.json files."""
        existing_module_dirs = [d for d in docs_dir.iterdir() if d.is_dir() and d.name.startswith("module")]

        for mod_dir in existing_module_dirs:
            category_file = mod_dir / "_category_.json"
            assert category_file.exists(), (
                f"Module directory '{mod_dir.name}' is missing '_category_.json' for Docusaurus sidebar"
            )
            data = json.loads(category_file.read_text(encoding="utf-8"))
            assert "label" in data and isinstance(data["label"], str), (
                f"{category_file} missing string 'label'"
            )
            assert "position" in data and isinstance(data["position"], int), (
                f"{category_file} missing integer 'position'"
            )

    def test_110_master_curriculum_audit(self, docs_dir: Path, project_root: Path):
        """
        Audit the 110-chapter master curriculum expansion.

        In progressive mode (M1-M4), asserts that all currently authored chapters exist,
        tracks planned chapters, and validates completion progress.
        In STRICT_110 mode (M5 final release gate), asserts that all 110 chapters exist.
        """
        all_specs = get_all_chapters()
        assert len(all_specs) == 111, f"Master manifest must declare exactly 111 documents (found {len(all_specs)})"

        present_chapters: List[ChapterSpec] = []
        missing_chapters: List[ChapterSpec] = []

        for spec in all_specs:
            full_path = project_root / spec.relative_path
            if full_path.exists():
                present_chapters.append(spec)
            else:
                missing_chapters.append(spec)

        print(f"\n[Curriculum Audit] Present: {len(present_chapters)}/111, Pending: {len(missing_chapters)}/111")

        # All chapters marked as initially existing MUST exist
        for spec in all_specs:
            if spec.is_existing_initially:
                full_path = project_root / spec.relative_path
                assert full_path.exists(), f"Initial chapter missing from repository: {spec.relative_path}"

        # If STRICT_110 is requested (M5 release gate), require all 110
        if os.environ.get("STRICT_110") == "1":
            assert len(missing_chapters) == 0, (
                f"STRICT_110 Gate Failed: {len(missing_chapters)} chapters not yet authored: "
                f"{[c.chapter_num for c in missing_chapters[:5]]}..."
            )
        else:
            # Progressive check: Ensure present chapters meet high quality standards
            assert len(present_chapters) >= 36, (
                f"Expected at least 36 pre-expansion chapters, found {len(present_chapters)}"
            )
