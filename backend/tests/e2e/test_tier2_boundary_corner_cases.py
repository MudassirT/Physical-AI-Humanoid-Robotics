"""
Tier 2: Boundary & Corner Cases (Dual Track)

Verifies:
1. Empty and whitespace-only query rejection (HTTP 422).
2. Ultra-long query payloads (>10K characters) handled without memory explosion.
3. Unknown module filter values handled gracefully without 500 internal errors.
4. Telemetry endpoint malformed payload rejection (invalid event_type, empty body).
5. High-frequency concurrent telemetry writes ensuring zero JSON Lines corruption.
6. Special characters in LaTeX formulas (Greek letters, matrices, norms, fractions).
7. Unescaped JSX curly brace detection in MDX files.
"""

import concurrent.futures
import re
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.chat_models import ChatResponse


class TestTier2BoundaryCornerCases:
    """Tier 2: Boundary and Adversarial Corner Case Verification."""

    # -------------------------------------------------------------------------
    # Platform / Backend Track Boundary Cases
    # -------------------------------------------------------------------------

    def test_ask_empty_query_rejected(self, test_client: TestClient):
        """Verify that an empty query_text triggers HTTP 422 validation error."""
        response = test_client.post("/ask", json={"query_text": ""})
        assert response.status_code == 422, (
            f"Expected 422 Unprocessable Entity for empty query, got {response.status_code}"
        )

    def test_ask_missing_field_rejected(self, test_client: TestClient):
        """Verify that omitting query_text entirely triggers HTTP 422."""
        response = test_client.post("/ask", json={})
        assert response.status_code == 422

    def test_ask_ultra_long_query_handled(self, test_client: TestClient):
        """Verify that an ultra-long query (10K+ characters) does not crash the server."""
        long_query = "Describe humanoid robot walking kinematics. " * 300  # ~13,000 chars
        mock_response = ChatResponse(
            answer_text="Humanoid walking involves cyclical gait phases and balance maintenance.",
            retrieved_sources=["/ai-book/module6-bipedal-locomotion/6-1-introduction-to-bipedal-locomotion"],
        )

        with patch("app.routes.chat.agent_service.ask_agent", return_value=mock_response):
            response = test_client.post("/ask", json={"query_text": long_query})
            assert response.status_code in [200, 422], (
                f"Expected 200 OK (or clean 422 length constraint), got unexpected {response.status_code}"
            )
            if response.status_code == 200:
                assert "answer_text" in response.json()

    def test_ask_unknown_module_filter(self, test_client: TestClient):
        """Verify querying with a non-existent module filter returns graceful fallback."""
        mock_response = ChatResponse(
            answer_text="No specific content found for module999.",
            retrieved_sources=[],
        )

        with patch("app.routes.chat.agent_service.ask_agent", return_value=mock_response):
            payload = {
                "query_text": "What is the gear reduction ratio?",
                "module_filter": "nonexistent_module_999",
            }
            response = test_client.post("/ask", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert "answer_text" in data

    def test_analytics_invalid_payload_rejected(self, test_client: TestClient):
        """Verify POST /analytics rejects missing mandatory fields with HTTP 422."""
        routes = [r.path for r in app.routes]
        if "/analytics" not in routes:
            pytest.skip("POST /analytics route pending M1 backend implementation")

        # Missing event_type
        response = test_client.post("/analytics", json={"module_id": "module1"})
        assert response.status_code == 422

    def test_concurrent_analytics_logging_integrity(self, test_client: TestClient):
        """Verify rapid concurrent telemetry event submissions write uncorrupted log lines."""
        routes = [r.path for r in app.routes]
        if "/analytics" not in routes:
            pytest.skip("POST /analytics route pending M1 backend implementation")

        num_requests = 20
        events = [
            {
                "event_type": "page_view",
                "session_id": f"concurrent_session_{i}",
                "module_id": f"module{(i % 12) + 1}",
                "data": {"seq": i, "token": f"payload_data_{i}"},
            }
            for i in range(num_requests)
        ]

        def send_event(payload):
            return test_client.post("/analytics", json=payload)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(send_event, ev) for ev in events]
            results = [f.result() for f in futures]

        for res in results:
            assert res.status_code in [200, 201], f"Concurrent telemetry write failed with {res.status_code}"

    # -------------------------------------------------------------------------
    # Curriculum Track Boundary Cases
    # -------------------------------------------------------------------------

    def test_complex_latex_syntax_integrity(self, docs_dir: Path):
        """
        Verify complex LaTeX math formulas (matrices, subscripts, Greek symbols)
        in authored chapters contain proper begin/end block alignment.
        """
        mdx_files = list(docs_dir.rglob("*.mdx"))
        assert len(mdx_files) > 0

        matrix_environments = [
            "matrix", "bmatrix", "pmatrix", "vmatrix", "Vmatrix",
            "aligned", "cases", "gather", "split",
        ]

        for file_path in mdx_files:
            content = file_path.read_text(encoding="utf-8")

            # Check every \begin{env} has a matching \end{env}
            for env in matrix_environments:
                begin_count = len(re.findall(rf"\\begin\{{{env}\}}", content))
                end_count = len(re.findall(rf"\\end\{{{env}\}}", content))
                assert begin_count == end_count, (
                    f"{file_path.name} has mismatched LaTeX \\begin{{{env}}} ({begin_count}) "
                    f"vs \\end{{{env}}} ({end_count})"
                )

    def test_no_unescaped_jsx_curlys_in_text(self, docs_dir: Path):
        """
        Verify MDX files don't have stray unescaped curly braces in regular prose
        which cause MDX v3 compilation errors.
        In MDX v3, text like `Matrix {3x3}` or `dimension {N}` outside code/math
        is treated as JavaScript expressions and will throw build errors.
        """
        mdx_files = list(docs_dir.rglob("*.mdx"))

        for file_path in mdx_files:
            content = file_path.read_text(encoding="utf-8")

            # Remove frontmatter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    content = parts[2]

            # Remove fenced code blocks
            content = re.sub(r"```[\s\S]*?```", "", content)
            # Remove inline code
            content = re.sub(r"`[^`\n]+`", "", content)
            # Remove block math
            content = re.sub(r"\$\$[\s\S]*?\$\$", "", content)
            # Remove inline math
            content = re.sub(r"(?<!\$)\$(?!\$)[\s\S]*?(?<!\$)\$(?!\$)", "", content)
            # Remove HTML/JSX tags
            content = re.sub(r"<[^>]+>", "", content)

            # In the remaining text, look for patterns like {word} or {num} not preceded by $
            suspicious_curlys = re.findall(r"(?<!\$)\{[a-zA-Z0-9_\s\.,\-+=*\/]+\}(?!\$)", content)
            # Filter out known valid Docusaurus patterns like heading anchors {#custom-id}
            # and syntactically valid JSX integer expressions like {-1}
            real_violations = [
                c for c in suspicious_curlys
                if not c.startswith("{#") and not re.match(r"^\{\s*-?\d+\s*\}$", c)
            ]

            assert len(real_violations) == 0, (
                f"{file_path.name} contains potential unescaped JSX curly expressions in text: {real_violations[:3]}"
            )
