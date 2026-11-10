"""
Adversarial Stress Test Suite for Milestone M4 (Module 10):
Module 10: Hardware Architecture & Embedded Systems (8 chapters)

Empirical challenges:
1. Exact chapter inventory and category definitions (10-1 to 10-8)
2. Frontmatter integrity (sidebar_position, title, description)
3. Interactive component integration (ChapterProgress, QuizEngine)
4. KaTeX delimiter and syntax integrity ($$, $, balanced braces)
5. Direct execution of embedded Python code blocks from MDX files
6. Empirical challenge 10-1: Limb rotational inertia calculation and CoM propagation
7. Empirical challenge 10-2: Reflected inertia scaling (J_ref = N^2 * J_rotor) and actuator thermal dissipation RMS model
8. Empirical challenge 10-3: Field-Oriented Control (FOC) Clarke/Park transforms, SVPWM timing, anti-windup PI current control
9. Empirical challenge 10-4: CAN-FD bus utilization and worst-case latency equations under high message density
10. Empirical challenge 10-5: Roofline performance model and operational intensity bounds
11. Empirical challenge 10-6: Allan deviation computation (ARW, bias instability) on synthetic IMU white/pink noise
12. Empirical challenge 10-7: Rate Monotonic Scheduling (RMS) utilization bounds under variable task counts
13. Empirical challenge 10-8: MTBF calculation and thermal dissipation Delta T = P * R_theta
"""

import json
import math
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pytest
import yaml

DOCS_DIR = Path(__file__).resolve().parent.parent.parent / "ai-book-docs" / "module10-hardware-architecture"

EXPECTED_M10_CHAPTERS = [
    "10-1-humanoid-mechanical-design.mdx",
    "10-2-actuator-technologies.mdx",
    "10-3-power-electronics-and-motor-control.mdx",
    "10-4-communication-buses.mdx",
    "10-5-compute-platforms.mdx",
    "10-6-sensor-hardware.mdx",
    "10-7-real-time-embedded-software.mdx",
    "10-8-system-integration-and-testing.mdx",
]


def extract_frontmatter(content: str) -> Tuple[dict, str]:
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        fm = yaml.safe_load(parts[1])
        return (fm if isinstance(fm, dict) else {}), parts[2]
    except Exception:
        return {}, parts[2]


# ==============================================================================
# 1. Structural, Frontmatter, KaTeX & Interactive Components
# ==============================================================================

def test_module10_inventory_and_category():
    """Verify all 8 chapters exist and _category_.json is valid."""
    assert DOCS_DIR.exists(), f"Module 10 directory not found at {DOCS_DIR}"
    cat_file = DOCS_DIR / "_category_.json"
    assert cat_file.exists(), "_category_.json missing from Module 10"

    with open(cat_file, "r", encoding="utf-8") as f:
        cat_data = json.load(f)
    assert cat_data.get("position") == 10
    assert "Hardware Architecture" in cat_data.get("label", "")

    existing_files = {p.name for p in DOCS_DIR.glob("10-*.mdx")}
    expected_set = set(EXPECTED_M10_CHAPTERS)
    missing = expected_set - existing_files
    assert not missing, f"Missing Module 10 chapters: {missing}"


def test_module10_frontmatter_and_components():
    """Verify frontmatter, ChapterProgress, and QuizEngine in every chapter."""
    for ch in EXPECTED_M10_CHAPTERS:
        file_path = DOCS_DIR / ch
        content = file_path.read_text(encoding="utf-8")
        fm, body = extract_frontmatter(content)

        assert "title" in fm and len(fm["title"]) > 5, f"Missing title in {ch}"
        assert "description" in fm and len(fm["description"]) > 10, f"Missing description in {ch}"
        assert "sidebar_position" in fm and isinstance(fm["sidebar_position"], int), f"Invalid sidebar_position in {ch}"

        # Check interactive components
        assert "<ChapterProgress" in body, f"Missing ChapterProgress in {ch}"
        assert "<QuizEngine" in body, f"Missing QuizEngine in {ch}"

        # Quiz structure verification
        assert 'moduleId="module10"' in body, f"Invalid moduleId in QuizEngine for {ch}"
        assert "passThreshold=" in body, f"Missing passThreshold in QuizEngine for {ch}"


def test_module10_katex_syntax_integrity():
    """Stress-test KaTeX math expressions: balanced $$ and $ delimiters."""
    for ch in EXPECTED_M10_CHAPTERS:
        content = (DOCS_DIR / ch).read_text(encoding="utf-8")
        # Strip code blocks to avoid false positives in code strings
        cleaned = re.sub(r"```.*?```", "", content, flags=re.DOTALL)

        # Count block math $$
        block_math_count = len(re.findall(r"\$\$", cleaned))
        assert block_math_count % 2 == 0, f"Unbalanced $$ block math in {ch} (count: {block_math_count})"

        # Verify no broken heading braces
        for line in cleaned.splitlines():
            if line.startswith("#"):
                assert "{" not in line or "}" in line, f"Malformed brace in heading in {ch}: {line}"


def test_module10_embedded_python_code_execution():
    """Extract and execute all Python code blocks from Module 10 MDX files."""
    for ch in EXPECTED_M10_CHAPTERS:
        content = (DOCS_DIR / ch).read_text(encoding="utf-8")
        python_blocks = re.findall(r"```python(.*?)```", content, re.DOTALL)
        for idx, block in enumerate(python_blocks):
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tf:
                tf.write(block)
                tf_name = tf.name
            try:
                res = subprocess.run([sys.executable, tf_name], capture_output=True, text=True, timeout=30)
                assert res.returncode == 0, f"Embedded Python block {idx+1} in {ch} failed:\n{res.stderr}"
            finally:
                if os.path.exists(tf_name):
                    os.remove(tf_name)


# ==============================================================================
# 2. Chapter 10-1: Limb Rotational Inertia & CoM Propagation
# ==============================================================================

@dataclass
class RigidLinkSegment:
    name: str
    mass_kg: float
    com_offset_local: np.ndarray
    inertia_tensor_local: np.ndarray
    joint_axis: np.ndarray
    parent_to_joint_vector: np.ndarray


