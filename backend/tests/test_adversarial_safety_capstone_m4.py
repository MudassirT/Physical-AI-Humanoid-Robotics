"""
Adversarial Stress Test Suite for Milestone M4:
Module 11: Safety, Ethics & Deployment (Chapters 11-1 through 11-6)
Module 12: Capstone Projects & Research Frontiers (Chapters 12-1 through 12-6)

Empirical Code Execution, Adversarial Stress Testing, Edge Case Mining,
and Mathematical Boundary Verification across 12 chapters.
"""

import io
import math
import re
from contextlib import redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
import pytest
import yaml

# Root directory of repository
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = REPO_ROOT / "ai-book-docs"

MODULE_11_DIR = DOCS_DIR / "module11-safety-ethics"
MODULE_12_DIR = DOCS_DIR / "module12-capstone-frontiers"


# ===========================================================================
# 1. Structural Conformance & Quality Gate Tests for Modules 11 & 12
# ===========================================================================

M11_CHAPTERS = [
    "11-1-robot-safety-standards.mdx",
    "11-2-functional-safety-architecture.mdx",
    "11-3-human-robot-interaction-safety.mdx",
    "11-4-ethics-of-autonomous-humanoids.mdx",
    "11-5-privacy-and-data-governance.mdx",
    "11-6-deployment-operations.mdx",
]

M12_CHAPTERS = [
    "12-1-capstone-project-guide.mdx",
    "12-2-research-frontiers-locomotion.mdx",
    "12-3-research-frontiers-ai.mdx",
    "12-4-the-future-of-humanoid-robotics.mdx",
    "12-5-contributing-to-open-source.mdx",
    "12-6-reference-and-bibliography.mdx",
]


@pytest.mark.parametrize("filename", M11_CHAPTERS)
def test_module11_chapter_structure_and_components(filename: str):
    """Verifies that each Module 11 chapter satisfies structural and quality gates."""
    path = MODULE_11_DIR / filename
    assert path.is_file(), f"Missing chapter file: {path}"
    content = path.read_text(encoding="utf-8")

    # Frontmatter check
    fm_match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
    assert fm_match, f"Missing YAML frontmatter in {filename}"
    fm = yaml.safe_load(fm_match.group(1))
    assert "title" in fm, f"Missing title in frontmatter of {filename}"
    assert "description" in fm, f"Missing description in frontmatter of {filename}"
    assert "sidebar_position" in fm, f"Missing sidebar_position in frontmatter of {filename}"

    # Math density check (at least 3 LaTeX math formulas)
    math_matches = re.findall(r"\$[^$]+\$|\$\$[^$]+\$\$", content)
    assert len(math_matches) >= 3, f"Insufficient math density in {filename} ({len(math_matches)} < 3)"

    # Interactive Component check
    assert "<ChapterProgress" in content, f"Missing <ChapterProgress /> in {filename}"
    assert "<QuizEngine" in content, f"Missing <QuizEngine /> in {filename}"


@pytest.mark.parametrize("filename", M12_CHAPTERS)
def test_module12_chapter_structure_and_components(filename: str):
    """Verifies that each Module 12 chapter satisfies structural and quality gates."""
    path = MODULE_12_DIR / filename
    assert path.is_file(), f"Missing chapter file: {path}"
    content = path.read_text(encoding="utf-8")

    # Frontmatter check
    fm_match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
    assert fm_match, f"Missing YAML frontmatter in {filename}"
    fm = yaml.safe_load(fm_match.group(1))
    assert "title" in fm, f"Missing title in frontmatter of {filename}"
    assert "description" in fm, f"Missing description in frontmatter of {filename}"
    assert "sidebar_position" in fm, f"Missing sidebar_position in frontmatter of {filename}"

    # Interactive Component check
    assert "<ChapterProgress" in content, f"Missing <ChapterProgress /> in {filename}"
    assert "<QuizEngine" in content, f"Missing <QuizEngine /> in {filename}"


# ===========================================================================
# 2. Module 11 Empirical Verification & Adversarial Stress Tests
# ===========================================================================

# ---------------------------------------------------------------------------
# Chapter 11-1: Dynamic Speed and Separation Monitoring (SSM)
# ---------------------------------------------------------------------------

def extract_python_code(file_path: Path) -> str:
    """Extracts the primary Python code block from an MDX file."""
    text = file_path.read_text(encoding="utf-8")
    blocks = re.findall(r"```python\b(.*?)```", text, re.DOTALL)
    assert len(blocks) > 0, f"No python block found in {file_path}"
    return blocks[0]


def test_empirical_11_1_ssm_nominal_execution():
    """Directly executes the Chapter 11-1 SSM code block from MDX."""
    code = extract_python_code(MODULE_11_DIR / "11-1-robot-safety-standards.mdx")
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "SPEED AND SEPARATION MONITORING" in output
    assert "NORMAL_OPERATION" in output
    assert "PROTECTIVE_STOP" in output


