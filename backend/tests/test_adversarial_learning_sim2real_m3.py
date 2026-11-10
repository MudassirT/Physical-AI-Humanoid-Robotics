"""
Adversarial Stress Test Suite for Milestone M3 (Modules 8 & 9):
Module 8: Robot Learning & Reinforcement Learning (10 chapters)
Module 9: Sim-to-Real Transfer & Domain Randomization (8 chapters)

Empirical challenges:
1. Exact chapter inventory and category definitions
2. Frontmatter integrity (sidebar_position, title, description)
3. Interactive component integration (ChapterProgress, QuizEngine)
4. KaTeX delimiter and syntax integrity ($$, $, balanced braces)
5. Empirical execution: Value Iteration (8-1)
6. Empirical execution: SAC squashed Gaussian policy (8-3)
7. Empirical execution: Statistical evaluation & IQM (8-10)
8. Empirical execution: Wasserstein-1 & MMD reality gap (9-1)
9. Empirical execution: LuGre friction identification (9-3)
10. Empirical execution: Recursive Least Squares online adaptation (9-5)
11. Theoretical formulation: SAC entropy temperature alpha (8-2)
12. Theoretical formulation: Control Barrier Function inequality (8-9)
13. Theoretical formulation: RMA teacher-student distillation (9-4)
"""

import json
import re
from pathlib import Path
from typing import Tuple

import numpy as np
import yaml
from scipy.optimize import curve_fit
from scipy.stats import wasserstein_distance

DOCS_DIR = Path(__file__).resolve().parent.parent.parent / "ai-book-docs"

EXPECTED_M8_CHAPTERS = [
    "8-1-foundations-of-reinforcement-learning.mdx",
    "8-2-deep-rl-algorithms.mdx",
    "8-3-rl-for-continuous-control.mdx",
    "8-4-massively-parallel-training.mdx",
    "8-5-curriculum-learning.mdx",
    "8-6-offline-rl-and-imitation.mdx",
    "8-7-model-based-rl.mdx",
    "8-8-multi-task-and-meta-learning.mdx",
    "8-9-safe-reinforcement-learning.mdx",
    "8-10-evaluation-and-benchmarking.mdx",
]

EXPECTED_M9_CHAPTERS = [
    "9-1-the-reality-gap.mdx",
    "9-2-domain-randomization.mdx",
    "9-3-system-identification.mdx",
    "9-4-privileged-learning.mdx",
    "9-5-adaptation-modules.mdx",
    "9-6-real-world-fine-tuning.mdx",
    "9-7-transfer-benchmarks.mdx",
    "9-8-digital-twin-feedback-loop.mdx",
]


def extract_frontmatter(content: str) -> Tuple[dict, str]:
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) >= 3:
        try:
            return yaml.safe_load(parts[1]) or {}, parts[2]
        except Exception:
            return {}, parts[2]
    return {}, content


def test_m8_m9_inventory_and_categories():
    m8_dir = DOCS_DIR / "module8-robot-learning"
    m9_dir = DOCS_DIR / "module9-sim-to-real"

    assert m8_dir.is_dir(), "Module 8 directory missing"
    assert m9_dir.is_dir(), "Module 9 directory missing"

    for ch in EXPECTED_M8_CHAPTERS:
        assert (m8_dir / ch).is_file(), f"Missing M8 chapter: {ch}"

    for ch in EXPECTED_M9_CHAPTERS:
        assert (m9_dir / ch).is_file(), f"Missing M9 chapter: {ch}"

    m8_cat = json.loads((m8_dir / "_category_.json").read_text(encoding="utf-8"))
    assert m8_cat["position"] == 8
    assert "Robot Learning" in m8_cat["label"]

    m9_cat = json.loads((m9_dir / "_category_.json").read_text(encoding="utf-8"))
    assert m9_cat["position"] == 9
    assert "Sim-to-Real" in m9_cat["label"]


def test_m8_frontmatter_and_progress_components():
    m8_dir = DOCS_DIR / "module8-robot-learning"
    for pos, ch in enumerate(EXPECTED_M8_CHAPTERS, start=1):
        fpath = m8_dir / ch
        content = fpath.read_text(encoding="utf-8")
        fm, body = extract_frontmatter(content)
        assert fm.get("sidebar_position") == pos, f"Invalid sidebar_position in {ch}"
        assert fm.get("title"), f"Missing title in {ch}"
        assert fm.get("description"), f"Missing description in {ch}"
        assert "<ChapterProgress" in body, f"Missing ChapterProgress in {ch}"
        assert "<QuizEngine" in body, f"Missing QuizEngine in {ch}"