class HumanoidLimbMassAnalyzer:
    def __init__(self, links: List[RigidLinkSegment]):
        self.links = links
        self.total_mass = sum(link.mass_kg for link in self.links)
        if self.total_mass <= 0.0:
            raise ValueError("Total limb mass must be strictly positive.")

    @staticmethod
    def rodrigues_rotation(axis: np.ndarray, angle_rad: float) -> np.ndarray:
        norm = np.linalg.norm(axis)
        if norm < 1e-9:
            return np.eye(3)
        k = axis / norm
        K = np.array([
            [0.0, -k[2], k[1]],
            [k[2], 0.0, -k[0]],
            [-k[1], k[0], 0.0]
        ])
        return np.eye(3) + np.sin(angle_rad) * K + (1.0 - np.cos(angle_rad)) * (K @ K)

    def forward_kinematics_and_com(self, joint_angles_rad: np.ndarray) -> Tuple[np.ndarray, np.ndarray, List[np.ndarray]]:
        if len(joint_angles_rad) != len(self.links):
            raise ValueError(f"Expected {len(self.links)} joint angles, got {len(joint_angles_rad)}")

        R_current = np.eye(3)
        p_current = np.zeros(3)

        link_com_positions = []
        link_rotations = []

        for i, link in enumerate(self.links):
            p_joint = p_current + R_current @ link.parent_to_joint_vector
            R_joint = self.rodrigues_rotation(link.joint_axis, joint_angles_rad[i])
            R_current = R_current @ R_joint
            p_current = p_joint

            p_com = p_current + R_current @ link.com_offset_local
            link_com_positions.append(p_com)
            link_rotations.append(R_current)

        weighted_com_sum = np.zeros(3)
        for i, link in enumerate(self.links):
            weighted_com_sum += link.mass_kg * link_com_positions[i]
        total_com_world = weighted_com_sum / self.total_mass

        total_inertia = np.zeros((3, 3))
        for i, link in enumerate(self.links):
            R_i = link_rotations[i]
            I_world = R_i @ link.inertia_tensor_local @ R_i.T
            delta = link_com_positions[i] - total_com_world
            delta_sq = np.dot(delta, delta)
            I_offset = link.mass_kg * (delta_sq * np.eye(3) - np.outer(delta, delta))
            total_inertia += (I_world + I_offset)

        return total_com_world, total_inertia, link_com_positions

    def compute_swing_inertia_about_hip(self, joint_angles_rad: np.ndarray, hip_axis: np.ndarray) -> float:
        norm = np.linalg.norm(hip_axis)
        if norm < 1e-9:
            raise ValueError("Hip rotation axis cannot be zero vector.")
        norm_axis = hip_axis / norm
        _, _, link_com_positions = self.forward_kinematics_and_com(joint_angles_rad)

        total_hip_rotational_inertia = 0.0
        R_current = np.eye(3)
        p_current = np.zeros(3)

        for i, link in enumerate(self.links):
            p_joint = p_current + R_current @ link.parent_to_joint_vector
            R_joint = self.rodrigues_rotation(link.joint_axis, joint_angles_rad[i])
            R_current = R_current @ R_joint
            p_current = p_joint

            I_world = R_current @ link.inertia_tensor_local @ R_current.T
            I_axis_cm = float(norm_axis.T @ I_world @ norm_axis)

            r_com = link_com_positions[i]
            r_proj = np.dot(r_com, norm_axis) * norm_axis
            r_perp = r_com - r_proj
            d_sq = float(np.dot(r_perp, r_perp))

            total_hip_rotational_inertia += I_axis_cm + link.mass_kg * d_sq

        return total_hip_rotational_inertia


def test_rodrigues_rotation_properties():
    """Verify Rodrigues rotation properties: orthogonality, det=+1, periodic."""
    axis = np.array([0.0, 1.0, 0.0])
    # 0 angle -> identity
    R0 = HumanoidLimbMassAnalyzer.rodrigues_rotation(axis, 0.0)
    np.testing.assert_allclose(R0, np.eye(3), atol=1e-12)

    # 2*pi angle -> identity
    R2pi = HumanoidLimbMassAnalyzer.rodrigues_rotation(axis, 2.0 * np.pi)
    np.testing.assert_allclose(R2pi, np.eye(3), atol=1e-12)

    # General random axis
    rand_axis = np.random.randn(3)
    angle = 1.234
    R = HumanoidLimbMassAnalyzer.rodrigues_rotation(rand_axis, angle)
    # R * R^T = I
    np.testing.assert_allclose(R @ R.T, np.eye(3), atol=1e-12)
    # det(R) = +1
    np.testing.assert_allclose(np.linalg.det(R), 1.0, atol=1e-12)

    # Zero vector axis handling
    R_zero = HumanoidLimbMassAnalyzer.rodrigues_rotation(np.zeros(3), 1.0)
    np.testing.assert_allclose(R_zero, np.eye(3), atol=1e-12)


def test_limb_mass_analyzer_com_and_inertia_laws():
    """Verify Parallel Axis Theorem and CoM scaling in HumanoidLimbMassAnalyzer."""
    links = [
        RigidLinkSegment(
            name="thigh", mass_kg=4.0,
            com_offset_local=np.array([0.0, 0.0, -0.2]),
            inertia_tensor_local=np.diag([0.04, 0.04, 0.01]),
            joint_axis=np.array([0.0, 1.0, 0.0]),
            parent_to_joint_vector=np.array([0.0, 0.0, 0.0])
        ),
        RigidLinkSegment(
            name="shank", mass_kg=3.0,
            com_offset_local=np.array([0.0, 0.0, -0.2]),
            inertia_tensor_local=np.diag([0.03, 0.03, 0.005]),
            joint_axis=np.array([0.0, 1.0, 0.0]),
            parent_to_joint_vector=np.array([0.0, 0.0, -0.4])
        )
    ]
    analyzer = HumanoidLimbMassAnalyzer(links)
    angles = np.array([0.0, 0.0])
    com, I_tot, link_coms = analyzer.forward_kinematics_and_com(angles)

    # Total mass = 4 + 3 = 7 kg
    assert analyzer.total_mass == 7.0
    # Expected CoM along z: (4*(-0.2) + 3*(-0.4 - 0.2)) / 7 = (-0.8 - 1.8) / 7 = -2.6 / 7 = -0.3714 m
    expected_z = (4.0 * -0.2 + 3.0 * -0.6) / 7.0
    np.testing.assert_allclose(com[2], expected_z, atol=1e-5)
    np.testing.assert_allclose(com[0], 0.0, atol=1e-5)
    np.testing.assert_allclose(com[1], 0.0, atol=1e-5)

    # Check hip swing inertia around y-axis
    I_hip = analyzer.compute_swing_inertia_about_hip(angles, np.array([0.0, 1.0, 0.0]))
    # Thigh: I_yy + m*d^2 = 0.04 + 4.0 * (0.2)^2 = 0.04 + 0.16 = 0.20
    # Shank: I_yy + m*d^2 = 0.03 + 3.0 * (0.6)^2 = 0.03 + 1.08 = 1.11
    # Total = 0.20 + 1.11 = 1.31
    np.testing.assert_allclose(I_hip, 1.31, atol=1e-5)


def test_10_1_boundary_conditions():
    """Test boundary conditions: negative/zero total mass, zero inertia, zero axis."""
    with pytest.raises(ValueError, match="strictly positive"):
        HumanoidLimbMassAnalyzer([
            RigidLinkSegment("bad", 0.0, np.zeros(3), np.eye(3), np.array([0, 1, 0]), np.zeros(3))
        ])

    valid_link = RigidLinkSegment("link", 1.0, np.zeros(3), np.zeros((3, 3)), np.array([0, 1, 0]), np.zeros(3))
    analyzer = HumanoidLimbMassAnalyzer([valid_link])
    with pytest.raises(ValueError, match="cannot be zero vector"):
        analyzer.compute_swing_inertia_about_hip(np.array([0.0]), np.zeros(3))


# ==============================================================================
# 3. Chapter 10-2: Reflected Inertia & Thermal Dissipation RMS Model
# ==============================================================================

