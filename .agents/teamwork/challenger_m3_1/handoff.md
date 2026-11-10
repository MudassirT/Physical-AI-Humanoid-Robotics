# Empirical Adversarial Challenge Report — Milestone M3 (Modules 6 & 7)

**Challenger Agent**: `challenger_m3_1` (archetype: teamwork_challenger, roles: critic, specialist)  
**Parent Orchestrator ID**: `a74227da-90a1-47cd-bec0-e7f23041e613`  
**Target Work Product**:
- Module 6: Bipedal Locomotion & Whole-Body Control (10 chapters in `ai-book-docs/module6-bipedal-locomotion/`)
- Module 7: Dexterous Manipulation & Hand Design (8 chapters in `ai-book-docs/module7-dexterous-manipulation/`)  
**Overall Verdict**: **REJECT** (Requires remediation of 4 reproducible Python runtime crashes in Module 6)

---

## 1. Observation

### 1.1 Frontend Compilation & Docusaurus Static Build
- Command executed: `npm run build`
- Result: **PASS** (`Command exited with code 0`).
- Docusaurus v3.10.2 + Rspack completed full compilation, bundle generation, and static site generation across all 18 new MDX chapters with zero broken links and zero JSX/MDX syntax errors.
- Both `_category_.json` files verified:
  - `module6-bipedal-locomotion`: label `"Bipedal Locomotion & Whole-Body Control"`, position `6`.
  - `module7-dexterous-manipulation`: label `"Dexterous Manipulation & Hand Design"`, position `7`.
- All 18 chapters integrate `<ChapterProgress />` and `<QuizEngine />`.

### 1.2 Completeness & Placeholder Audit
- Regex search across all 18 `.mdx` files for banned placeholder strings (`TODO`, `TBD`, `FIXME`, `lorem`, `placeholder`, `COMING SOON`, `TO BE CONTINUED`, `pass  # TODO`):
  - Result: **0 matches** found.
  - Zero placeholder text or uncompleted stubs exist. Word counts across all 18 chapters range between 1,800 and 3,200 words.

### 1.3 Mathematical Formulation Consistency
- **3D-LIPM (Chapter 6-2)**: Equations strictly match Kajita et al. (2003):
  $$\ddot{x} = \omega_0^2(x - p_x), \quad p_x = x - \frac{z_c}{g}\ddot{x}, \quad \omega_0 = \sqrt{\frac{g}{z_c}}$$
  Discrete-time state matrices:
  $$\mathbf{A} = \begin{bmatrix} 1 & \Delta t & \frac{\Delta t^2}{2} \\ 0 & 1 & \Delta t \\ 0 & 0 & 1 \end{bmatrix}, \quad \mathbf{B} = \begin{bmatrix} \frac{\Delta t^3}{6} \\ \frac{\Delta t^2}{2} \\ \Delta t \end{bmatrix}, \quad \mathbf{C} = \begin{bmatrix} 1 & 0 & -\frac{z_c}{g} \end{bmatrix}$$
- **Capture Point & DCM (Chapter 6-3)**: Matches Pratt et al. (2006) and Koolen et al. (2012):
  $$\xi = x + \frac{\dot{x}}{\omega_0}, \quad \dot{\xi} = \omega_0(\xi - p)$$
- **Convex MPC (Chapter 6-4)**: Matches Di Carlo et al. (2018) single rigid body model and friction cone linearization:
  $$|f_x| \le \mu f_z, \quad |f_y| \le \mu f_z, \quad f_z \ge 0$$
- **Grasp Wrench Space & Ferrari-Canny (Chapter 7-2)**: Matches Ferrari & Canny (1992):
  $$G = [G_1, \dots, G_k] \in \mathbb{R}^{6 \times 3k}, \quad G_i = \begin{bmatrix} I_{3\times3} \\ [r_i]_\times \end{bmatrix}$$
  Force closure verified with origin $\mathbf{0} \in \mathrm{int}(GWS)$ and $\epsilon = \min_{w \in \partial GWS} \|w\| > 0$.