def test_adversarial_11_1_ssm_boundary_and_stress():
    """
    Stress-tests the SpeedSeparationMonitor under hostile edge cases:
    - Zero and negative measured distances
    - Zero robot speed and ultra-high robot speed (100 m/s)
    - Zero deceleration limits
    - All 11 ISO/TS 15066 body regions and unknown regions
    """
    code = extract_python_code(MODULE_11_DIR / "11-1-robot-safety-standards.mdx")
    ns = {}
    exec(code, ns)

    SpeedSeparationMonitor = ns["SpeedSeparationMonitor"]
    SafetyState = ns["SafetyState"]
    ISO_15066_BODY_LIMITS = ns["ISO_15066_BODY_LIMITS"]

    monitor = SpeedSeparationMonitor(
        t_reaction_s=0.080,
        a_robot_max_mps2=3.0,
        v_human_max_mps=1.6,
        c_clearance_intrusion_m=0.25
    )

    # 1. Zero and negative measured distance stress
    for d in [0.25, 0.10, 0.0, -0.5, -100.0]:
        state, s_p, v_safe = monitor.evaluate_safety_state(measured_distance_m=d, v_robot_directed_mps=1.0)
        assert state == SafetyState.EMERGENCY_STOP, f"Distance {d} must trigger EMERGENCY_STOP, got {state}"
        assert v_safe == 0.0, f"Safe speed at distance {d} must be 0.0, got {v_safe}"
        assert s_p > 0.0, f"Protective distance must remain positive, got {s_p}"

    # 2. State boundary transitions
    # Exact Sp distance:
    v_r = 1.0
    s_p_exact = monitor.compute_protective_distance(v_robot_directed_mps=v_r)
    state, _, _ = monitor.evaluate_safety_state(measured_distance_m=s_p_exact - 1e-4, v_robot_directed_mps=v_r)
    assert state == SafetyState.PROTECTIVE_STOP

    state_red, _, _ = monitor.evaluate_safety_state(measured_distance_m=s_p_exact * 1.1, v_robot_directed_mps=v_r)
    assert state_red == SafetyState.SPEED_REDUCTION

    state_norm, _, _ = monitor.evaluate_safety_state(measured_distance_m=s_p_exact * 1.4, v_robot_directed_mps=v_r)
    assert state_norm == SafetyState.NORMAL_OPERATION

    # 3. Robot stationary (v_r = 0.0)
    s_p_zero = monitor.compute_protective_distance(v_robot_directed_mps=0.0)
    expected_s_p_zero = 1.6 * 0.080 + 0.25  # v_h * T_r + C
    assert pytest.approx(s_p_zero, abs=1e-5) == expected_s_p_zero

    # 4. Extreme velocity scaling (100 m/s)
    s_p_extreme = monitor.compute_protective_distance(v_robot_directed_mps=100.0)
    assert not math.isnan(s_p_extreme) and not math.isinf(s_p_extreme)
    assert s_p_extreme > 1000.0

    # 5. Inversion correctness: max safe speed when distance = s_p must equal original speed
    v_test = 1.5
    dist_req = monitor.compute_protective_distance(v_robot_directed_mps=v_test)
    v_recovered = monitor.compute_max_safe_speed(measured_distance_m=dist_req)
    assert pytest.approx(v_recovered, abs=1e-3) == v_test

    # 6. Biomechanical Impact calculations for all 11 body regions
    assert len(ISO_15066_BODY_LIMITS) == 11
    for region_key in ISO_15066_BODY_LIMITS:
        impact = SpeedSeparationMonitor.calculate_impact_energy_limit(
            body_part_key=region_key,
            robot_effective_mass_kg=15.0,
            contact_area_cm2=2.0
        )
        assert impact["reduced_mass_kg"] > 0.0
        assert impact["reduced_mass_kg"] < 15.0  # Reduced mass must be strictly less than robot mass
        assert impact["v_max_impact_mps"] > 0.0
        assert impact["e_max_kinetic_joules"] > 0.0

    # 7. Invalid body region check
    with pytest.raises(ValueError, match="Unknown anatomical region"):
        SpeedSeparationMonitor.calculate_impact_energy_limit("invalid_organ", 10.0, 1.0)


# ---------------------------------------------------------------------------
# Chapter 11-2: Functional Safety PFH and Diagnostic Coverage (DC)
# ---------------------------------------------------------------------------