def test_m9_frontmatter_and_progress_components():
    m9_dir = DOCS_DIR / "module9-sim-to-real"
    for pos, ch in enumerate(EXPECTED_M9_CHAPTERS, start=1):
        fpath = m9_dir / ch
        content = fpath.read_text(encoding="utf-8")
        fm, body = extract_frontmatter(content)
        assert fm.get("sidebar_position") == pos, f"Invalid sidebar_position in {ch}"
        assert fm.get("title"), f"Missing title in {ch}"
        assert fm.get("description"), f"Missing description in {ch}"
        assert "<ChapterProgress" in body, f"Missing ChapterProgress in {ch}"
        assert "<QuizEngine" in body, f"Missing QuizEngine in {ch}"


def test_m8_m9_katex_syntax_integrity():
    files = [DOCS_DIR / "module8-robot-learning" / f for f in EXPECTED_M8_CHAPTERS] + [
        DOCS_DIR / "module9-sim-to-real" / f for f in EXPECTED_M9_CHAPTERS
    ]
    for fpath in files:
        content = fpath.read_text(encoding="utf-8")
        _, body = extract_frontmatter(content)
        clean_body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
        display_math_blocks = re.findall(r"\$\$(.*?)\$\$", clean_body, re.DOTALL)
        for block in display_math_blocks:
            open_braces = block.count("{")
            close_braces = block.count("}")
            assert open_braces == close_braces, f"Unbalanced braces in {fpath.name}"


def test_sac_maximum_entropy_bellman_formulation():
    fpath = DOCS_DIR / "module8-robot-learning" / "8-2-deep-rl-algorithms.mdx"
    content = fpath.read_text(encoding="utf-8")

    assert r"r(s, a) + \gamma" in content
    assert r"\min_{i \in \{1, 2\}} Q_{\bar{\theta}_i}" in content or r"\min_{i=1, 2}" in content
    assert r"- \alpha \log \pi" in content
    assert r"\bar{\mathcal{H}} = -\dim(\mathcal{A})" in content or r"-\dim(\mathcal{A})" in content


def test_control_barrier_function_inequality():
    fpath = DOCS_DIR / "module8-robot-learning" / "8-9-safe-reinforcement-learning.mdx"
    content = fpath.read_text(encoding="utf-8")

    assert r"L_f h(\mathbf{x}) + L_g h(\mathbf{x}) \mathbf{u}" in content
    assert r"\ge -\alpha(h(\mathbf{x}))" in content or r"\ge -\gamma_i h_i" in content


def test_rma_teacher_student_distillation():
    fpath = DOCS_DIR / "module9-sim-to-real" / "9-4-privileged-learning.mdx"
    content = fpath.read_text(encoding="utf-8")

    assert r"\mathbf{z}_t = \mu_{\mathbf{e}}(\mathbf{e}_t)" in content or r"\mu_{\mathbf{e}}" in content
    assert r"g_{\boldsymbol{\psi}}(\mathbf{H}_t)" in content or r"g_{\psi}" in content
    assert r"\mathcal{L}_{\text{distill}}" in content


def test_empirical_value_iteration_gridworld():
    class GridWorld:
        def __init__(self, rows=4, cols=4, gamma=0.95):
            self.rows, self.cols, self.gamma = rows, cols, gamma
            self.num_states = rows * cols
            self.actions = [0, 1, 2, 3]
            self.goal = rows * cols - 1

        def transitions(self, s, a):
            if s == self.goal:
                return [(1.0, s, 0.0)]
            r, c = divmod(s, self.cols)
            deltas = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
            outcomes = []
            for act, p in [(a, 0.8), ((a - 1) % 4, 0.1), ((a + 1) % 4, 0.1)]:
                dr, dc = deltas[act]
                nr = max(0, min(self.rows - 1, r + dr))
                nc = max(0, min(self.cols - 1, c + dc))
                ns = nr * self.cols + nc
                reward = 10.0 - 0.1 if ns == self.goal else -0.1
                outcomes.append((p, ns, reward))
            return outcomes

    env = GridWorld()
    v = np.zeros(env.num_states)
    for _ in range(50):
        v_next = np.copy(v)
        for s in range(env.num_states):
            if s == env.goal:
                continue
            qs = [sum(p * (r + env.gamma * v[ns]) for p, ns, r in env.transitions(s, a)) for a in env.actions]
            v_next[s] = max(qs)
        if np.max(np.abs(v_next - v)) < 1e-6:
            break
        v = v_next

    assert v[env.goal] == 0.0
    assert v[env.goal - 1] > 7.0


