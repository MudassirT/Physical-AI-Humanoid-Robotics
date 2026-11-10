# Worker M4 Fixer State Folder
Remediation of 3 Module 12 edge cases & test suite cleanup.
State folder: .agents/teamwork/worker_m4_fixer/


## 2026-11-09T20:29:30Z
You are worker_m4_fixer, an expert code remediation engineer and algorithmic verifier.
Your task is to resolve the 3 algorithmic edge cases in Module 12 and verify that the full backend test suite passes 100% and production Docusaurus build succeeds.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

First, read the review reports:
1. `C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\reviewer_m4_1\handoff.md` (Section 4 Actionable Recommendations)
2. `C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\challenger_m4_2\handoff.md` (Section 2 Logic Chain & Section 4 Conclusion)
3. `C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\ORIGINAL_REQUEST.md`

Your specific remediation tasks:

Task 1: Fix Centroidal Momentum Landing Controller Gravity Calculation in Chapter 12-2
File: `ai-book-docs/module12-capstone-frontiers/12-2-research-frontiers-locomotion.mdx`
- In `CentroidalMomentumLandingController.compute_desired_momentum_rates`:
  Remove `self.mass * self.gravity` from `p_dot_des` so that it correctly computes the desired net momentum rate:
  ```python
  p_dot_des = (
      self.kp_lin @ (com_pos_ref - com_pos)
      + self.kd_lin @ (com_vel_ref - com_vel)
  )
  ```
- In `solve_ground_reaction_forces`:
  Keep `b = np.concatenate([p_dot_des - self.mass * self.gravity, l_dot_des])`.
  This produces correct upward gravity compensation $-mg \approx +637.65\text{ N}$, yielding total vertical force $F_z \approx 717.65\text{ N}$ during the -2.5 m/s drop.
- In the `__main__` verification block at the bottom of the chapter, ensure:
  `print(f"Total Normal Force Fz (N): {round(forces['total_normal_force'], 2)}")`
  `assert forces['total_normal_force'] >= controller.mass * 9.81, "Normal force insufficient for gravity compensation!"`

Task 2: Fix Sigmoid Inversion Sign in Scaling Law Projector in Chapter 12-4
File: `ai-book-docs/module12-capstone-frontiers/12-4-the-future-of-humanoid-robotics.mdx`
- In `RoboticScalingLawProjector.project_required_data_hours`:
  Change line 279 from:
  `target_loss = self.L_0 - (1.0 / self.k) * np.log((1.0 / target_success_rate) - 1.0)`
  to:
  `target_loss = self.L_0 + (1.0 / self.k) * np.log((1.0 / target_success_rate) - 1.0)`
  This mathematically inverts $S = 1 / (1 + \exp(k(L - L_0)))$ correctly so that high target success rate (0.90) requires lower loss (0.0754) and yields positive required data hours.
- In the `__main__` verification block, ensure calculations reflect the correct inverted loss.

Task 3: Fix BibTeX Parsing Regex Anchor in Chapter 12-6
File: `ai-book-docs/module12-capstone-frontiers/12-6-reference-and-bibliography.mdx`
- In `RoboticsBibTeXSearchEngine.parse_and_insert_bibtex`:
  Change line 232 from:
  `entry_pattern = re.compile(r'@(\w+)\s*\{\s*([^,]+),\s*(.*?)\n\}', re.DOTALL)`
  to:
  `entry_pattern = re.compile(r'@(\w+)\s*\{\s*([^,]+),\s*(.*?)\n\s*\}', re.DOTALL)`
  Allow optional whitespace `\s*` before the closing brace `}` so indented BibTeX entries parse properly.

Task 4: Update Adversarial Test File & Clean Ruff Errors
File: `backend/tests/test_adversarial_safety_capstone_m4.py`
- Update test functions (`test_empirical_12_2_landing_controller_nominal_execution`, `test_adversarial_12_2_landing_controller_physics_stress`, `test_adversarial_12_4_scaling_laws_boundary_and_inversion`, `test_adversarial_12_6_bibtex_parsing_and_search`) to assert the correct, remediated behavior (e.g. `total_normal_force >= 637.65`, `target_loss < 0.35`, and BibTeX count == 3).
- Run `& "backend/.venv/Scripts/ruff.exe" check backend --fix` to fix all linting and unused import errors.
- Run `& "backend/.venv/Scripts/pytest.exe" backend` and ensure 100% of backend tests pass offline (all 214+ tests green).
- Run `npm run build` and ensure exit code 0 with zero broken links.