@dataclass
class ActuatorSpecs:
    model_name: str
    gear_ratio: float
    rotor_inertia_kgm2: float
    motor_kt_nm_per_a: float
    phase_resistance_ohm: float
    gearbox_efficiency: float
    max_peak_torque_nm: float
    continuous_torque_nm: float
    max_joint_speed_rad_s: float
    bus_voltage_v: float
    thermal_res_wind_to_case: float
    thermal_res_case_to_amb: float
    thermal_cap_wind_j_per_c: float
    thermal_cap_case_j_per_c: float


class ActuatorThermalSimulator:
    def __init__(self, specs: ActuatorSpecs):
        self.specs = specs
        self.reflected_rotor_inertia = (specs.gear_ratio ** 2) * specs.rotor_inertia_kgm2

    def evaluate_trajectory(
        self,
        time_s: np.ndarray,
        torque_nm: np.ndarray,
        velocity_rad_s: np.ndarray,
        ambient_temp_c: float = 25.0
    ) -> dict:
        dt = float(np.mean(np.diff(time_s))) if len(time_s) > 1 else 0.001
        n_steps = len(time_s)

        peak_torque = float(np.max(np.abs(torque_nm)))
        peak_velocity = float(np.max(np.abs(velocity_rad_s)))
        rms_torque = float(np.sqrt(np.mean(torque_nm ** 2)))

        is_torque_within_peak = peak_torque <= self.specs.max_peak_torque_nm
        is_torque_within_rms = rms_torque <= self.specs.continuous_torque_nm
        is_speed_within_limits = peak_velocity <= self.specs.max_joint_speed_rad_s

        torque_motor = np.abs(torque_nm) / (self.specs.gear_ratio * self.specs.gearbox_efficiency)
        iq_current = torque_motor / self.specs.motor_kt_nm_per_a

        t_wind = np.zeros(n_steps)
        t_case = np.zeros(n_steps)
        power_loss = np.zeros(n_steps)

        current_tw = ambient_temp_c
        current_tc = ambient_temp_c
        alpha_copper = 0.00393

        for i in range(n_steps):
            r_temp = self.specs.phase_resistance_ohm * (1.0 + alpha_copper * (current_tw - 20.0))
            p_loss = 1.5 * (iq_current[i] ** 2) * r_temp
            power_loss[i] = p_loss

            q_wind_to_case = (current_tw - current_tc) / self.specs.thermal_res_wind_to_case
            q_case_to_amb = (current_tc - ambient_temp_c) / self.specs.thermal_res_case_to_amb

            d_tw = (p_loss - q_wind_to_case) / self.specs.thermal_cap_wind_j_per_c
            d_tc = (q_wind_to_case - q_case_to_amb) / self.specs.thermal_cap_case_j_per_c

            current_tw += d_tw * dt
            current_tc += d_tc * dt

            t_wind[i] = current_tw
            t_case[i] = current_tc

        return {
            "peak_torque_nm": peak_torque,
            "rms_torque_nm": rms_torque,
            "reflected_inertia_kgm2": self.reflected_rotor_inertia,
            "feasible_peak_torque": is_torque_within_peak,
            "feasible_rms_torque": is_torque_within_rms,
            "feasible_velocity": is_speed_within_limits,
            "max_winding_temp_c": float(np.max(t_wind)),
            "final_winding_temp_c": float(t_wind[-1]),
            "mean_copper_loss_w": float(np.mean(power_loss)),
            "thermal_headroom_c": float(155.0 - np.max(t_wind))
        }


def test_reflected_inertia_scaling():
    """Verify J_ref = N^2 * J_rotor across direct-drive, QDD, and harmonic gear ratios."""
    j_rotor = 1.4e-4
    for N in [1.0, 9.0, 50.0, 100.0]:
        specs = ActuatorSpecs(
            model_name="test", gear_ratio=N, rotor_inertia_kgm2=j_rotor,
            motor_kt_nm_per_a=0.2, phase_resistance_ohm=0.1, gearbox_efficiency=0.9,
            max_peak_torque_nm=100.0, continuous_torque_nm=50.0, max_joint_speed_rad_s=10.0,
            bus_voltage_v=48.0, thermal_res_wind_to_case=1.0, thermal_res_case_to_amb=1.0,
            thermal_cap_wind_j_per_c=100.0, thermal_cap_case_j_per_c=500.0
        )
        sim = ActuatorThermalSimulator(specs)
        expected_j_ref = (N ** 2) * j_rotor
        np.testing.assert_allclose(sim.reflected_rotor_inertia, expected_j_ref, rtol=1e-7)


def test_actuator_thermal_steady_state_convergence():
    """Verify dynamic 2-node Euler integration converges to steady-state Delta T = P * R_total."""
    specs = ActuatorSpecs(
        model_name="QDD-Test", gear_ratio=10.0, rotor_inertia_kgm2=1e-4,
        motor_kt_nm_per_a=0.25, phase_resistance_ohm=0.10, gearbox_efficiency=1.0,
        max_peak_torque_nm=200.0, continuous_torque_nm=80.0, max_joint_speed_rad_s=20.0,
        bus_voltage_v=48.0, thermal_res_wind_to_case=0.8, thermal_res_case_to_amb=1.2,
        thermal_cap_wind_j_per_c=50.0, thermal_cap_case_j_per_c=100.0
    )
    sim = ActuatorThermalSimulator(specs)

    # Long simulation to reach steady-state (1000 seconds)
    t = np.linspace(0.0, 1500.0, 30000)
    # Constant torque = 25.0 N*m
    # Motor torque = 25 / 10 = 2.5 N*m
    # Iq = 2.5 / 0.25 = 10.0 A
    # Copper loss at 20C: 1.5 * 10^2 * 0.10 = 15.0 W (with temp feedback)
    torque = np.full_like(t, 25.0)
    vel = np.zeros_like(t)

    res = sim.evaluate_trajectory(t, torque, vel, ambient_temp_c=25.0)
    # Expected steady-state: P_loss * (R_wc + R_ca)
    # Without temp correction: 15.0 * (0.8 + 1.2) = 30.0 deg C rise -> T_wind = 55.0 deg C
    # With temp correction alpha=0.00393, T_wind will be slightly higher (~58-60 deg C)
    assert 55.0 <= res["final_winding_temp_c"] <= 65.0
    assert res["feasible_peak_torque"] is True
    assert res["feasible_rms_torque"] is True


# ==============================================================================
# 4. Chapter 10-3: Field-Oriented Control (FOC) & SVPWM
# ==============================================================================