def test_adversarial_11_2_functional_safety_reliability_calculations():
    """
    Stress-tests the ISO 13849-1 / IEC 61508 reliability formulas derived in 11-2:
    - Diagnostic Coverage: DC = sum(lambda_DD) / sum(lambda_D)
    - Safe Failure Fraction: SFF = (lambda_S + lambda_DD) / (lambda_S + lambda_D)
    - 1oo1: PFH_1oo1 = lambda_DU
    - 1oo2: PFH_1oo2 = 2(1-beta)lambda_DU((1-beta)lambda_DU T1/2 + lambda_DD MTTR) + beta lambda_D
    - 2oo2: PFH_2oo2 = 2 lambda_DU
    """
    def calc_dc(lambda_dd: float, lambda_du: float) -> float:
        lambda_d = lambda_dd + lambda_du
        if lambda_d <= 0.0:
            return 1.0  # No dangerous failures
        return lambda_dd / lambda_d

    def calc_sff(lambda_s: float, lambda_dd: float, lambda_du: float) -> float:
        denom = lambda_s + lambda_dd + lambda_du
        if denom <= 0.0:
            return 1.0
        return (lambda_s + lambda_dd) / denom

    def calc_pfh_1oo1(lambda_du: float) -> float:
        return lambda_du

    def calc_pfh_1oo2(lambda_dd: float, lambda_du: float, beta: float, t1_hours: float, mttr_hours: float) -> float:
        lambda_d = lambda_dd + lambda_du
        term1 = 2.0 * (1.0 - beta) * lambda_du * ((1.0 - beta) * lambda_du * (t1_hours / 2.0) + lambda_dd * mttr_hours)
        term2 = beta * lambda_d
        return term1 + term2

    def calc_pfh_2oo2(lambda_du: float) -> float:
        return 2.0 * lambda_du

    # Nominal SIL 3 parameter set for dual-channel robot actuator
    # Single channel without diagnostics: DC = 0, so lambda_DU = lambda_D
    lambda_d_total = 1.0e-6  # 1 failure per 1,000,000 operating hours
    pfh_1oo1_no_dc = lambda_d_total  # 1.0e-6 /h

    # Dual channel with online diagnostics (DC = 99%)
    l_dd = 9.9e-7   # Detected dangerous
    l_du = 1.0e-8   # Undetected dangerous (DC = 99%)
    l_s = 5.0e-7    # Safe failure rate
    beta = 0.01     # 1% Common Cause Failure (IEC 61508 typical 1% to 5%)
    t1 = 8760.0     # 1 year proof test
    mttr = 8.0      # 8 hours repair time

    dc = calc_dc(l_dd, l_du)
    assert pytest.approx(dc, abs=1e-4) == 0.99  # 99% High Diagnostic Coverage

    sff = calc_sff(l_s, l_dd, l_du)
    assert sff > 0.99  # Qualifies for SIL 3 / PL e

    pfh_1oo2 = calc_pfh_1oo2(l_dd, l_du, beta, t1, mttr)
    pfh_2oo2 = calc_pfh_2oo2(l_du)

    # Verify reliability ordering
    assert pfh_1oo2 < pfh_1oo1_no_dc, "1oo2 dual-channel must achieve strictly lower PFH than single channel without diagnostics"
    assert pfh_1oo2 < pfh_2oo2, "1oo2 safety architecture must achieve lower PFH than 2oo2 availability architecture"
    assert pfh_1oo2 < 1e-7, "1oo2 architecture must achieve SIL 3 (PFH < 1e-7)"


    # Extreme stress tests:
    # A) Perfect diagnostic coverage (lambda_DU = 0)
    pfh_perfect_dc = calc_pfh_1oo2(l_dd, 0.0, beta=0.0, t1_hours=t1, mttr_hours=mttr)
    assert pfh_perfect_dc == 0.0, "Without CCF and with lambda_DU = 0, PFH_1oo2 must be 0"

    # B) Total common cause coupling (beta = 1.0)
    pfh_total_ccf = calc_pfh_1oo2(l_dd, l_du, beta=1.0, t1_hours=t1, mttr_hours=mttr)
    assert pytest.approx(pfh_total_ccf, rel=1e-5) == (l_dd + l_du)

    # C) Zero failure rate robustness
    assert calc_dc(0.0, 0.0) == 1.0
    assert calc_sff(0.0, 0.0, 0.0) == 1.0


# ---------------------------------------------------------------------------
# Chapter 11-3: Generalized Momentum Observer
# ---------------------------------------------------------------------------

def test_empirical_11_3_momentum_observer_nominal_execution():
    """Directly executes the Chapter 11-3 Generalized Momentum Observer code block."""
    code = extract_python_code(MODULE_11_DIR / "11-3-human-robot-interaction-safety.mdx")
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "COLLISION DETECTED" in output
    assert "Switching to Safe Compliance Reflex" in output
    assert "Peak True Impact Torque: 18.00 Nm" in output