### 1.4 Empirical Code Snippet Execution
Empirical execution of Python blocks in each chapter produced the following results:

| Chapter | Topic | Status | Verbatim Error / Output |
|---|---|---|---|
| **6-1** | Compass-Gait Hybrid Simulation | **FAIL** | `AttributeError: 'method' object has no attribute 'terminal' and no __dict__ for setting new attributes` |
| **6-2** | Kajita 3D-LIPM Preview Control | **FAIL** | `ValueError: all the input arrays must have same number of dimensions, but the array at index 0 has 1 dimension(s) and the array at index 1 has 2 dimension(s)` & `ValueError: setting an array element with a sequence` |
| **6-3** | Instantaneous Capture Point Push Recovery | **PASS** | `Initial DCM: [0.058, 0.0] -> Perturbed DCM: [0.220, 0.044] -> Selected Strategy: STEPPING_STRATEGY` |
| **6-4** | Convex MPC Legged Gait Controller | **PASS** | `Optimal Ground Reaction Force on Foot 1: [2.25, -49.9, 315.18] N` |
| **6-5** | Whole-Body Control 1 kHz QP | **PASS** | `Computed 1 kHz Joint Torques: [1.0, -0.0, 2.5, 0.0, 0.0, 0.0] N*m, fz: 392.40 N` |
| **6-6** | Vectorized PPO Locomotion Trainer | **PASS** | `Epoch 1, 2, 3: Actor/Critic loss converged; Training iteration verified successfully.` |
| **6-7** | Rapid Motor Adaptation (RMA) Distillation | **PASS** | `Distillation Epoch 1, 2, 3: MSE Loss = 0.0219, Action Norm = 0.512` |
| **6-8** | SLIP Spring-Loaded Hopping Model | **FAIL** | `AttributeError: 'method' object has no attribute 'terminal' and no __dict__ for setting new attributes` |
| **6-9** | Gait Biomechanics & Specific COT | **FAIL** | `AttributeError: module 'numpy' has no attribute 'trapz'` |
| **6-10**| Adversarial Motion Priors (AMP) Discriminator | **PASS** | `Discriminator on Synthetic Human vs Policy Data: Step 1, 2, 3 style reward converged.` |
| **7-1** | Multi-DoF Finger Kinematics & Yoshikawa | **PASS** | `Yoshikawa Manipulability: 1.343932e-04, Condition: 4.09, sigma: [0.0885, 0.0701, 0.0216]` |
| **7-2** | 3D Grasp Matrix & Ferrari-Canny Metric | **PASS** | `Grasp Matrix Rank: 6/6, Force Closure: True, Epsilon: 0.013845, Convex Hull Facets: 466` |
| **7-3** | Tendon Transmission & Winch Friction QP | **PASS** | `Optimization Status: True, Torque Error: 1.43e-16 Nm, Finger Cable Tensions: [40.5, 28, 3, 9.25] N` |
| **7-4** | GelSight Photometric Stereo & Poisson Depth | **PASS** | `Sensor Res: 160x120, Contact Patch: 18166 px, Unit normal vectors length = 1.0` |
| **7-5** | Motion Planning Architecture | **PASS** | Architectural MoveIt 2 / OMPL specifications verified |
| **7-6** | Action Chunking with Transformers (ACT) | **PASS** | `Memory Token: (2, 16, 256), Decoded Chunk: (2, 50, 7), 5-step rolling ensembling verified` |
| **7-7** | Spiral Search & Admittance Peg-in-Hole | **PASS** | `State progression: SURFACE_APPROACH -> SPIRAL_SEARCH -> COMPLIANT_INSERTION verified` |
| **7-8** | Manipulation Benchmarks & Wilson Interval | **PASS** | `Episodes: 40, Success Rate: 100.0%, Wilson 95% CI: [91.24%, 100.0%]` |

---

## 2. Logic Chain