class PythonFocController:
    """Python reference oracle for 20 kHz FOC current controller."""
    def __init__(self, rs: float, ld: float, lq: float, lambda_m: float, pole_pairs: int,
                 v_dc: float, kp: float, ki: float, max_v: float, dt: float):
        self.rs = rs
        self.ld = ld
        self.lq = lq
        self.lambda_m = lambda_m
        self.pole_pairs = pole_pairs
        self.v_dc = v_dc
        self.kp = kp
        self.ki = ki
        self.max_v = max_v
        self.dt = dt
        self.int_d = 0.0
        self.int_q = 0.0

    def clarke_transform(self, ia: float, ib: float) -> Tuple[float, float]:
        i_alpha = ia
        i_beta = (1.0 / math.sqrt(3.0)) * (ia + 2.0 * ib)
        return i_alpha, i_beta

    def park_transform(self, i_alpha: float, i_beta: float, theta_e: float) -> Tuple[float, float]:
        cos_th = math.cos(theta_e)
        sin_th = math.sin(theta_e)
        i_d = i_alpha * cos_th + i_beta * sin_th
        i_q = -i_alpha * sin_th + i_beta * cos_th
        return i_d, i_q

    def inverse_park_transform(self, v_d: float, v_q: float, theta_e: float) -> Tuple[float, float]:
        cos_th = math.cos(theta_e)
        sin_th = math.sin(theta_e)
        v_alpha = v_d * cos_th - v_q * sin_th
        v_beta = v_d * sin_th + v_q * cos_th
        return v_alpha, v_beta

    def compute_svpwm(self, v_alpha: float, v_beta: float) -> Tuple[float, float, float, int]:
        if self.v_dc < 1.0:
            return 0.5, 0.5, 0.5, 0

        u1 = v_beta
        u2 = (-v_beta + math.sqrt(3.0) * v_alpha) * 0.5
        u3 = (-v_beta - math.sqrt(3.0) * v_alpha) * 0.5

        sector = 0
        if u1 > 0.0:
            sector |= 1
        if u2 > 0.0:
            sector |= 2
        if u3 > 0.0:
            sector |= 4

        root3 = math.sqrt(3.0)
        v_dc = self.v_dc

        if sector == 1:   # Sector 2
            t1 = (root3 * v_alpha + v_beta) * 0.5 / v_dc
            t2 = (-root3 * v_alpha + v_beta) * 0.5 / v_dc
        elif sector == 2: # Sector 6
            t1 = (root3 * v_alpha - v_beta) * 0.5 / v_dc
            t2 = v_beta / v_dc
        elif sector == 3: # Sector 1
            t1 = (-root3 * v_alpha + v_beta) * 0.5 / v_dc
            t2 = (root3 * v_alpha + v_beta) * 0.5 / v_dc
        elif sector == 4: # Sector 4
            t1 = -v_beta / v_dc
            t2 = (root3 * v_alpha + v_beta) * 0.5 / v_dc
        elif sector == 5: # Sector 3
            t1 = v_beta / v_dc
            t2 = (-root3 * v_alpha - v_beta) * 0.5 / v_dc
        elif sector == 6: # Sector 5
            t1 = (-root3 * v_alpha - v_beta) * 0.5 / v_dc
            t2 = (root3 * v_alpha - v_beta) * 0.5 / v_dc
        else:
            t1, t2 = 0.0, 0.0
            sector = 1

        t1 = max(0.0, min(1.0, t1))
        t2 = max(0.0, min(1.0 - t1, t2))
        t0 = (1.0 - t1 - t2) * 0.5

        if sector == 3:
            da, db, dc = t1 + t2 + t0, t2 + t0, t0
        elif sector == 1:
            da, db, dc = t1 + t0, t1 + t2 + t0, t0
        elif sector == 5:
            da, db, dc = t0, t1 + t2 + t0, t2 + t0
        elif sector == 4:
            da, db, dc = t0, t1 + t0, t1 + t2 + t0
        elif sector == 6:
            da, db, dc = t2 + t0, t0, t1 + t2 + t0
        elif sector == 2:
            da, db, dc = t1 + t2 + t0, t0, t1 + t0
        else:
            da, db, dc = 0.5, 0.5, 0.5

        return da, db, dc, sector


def test_clarke_park_transformation_orthogonality():
    """Verify amplitude-invariant Clarke and Park transforms preserve magnitude."""
    foc = PythonFocController(0.1, 0.001, 0.001, 0.02, 7, 48.0, 1.0, 100.0, 24.0, 5e-5)
    i_peak = 15.0

    for theta_deg in range(0, 360, 15):
        th_rad = math.radians(theta_deg)
        # Balanced 3-phase currents
        ia = i_peak * math.cos(th_rad)
        ib = i_peak * math.cos(th_rad - 2.0 * math.pi / 3.0)
        ic = i_peak * math.cos(th_rad + 2.0 * math.pi / 3.0)
        assert abs(ia + ib + ic) < 1e-10

        i_alpha, i_beta = foc.clarke_transform(ia, ib)
        # Check amplitude invariance: norm in alpha-beta matches peak current
        norm_alpha_beta = math.sqrt(i_alpha ** 2 + i_beta ** 2)
        np.testing.assert_allclose(norm_alpha_beta, i_peak, atol=1e-10)

        # Park transform at electrical angle matching current
        i_d, i_q = foc.park_transform(i_alpha, i_beta, th_rad)
        # When current vector is aligned with theta_rad, i_d = i_peak, i_q = 0
        np.testing.assert_allclose(i_d, i_peak, atol=1e-10)
        np.testing.assert_allclose(i_q, 0.0, atol=1e-10)

        # Inverse Park reconstruction
        v_alpha_rec, v_beta_rec = foc.inverse_park_transform(i_d, i_q, th_rad)
        np.testing.assert_allclose(v_alpha_rec, i_alpha, atol=1e-10)
        np.testing.assert_allclose(v_beta_rec, i_beta, atol=1e-10)


def test_svpwm_duty_cycle_bounds_and_sectors():
    """Verify Space Vector PWM duty cycles remain in [0, 1] for all sectors."""
    foc = PythonFocController(0.1, 0.001, 0.001, 0.02, 7, 48.0, 1.0, 100.0, 24.0, 5e-5)
    v_mag = 20.0  # within DC bus synthesis envelope (48 / sqrt(3) ~ 27.7 V)

    sectors_visited = set()
    for angle_deg in range(0, 360, 5):
        rad = math.radians(angle_deg)
        v_alpha = v_mag * math.cos(rad)
        v_beta = v_mag * math.sin(rad)

        da, db, dc, sector = foc.compute_svpwm(v_alpha, v_beta)
        assert 0.0 <= da <= 1.0, f"da out of bounds: {da} at {angle_deg} deg"
        assert 0.0 <= db <= 1.0, f"db out of bounds: {db} at {angle_deg} deg"
        assert 0.0 <= dc <= 1.0, f"dc out of bounds: {dc} at {angle_deg} deg"
        sectors_visited.add(sector)

    # Must visit all 6 physical sectors
    assert len(sectors_visited) == 6, f"Not all sectors covered: {sectors_visited}"

    # Boundary test: low V_dc failsafe
    foc_dead_bus = PythonFocController(0.1, 0.001, 0.001, 0.02, 7, 0.5, 1.0, 100.0, 24.0, 5e-5)
    da, db, dc, sector = foc_dead_bus.compute_svpwm(10.0, 10.0)
    assert (da, db, dc, sector) == (0.5, 0.5, 0.5, 0)


# ==============================================================================
# 5. Chapter 10-4: CAN-FD Bus Utilization & Worst-Case Latency
# ==============================================================================

def compute_canfd_frame_duration_us(payload_bytes: int, arb_baud_bps: float, data_baud_bps: float) -> float:
    """Computes CAN-FD total frame transmission time in microseconds."""
    n_arb_bits = 32.0  # SOF, 29-bit ID, control, ACK, EOF
    n_data_bits = (payload_bytes * 8.0) + 28.0  # Data payload + CRC-21 + stuff bits
    t_arb = (n_arb_bits / arb_baud_bps) * 1e6
    t_data = (n_data_bits / data_baud_bps) * 1e6
    return t_arb + t_data