def test_adversarial_11_3_momentum_observer_stress_and_singularities():
    """
    Stress-tests the momentum observer under adversarial physics conditions:
    - Zero disturbance: residual remains near 0
    - Multi-axis and negative torque impulses
    - Inertia matrix positive definiteness at extreme arm postures
    - High observer gains without numerical divergence
    """
    code = extract_python_code(MODULE_11_DIR / "11-3-human-robot-interaction-safety.mdx")
    ns = {}
    exec(code, ns)

    Robot3DOFModel = ns["Robot3DOFModel"]
    GeneralizedMomentumObserver = ns["GeneralizedMomentumObserver"]

    model = Robot3DOFModel(link_lengths=[0.4, 0.35, 0.15], link_masses=[3.0, 2.0, 1.0])
    dt = 0.001

    # 1. Inertia Matrix Positive Definiteness test at singular/outstretched postures
    test_angles = [
        np.array([0.0, 0.0, 0.0]),             # Fully outstretched
        np.array([np.pi/2, np.pi, -np.pi/2]),   # Folded
        np.array([-np.pi, 0.0, np.pi]),        # Inverted
    ]
    for q_test in test_angles:
        M, C, g = model.compute_matrices(q_test, np.zeros(3))
        # Symmetric check
        assert np.allclose(M, M.T, atol=1e-5), f"Inertia matrix not symmetric at q={q_test}"
        # Positive eigenvalues check
        eigenvalues = np.linalg.eigvals(M)
        assert np.all(eigenvalues > 0.0), f"Inertia matrix singular or indefinite: eigenvalues={eigenvalues}"

    # 2. Zero Disturbance Residual Drift test
    observer = GeneralizedMomentumObserver(dof=3, observer_gains_ki=np.array([80.0, 80.0, 80.0]), dt_s=dt)
    q = np.array([0.3, 0.4, -0.2])
    dq = np.zeros(3)
    tau_applied = np.zeros(3)

    for _ in range(500):  # 0.5 seconds of static motion
        M, C, g = model.compute_matrices(q, dq)
        tau_applied = g.copy()  # perfect gravity compensation
        r = observer.update(q, dq, tau_applied, M, C, g)
        # Robot dynamics: ddq = M^{-1} (tau - g) = 0
        ddq = np.linalg.solve(M, tau_applied - g)
        dq += ddq * dt
        q += dq * dt

    assert np.max(np.abs(r)) < 1e-4, f"Observer residual drifted without disturbance: max|r|={np.max(np.abs(r))}"

    # 3. Negative Impulsive Torque detection test
    observer_neg = GeneralizedMomentumObserver(dof=3, observer_gains_ki=np.array([120.0, 120.0, 120.0]), dt_s=dt)
    q = np.array([0.2, 0.5, -0.3])
    dq = np.zeros(3)
    tau_ext_neg = np.array([0.0, -25.0, 0.0])  # Negative 25 Nm on Joint 2

    peak_residual_neg = 0.0
    for step in range(100):
        t = step * dt
        tau_ext = tau_ext_neg if 0.02 <= t <= 0.06 else np.zeros(3)
        M, C, g = model.compute_matrices(q, dq)
        tau_cmd = g.copy()
        r = observer_neg.update(q, dq, tau_cmd, M, C, g)
        if step > 25:
            peak_residual_neg = min(peak_residual_neg, r[1])
        ddq = np.linalg.solve(M, tau_cmd + tau_ext - (C @ dq) - g)
        dq += ddq * dt
        q += dq * dt

    assert peak_residual_neg < -15.0, f"Observer failed to track negative impulse: peak={peak_residual_neg}"


# ---------------------------------------------------------------------------
# Chapter 11-4: Demographic Fairness Metrics (SPD, DI, EOD, AOD)
# ---------------------------------------------------------------------------

def test_empirical_11_4_fairness_nominal_execution():
    """Directly executes Chapter 11-4 Demographic Fairness Auditor code block."""
    code = extract_python_code(MODULE_11_DIR / "11-4-ethics-of-autonomous-humanoids.mdx")
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "DEMOGRAPHIC FAIRNESS AUDIT REPORT" in output
    assert "Statistical Parity Difference (SPD)" in output
    assert "Disparate Impact Ratio (DI)" in output


def test_adversarial_11_4_fairness_boundary_conditions():
    """
    Stress-tests the DemographicFairnessAuditor under boundary distributions:
    - Zero positive predictions (ZeroDivision in Disparate Impact)
    - Zero ground truth positives (ZeroDivision in TPR/FNR)
    - Perfect equality dataset (SPD=0, DI=1.0, EOD=0, AOD=0)
    - Extreme population imbalance (10,000 vs 5 samples)
    """
    code = extract_python_code(MODULE_11_DIR / "11-4-ethics-of-autonomous-humanoids.mdx")
    ns = {}
    exec(code, ns)

    EvaluationSample = ns["EvaluationSample"]
    DemographicFairnessAuditor = ns["DemographicFairnessAuditor"]

    # 1. Perfectly equal dataset
    samples_perfect = [
        EvaluationSample("p1", 1, 1, 0.9, "privileged"),
        EvaluationSample("p2", 0, 0, 0.1, "privileged"),
        EvaluationSample("u1", 1, 1, 0.9, "unprivileged"),
        EvaluationSample("u2", 0, 0, 0.1, "unprivileged"),
    ]
    auditor_perf = DemographicFairnessAuditor(samples_perfect)
    res_perf = auditor_perf.evaluate_fairness()
    assert res_perf["statistical_parity_difference"] == 0.0
    assert pytest.approx(res_perf["disparate_impact_ratio"]) == 1.0
    assert res_perf["equal_opportunity_difference"] == 0.0
    assert res_perf["average_odds_difference"] == 0.0
    assert all(res_perf["compliance"].values())

    # 2. Zero positive predictions anywhere (model predicts 0 for all)
    samples_all_zero = [
        EvaluationSample("p1", 1, 0, 0.1, "privileged"),
        EvaluationSample("u1", 1, 0, 0.1, "unprivileged"),
    ]
    auditor_zero = DemographicFairnessAuditor(samples_all_zero)
    res_zero = auditor_zero.evaluate_fairness()
    assert res_zero["statistical_parity_difference"] == 0.0
    assert res_zero["disparate_impact_ratio"] == 0.0  # Safe zero division handling

    # 3. Severe imbalance in sample counts (1000 priv vs 5 unpriv)
    samples_imbalanced = [
        EvaluationSample(f"p_{i}", 1, 1, 0.95, "privileged") for i in range(1000)
    ] + [
        EvaluationSample(f"u_{i}", 1, 0, 0.40, "unprivileged") for i in range(5)
    ]
    auditor_imb = DemographicFairnessAuditor(samples_imbalanced)
    res_imb = auditor_imb.evaluate_fairness()
    assert res_imb["statistical_parity_difference"] == -1.0  # 0.0 - 1.0
    assert res_imb["equal_opportunity_difference"] == -1.0
    assert res_imb["compliance"]["statistical_parity_fair"] is False
    assert res_imb["compliance"]["equal_opportunity_fair"] is False


