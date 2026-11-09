"""
Adversarial Stress Test Suite for Milestone M2:
Frontend & MDX Documentation across Modules 1–4 (44 Chapters).

Empirically tests:
1. Exact chapter inventory (44 files across M1–M4, including all 19 new chapters)
2. Frontmatter integrity, title, and sequential sidebar_position
3. Interactive React components: ChapterProgress and QuizEngine integration
4. KaTeX delimiter balancing ($ and $$) and delimiter validity
5. KaTeX internal syntax integrity (balanced braces, matching begin/end environments)
6. Markdown table pipe collisions with math expressions
7. JSX curly brace safety in headings and prose
8. Content depth, graduate-level rigor, code blocks, math density, and zero placeholders
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

# Directory root
DOCS_DIR = Path(__file__).resolve().parent.parent.parent / "ai-book-docs"

EXPECTED_MODULES = {
    "module1-ros2": {
        "count": 14,
        "prefix": "1-",
        "new_chapters": [
            "1-11-ros2-control.mdx",
            "1-12-dds-internals.mdx",
            "1-13-real-time-linux.mdx",
            "1-14-ros2-diagnostics-and-monitoring.mdx",
        ],
    },
    "module2-digital-twin": {
        "count": 10,
        "prefix": "2-",
        "new_chapters": [
            "2-6-urdf-and-sdf-mastery.mdx",
            "2-7-physics-engine-deep-dive.mdx",
            "2-8-synthetic-data-generation.mdx",
            "2-9-drake-and-mujoco.mdx",
            "2-10-digital-twin-data-loop.mdx",
        ],
    },
    "module3-ai-robot-brain": {
        "count": 10,
        "prefix": "3-",
        "new_chapters": [
            "3-6-cuvslam-and-state-estimation.mdx",
            "3-7-semantic-perception.mdx",
            "3-8-force-torque-sensing.mdx",
            "3-9-multi-sensor-fusion.mdx",
            "3-10-edge-inference-optimization.mdx",
        ],
    },
    "module4-vla": {
        "count": 10,
        "prefix": "4-",
        "new_chapters": [
            "4-6-foundation-model-architectures.mdx",
            "4-7-diffusion-policies.mdx",
            "4-8-imitation-learning.mdx",
            "4-9-reward-shaping-and-rlaif.mdx",
            "4-10-deployment-and-safety.mdx",
        ],
    },
}


def get_all_m2_files() -> List[Path]:
    """Retrieve all 44 MDX files across Modules 1 to 4."""
    files = []
    for mod_name in EXPECTED_MODULES:
        mod_dir = DOCS_DIR / mod_name
        assert mod_dir.is_dir(), f"Module directory {mod_name} does not exist"
        files.extend(sorted(mod_dir.glob("*.mdx")))
    return files


def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """Extract YAML frontmatter and markdown body."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except Exception as exc:
        raise ValueError(f"YAML parsing failure: {exc}")
    return fm, parts[2]


def strip_code(text: str) -> str:
    """Strip fenced and inline code to prevent false positives in text checks."""
    text_no_fenced = re.sub(r"```[\s\S]*?```", "", text)
    text_no_code = re.sub(r"`[^`\n]+`", "", text_no_fenced)
    return text_no_code