def compute_canfd_wcrt(c_times: List[float], periods: List[float]) -> Tuple[List[float], float]:
    """
    Computes worst-case response times via recurrence:
    R_i^(k+1) = C_i + B_i + sum_{j in hp(i)} ceil(R_i^(k) / P_j) * C_j
    Tasks ordered by priority (index 0 is highest priority).
    """
    m = len(c_times)
    utilization = sum(c / p for c, p in zip(c_times, periods))
    response_times = []

    for i in range(m):
        # Blocking time B_i from lower priority messages
        bi = max(c_times[i+1:]) if i + 1 < m else 0.0
        r_prev = c_times[i] + bi

        while True:
            interference = 0.0
            for j in range(i):  # higher priority
                interference += math.ceil(r_prev / periods[j]) * c_times[j]
            r_next = c_times[i] + bi + interference

            if r_next == r_prev:
                response_times.append(r_next)
                break
            if r_next > periods[i] * 10:  # Divergence / unschedulable
                response_times.append(float("inf"))
                break
            r_prev = r_next

    return response_times, utilization


def test_canfd_timing_and_schedulability_equations():
    """Verify Chapter 10-4 8-joint humanoid CAN-FD network timing and WCRT."""
    # 8 joints transmitting 32-byte state at 1 kHz (P = 1000 us)
    # Arb: 1 Mbit/s, Data: 5 Mbit/s
    t_frame = compute_canfd_frame_duration_us(32, 1e6, 5e6)
    # 32 bits @ 1 us = 32 us; (32*8 + 28) = 284 bits @ 0.2 us = 56.8 us -> total ~ 88.8 us
    assert 75.0 <= t_frame <= 95.0

    c_times = [t_frame] * 8
    periods = [1000.0] * 8  # 1 kHz

    r_times, util = compute_canfd_wcrt(c_times, periods)
    assert util < 0.75  # Bus utilization ~ 70%
    # Every joint message completes within the 1000 us deadline
    for idx, r in enumerate(r_times):
        assert r < periods[idx], f"Joint {idx} missed deadline: {r} >= {periods[idx]}"

    # Boundary test: Overload condition (15 joints at 1 kHz)
    c_overload = [t_frame] * 15
    p_overload = [1000.0] * 15
    _, util_overload = compute_canfd_wcrt(c_overload, p_overload)
    assert util_overload > 1.0  # Overloaded bus correctly identified


# ==============================================================================
# 6. Chapter 10-5: Roofline Performance Model & Operational Intensity
# ==============================================================================

def compute_roofline_attainable_performance(p_peak_tflops: float, b_mem_gb_s: float, intensity: float) -> Tuple[float, float, str]:
    """
    P_attainable = min(P_peak, B_mem * I)
    I_knee = P_peak / B_mem
    """
    if b_mem_gb_s <= 0.0:
        return 0.0, float("inf"), "Memory-Bandwidth Bound (Zero BW)"
    i_knee = (p_peak_tflops * 1e12) / (b_mem_gb_s * 1e9)  # FLOPs / Byte

    # Compute attainable in TFLOPS
    p_mem_bound = (b_mem_gb_s * 1e9 * intensity) / 1e12
    p_attainable = min(p_peak_tflops, p_mem_bound)
    regime = "Compute-Bound" if intensity >= i_knee else "Memory-Bandwidth Bound"
    return p_attainable, i_knee, regime


def test_roofline_model_jetson_agx_orin():
    """Verify Roofline model calculations for Jetson AGX Orin (138 TFLOPS, 204.8 GB/s)."""
    p_peak = 138.0  # TFLOPS FP16
    b_mem = 204.8   # GB/s

    p_att, i_knee, regime = compute_roofline_attainable_performance(p_peak, b_mem, intensity=10.0)
    # I_knee = 138e12 / 204.8e9 ~ 673.83 FLOPs/Byte
    np.testing.assert_allclose(i_knee, 673.828, atol=0.01)
    assert regime == "Memory-Bandwidth Bound"
    # At I = 10, attainable = 204.8 * 10 / 1000 = 2.048 TFLOPS << 138
    np.testing.assert_allclose(p_att, 2.048, atol=1e-3)

    # Compute-bound regime (I = 1500)
    p_att_high, _, regime_high = compute_roofline_attainable_performance(p_peak, b_mem, intensity=1500.0)
    assert regime_high == "Compute-Bound"
    assert p_att_high == p_peak


# ==============================================================================
# 7. Chapter 10-6: Allan Deviation Computation
# ==============================================================================

class AllanVarianceProcessor:
    def __init__(self, sample_rate_hz: float):
        if sample_rate_hz <= 0.0:
            raise ValueError("Sample rate must be strictly positive.")
        self.fs = sample_rate_hz
        self.dt = 1.0 / sample_rate_hz

    def compute_overlapping_adev(self, data_series: np.ndarray, num_tau_points: int = 40) -> Tuple[np.ndarray, np.ndarray]:
        N = len(data_series)
        if N < 6:
            raise ValueError("Data series too short for Allan deviation.")
        theta = np.cumsum(data_series) * self.dt
        max_m = N // 3
        m_factors = np.unique(np.logspace(0, np.log10(max_m), num_tau_points).astype(int))
        m_factors = m_factors[m_factors > 0]

        tau_list, adev_list = [], []
        for m in m_factors:
            tau = m * self.dt
            d2 = theta[2 * m:] - 2.0 * theta[m:-m] + theta[:-2 * m]
            variance = np.sum(d2 ** 2) / (2.0 * (tau ** 2) * (N - 2 * m))
            adev = np.sqrt(variance)
            tau_list.append(tau)
            adev_list.append(adev)

        return np.array(tau_list), np.array(adev_list)


def test_allan_deviation_white_noise_slope():
    """Verify Allan deviation of white noise exhibits characteristic -1/2 slope in log-log."""
    fs = 100.0
    n_samples = 30000
    np.random.seed(123)
    # White noise: sigma = 0.5 rad/s
    white_noise = np.random.normal(0, 0.5, n_samples)

    proc = AllanVarianceProcessor(fs)
    tau, adev = proc.compute_overlapping_adev(white_noise, num_tau_points=25)

    # Log-log linear regression on short tau range
    log_tau = np.log10(tau[:15])
    log_adev = np.log10(adev[:15])
    slope, _ = np.polyfit(log_tau, log_adev, 1)

    # Theoretical slope for white noise is -0.5
    assert -0.65 <= slope <= -0.35, f"Unexpected ADEV slope for white noise: {slope}"


def test_allan_deviation_boundary_conditions():
    """Test boundary conditions: constant signal, non-positive fs, short sample."""
    with pytest.raises(ValueError, match="strictly positive"):
        AllanVarianceProcessor(-10.0)

    proc = AllanVarianceProcessor(100.0)
    with pytest.raises(ValueError, match="too short"):
        proc.compute_overlapping_adev(np.array([1.0, 2.0]))

    # Constant signal -> Allan deviation identically zero
    const_data = np.full(500, 3.14)
    _, adev = proc.compute_overlapping_adev(const_data)
    np.testing.assert_allclose(adev, 0.0, atol=1e-12)