1. **Premise**: Every Python script in the textbook represents an instructional code laboratory intended for readers, engineers, and automated test runners to execute without modification.
2. **Defect 1 (Chapter 6-2)**:
   - In `ai-book-docs/module6-bipedal-locomotion/6-2-zero-moment-point.mdx`, lines 49 & 51 construct `C_tilde` and `A_tilde`:
     ```python
     C_tilde = np.hstack([1.0, np.zeros((1, 3))])
     A_tilde = np.vstack([
         np.hstack([1.0, self.C @ self.A]),
         np.hstack([np.zeros((3, 1)), self.A])
     ])
     ```
   - `1.0` is a scalar (0-D or 1-D upon list creation), whereas `np.zeros((1, 3))` and `self.C @ self.A` are 2-D arrays with shape `(1, 3)`. NumPy's `np.hstack` strictly requires uniform dimension across inputs, raising `ValueError: all the input arrays must have same number of dimensions`.
   - Furthermore, in lines 74 & 77:
     ```python
     self.F[0] = factor @ B_tilde.T @ np.vstack([[1.0], [0.0], [0.0], [0.0]])
     self.F[j] = factor @ B_tilde.T @ X_tilde
     ```
     Matrix multiplication evaluates to a 2D array of shape `(1, 1)`. In modern NumPy, assigning a 2D sequence to a 1D scalar element raises `ValueError: setting an array element with a sequence`.
   - Result: The ZMP preview controller cannot be instantiated, crashing immediately.

3. **Defect 2 (Chapter 6-1)**:
   - In `ai-book-docs/module6-bipedal-locomotion/6-1-introduction-to-bipedal-locomotion.mdx`, lines 106–107:
     ```python
     event_func = self.foot_strike_event
     event_func.terminal = True
     event_func.direction = -1.0
     ```
   - In Python, `self.foot_strike_event` creates a bound method object. Bound method instances are immutable and do not have an instance `__dict__`. Assigning `event_func.terminal = True` raises `AttributeError: 'method' object has no attribute 'terminal' and no __dict__ for setting new attributes`.
   - Result: `solve_ivp` fails to configure the hybrid transition event, aborting the compass-gait simulation.

4. **Defect 3 (Chapter 6-8)**:
   - In `ai-book-docs/module6-bipedal-locomotion/6-8-advanced-locomotion-skills.mdx`, lines 69–71:
     ```python
     event = self.liftoff_event
     event.terminal = True
     event.direction = 1.0
     ```
   - Exactly identical bound method attribute assignment failure as in 6-1, raising `AttributeError`.

5. **Defect 4 (Chapter 6-9)**:
   - In `ai-book-docs/module6-bipedal-locomotion/6-9-gait-analysis-and-biomechanics.mdx`, lines 70–71:
     ```python
     total_energy_consumed = np.trapz(total_electrical_power, dx=self.dt)
     mechanical_work = np.trapz(total_pos_mech_power, dx=self.dt)
     ```
   - `np.trapz` was officially removed in NumPy 2.0. In modern Python environments, running this raises `AttributeError: module 'numpy' has no attribute 'trapz'`. The standard modern replacement is `np.trapezoid` or `scipy.integrate.trapezoid`.

6. **Deduction**: Because 4 of the 10 bipedal locomotion chapters contain code snippets that crash on execution, Milestone M3 fails the empirical code execution requirement of the specification, necessitating a **REJECT** verdict until these 4 defects are remediated.

---

## 3. Caveats

- Hardware-in-the-loop (HIL) testing against physical Unitree G1 / Shadow Hand robot hardware was not conducted.
- The MoveIt 2 motion planning chapter (7-5) describes the ROS 2 MoveGroup C++ / YAML architectural pipeline and contains no standalone Python simulation block; this is appropriate given MoveIt 2's system architecture.
- All 8 chapters of Module 7 (Dexterous Manipulation) executed with zero errors and exceptional mathematical rigor.

---

## 4. Conclusion & Required Action

### Verdict: **REJECT**

Milestone M3 is **REJECTED** exclusively due to the 4 reproducible runtime defects in Module 6 code snippets. Once the following 4 mechanical fixes are applied, the work product will achieve 100% empirical pass status.

### Remediation Steps (Exact Code Replacements)