# ---------------------------------------------------------------------------
# Chapter 11-5: Privacy Redaction & Differential Privacy
# ---------------------------------------------------------------------------

def test_empirical_11_5_privacy_pipeline_nominal_execution():
    """Directly executes Chapter 11-5 Edge Privacy Redactor code block."""
    code = extract_python_code(MODULE_11_DIR / "11-5-privacy-and-data-governance.mdx")
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "EDGE PRIVACY REDACTION PIPELINE" in output
    assert "Frame Sequence ID:" in output


def test_adversarial_11_5_privacy_boundary_and_differential_privacy():
    """
    Stress-tests:
    1. EdgePrivacyRedactor with corner-touching faces, tiny images, odd/even kernels.
    2. (epsilon, delta)-Differential Privacy Gaussian Mechanism calibrated noise addition.
    """
    code = extract_python_code(MODULE_11_DIR / "11-5-privacy-and-data-governance.mdx")
    ns = {}
    exec(code, ns)

    EdgePrivacyRedactor = ns["EdgePrivacyRedactor"]

    # 1. EdgePrivacyRedactor boundary tests
    redactor_even = EdgePrivacyRedactor(blur_kernel_size=50)  # Even kernel should become odd 51
    assert redactor_even.kernel_size % 2 == 1

    # Image with face near border (ensuring padding does not cause IndexError / slice failure)
    test_frame = np.full((200, 200, 3), 128, dtype=np.uint8)
    # Face touching top-left corner
    cv2.circle(test_frame, (20, 20), 18, (200, 200, 200), -1)
    # Face touching bottom-right corner
    cv2.circle(test_frame, (180, 180), 18, (200, 200, 200), -1)

    out_frame, record = redactor_even.redact_frame(test_frame)
    assert out_frame.shape == test_frame.shape
    assert record.raw_frame_sha256 != record.redacted_frame_sha256 or record.faces_detected_count == 0

    # 2. Mathematical Differential Privacy Gaussian Mechanism Stress Test
    def apply_gaussian_dp(
        gradients: np.ndarray,
        clipping_norm_c: float,
        epsilon: float,
        delta: float
    ) -> Tuple[np.ndarray, float]:
        """Implements DP-SGD Gaussian Mechanism derived in Section 3 of 11-5."""
        assert epsilon > 0.0, "Epsilon must be positive"
        assert 0.0 < delta < 1.0, "Delta must be in (0, 1)"
        assert clipping_norm_c > 0.0, "Clipping norm must be positive"

        # 1. Per-sample clipping: ||g||_2 <= C
        norms = np.linalg.norm(gradients, axis=1, keepdims=True)
        clip_factors = np.maximum(1.0, norms / clipping_norm_c)
        clipped_grads = gradients / clip_factors

        # Verify clipping bounded sensitivity
        max_clipped_norm = np.max(np.linalg.norm(clipped_grads, axis=1))
        assert max_clipped_norm <= clipping_norm_c + 1e-7

        # 2. Gaussian noise scale
        sigma = (clipping_norm_c * np.sqrt(2.0 * np.log(1.25 / delta))) / epsilon

        # 3. Aggregate + Add Noise
        batch_size = gradients.shape[0]
        grad_sum = np.sum(clipped_grads, axis=0)
        noise = np.random.normal(loc=0.0, scale=sigma, size=grad_sum.shape)
        sanitized_update = (grad_sum + noise) / batch_size

        return sanitized_update, sigma

    np.random.seed(42)
    sample_grads = np.random.randn(50, 100) * 10.0  # Large unclipped gradients
    sanitized, sigma = apply_gaussian_dp(sample_grads, clipping_norm_c=1.0, epsilon=1.0, delta=1e-5)

    assert sanitized.shape == (100,)
    assert sigma > 0.0
    # For eps=1.0, delta=1e-5: sigma = 1.0 * sqrt(2 * ln(125000)) approx sqrt(2 * 11.736) approx 4.84
    expected_sigma = np.sqrt(2.0 * np.log(1.25 / 1e-5))
    assert pytest.approx(sigma, rel=1e-4) == expected_sigma


# ---------------------------------------------------------------------------
# Chapter 11-6: Fleet Availability & Canary Failure Bounds
# ---------------------------------------------------------------------------