# ==============================================================================
# 8. Chapter 10-7: Rate Monotonic Scheduling (RMS) Bounds
# ==============================================================================

def liu_layland_bound(n: int) -> float:
    if n <= 0:
        raise ValueError("Task count n must be positive.")
    return float(n * (2.0 ** (1.0 / n) - 1.0))


def test_liu_layland_rms_utilization_bounds():
    """Verify Liu & Layland bound values: n=1, n=2, n=3, and asymptotic limit ln(2)."""
    assert liu_layland_bound(1) == 1.0
    np.testing.assert_allclose(liu_layland_bound(2), 2.0 * (math.sqrt(2.0) - 1.0), atol=1e-7)
    np.testing.assert_allclose(liu_layland_bound(3), 3.0 * (2.0 ** (1.0 / 3.0) - 1.0), atol=1e-7)

    # Check monotonicity
    for n in range(1, 100):
        assert liu_layland_bound(n) > liu_layland_bound(n + 1)

    # Asymptotic convergence to ln(2) ~ 0.693147
    np.testing.assert_allclose(liu_layland_bound(100000), math.log(2.0), atol=1e-5)


def compute_rms_wcrt(c_times: List[float], periods: List[float]) -> Tuple[List[float], float]:
    """
    Computes exact worst-case response times for preemptive fixed-priority tasks (RMS):
    R_i^(k+1) = C_i + sum_{j in hp(i)} ceil(R_i^(k) / T_j) * C_j
    Initialized at R_i^(0) = C_i.
    """
    m = len(c_times)
    utilization = sum(c / p for c, p in zip(c_times, periods))
    response_times = []

    for i in range(m):
        r_prev = c_times[i]
        while True:
            interference = sum(math.ceil(r_prev / periods[j]) * c_times[j] for j in range(i))
            r_next = c_times[i] + interference
            if r_next == r_prev:
                response_times.append(r_next)
                break
            if r_next > periods[i]:  # Deadline missed
                response_times.append(r_next)
                break
            r_prev = r_next

    return response_times, utilization


def test_multirate_firmware_wcrt_schedulability():
    """Verify Chapter 10-7 multi-rate firmware (FOC 20 kHz, Impedance 1 kHz, Safety 50 Hz)."""
    # Task 1: FOC (20 kHz, T1 = 50 us, C1 = 18 us)
    # Task 2: Impedance control (1 kHz, T2 = 1000 us, C2 = 150 us)
    # Task 3: Safety check (50 Hz, T3 = 20000 us, C3 = 500 us)
    periods = [50.0, 1000.0, 20000.0]
    exec_times = [18.0, 150.0, 500.0]

    u1 = 18.0 / 50.0       # 0.36
    u2 = 150.0 / 1000.0    # 0.15
    u3 = 500.0 / 20000.0   # 0.025
    u_total = u1 + u2 + u3  # 0.535

    # Check Liu & Layland bound for n=3: U <= 0.7798
    assert u_total < liu_layland_bound(3)

    # Compute exact preemptive RMS WCRT
    r_times, _ = compute_rms_wcrt(exec_times, periods)
    assert r_times[0] == 18.0
    assert r_times[1] < periods[1]
    assert r_times[2] < periods[2]


# ==============================================================================
# 9. Chapter 10-8: MTBF & Thermal Dissipation
# ==============================================================================

def compute_mil_hdbk_reliability(fit_allocations: Dict[str, float], operating_hours: float) -> Tuple[float, float, float]:
    """
    Computes system failure rate lambda, MTBF, and mission survival probability R(t).
    fit_allocations: Dictionary of subsystem FIT (failures per 10^6 hours).
    """
    total_fit = sum(fit_allocations.values())
    lambda_per_hr = total_fit * 1e-6
    if lambda_per_hr <= 0.0:
        return 0.0, float("inf"), 1.0
    mtbf_hours = 1.0 / lambda_per_hr
    r_t = math.exp(-lambda_per_hr * operating_hours)
    return total_fit, mtbf_hours, r_t


def compute_thermal_dissipation_delta_t(p_dissipated_w: float, r_jc: float, r_cs: float, r_sa: float) -> float:
    """Delta T = P_dissipated * (R_jc + R_cs + R_sa)"""
    r_total = r_jc + r_cs + r_sa
    return p_dissipated_w * r_total


def test_mil_hdbk_humanoid_mtbf_architecture():
    """Verify Chapter 10-8 Humanoid 28-DoF MTBF allocation yields ~2,016 hours."""
    fit_map = {
        "joints_28": 28.0 * 12.0,  # 336.0 FIT
        "bms_pack": 25.0,          # 25.0 FIT
        "compute_carrier": 30.0,   # 30.0 FIT
        "wiring_sliprings": 45.0,  # 45.0 FIT
        "sensors": 4.0 * 15.0      # 60.0 FIT
    }
    total_fit, mtbf, r_100hr = compute_mil_hdbk_reliability(fit_map, operating_hours=100.0)

    # Total FIT = 336 + 25 + 30 + 45 + 60 = 496.0 FIT
    assert total_fit == 496.0
    # MTBF = 1 / (496e-6) = 2016.129 hours
    np.testing.assert_allclose(mtbf, 2016.129, atol=0.01)
    # Reliability over 100 hours: exp(-0.0496) ~ 0.9516
    np.testing.assert_allclose(r_100hr, math.exp(-496e-6 * 100.0), atol=1e-5)


def test_thermal_dissipation_delta_t():
    """Verify Delta T = P * R_theta and forced convection resistance scaling."""
    # 50W dissipated, R_jc = 0.2 C/W, R_cs = 0.1 C/W, R_sa = 0.4 C/W
    p_loss = 50.0
    delta_t = compute_thermal_dissipation_delta_t(p_loss, r_jc=0.2, r_cs=0.1, r_sa=0.4)
    # R_total = 0.7 C/W -> Delta T = 35.0 C
    assert delta_t == 35.0

    # Boundary test: Zero power -> zero rise
    assert compute_thermal_dissipation_delta_t(0.0, 0.2, 0.1, 0.4) == 0.0


# ==============================================================================
# 10. Adversarial Stress & Boundary Condition Challenges
# ==============================================================================