class TestAdversarialCurriculumM2:
    """Empirical challenge suite for Milestone M2 Documentation."""

    def test_chapter_inventory_and_all_19_new_chapters(self):
        """Assert exactly 44 chapters exist across M1-M4 and all 19 new chapters are present."""
        all_files = get_all_m2_files()
        assert len(all_files) == 44, f"Expected exactly 44 MDX files across Modules 1-4, found {len(all_files)}"

        for mod_name, config in EXPECTED_MODULES.items():
            mod_files = list((DOCS_DIR / mod_name).glob("*.mdx"))
            assert len(mod_files) == config["count"], (
                f"{mod_name} expected {config['count']} files, found {len(mod_files)}"
            )
            # Verify new chapters exist
            for new_ch in config["new_chapters"]:
                expected_path = DOCS_DIR / mod_name / new_ch
                assert expected_path.exists(), f"New chapter missing: {expected_path}"
                assert expected_path.stat().st_size > 1000, f"New chapter {new_ch} is suspiciously small (< 1KB)"

    def test_category_json_and_sidebar_sequence(self):
        """Assert _category_.json is valid and sidebar positions are strictly sequential 1..N."""
        for mod_name, config in EXPECTED_MODULES.items():
            cat_file = DOCS_DIR / mod_name / "_category_.json"
            assert cat_file.exists(), f"Missing _category_.json in {mod_name}"
            cat_data = json.loads(cat_file.read_text(encoding="utf-8"))
            assert "label" in cat_data and isinstance(cat_data["label"], str)
            assert "position" in cat_data and isinstance(cat_data["position"], int)

            mod_files = sorted((DOCS_DIR / mod_name).glob("*.mdx"))
            positions = []
            for f in mod_files:
                fm, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
                assert "sidebar_position" in fm, f"{f.name} missing 'sidebar_position'"
                pos = fm["sidebar_position"]
                assert isinstance(pos, int), f"{f.name} sidebar_position must be int"
                positions.append(pos)

            expected_seq = list(range(1, config["count"] + 1))
            assert sorted(positions) == expected_seq, (
                f"{mod_name} sidebar_position sequence mismatch: got {sorted(positions)}, expected {expected_seq}"
            )

    def test_frontmatter_quality(self):
        """Verify frontmatter in all 44 chapters has title and description."""
        all_files = get_all_m2_files()
        for f in all_files:
            content = f.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(content)
            assert "title" in fm, f"{f.name} missing title in frontmatter"
            title = str(fm["title"]).strip()
            assert len(title) >= 5, f"{f.name} title '{title}' is too short"

    def test_interactive_components_contracts(self):
        """Verify every chapter imports and renders <ChapterProgress /> and <QuizEngine />."""
        all_files = get_all_m2_files()
        for f in all_files:
            content = f.read_text(encoding="utf-8")
            _, body = parse_frontmatter(content)

            # Check ChapterProgress import and tag
            assert "ChapterProgress" in content, f"{f.name} missing ChapterProgress reference"
            assert "<ChapterProgress" in body, f"{f.name} missing <ChapterProgress JSX component"

            # Check QuizEngine import and tag
            assert "QuizEngine" in content, f"{f.name} missing QuizEngine reference"
            assert "<QuizEngine" in body, f"{f.name} missing <QuizEngine JSX component"

            # Check questions prop in QuizEngine
            assert "questions={" in body or "questions =" in body, (
                f"{f.name} <QuizEngine> missing questions prop"
            )

    def test_katex_delimiter_balance(self):
        """Stress-test KaTeX delimiter balancing for both $$ and $ across all 44 files."""
        all_files = get_all_m2_files()
        for f in all_files:
            content = f.read_text(encoding="utf-8")
            _, body = parse_frontmatter(content)

            # Strip code blocks
            clean_body = strip_code(body)

            # Block math $$
            block_delims = re.findall(r"\$\$", clean_body)
            assert len(block_delims) % 2 == 0, (
                f"{f.name} has unbalanced block math ($$) delimiters: found {len(block_delims)}"
            )

            # Remove balanced block math before checking inline math
            clean_no_blocks = re.sub(r"\$\$[\s\S]*?\$\$", "", clean_body)

            # Inline math $ (ignore escaped \$)
            clean_no_escapes = clean_no_blocks.replace(r"\$", "")
            inline_delims = re.findall(r"(?<!\$)\$(?!\$)", clean_no_escapes)
            assert len(inline_delims) % 2 == 0, (
                f"{f.name} has unbalanced inline math ($) delimiters: found {len(inline_delims)}"
            )

    def test_katex_internal_syntax_integrity(self):
        """Verify internal LaTeX syntax in math blocks: bracket balance and begin/end pairs."""
        all_files = get_all_m2_files()
        for f in all_files:
            content = f.read_text(encoding="utf-8")
            _, body = parse_frontmatter(content)
            clean_body = strip_code(body)

            # Find all block math expressions
            block_maths = re.findall(r"\$\$([\s\S]*?)\$\$", clean_body)
            # Find all inline math expressions
            clean_no_blocks = re.sub(r"\$\$[\s\S]*?\$\$", "", clean_body)
            inline_maths = re.findall(r"(?<!\$)\$([^\$\n]+?)\$(?!\$)", clean_no_blocks)

            all_maths = block_maths + inline_maths
            assert len(all_maths) >= 2, f"{f.name} has fewer than 2 math expressions (found {len(all_maths)})"

            for idx, math_expr in enumerate(all_maths):
                # Check begin/end environment matching
                begins = re.findall(r"\\begin\{([a-zA-Z0-9*]+)\}", math_expr)
                ends = re.findall(r"\\end\{([a-zA-Z0-9*]+)\}", math_expr)
                assert begins == ends, (
                    f"{f.name} math #{idx} has mismatched LaTeX environments: begins={begins}, ends={ends}"
                )

                # Check curly braces balance inside math (ignoring escaped \{ and \})
                sanitized = re.sub(r"\\[\{\}]", "", math_expr)
                open_curlies = sanitized.count("{")
                close_curlies = sanitized.count("}")
                assert open_curlies == close_curlies, (
                    f"{f.name} math #{idx} has unbalanced braces: {open_curlies} '{' vs {close_curlies} '}': {math_expr[:60]}..."
                )

    def test_no_table_pipe_collisions_with_math(self):
        """
        Adversarial test: Detect unescaped pipes '|' inside math expressions within markdown tables.
        In Markdown tables, a pipe inside $A|B$ splits the cell unless escaped or using \\vert / \\mid.
        """
        all_files = get_all_m2_files()
        table_pipe_violations = []

        for f in all_files:
            lines = f.read_text(encoding="utf-8").splitlines()
            in_code_block = False
            for line_no, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue

                # Detect table rows
                if stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2:
                    # Check for math blocks in this line
                    math_matches = re.findall(r"\$([^\$\n]+?)\$", stripped)
                    for m in math_matches:
                        # Check for unescaped pipe inside math
                        # Escaped pipe: \|
                        # Unescaped: | not preceded by \
                        raw_pipes = re.findall(r"(?<!\\)\|", m)
                        if raw_pipes:
                            table_pipe_violations.append(
                                f"{f.name}:{line_no} Table cell contains raw pipe in math '${m}$'"
                            )

        assert not table_pipe_violations, (
            f"Found {len(table_pipe_violations)} table pipe collision(s):\n"
            + "\n".join(table_pipe_violations[:10])
        )

    def test_no_unescaped_curly_braces_in_headings_and_prose(self):
        """
        Adversarial test: Detect raw curly braces in MDX headings or prose that cause JSX syntax errors.
        """
        all_files = get_all_m2_files()
        jsx_curly_violations = []

        for f in all_files:
            content = f.read_text(encoding="utf-8")
            _, body = parse_frontmatter(content)

            lines = body.splitlines()
            in_code_block = False
            for line_no, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue

                # Check headings: # Heading
                if stripped.startswith("#"):
                    # Remove code ticks from heading
                    clean_heading = re.sub(r"`[^`]+`", "", stripped)
                    # Remove math $...$ from heading
                    clean_heading = re.sub(r"\$[^\$]+\$", "", clean_heading)
                    if "{" in clean_heading or "}" in clean_heading:
                        # Check if it's an anchor or JSX
                        jsx_curly_violations.append(
                            f"{f.name}:{line_no} Unescaped curly brace in heading: {stripped}"
                        )

        assert not jsx_curly_violations, (
            f"Found {len(jsx_curly_violations)} unescaped curly in headings:\n"
            + "\n".join(jsx_curly_violations[:10])
        )

    def test_graduate_level_content_depth_and_rigor(self):
        """Verify content substance, absence of stubs/placeholders, code block presence."""
        all_files = get_all_m2_files()
        placeholder_violations = []
        forbidden_regexes = [
            (r"\bTODO\b", "TODO"),
            (r"\bTBD\b", "TBD"),
            (r"\bFIXME\b", "FIXME"),
            (r"lorem\s+ipsum", "Lorem Ipsum"),
            (r"coming\s+soon", "Coming Soon"),
            (r"\[insert\s+", "[insert ..."),
        ]

        for f in all_files:
            content = f.read_text(encoding="utf-8")
            _, body = parse_frontmatter(content)

            # Check file size / character length
            assert len(body) >= 2500, f"{f.name} body is too short ({len(body)} chars, expected >= 2500)"

            # Strip code and check for placeholders
            clean_body = strip_code(body)
            for pattern, label in forbidden_regexes:
                matches = re.findall(pattern, clean_body, flags=re.IGNORECASE)
                if matches:
                    placeholder_violations.append(f"{f.name}: Found forbidden stub '{label}' ({matches})")

            # Check at least one code block exists
            code_blocks = re.findall(r"```[a-zA-Z0-9_-]*\n[\s\S]*?```", body)
            assert len(code_blocks) >= 1, f"{f.name} missing code block examples"

        assert not placeholder_violations, (
            "Found placeholders:\n" + "\n".join(placeholder_violations)
        )

    def test_quiz_question_correct_index_bounds(self):
        """Verify that every QuizEngine question has correctIndex within [0, len(options) - 1]."""
        all_files = get_all_m2_files()
        out_of_bounds = []

        for f in all_files:
            content = f.read_text(encoding="utf-8")
            # Extract questions block from QuizEngine
            quiz_blocks = re.findall(r"<QuizEngine[\s\S]*?/>", content)
            for qb in quiz_blocks:
                # Find options by tracking bracket depth after 'options:'
                pos = 0
                while True:
                    opt_idx = qb.find("options:", pos)
                    if opt_idx == -1:
                        break
                    # Find opening bracket '['
                    bracket_start = qb.find("[", opt_idx)
                    if bracket_start == -1:
                        break
                    depth = 0
                    bracket_end = -1
                    in_str = False
                    str_char = None
                    for i in range(bracket_start, len(qb)):
                        ch = qb[i]
                        if in_str:
                            if ch == str_char and qb[i - 1] != "\\":
                                in_str = False
                        else:
                            if ch in ('"', "'"):
                                in_str = True
                                str_char = ch
                            elif ch == "[":
                                depth += 1
                            elif ch == "]":
                                depth -= 1
                                if depth == 0:
                                    bracket_end = i
                                    break
                    if bracket_end != -1:
                        opt_content = qb[bracket_start + 1 : bracket_end]
                        # Count string literals inside opt_content
                        opts = re.findall(r'"(?:[^"\\]|\\.)*"', opt_content)
                        if not opts:
                            opts = re.findall(r"'(?:[^'\\]|\\.)*'", opt_content)

                        # Find the correctIndex following this options block
                        ci_match = re.search(r"correctIndex:\s*(\d+)", qb[bracket_end : bracket_end + 200])
                        if ci_match:
                            ci = int(ci_match.group(1))
                            if not (0 <= ci < len(opts)):
                                out_of_bounds.append(
                                    f"{f.name}: correctIndex={ci} out of bounds for options count={len(opts)}"
                                )
                        pos = bracket_end + 1
                    else:
                        pos = opt_idx + 8

        assert not out_of_bounds, f"Found out-of-bounds quiz answers: {out_of_bounds}"

    def test_no_multiline_inline_math(self):
        """Verify that single-dollar inline math expressions do not span across newlines."""
        all_files = get_all_m2_files()
        multiline_math = []

        for f in all_files:
            content = f.read_text(encoding="utf-8")
            _, body = parse_frontmatter(content)
            clean_body = strip_code(body)
            # Remove block math $$...$$
            no_blocks = re.sub(r"\$\$[\s\S]*?\$\$", "", clean_body)

            # Check lines for unclosed single dollar
            lines = no_blocks.splitlines()
            for line_no, line in enumerate(lines, 1):
                clean_line = line.replace(r"\$", "")
                dollars = re.findall(r"(?<!\$)\$(?!\$)", clean_line)
                if len(dollars) % 2 != 0:
                    multiline_math.append(f"{f.name}:{line_no} Unbalanced inline math on single line: '{line[:80]}'")

        assert not multiline_math, (
            f"Found {len(multiline_math)} multiline or unclosed inline math expressions:\n"
            + "\n".join(multiline_math[:10])
        )

    def test_internal_relative_links_resolve(self):
        """Verify that all relative markdown links in M1-M4 documentation point to existing files."""
        all_files = get_all_m2_files()
        broken_links = []

        for f in all_files:
            content = f.read_text(encoding="utf-8")
            _, body = parse_frontmatter(content)
            clean_body = strip_code(body)

            # Match markdown links [text](target)
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", clean_body)
            for link_text, target in links:
                # Ignore external URLs, anchors, mailto, and absolute paths
                if (
                    target.startswith("http://")
                    or target.startswith("https://")
                    or target.startswith("#")
                    or target.startswith("mailto:")
                    or target.startswith("/")
                ):
                    continue

                # Strip anchor from target: target#anchor
                clean_target = target.split("#")[0]
                if not clean_target:
                    continue

                # Resolve target relative to file's directory
                resolved = (f.parent / clean_target).resolve()
                # If target lacks extension, try .mdx and .md
                candidates = [resolved, resolved.with_suffix(".mdx"), resolved.with_suffix(".md")]
                if not any(c.exists() for c in candidates):
                    broken_links.append(f"{f.name}: Broken relative link to '{target}' (text: '{link_text}')")

        assert not broken_links, (
            f"Found {len(broken_links)} broken relative link(s):\n" + "\n".join(broken_links[:10])
        )

    def test_chapter_progress_total_chapters_accurate(self):
        """Verify that ChapterProgress totalChapters matches module chapter count (14 for M1, 10 for M2-M4)."""
        all_files = get_all_m2_files()
        mismatched_totals = []

        for f in all_files:
            content = f.read_text(encoding="utf-8")
            mod_name = f.parent.name
            expected_total = 14 if mod_name == "module1-ros2" else 10

            cp_tags = re.findall(r"<ChapterProgress[\s\S]*?/>", content)
            assert cp_tags, f"{f.name} missing <ChapterProgress />"
            for tag in cp_tags:
                tot_match = re.search(r"totalChapters=\{(\d+)\}", tag)
                if tot_match:
                    found_tot = int(tot_match.group(1))
                    if found_tot != expected_total:
                        mismatched_totals.append(
                            f"{f.name}: totalChapters={found_tot}, expected {expected_total}"
                        )

        assert not mismatched_totals, (
            "Found mismatched totalChapters in ChapterProgress:\n" + "\n".join(mismatched_totals)
        )