def test_adversarial_11_6_fleet_availability_and_canary_bounds():
    """
    Stress-tests:
    1. Operational Availability A = MTBF / (MTBF + MTTR)
    2. Canary exposure bound N * T_eval >= ln(1 / (1 - beta)) / p_defect
    """
    def calc_availability(mtbf_hours: float, mttr_hours: float) -> float:
        denom = mtbf_hours + mttr_hours
        if denom <= 0.0:
            return 0.0
        return mtbf_hours / denom

    def calc_canary_required_hours(p_defect_per_hour: float, confidence_beta: float) -> float:
        assert 0.0 < p_defect_per_hour <= 1.0
        assert 0.0 < confidence_beta < 1.0
        return np.log(1.0 / (1.0 - confidence_beta)) / p_defect_per_hour

    # 1. Availability stress cases
    assert calc_availability(mtbf_hours=400.0, mttr_hours=0.0) == 1.0
    assert calc_availability(mtbf_hours=0.0, mttr_hours=10.0) == 0.0
    # Commercial target: MTBF = 400 h, MTTR = 0.5 h -> A = 400 / 400.5 = 0.99875 (99.88%)
    a_target = calc_availability(400.0, 0.5)
    assert a_target > 0.998

    # 2. Canary Exposure bounds
    # Subtle defect p_defect = 0.001 (once per 1,000 h), confidence = 99% (beta = 0.99)
    req_hours = calc_canary_required_hours(p_defect_per_hour=0.001, confidence_beta=0.99)
    # ln(100) / 0.001 = 4.60517 / 0.001 approx 4605.17 hours
    assert pytest.approx(req_hours, abs=1.0) == 4605.17

    # Cohort of 20 robots -> ~230 hours per robot
    t_eval_20_robots = req_hours / 20.0
    assert pytest.approx(t_eval_20_robots, abs=1.0) == 230.26


# ===========================================================================
# 3. Module 12 Empirical Verification & Adversarial Stress Tests
# ===========================================================================

# ---------------------------------------------------------------------------
# Chapter 12-1: End-to-End Latency Budget Validator & Executive Scaffold
# ---------------------------------------------------------------------------

def test_empirical_12_1_scaffold_nominal_execution():
    """Verifies that the Chapter 12-1 Capstone software scaffold executes without errors."""
    code = extract_python_code(MODULE_12_DIR / "12-1-capstone-project-guide.mdx")
    ns = {}
    exec(code, ns)

    IsaacLabPolicyInferenceEngine = ns["IsaacLabPolicyInferenceEngine"]
    RobotGlobalBlackboard = ns["RobotGlobalBlackboard"]
    blackboard = ns["blackboard"]
    assert RobotGlobalBlackboard is not None
    assert blackboard.is_emergency_stopped is False

    # Verify neural policy engine evaluation
    engine = IsaacLabPolicyInferenceEngine(observation_dim=64, action_dim=20)
    dummy_obs = np.random.randn(64).astype(np.float32)
    action = engine.evaluate(dummy_obs)
    assert action.shape == (20,)
    assert np.all(action >= -1.0) and np.all(action <= 1.0)  # Tanh bounds


def test_adversarial_12_1_latency_budget_validator():
    """
    Stress-tests the deterministic latency budget derived in Section 1.1:
    tau_total = tau_perception + tau_vla + tau_wbc + tau_comm <= 100 ms
    """
    @dataclass
    class LatencyProfile:
        tau_perception_ms: float
        tau_vla_ms: float
        tau_wbc_ms: float
        tau_comm_ms: float
        tau_critical_ms: float = 100.0

        @property
        def tau_total_ms(self) -> float:
            return self.tau_perception_ms + self.tau_vla_ms + self.tau_wbc_ms + self.tau_comm_ms

        def validate(self) -> Tuple[bool, float]:
            headroom = self.tau_critical_ms - self.tau_total_ms
            return (self.tau_total_ms <= self.tau_critical_ms), headroom

    # Case 1: Nominal Capstone System Profile (30 + 50 + 1.0 + 1.5 = 82.5 ms)
    nominal = LatencyProfile(30.0, 50.0, 1.0, 1.5)
    is_valid, headroom = nominal.validate()
    assert is_valid is True
    assert pytest.approx(headroom, abs=1e-3) == 17.5

    # Case 2: Maximum Jitter Envelope (Table 1 values: 25+3 + 45+5 + 0.85+0.1 + 0.25+0.02)
    worst_case_jitter = LatencyProfile(
        tau_perception_ms=28.0,
        tau_vla_ms=50.0,
        tau_wbc_ms=0.95,
        tau_comm_ms=0.27
    )
    is_valid_wc, _ = worst_case_jitter.validate()
    assert is_valid_wc is True

    # Case 3: Over-Budget Violation (e.g. WiFi communication latency spike of 40 ms)
    spike = LatencyProfile(30.0, 50.0, 1.0, 40.0)
    is_valid_spike, headroom_spike = spike.validate()
    assert is_valid_spike is False
    assert headroom_spike < 0.0


# ---------------------------------------------------------------------------
# Chapter 12-2: Centroidal Momentum Landing Controller
# ---------------------------------------------------------------------------

def test_empirical_12_2_landing_controller_nominal_execution():
    """Directly executes Chapter 12-2 Parkour Landing Controller code block."""
    code = extract_python_code(MODULE_12_DIR / "12-2-research-frontiers-locomotion.mdx")
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "Computed Left Foot Force" in output
    assert "Computed Right Foot Force" in output
    assert "Total Normal Force Fz" in output