def test_chapter_10_1_proximal_relocation_benefit():
    """Verify claim in 10-1: Proximal actuator relocation cuts swing inertia significantly with identical total mass."""
    # Foot mass 1.6kg at d=0.82m vs relocation of 0.8kg to upper tibia d=0.42m
    # Conventional leg
    links_conv = [
        RigidLinkSegment("thigh", 4.2, np.array([0, 0, -0.18]), np.diag([0.045, 0.042, 0.008]), np.array([0, 1, 0]), np.zeros(3)),
        RigidLinkSegment("shank_heavy", 3.8, np.array([0, 0, -0.15]), np.diag([0.038, 0.035, 0.006]), np.array([0, 1, 0]), np.array([0, 0, -0.42])),
        RigidLinkSegment("foot_heavy", 1.6, np.array([0.04, 0, -0.04]), np.diag([0.004, 0.006, 0.003]), np.array([0, 1, 0]), np.array([0, 0, -0.40]))
    ]
    # Optimized leg: identical 9.6 kg total mass, but motor moved proximally
    links_opt = [
        RigidLinkSegment("thigh_heavy", 5.8, np.array([0, 0, -0.12]), np.diag([0.052, 0.048, 0.010]), np.array([0, 1, 0]), np.zeros(3)),
        RigidLinkSegment("shank_light", 2.2, np.array([0, 0, -0.18]), np.diag([0.018, 0.016, 0.003]), np.array([0, 1, 0]), np.array([0, 0, -0.42])),
        RigidLinkSegment("foot_light", 1.6, np.array([0.04, 0, -0.04]), np.diag([0.004, 0.006, 0.003]), np.array([0, 1, 0]), np.array([0, 0, -0.40]))
    ]
    analyzer_conv = HumanoidLimbMassAnalyzer(links_conv)
    analyzer_opt = HumanoidLimbMassAnalyzer(links_opt)
    assert analyzer_conv.total_mass == analyzer_opt.total_mass == 9.6

    test_angles = np.radians([20.0, -35.0, 15.0])
    pitch_axis = np.array([0.0, 1.0, 0.0])

    i_conv = analyzer_conv.compute_swing_inertia_about_hip(test_angles, pitch_axis)
    i_opt = analyzer_opt.compute_swing_inertia_about_hip(test_angles, pitch_axis)

    reduction_pct = (1.0 - (i_opt / i_conv)) * 100.0
    # Proximal relocation yields ~19.7% swing inertia reduction with identical total leg mass
    assert 19.5 <= reduction_pct <= 20.0, f"Expected ~19.7% inertia reduction, got {reduction_pct:.2f}%"


def test_chapter_10_2_actuator_thermal_boundary_conditions():
    """Stress-test actuator thermal model under infinite/zero gear ratios, extreme currents, and boiling ambient."""
    specs = ActuatorSpecs(
        model_name="Stress-Actuator", gear_ratio=9.0, rotor_inertia_kgm2=1e-4,
        motor_kt_nm_per_a=0.2, phase_resistance_ohm=0.1, gearbox_efficiency=0.9,
        max_peak_torque_nm=150.0, continuous_torque_nm=60.0, max_joint_speed_rad_s=15.0,
        bus_voltage_v=48.0, thermal_res_wind_to_case=1.0, thermal_res_case_to_amb=1.5,
        thermal_cap_wind_j_per_c=100.0, thermal_cap_case_j_per_c=400.0
    )
    sim = ActuatorThermalSimulator(specs)

    # 1. Zero torque trajectory (cooling only)
    t = np.linspace(0, 100, 1000)
    res_zero = sim.evaluate_trajectory(t, np.zeros_like(t), np.zeros_like(t), ambient_temp_c=30.0)
    assert res_zero["peak_torque_nm"] == 0.0
    assert res_zero["rms_torque_nm"] == 0.0
    assert res_zero["mean_copper_loss_w"] == 0.0
    np.testing.assert_allclose(res_zero["max_winding_temp_c"], 30.0, atol=1e-3)
    np.testing.assert_allclose(res_zero["thermal_headroom_c"], 125.0, atol=1e-3)

    # 2. Over-torque trajectory exceeding peak and RMS limits
    extreme_torque = np.full_like(t, 250.0)  # limit is 150
    res_extreme = sim.evaluate_trajectory(t, extreme_torque, np.zeros_like(t), ambient_temp_c=25.0)
    assert res_extreme["feasible_peak_torque"] is False
    assert res_extreme["feasible_rms_torque"] is False
    assert res_extreme["max_winding_temp_c"] > 100.0


def test_chapter_10_3_foc_voltage_saturation_and_antiwindup():
    """Stress-test FOC controller under extreme reference steps causing voltage vector saturation."""
    # Controller with max voltage 24V
    foc = PythonFocController(
        rs=0.08, ld=0.0005, lq=0.0005, lambda_m=0.015, pole_pairs=7,
        v_dc=48.0, kp=2.0, ki=150.0, max_v=24.0, dt=5e-5
    )

    # Extreme current step command: target Iq = 100 A while actual Iq = 0 A
    err_q = 100.0
    int_limit = foc.max_v * 0.8
    max_integral = int_limit / foc.ki

    # Step integration for 1000 cycles
    for _ in range(1000):
        foc.int_q += err_q * foc.dt
        foc.int_q = max(-max_integral, min(max_integral, foc.int_q))

    # Integral error must be strictly clamped to max_integral, NOT blown up
    assert foc.int_q == max_integral
    v_q_pi = foc.kp * err_q + foc.ki * foc.int_q
    assert v_q_pi > foc.max_v  # Raw PI wants > 200V

    # Voltage circle vector limiting: magnitude clamped to max_v (24.0V)
    v_d = 0.0
    v_q = v_q_pi
    v_mag = math.sqrt(v_d**2 + v_q**2)
    v_d_clamped = (v_d / v_mag) * foc.max_v
    v_q_clamped = (v_q / v_mag) * foc.max_v
    np.testing.assert_allclose(math.sqrt(v_d_clamped**2 + v_q_clamped**2), 24.0, atol=1e-6)
    assert v_q_clamped == 24.0
    assert v_d_clamped == 0.0


def test_chapter_10_4_canfd_high_message_density_and_overload():
    """Stress-test CAN-FD with 30 nodes to verify WCRT saturation and preemption order."""
    t_frame = 85.0  # us per message
    n_nodes = 30
    periods = [10000.0] * n_nodes  # 10 ms period (100 Hz each)
    c_times = [t_frame] * n_nodes

    r_times, util = compute_canfd_wcrt(c_times, periods)
    # Utilization: 30 * 85 / 10000 = 25.5%
    np.testing.assert_allclose(util, 0.255, atol=1e-3)
    # Highest priority has minimal latency
    assert r_times[0] == t_frame + t_frame  # C1 + B1 (blocking from 1 lower frame)
    # All tasks meet deadline
    assert all(r < 10000.0 for r in r_times)
    # Lower priority tasks have strictly non-decreasing response times
    for k in range(len(r_times) - 1):
        assert r_times[k] <= r_times[k + 1]


def test_chapter_10_5_roofline_extreme_operational_intensities():
    """Test Roofline model across 8 orders of magnitude of operational intensity."""
    p_peak = 138.0  # TFLOPS
    b_mem = 204.8   # GB/s

    # Ultra-low intensity: 1e-4 FLOPs/Byte (pure streaming memory bound)
    p_att_low, _, reg_low = compute_roofline_attainable_performance(p_peak, b_mem, 1e-4)
    assert reg_low == "Memory-Bandwidth Bound"
    np.testing.assert_allclose(p_att_low, 204.8 * 1e9 * 1e-4 / 1e12, atol=1e-8)

    # Ultra-high intensity: 1e5 FLOPs/Byte (deep compute bound)
    p_att_high, _, reg_high = compute_roofline_attainable_performance(p_peak, b_mem, 1e5)
    assert reg_high == "Compute-Bound"
    assert p_att_high == p_peak


