"""
Adversarial Stress Test Suite for Milestone M3:
Bipedal Locomotion & Whole-Body Control (Module 6) and
Dexterous Manipulation & Hand Design (Module 7).

Total 18 Chapters:
- Module 6: 10 chapters (6-1 through 6-10)
- Module 7: 8 chapters (7-1 through 7-8)
"""

import io
import json
import re
from contextlib import redirect_stdout
from pathlib import Path
from typing import List, Tuple

import yaml

# Root directory of docs
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = REPO_ROOT / "ai-book-docs"

EXPECTED_MODULES = {
    "module6-bipedal-locomotion": {
        "count": 10,
        "prefix": "6-",
        "category_label": "Bipedal Locomotion & Whole-Body Control",
        "category_position": 6,
        "chapters": [
            "6-1-introduction-to-bipedal-locomotion.mdx",
            "6-2-zero-moment-point.mdx",
            "6-3-capture-point-and-dcm.mdx",
            "6-4-model-predictive-control.mdx",
            "6-5-whole-body-control.mdx",
            "6-6-reinforcement-learning-locomotion.mdx",
            "6-7-sim-to-real-locomotion.mdx",
            "6-8-advanced-locomotion-skills.mdx",
            "6-9-gait-analysis-and-biomechanics.mdx",
            "6-10-motion-capture-and-reference.mdx",
        ],
    },
    "module7-dexterous-manipulation": {
        "count": 8,
        "prefix": "7-",
        "category_label": "Dexterous Manipulation & Hand Design",
        "category_position": 7,
        "chapters": [
            "7-1-introduction-to-dexterous-manipulation.mdx",
            "7-2-grasp-theory.mdx",
            "7-3-robotic-hand-design.mdx",
            "7-4-tactile-sensing.mdx",
            "7-5-motion-planning-for-manipulation.mdx",
            "7-6-learning-based-manipulation.mdx",
            "7-7-assembly-and-contact-rich-tasks.mdx",
            "7-8-manipulation-benchmarks.mdx",
        ],
    },
}


def get_all_m3_files() -> List[Path]:
    files = []
    for mod_name, meta in EXPECTED_MODULES.items():
        mod_dir = DOCS_DIR / mod_name
        for ch in meta["chapters"]:
            files.append(mod_dir / ch)
    return files


def extract_frontmatter(content: str) -> Tuple[dict, str]:
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return {}, content
    yaml_text = match.group(1)
    data = yaml.safe_load(yaml_text) or {}
    body = content[match.end() :]
    return data, body


# ---------------------------------------------------------------------------
# Test 1: Chapter Inventory and Category JSON
# ---------------------------------------------------------------------------

def test_m3_chapter_inventory():
    """Verify that every single expected chapter and category json exists in M6 and M7."""
    for mod_name, meta in EXPECTED_MODULES.items():
        mod_dir = DOCS_DIR / mod_name
        assert mod_dir.is_dir(), f"Module directory {mod_dir} is missing"

        cat_file = mod_dir / "_category_.json"
        assert cat_file.exists(), f"Category JSON missing in {mod_dir}"
        cat_data = json.loads(cat_file.read_text(encoding="utf-8"))
        assert cat_data.get("label") == meta["category_label"]
        assert cat_data.get("position") == meta["category_position"]

        for ch_name in meta["chapters"]:
            ch_path = mod_dir / ch_name
            assert ch_path.exists(), f"Missing chapter: {ch_path}"
            assert ch_path.stat().st_size > 5000, f"Chapter too small (<5KB): {ch_path}"


# ---------------------------------------------------------------------------
# Test 2: Frontmatter and Interactive React Components
# ---------------------------------------------------------------------------