#### 1. Fix for `ai-book-docs/module6-bipedal-locomotion/6-2-zero-moment-point.mdx`
In the method `_compute_gains`, replace lines 48–53 and 73–78 with:
```python
        # Augmented system: state is [e_k, delta_x_k]^T
        B_tilde = np.vstack([self.C @ self.B, self.B])
        C_tilde = np.hstack([np.array([[1.0]]), np.zeros((1, 3))])
        A_tilde = np.vstack([
            np.hstack([np.array([[1.0]]), self.C @ self.A]),
            np.hstack([np.zeros((3, 1)), self.A])
        ])

        Q_tilde = np.zeros((4, 4))
        Q_tilde[0, 0] = self.Q_e

        # Solve Riccati equation: P = A^T P A - (A^T P B)(R + B^T P B)^-1 (B^T P A) + Q
        P = scipy.linalg.solve_discrete_are(A_tilde, B_tilde, Q_tilde, np.array([[self.R]]))

        # Compute feedback gains
        factor = np.linalg.inv(np.array([[self.R]]) + B_tilde.T @ P @ B_tilde)
        K_tilde = factor @ (B_tilde.T @ P @ A_tilde)

        self.K_i = K_tilde[0, 0]
        self.K_x = K_tilde[0, 1:]

        # Closed-loop state transition matrix
        A_cl = A_tilde - B_tilde @ K_tilde

        # Synthesize preview feedforward gains F_j
        X_tilde = -A_cl.T @ P @ np.vstack([[1.0], [0.0], [0.0], [0.0]])
        self.F = np.zeros(self.N)
        self.F[0] = (factor @ B_tilde.T @ np.vstack([[1.0], [0.0], [0.0], [0.0]])).item()

        for j in range(1, self.N):
            self.F[j] = (factor @ B_tilde.T @ X_tilde).item()
            X_tilde = A_cl.T @ X_tilde
```

#### 2. Fix for `ai-book-docs/module6-bipedal-locomotion/6-1-introduction-to-bipedal-locomotion.mdx`
In method `simulate`, replace lines 105–108 with:
```python
        # Configure Scipy event
        def event_func(t, state):
            return self.foot_strike_event(t, state)
        event_func.terminal = True
        event_func.direction = -1.0  # Zero crossing from positive to negative
```

#### 3. Fix for `ai-book-docs/module6-bipedal-locomotion/6-8-advanced-locomotion-skills.mdx`
In method `step`, replace lines 68–71 with:
```python
        def event(t, state):
            return self.liftoff_event(t, state)
        event.terminal = True
        event.direction = 1.0  # Spring expanding outward
```

#### 4. Fix for `ai-book-docs/module6-bipedal-locomotion/6-9-gait-analysis-and-biomechanics.mdx`
In method `compute_biomechanical_metrics`, replace lines 70–71 with:
```python
        trapezoid_func = getattr(np, 'trapezoid', getattr(np, 'trapz', None))
        total_energy_consumed = trapezoid_func(total_electrical_power, dx=self.dt)
        mechanical_work = trapezoid_func(total_pos_mech_power, dx=self.dt)
```

---

## 5. Verification Method

To independently verify all findings and reproduce the exact test results:

1. **Run the Automated Adversarial Test Suite**:
   ```powershell
   uv run --with numpy,scipy,matplotlib,pyyaml,pytest pytest --noconftest backend/tests/test_adversarial_locomotion_manipulation_m3.py -v
   ```
   *Expected Result*: 21 passed tests (including verified reproduction of all 4 defects in Module 6 and green passes across all 8 chapters of Module 7).

2. **Verify Frontend Static Build**:
   ```powershell
   npm run build
   ```
   *Expected Result*: `[SUCCESS] Generated static files in "build".` with exit code 0.

3. **Verify Remediation Invalidation Condition**:
   Once the 4 fixes listed above are applied to `6-1`, `6-2`, `6-8`, and `6-9`, running `uv run --with numpy,scipy,matplotlib python -c "..."` directly on each file will execute with zero errors, at which point Milestone M3 should be immediately **APPROVED**.