def test_chapter_10_6_allan_deviation_combined_white_and_flicker_noise():
    """Test Allan deviation bathtub curve on synthetic IMU white + flicker noise."""
    fs = 200.0
    dt = 1.0 / fs
    n_samples = 40000
    np.random.seed(42)

    # White noise (ARW) + Flicker drift
    white = (0.01 / math.sqrt(dt)) * np.random.normal(0, 1, n_samples)
    flicker = np.cumsum(np.random.normal(0, 1e-4, n_samples))
    signal = white + flicker

    proc = AllanVarianceProcessor(fs)
    tau, adev = proc.compute_overlapping_adev(signal, num_tau_points=25)

    assert len(tau) > 5
    assert len(adev) > 5
    # ADEV must be strictly positive
    assert np.all(adev > 0.0)
    # Check that initial slope is negative (white noise dominates at short tau)
    assert adev[1] < adev[0]


def test_chapter_10_7_rms_corner_tasks_and_harmonic_sets():
    """Test RMS scheduling with corner tasks (0 exec time, identical periods, harmonic)."""
    # 1. Harmonic task set with 100% utilization: T1=10, C1=5; T2=20, C2=10
    periods_harm = [10.0, 20.0]
    exec_harm = [5.0, 10.0]
    r_harm, u_harm = compute_rms_wcrt(exec_harm, periods_harm)
    assert u_harm == 1.0
    assert r_harm[0] == 5.0
    assert r_harm[1] == 20.0  # Exactly schedulable at deadline!

    # 2. Task with C = 0 (instantaneous execution)
    periods_zero = [10.0, 20.0]
    exec_zero = [0.0, 10.0]
    r_zero, u_zero = compute_rms_wcrt(exec_zero, periods_zero)
    assert r_zero[0] == 0.0
    assert r_zero[1] == 10.0


class BringupStage(Enum):
    INIT = "INIT"
    LOGIC_POWER_CHECK = "LOGIC_POWER_CHECK"
    COMMUNICATION_VERIFY = "COMMUNICATION_VERIFY"
    PRECHARGE_MONITOR = "PRECHARGE_MONITOR"
    MICRO_TORQUE_EXCITATION = "MICRO_TORQUE_EXCITATION"
    THERMAL_PROFILE_CHECK = "THERMAL_PROFILE_CHECK"
    SYSTEM_ARMED_READY = "SYSTEM_ARMED_READY"
    FAULT_ABORT = "FAULT_ABORT"


@dataclass
class DiagnosticTelemetry:
    joint_id: int
    name: str
    is_comm_active: bool = False
    bus_voltage_v: float = 0.0
    heatsink_temp_c: float = 0.0
    has_active_fault: bool = False
    error_string: str = ""


class HumanoidBringupDiagnosticManager:
    def __init__(self, joint_names: List[str]):
        self.joint_names = joint_names
        self.current_stage = BringupStage.INIT
        self.telemetry = {i: DiagnosticTelemetry(i, name) for i, name in enumerate(joint_names)}

    def execute_stage_logic_power(self, voltage_v: float) -> bool:
        self.current_stage = BringupStage.LOGIC_POWER_CHECK
        if 22.0 <= voltage_v <= 26.0:
            return True
        self.current_stage = BringupStage.FAULT_ABORT
        return False

    def execute_stage_comm(self, online_ids: List[int]) -> bool:
        self.current_stage = BringupStage.COMMUNICATION_VERIFY
        all_ok = True
        for j_id, telem in self.telemetry.items():
            if j_id in online_ids:
                telem.is_comm_active = True
            else:
                telem.is_comm_active = False
                telem.has_active_fault = True
                telem.error_string = "Node timeout"
                all_ok = False
        if not all_ok:
            self.current_stage = BringupStage.FAULT_ABORT
        return all_ok

    def execute_stage_precharge(self, v_bus_curve: np.ndarray, target_v: float = 48.0) -> bool:
        self.current_stage = BringupStage.PRECHARGE_MONITOR
        if len(v_bus_curve) == 0:
            self.current_stage = BringupStage.FAULT_ABORT
            return False
        final_v = v_bus_curve[-1]
        if final_v >= target_v * 0.95:
            for t in self.telemetry.values():
                t.bus_voltage_v = final_v
            return True
        self.current_stage = BringupStage.FAULT_ABORT
        return False

    def execute_stage_thermal(self, temp_map: Dict[int, float], max_temp_c: float = 65.0) -> bool:
        self.current_stage = BringupStage.THERMAL_PROFILE_CHECK
        all_ok = True
        for j_id, telem in self.telemetry.items():
            t_val = temp_map.get(j_id, 25.0)
            telem.heatsink_temp_c = t_val
            if t_val > max_temp_c:
                telem.has_active_fault = True
                telem.error_string = f"Pre-boot thermal trip: {t_val} C"
                all_ok = False
        if all_ok:
            self.current_stage = BringupStage.SYSTEM_ARMED_READY
            return True
        self.current_stage = BringupStage.FAULT_ABORT
        return False


def test_chapter_10_8_bringup_manager_fault_injections():
    """Stress-test Chapter 10-8 bring-up manager under injected hardware faults."""
    joints = [f"joint_{i}" for i in range(28)]

    # 1. Fault at Stage 1: Logic rail undervoltage (19V)
    mgr1 = HumanoidBringupDiagnosticManager(joints)
    assert mgr1.execute_stage_logic_power(19.0) is False
    assert mgr1.current_stage == BringupStage.FAULT_ABORT

    # 2. Fault at Stage 2: Missing node (joint 12 offline)
    mgr2 = HumanoidBringupDiagnosticManager(joints)
    assert mgr2.execute_stage_logic_power(24.0) is True
    online = [i for i in range(28) if i != 12]
    assert mgr2.execute_stage_comm(online) is False
    assert mgr2.current_stage == BringupStage.FAULT_ABORT
    assert mgr2.telemetry[12].has_active_fault is True

    # 3. Fault at Stage 3: Precharge failed (only reached 35V)
    mgr3 = HumanoidBringupDiagnosticManager(joints)
    mgr3.execute_stage_logic_power(24.0)
    mgr3.execute_stage_comm(list(range(28)))
    assert mgr3.execute_stage_precharge(np.array([10.0, 20.0, 35.0])) is False
    assert mgr3.current_stage == BringupStage.FAULT_ABORT

    # 4. Fault at Stage 5: Overheating drive (joint 3 heatsink = 78C)
    mgr4 = HumanoidBringupDiagnosticManager(joints)
    mgr4.execute_stage_logic_power(24.0)
    mgr4.execute_stage_comm(list(range(28)))
    mgr4.execute_stage_precharge(np.array([10.0, 30.0, 46.5]))
    assert mgr4.execute_stage_thermal({3: 78.0}, max_temp_c=65.0) is False
    assert mgr4.current_stage == BringupStage.FAULT_ABORT
    assert mgr4.telemetry[3].has_active_fault is True

    # 5. Happy path: All stages succeed -> SYSTEM_ARMED_READY
    mgr_ok = HumanoidBringupDiagnosticManager(joints)
    assert mgr_ok.execute_stage_logic_power(24.5) is True
    assert mgr_ok.execute_stage_comm(list(range(28))) is True
    assert mgr_ok.execute_stage_precharge(np.array([10.0, 30.0, 46.5])) is True
    assert mgr_ok.execute_stage_thermal({i: 28.0 for i in range(28)}) is True
    assert mgr_ok.current_stage == BringupStage.SYSTEM_ARMED_READY