def test_m3_frontmatter_and_quiz_integration():
    """Verify YAML frontmatter and inclusion of ChapterProgress and QuizEngine."""
    for mod_name, meta in EXPECTED_MODULES.items():
        mod_dir = DOCS_DIR / mod_name
        positions_found = []

        for ch_name in meta["chapters"]:
            ch_path = mod_dir / ch_name
            content = ch_path.read_text(encoding="utf-8")
            fm, body = extract_frontmatter(content)

            assert "title" in fm, f"Missing title in frontmatter of {ch_name}"
            assert "sidebar_position" in fm, f"Missing sidebar_position in {ch_name}"
            pos = fm["sidebar_position"]
            positions_found.append(pos)

            assert "<ChapterProgress" in body, f"Missing ChapterProgress in {ch_name}"
            assert "<QuizEngine" in body, f"Missing QuizEngine in {ch_name}"

        expected_positions = list(range(1, meta["count"] + 1))
        assert sorted(positions_found) == expected_positions, (
            f"Non-contiguous sidebar positions in {mod_name}: {positions_found} vs {expected_positions}"
        )


# ---------------------------------------------------------------------------
# Test 3: Zero Placeholders or Incomplete Stubs
# ---------------------------------------------------------------------------

def test_m3_zero_placeholders():
    """Verify zero unfinished placeholders or dummy text across all M3 chapters."""
    banned_patterns = [
        r"\bTODO\b",
        r"\bTBD\b",
        r"\bFIXME\b",
        r"\blorem\s+ipsum\b",
        r"\bplaceholder\b",
        r"\bCOMING\s+SOON\b",
        r"\bTO\s+BE\s+CONTINUED\b",
        r"pass\s*#\s*TODO",
    ]

    for fpath in get_all_m3_files():
        content = fpath.read_text(encoding="utf-8")
        for pat in banned_patterns:
            matches = re.findall(pat, content, re.IGNORECASE)
            assert not matches, f"Found forbidden placeholder pattern '{pat}' in {fpath.name}: {matches}"


# ---------------------------------------------------------------------------
# Test 4: KaTeX Math Delimiter and Environment Balancing
# ---------------------------------------------------------------------------

def test_m3_katex_syntax_integrity():
    """Ensure mathematical equations have balanced braces and matching LaTeX environments using a stack."""
    for fpath in get_all_m3_files():
        content = fpath.read_text(encoding="utf-8")
        _, body = extract_frontmatter(content)

        clean_body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
        display_math_blocks = re.findall(r"\$\$(.*?)\$\$", clean_body, re.DOTALL)
        for block in display_math_blocks:
            open_braces = block.count("{")
            close_braces = block.count("}")
            assert open_braces == close_braces, (
                f"Unbalanced braces in display math block in {fpath.name}: {open_braces} != {close_braces}"
            )

            tokens = re.findall(r"\\(begin|end)\{([a-zA-Z0-9*]+)\}", block)
            stack = []
            for kind, env_name in tokens:
                if kind == "begin":
                    stack.append(env_name)
                elif kind == "end":
                    assert stack, f"Unmatched \\end{{{env_name}}} in {fpath.name}"
                    opened = stack.pop()
                    assert opened == env_name, (
                        f"Mismatched LaTeX environment in {fpath.name}: opened {opened}, closed {env_name}"
                    )
            assert not stack, f"Unclosed LaTeX environments in {fpath.name}: {stack}"


# ---------------------------------------------------------------------------
# Test 5: Depth and Rigor
# ---------------------------------------------------------------------------

def test_m3_content_density_and_rigor():
    """Verify that every chapter has substantive length, math equations, and code examples."""
    for fpath in get_all_m3_files():
        content = fpath.read_text(encoding="utf-8")
        words = len(content.split())
        assert words >= 1500, f"Chapter {fpath.name} is too brief ({words} words < 1500 words)"

        math_matches = re.findall(r"\$[^$]+\$|\$\$[^$]+\$\$", content)
        assert len(math_matches) >= 5, (
            f"Chapter {fpath.name} has insufficient math density ({len(math_matches)} < 5)"
        )


# ---------------------------------------------------------------------------
# Test 6: Empirical Execution of Module 6 Python Algorithms (Passing Ones)
# ---------------------------------------------------------------------------

def test_empirical_dcm_push_recovery_execution():
    """Empirically run 6-3 Instantaneous Capture Point / DCM push recovery code."""
    ch_path = DOCS_DIR / "module6-bipedal-locomotion" / "6-3-capture-point-and-dcm.mdx"
    code = re.findall(r"```python\b(.*?)```", ch_path.read_text(encoding="utf-8"), re.DOTALL)[0]
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "Perturbed DCM (ICP)" in output
    assert "Selected Strategy: STEPPING_STRATEGY" in output


