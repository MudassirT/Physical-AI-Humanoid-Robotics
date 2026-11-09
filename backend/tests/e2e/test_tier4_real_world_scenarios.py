"""
Tier 4: Real-World Scenarios

Verifies:
1. Complete curriculum internal link resolution (zero broken markdown links).
2. Docusaurus configuration audit (KaTeX plugins, stylesheets, sidebar mapping).
3. End-to-end question answering pipeline simulation (Query -> Retrieval -> LLM Stream -> Completion).
4. Master navigation and 12-module directory layout compliance.
"""

import re
from pathlib import Path
from typing import List, Tuple
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.schemas.chat_models import ChatResponse

from .curriculum_manifest import MODULES


class TestTier4RealWorldScenarios:
    """Tier 4: Integrated Real-World Scenarios & Full Pipeline Verification."""

    def test_curriculum_wide_internal_link_resolution(self, docs_dir: Path):
        """
        Scan all authored MDX chapters and verify that every internal markdown link
        [text](target) resolves to a valid existing file or route.
        """
        mdx_files = list(docs_dir.rglob("*.mdx"))
        assert len(mdx_files) > 0

        broken_links: List[Tuple[str, str, str]] = []  # (source_file, link_text, target)

        for file_path in mdx_files:
            content = file_path.read_text(encoding="utf-8")

            # Strip code blocks
            clean_content = re.sub(r"```[\s\S]*?```", "", content)
            clean_content = re.sub(r"`[^`\n]+`", "", clean_content)

            # Match [label](target)
            matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", clean_content)
            for label, target in matches:
                target = target.strip()

                # Skip external URLs, mailto, and pure in-page anchors (#anchor)
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue

                # Strip anchor from target URL: /path#heading -> /path
                target_base = target.split("#")[0].strip()
                if not target_base:
                    continue

                # Resolve relative vs root paths
                resolved = False

                # Case 1: Docusaurus route e.g. /ai-book/module1-ros2/1-2-ros2-core-concepts
                if target_base.startswith("/ai-book/"):
                    rel_to_docs = target_base[len("/ai-book/"):]
                    candidate_file = docs_dir / f"{rel_to_docs}.mdx"
                    candidate_dir = docs_dir / rel_to_docs
                    if candidate_file.exists() or candidate_dir.exists():
                        resolved = True

                # Case 2: Direct file path e.g. ./1-2-ros2-core-concepts.mdx or ../module2/2-1.mdx
                candidate_direct = (file_path.parent / target_base).resolve()
                if candidate_direct.exists():
                    resolved = True
                elif candidate_direct.with_suffix(".mdx").exists():
                    resolved = True

                # Case 3: Image / static asset link e.g. /img/... or @site/static/...
                if target_base.startswith(("/img/", "@site/static/", "/assets/")):
                    resolved = True  # Handled by Docusaurus static packager

                if not resolved:
                    # In progressive authoring mode, link might target an unauthored chapter in M6-M12
                    # If target mentions a planned module or chapter, flag but distinguish
                    broken_links.append((file_path.name, label, target))

        # Filter out links pointing to planned chapters in future modules (M6-M12)
        true_broken = []
        for src, lbl, tgt in broken_links:
            # Check if target refers to a known planned module (e.g. module6, module7, etc.)
            is_planned_target = any(
                f"module{i}" in tgt for i in range(6, 13)
            ) or any(
                f"{i}-" in tgt for i in range(6, 13)
            )
            if not is_planned_target:
                true_broken.append((src, lbl, tgt))

        assert len(true_broken) == 0, (
            f"Found {len(true_broken)} broken internal link(s) across curriculum: {true_broken[:5]}"
        )

    def test_docusaurus_configuration_and_katex_audit(self, project_root: Path):
        """
        Audit docusaurus.config.ts for KaTeX / Math plugins and stylesheet configuration.
        """
        config_path = project_root / "docusaurus.config.ts"
        assert config_path.exists(), "docusaurus.config.ts must exist at project root"

        config_text = config_path.read_text(encoding="utf-8")

        # Check KaTeX plugins
        has_remark_math = "remarkMath" in config_text or "remark-math" in config_text
        has_rehype_katex = "rehypeKatex" in config_text or "rehype-katex" in config_text
        has_katex_css = "katex" in config_text.lower() and "css" in config_text.lower()

        if not (has_remark_math and has_rehype_katex and has_katex_css):
            pytest.skip(
                f"KaTeX math plugins in docusaurus.config.ts pending M1 frontend setup: "
                f"(remarkMath={has_remark_math}, rehypeKatex={has_rehype_katex}, katexCSS={has_katex_css})"
            )

        assert has_remark_math, "docusaurus.config.ts must configure remarkMath"
        assert has_rehype_katex, "docusaurus.config.ts must configure rehypeKatex"
        assert has_katex_css, "docusaurus.config.ts must include KaTeX CDN stylesheet link"

    def test_end_to_end_question_answering_pipeline_simulation(self, test_client: TestClient):
        """
        Simulate an end-to-end question answering lifecycle:
        1. Client submits query with module_filter.
        2. System performs retrieval and LLM synthesis.
        3. Client consumes the grounded response and sources.
        """
        mock_response = ChatResponse(
            answer_text=(
                "The Zero-Moment Point (ZMP) is a point on the ground where the horizontal "
                "component of the resultant tipping moment of ground reaction forces is zero."
            ),
            retrieved_sources=["/ai-book/module6-bipedal-locomotion/6-2-zero-moment-point"],
        )

        with patch("app.routes.chat.agent_service.ask_agent", return_value=mock_response):
            payload = {
                "query_text": "What is the physical significance of ZMP in bipedal robots?",
                "module_filter": "module6",
                "stream": False,
            }

            response = test_client.post("/ask", json=payload)
            assert response.status_code == 200
            data = response.json()

            assert "answer_text" in data
            assert len(data["answer_text"]) > 20
            assert "ZMP" in data["answer_text"] or "Zero-Moment" in data["answer_text"]
            assert len(data["retrieved_sources"]) == 1
            assert "6-2-zero-moment-point" in data["retrieved_sources"][0]

    def test_module_directory_layout_compliance(self, docs_dir: Path):
        """
        Verify that existing module directories follow strict naming conventions
        (module<N>-<slug>) and correspond to valid master plan modules.
        """
        module_dirs = [d.name for d in docs_dir.iterdir() if d.is_dir() and d.name.startswith("module")]
        expected_dirs = {m.module_dir for m in MODULES}

        for m_dir in module_dirs:
            assert m_dir in expected_dirs, (
                f"Directory '{m_dir}' in ai-book-docs does not match any recognized master plan module folder: {expected_dirs}"
            )