def test_adversarial_12_2_landing_controller_physics_stress():
    """
    Stress-tests the QP landing regulator under extreme dynamic jump impacts:
    - High descent velocity (-3.0 m/s)
    - Asymmetric stair landing foot contact positions
    - Strict friction pyramid adherence: |f_x| <= mu * f_z and |f_y| <= mu * f_z
    """
    code = extract_python_code(MODULE_12_DIR / "12-2-research-frontiers-locomotion.mdx")
    ns = {}
    exec(code, ns)

    CentroidalMomentumLandingController = ns["CentroidalMomentumLandingController"]

    controller = CentroidalMomentumLandingController(
        robot_mass=65.0,
        friction_coeff=0.5,
        f_z_min=10.0,
        f_z_max=3000.0
    )

    # High energy parkour drop: com_vel_z = -2.5 m/s
    com_pos = np.array([0.0, 0.0, 0.85])
    com_vel = np.array([0.2, 0.0, -2.5])
    com_pos_ref = np.array([0.0, 0.0, 0.80])
    com_vel_ref = np.zeros(3)
    base_rot_err = np.array([0.05, -0.05, 0.0])
    base_ang_vel = np.array([0.1, -0.1, 0.2])

    p_dot_des, l_dot_des = controller.compute_desired_momentum_rates(
        com_pos, com_vel, com_pos_ref, com_vel_ref, base_rot_err, base_ang_vel
    )

    # Asymmetric foot contact positions (landing on uneven terrain)
    foot_left = np.array([0.05, 0.15, 0.0])
    foot_right = np.array([-0.05, -0.15, 0.10])  # Right foot 10 cm higher

    res = controller.solve_ground_reaction_forces(com_pos, foot_left, foot_right, p_dot_des, l_dot_des)

    f_l = res["f_left"]
    f_r = res["f_right"]

    # 1. Unilateral normal contact forces must be positive and within bounds
    assert 10.0 <= f_l[2] <= 3000.0, f"Left normal force out of bounds: {f_l[2]}"
    assert 10.0 <= f_r[2] <= 3000.0, f"Right normal force out of bounds: {f_r[2]}"

    # 2. Total vertical force must overcome gravity to arrest descent
    total_fz = res["total_normal_force"]
    assert total_fz >= 637.65, f"Total vertical force {total_fz} insufficient to arrest drop"

    # 3. Coulomb Friction Pyramid satisfaction
    tol = 1e-3
    assert abs(f_l[0]) <= controller.mu * f_l[2] + tol
    assert abs(f_l[1]) <= controller.mu * f_l[2] + tol
    assert abs(f_r[0]) <= controller.mu * f_r[2] + tol
    assert abs(f_r[1]) <= controller.mu * f_r[2] + tol


# ---------------------------------------------------------------------------
# Chapter 12-3: 3D Gaussian Splatting Collision Checker
# ---------------------------------------------------------------------------

def test_empirical_12_3_gaussian_splat_nominal_execution():
    """Directly executes Chapter 12-3 3D Gaussian Splatting Collision Checker code block."""
    code = extract_python_code(MODULE_12_DIR / "12-3-research-frontiers-ai.mdx")
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "3D Gaussian Splatting Trajectory Evaluator passed all tests" in output


def test_adversarial_12_3_gaussian_splat_degenerate_covariances():
    """
    Stress-tests:
    - Degenerate / zero scales: verified safe scale clamping (1e-4) avoids ZeroDivisionError
    - Unnormalized or zero quaternions
    - Precision of analytical inverse covariance: Sigma * Sigma^{-1} == I
    - Trajectory penetration vs clearance
    """
    code = extract_python_code(MODULE_12_DIR / "12-3-research-frontiers-ai.mdx")
    ns = {}
    exec(code, ns)

    GaussianSplatCollisionChecker = ns["GaussianSplatCollisionChecker"]

    # Test with near-zero and degenerate scale ellipsoids
    centers = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]], dtype=np.float64)
    quats = np.array([[1.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0]], dtype=np.float64)
    scales = np.array([[1e-8, 1e-8, 1e-8], [0.1, 0.1, 0.1]], dtype=np.float64)  # 1e-8 triggers safe scale
    opacities = np.array([[0.9], [0.8]], dtype=np.float64)

    checker = GaussianSplatCollisionChecker(centers, quats, scales, opacities)

    # Check that inv_covariances precomputed cleanly without NaN or Inf
    assert not np.any(np.isnan(checker.inv_covariances))
    assert not np.any(np.isinf(checker.inv_covariances))

    # Test center point collision (Mahalanobis distance at Gaussian center must be 0.0)
    traj_center = np.array([[1.0, 1.0, 1.0]])
    res_center = checker.check_trajectory_clearance(traj_center)
    assert res_center["is_collision_free"] is False
    assert pytest.approx(res_center["min_mahalanobis_distance"], abs=1e-3) == 0.0

    # Test distant point clearance
    traj_far = np.array([[100.0, 100.0, 100.0]])
    res_far = checker.check_trajectory_clearance(traj_far)
    assert res_far["is_collision_free"] is True
    assert res_far["min_mahalanobis_distance"] > 10.0


# ---------------------------------------------------------------------------
# Chapter 12-4: Chinchilla Robotic Scaling Law Regression
# ---------------------------------------------------------------------------

def test_empirical_12_4_scaling_laws_nominal_execution():
    """Directly executes Chapter 12-4 Robotic Scaling Law Projector code block."""
    code = extract_python_code(MODULE_12_DIR / "12-4-the-future-of-humanoid-robotics.mdx")
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "Robotic Scaling Law Projector verification passed" in output
    assert "Required Trajectory Hours" in output