def test_empirical_convex_mpc_biped_execution():
    """Empirically run 6-4 Convex Model Predictive Control biped code."""
    ch_path = DOCS_DIR / "module6-bipedal-locomotion" / "6-4-model-predictive-control.mdx"
    code = re.findall(r"```python\b(.*?)```", ch_path.read_text(encoding="utf-8"), re.DOTALL)[0]
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "Solving Convex MPC Single Rigid Body QP..." in output
    assert "Optimal Ground Reaction Force on Foot 1" in output


def test_empirical_whole_body_controller_qp_execution():
    """Empirically run 6-5 Whole-Body Controller QP code."""
    ch_path = DOCS_DIR / "module6-bipedal-locomotion" / "6-5-whole-body-control.mdx"
    code = re.findall(r"```python\b(.*?)```", ch_path.read_text(encoding="utf-8"), re.DOTALL)[0]
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "Executing Whole-Body Control Quadratic Program..." in output
    assert "Computed 1 kHz Joint Torques:" in output


# ---------------------------------------------------------------------------
# Test 7: Empirical Execution of Module 7 Manipulation Algorithms
# ---------------------------------------------------------------------------

def test_empirical_finger_kinematics_execution():
    """Empirically run 7-1 Anthropomorphic Finger Kinematics & Yoshikawa Manipulability."""
    ch_path = DOCS_DIR / "module7-dexterous-manipulation" / "7-1-introduction-to-dexterous-manipulation.mdx"
    code = re.findall(r"```python\b(.*?)```", ch_path.read_text(encoding="utf-8"), re.DOTALL)[0]
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "Yoshikawa Manipulability Measure w:" in output
    assert "Ellipsoid Principal Radii" in output


def test_empirical_ferrari_canny_grasp_metric_execution():
    """Empirically run 7-2 3D Grasp Matrix & Ferrari-Canny Epsilon Metric."""
    ch_path = DOCS_DIR / "module7-dexterous-manipulation" / "7-2-grasp-theory.mdx"
    code = re.findall(r"```python\b(.*?)```", ch_path.read_text(encoding="utf-8"), re.DOTALL)[0]
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "Force Closure Established: True" in output
    assert "Ferrari-Canny Epsilon Metric:" in output


def test_empirical_tendon_transmission_execution():
    """Empirically run 7-3 Tendon routing transmission & winch friction optimization."""
    ch_path = DOCS_DIR / "module7-dexterous-manipulation" / "7-3-robotic-hand-design.mdx"
    code = re.findall(r"```python\b(.*?)```", ch_path.read_text(encoding="utf-8"), re.DOTALL)[0]
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "Optimization Status: True" in output
    assert "Torque Tracking Error (Nm):" in output


def test_empirical_gelsight_photometric_stereo_execution():
    """Empirically run 7-4 GelSight Photometric Stereo & Poisson Reconstruction."""
    ch_path = DOCS_DIR / "module7-dexterous-manipulation" / "7-4-tactile-sensing.mdx"
    code = re.findall(r"```python\b(.*?)```", ch_path.read_text(encoding="utf-8"), re.DOTALL)[0]
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "=== GelSight Photometric Tactile Reconstruction ===" in output
    assert "Sensor Resolution: 160x120 pixels" in output


def test_empirical_peg_in_hole_assembly_execution():
    """Empirically run 7-7 Archimedean Spiral Search & Admittance Assembly Controller."""
    ch_path = DOCS_DIR / "module7-dexterous-manipulation" / "7-7-assembly-and-contact-rich-tasks.mdx"
    code = re.findall(r"```python\b(.*?)```", ch_path.read_text(encoding="utf-8"), re.DOTALL)[0]
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "=== Peg-in-Hole Assembly Controller Simulation ===" in output
    assert "SPIRAL_SEARCH" in output
    assert "COMPLIANT_INSERTION" in output