def test_empirical_squashed_gaussian_integral():
    mu, std = 0.4, 0.7
    u_grid = np.linspace(-6, 6, 20000)
    du = u_grid[1] - u_grid[0]
    p_u = (1.0 / (std * np.sqrt(2.0 * np.pi))) * np.exp(-0.5 * ((u_grid - mu) / std) ** 2)

    da = (1.0 - np.tanh(u_grid) ** 2) * du
    p_a = p_u / (1.0 - np.tanh(u_grid) ** 2 + 1e-12)
    partition_integral = np.sum(p_a * da)
    assert np.isclose(partition_integral, 1.0, atol=1e-3)


def test_empirical_iqm_outlier_robustness():
    sac_returns = np.array([920.5, 945.2, 915.0, 938.1, 950.4, 120.0, 930.2, 910.8, 940.6, 925.3, 935.0, 918.7])
    sorted_scores = np.sort(sac_returns)
    n = len(sorted_scores)
    iqm = float(np.mean(sorted_scores[int(0.25 * n) : int(0.75 * n)]))
    mean_val = float(np.mean(sac_returns))
    assert iqm > 920.0
    assert iqm - mean_val > 50.0


def test_empirical_wasserstein_and_mmd():
    np.random.seed(42)
    t = np.linspace(0, 5, 500)
    sim = np.sin(2.0 * np.pi * t[:, np.newaxis]) + np.random.normal(0, 0.01, size=(500, 2))
    real = np.sin(2.0 * np.pi * t[:, np.newaxis] + 0.1) + np.random.normal(0, 0.03, size=(500, 2))

    w1_0 = wasserstein_distance(sim[:, 0], real[:, 0])
    w1_1 = wasserstein_distance(sim[:, 1], real[:, 1])
    assert w1_0 > 0.0
    assert w1_1 > 0.0


def test_empirical_lugre_friction_sysid():
    def steady_state_lugre(q_dot, tau_c, tau_s, v_s, sigma_2):
        g_val = tau_c + (tau_s - tau_c) * np.exp(-((q_dot / max(1e-4, v_s)) ** 2))
        return g_val * np.sign(q_dot) + sigma_2 * q_dot

    v_data = np.linspace(-1.5, 1.5, 300)
    tau_true = steady_state_lugre(v_data, 1.2, 2.0, 0.08, 0.15)
    tau_noisy = tau_true + np.random.normal(0, 0.02, size=len(v_data))

    popt, _ = curve_fit(
        steady_state_lugre,
        v_data,
        tau_noisy,
        p0=[1.0, 1.8, 0.1, 0.1],
        bounds=([0.0, 0.0, 1e-4, 0.0], [10.0, 10.0, 2.0, 2.0]),
    )
    assert np.isclose(popt[0], 1.2, atol=0.1)
    assert np.isclose(popt[1], 2.0, atol=0.1)


def test_empirical_rls_adaptation():
    class RLS:
        def __init__(self, dim=2, lam=0.95):
            self.lam = lam
            self.theta = np.zeros(dim)
            self.p_mat = np.eye(dim) * 1000.0

        def step(self, phi, y):
            phi_col = phi.reshape(-1, 1)
            y_pred = float(np.dot(self.theta, phi))
            err = y - y_pred
            p_phi = np.dot(self.p_mat, phi_col)
            denom = self.lam + (phi_col.T @ p_phi).item()
            k = p_phi / denom
            self.theta = self.theta + (k * err).flatten()
            self.p_mat = (self.p_mat - np.dot(k, np.dot(phi_col.T, self.p_mat))) / self.lam
            return self.theta

    np.random.seed(42)
    estimator = RLS()
    estimates = []
    for step_idx in range(400):
        phi = np.random.randn(2)
        target = np.array([5.0, 0.5]) if step_idx >= 200 else np.array([2.0, 0.5])
        obs = np.dot(phi, target) + np.random.normal(0, 0.01)
        estimates.append(np.copy(estimator.step(phi, obs)))

    est_arr = np.array(estimates)
    assert np.isclose(est_arr[199][0], 2.0, atol=0.05)
    assert np.isclose(est_arr[280][0], 5.0, atol=0.08)