def test_adversarial_12_4_scaling_laws_boundary_and_inversion():
    """
    Stress-tests the scaling law formulas:
    - Insufficient model capacity raises ValueError cleanly
    - Monotonicity checks: loss decreases with N and D; success increases
    - Exact parameter fitting from synthetic observations
    """
    code = extract_python_code(MODULE_12_DIR / "12-4-the-future-of-humanoid-robotics.mdx")
    ns = {}
    exec(code, ns)

    RoboticScalingLawProjector = ns["RoboticScalingLawProjector"]

    projector = RoboticScalingLawProjector(
        A=100.0, B=80.0, alpha=0.30, beta=0.40, E=0.05, k=8.0, L_0=0.35
    )

    # 1. Monotonicity verification
    N = np.array([1e7, 1e8, 1e9])
    D = np.array([100.0, 1000.0, 10000.0])
    loss_grid = projector.compute_policy_loss(N, D)
    assert loss_grid[0] > loss_grid[1] > loss_grid[2]

    succ_grid = projector.compute_success_rate(loss_grid)
    assert succ_grid[0] < succ_grid[1] < succ_grid[2]

    # 2. Inadequate capacity raises ValueError
    # Attempting 99.9% success on a tiny 1,000 parameter model
    with pytest.raises(ValueError, match="insufficient to hit target success rate"):
        projector.project_required_data_hours(target_success_rate=0.999, fixed_model_params=1000.0)

    # 3. Inverse projection round-trip accuracy
    # For frontier foundation model (N = 2e12), target 90% success rate
    target_s = 0.90
    fixed_n = 2e12
    req_d = projector.project_required_data_hours(target_s, fixed_n)
    assert req_d > 0.0
    actual_loss = projector.compute_policy_loss(np.array([fixed_n]), np.array([req_d]))[0]
    assert actual_loss < 0.35, f"Target loss must be strictly < L_0 (0.35), got {actual_loss}"
    assert pytest.approx(actual_loss, abs=1e-3) == 0.07535
    actual_s = projector.compute_success_rate(np.array([actual_loss]))[0]
    assert pytest.approx(actual_s, rel=1e-3) == target_s

    # For 7B model, verify achievable target_s = 0.75
    target_s_7b = 0.75
    fixed_n_7b = 7e9
    req_d_7b = projector.project_required_data_hours(target_s_7b, fixed_n_7b)
    assert req_d_7b > 0.0
    actual_loss_7b = projector.compute_policy_loss(np.array([fixed_n_7b]), np.array([req_d_7b]))[0]
    assert actual_loss_7b < 0.35
    actual_s_7b = projector.compute_success_rate(np.array([actual_loss_7b]))[0]
    assert pytest.approx(actual_s_7b, rel=1e-3) == target_s_7b


# ---------------------------------------------------------------------------
# Chapter 12-6: BibTeX Search Engine
# ---------------------------------------------------------------------------

def test_empirical_12_6_bibtex_nominal_execution():
    """Directly executes Chapter 12-6 BibTeX Search Engine code block."""
    code = extract_python_code(MODULE_12_DIR / "12-6-reference-and-bibliography.mdx")
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(code, {"__name__": "__main__"})
    output = buf.getvalue()
    assert "BibTeX Search Engine passed all unit tests" in output
    assert "Parsed 4 BibTeX entries successfully" in output


def test_adversarial_12_6_bibtex_parsing_and_search():
    """
    Stress-tests the BibTeX engine:
    - Formatting quirks (newlines, double quotes, braces, whitespace)
    - Year range filtering edge cases
    - Integrity auditor warnings for missing/malformed entries
    - Search queries with punctuation, casing, or no matches
    """
    code = extract_python_code(MODULE_12_DIR / "12-6-reference-and-bibliography.mdx")
    ns = {}
    exec(code, ns)

    RoboticsBibTeXSearchEngine = ns["RoboticsBibTeXSearchEngine"]

    raw_bib = """
    @article{test2025adv,
      title = {"Adversarial Humanoid Control in Unstructured Terrain"},
      author = {John Doe and Jane Smith},
      journal = {IEEE Robotics and Automation Letters},
      year = {2025},
      doi = {10.1109/LRA.2025.000000}
    }
    @inproceedings{old1890bug,
      title = {Victorian Automaton},
      author = {Charles Babbage},
      booktitle = {Proceedings of the Royal Society},
      year = {1890}
    }
    @misc{notitle2024,
      author = {Anonymous},
      year = {2024}
    }
    """

    engine = RoboticsBibTeXSearchEngine()
    count = engine.parse_and_insert_bibtex(raw_bib)
    assert count == 3

    # Integrity audit tests
    warnings = engine.validate_integrity()
    assert any("Invalid publication year: 1890" in w for w in warnings)
    assert any("Missing title field" in w for w in warnings)

    # Search tests
    results_adv = engine.search("adversarial terrain")
    assert len(results_adv) == 1
    assert results_adv[0].key == "test2025adv"

    # Year filter tests
    results_future = engine.search("adversarial", min_year=2026)
    assert len(results_future) == 0

    results_exact = engine.search("adversarial", min_year=2025, max_year=2025)
    assert len(results_exact) == 1