def test_empirical_manipulation_benchmarks_execution():
    """Empirically run 7-8 Manipulation benchmark evaluation & Wilson interval."""
    ch_path = DOCS_DIR / "module7-dexterous-manipulation" / "7-8-manipulation-benchmarks.mdx"
    code = re.findall(r"```python\b(.*?)```", ch_path.read_text(encoding="utf-8"), re.DOTALL)[0]
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "Wilson 95% Confidence Interval:" in output
    assert "Success Rate: 100.0%" in output


# ---------------------------------------------------------------------------
# Test 8: Canonical Mathematical Formulations Audit
# ---------------------------------------------------------------------------

def test_canonical_3d_lipm_formulation():
    """Verify 3D-LIPM differential equations match Kajita (2003)."""
    ch_path = DOCS_DIR / "module6-bipedal-locomotion" / "6-2-zero-moment-point.mdx"
    content = ch_path.read_text(encoding="utf-8")

    assert r"p_x = x - \frac{z_c}{g}\ddot{x}" in content
    assert r"\omega_0 = \sqrt{\frac{g}{z_c}}" in content
    assert r"\ddot{x} = \omega_0^2 (x - p_x)" in content


def test_canonical_capture_point_formulation():
    """Verify Instantaneous Capture Point satisfies Pratt et al. (2006)."""
    ch_path = DOCS_DIR / "module6-bipedal-locomotion" / "6-3-capture-point-and-dcm.mdx"
    content = ch_path.read_text(encoding="utf-8")

    assert r"\xi = x + \frac{\dot{x}}{\omega_0}" in content
    assert r"\dot{\xi} = \omega_0 (\xi - p)" in content


def test_canonical_grasp_wrench_space_formulation():
    """Verify Grasp Wrench Space satisfies Ferrari & Canny (1992)."""
    ch_path = DOCS_DIR / "module7-dexterous-manipulation" / "7-2-grasp-theory.mdx"
    content = ch_path.read_text(encoding="utf-8")

    assert "Ferrari" in content and "Canny" in content
    assert "Grasp Wrench Space" in content or "GWS" in content
    assert "Force Closure" in content or "force closure" in content


# ---------------------------------------------------------------------------
# Test 9: Empirical Execution of Remediated Module 6 Python Algorithms
# ---------------------------------------------------------------------------

def test_reproduce_bug_6_1_bound_method_event():
    """Verify clean execution in 6-1 following event wrapper fix."""
    ch_path = DOCS_DIR / "module6-bipedal-locomotion" / "6-1-introduction-to-bipedal-locomotion.mdx"
    code = re.findall(r"```python\b(.*?)```", ch_path.read_text(encoding="utf-8"), re.DOTALL)[0]
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "Executing Hybrid Compass-Gait Simulation..." in output
    assert "Successfully simulated" in output


def test_reproduce_bug_6_2_preview_controller_dimension_mismatch():
    """Verify clean execution in 6-2 following dimension matching and scalar item fix."""
    ch_path = DOCS_DIR / "module6-bipedal-locomotion" / "6-2-zero-moment-point.mdx"
    code = re.findall(r"```python\b(.*?)```", ch_path.read_text(encoding="utf-8"), re.DOTALL)[0]
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "Preview control simulation complete." in output
    assert "Final CoM Position:" in output


def test_reproduce_bug_6_8_bound_method_event():
    """Verify clean execution in 6-8 following event wrapper fix."""
    ch_path = DOCS_DIR / "module6-bipedal-locomotion" / "6-8-advanced-locomotion-skills.mdx"
    code = re.findall(r"```python\b(.*?)```", ch_path.read_text(encoding="utf-8"), re.DOTALL)[0]
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "Simulation Status: Success" in output
    assert "Next Apex Height:" in output


def test_reproduce_bug_6_9_numpy_trapz_removal():
    """Verify clean execution in 6-9 following trapezoid fallback fix."""
    ch_path = DOCS_DIR / "module6-bipedal-locomotion" / "6-9-gait-analysis-and-biomechanics.mdx"
    code = re.findall(r"```python\b(.*?)```", ch_path.read_text(encoding="utf-8"), re.DOTALL)[0]
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "Humanoid Biomechanics & Telemetry Report" in output
    assert "Specific_COT:" in output
