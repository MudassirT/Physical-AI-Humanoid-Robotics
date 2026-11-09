# Handoff Report: Curriculum Execution Blueprint for Modules 6 & 7
**Author**: `teamwork_explorer_m3_1` (Curriculum Explorer)  
**Target Recipient**: Orchestrator (`9c96a791-1769-4c88-9445-500c157ed676`) / Downstream Author Agents  
**Scope**: Module 6 (Bipedal Locomotion & Whole-Body Control: 10 Chapters) & Module 7 (Dexterous Manipulation & Hand Design: 8 Chapters)  
**Date**: 2026-11-09  

---

## 1. Observation

### 1.1 Direct Repository and Document Observations
1. **Master Curriculum Plan (`specs/010-master-plan-curriculum-expansion/spec.md`)**:
   - Lines 360–448 define **Module 6: Bipedal Locomotion & Whole-Body Control** (10 chapters: `6-1` to `6-10`) spanning classical stability (ZMP, 3D-LIPM, DCM), modern optimal control (Convex MPC, Hierarchical WBC QP), and cutting-edge robot learning (PPO, Sim-to-Real RMA, Neural Parkour, MoCap retargeting, AMP).
   - Lines 450–516 define **Module 7: Dexterous Manipulation & Hand Design** (8 chapters: `7-1` to `7-8`) spanning multi-finger kinematics, grasp wrench space mechanics, tendon transmission and underactuation, optical tactile sensing (GelSight photometric stereo), MoveIt 2 / TAMP motion planning, imitation learning (ACT), compliant peg-in-hole assembly, and manipulation benchmarks (RoboSuite, ManiSkill3, DROID).
2. **Prior Curriculum Miner Blueprint (`.agents/teamwork/spec_miner_curriculum/handoff.md`)**:
   - Lines 434–524 define the specific mathematical formulations and seminal citations for Module 6.
   - Lines 527–596 define the specific mathematical formulations and seminal citations for Module 7.
3. **Existing Documentation Style & Component Standards (`ai-book-docs/`)**:
   - Frontmatter pattern in completed chapters:
     ```yaml
     ---
     sidebar_position: <int>
     title: <string>
     description: <string>
     ---
     ```
   - Interactive assessment component syntax: `<QuizEngine quizId="..." title="..." moduleId="..." passThreshold={70} questions={[...]} />` imported from `@site/src/components/QuizEngine`.
   - Category metadata: Each module directory requires a `_category_.json` file (e.g., `{"label": "Bipedal Locomotion & Whole-Body Control", "position": 6}`).
   - Filesystem verification: Verified via PowerShell that `ai-book-docs/module6-bipedal-locomotion/` and `ai-book-docs/module7-dexterous-manipulation/` currently do not exist (`Test-Path` returned `False`), establishing that full execution specifications must be produced prior to parallel authoring.

---

## 2. Logic Chain

1. **Prerequisite Continuum**: Module 5 established floating-base kinematics, rigid body dynamics ($RNEA$, $CRBA$, $ABA$), and spatial contact geometry. Module 6 builds upon this floating-base formulation by introducing intermittent ground contact constraints, balance stability criteria, and whole-body optimization. Module 7 extends contact mechanics to multi-point object interaction, grasping wrench spaces, and fine-motor tactile feedback.
2. **Mathematical Rigor Requirement**: For the curriculum to rank as the world's premier humanoid textbook, hand-waving conceptual summaries must be replaced with graduate-level, publishable-quality derivations:
   - For locomotion: 3D-LIPM preview Riccati equations, DCM exponential step-adjustment maps, sparse Convex MPC QP matrices under polyhedral friction cones, and hierarchical null-space projection.
   - For manipulation: Grasp matrix wrench equilibrium $\mathbf{w} = -\mathbf{G} \mathbf{f}_c$, Ferrari-Canny $\epsilon$-ball convex hull geometry, Bowden cable Capstan exponential decay, and Poisson surface normal integration for photometric stereo.
3. **Physical Embodiment Grounding**: Theoretical equations must be mapped to real-world humanoid actuators and sensors: Unitree G1/H1, Tesla Optimus Gen 2, Boston Dynamics Atlas (hydraulic and electric), Shadow Dexterous Hand, Wonik Allegro Hand, Robotiq 2F-85, and GelSight/DIGIT optical tactile fingers.
4. **Pedagogical Closure**: Every chapter must provide a complete, self-contained Python/C++ runnable code block and a 2-3 question mastery assessment for the `<QuizEngine />` component.

---

## 3. Module 6 Execution Specifications: Bipedal Locomotion & Whole-Body Control
**Module Path**: `ai-book-docs/module6-bipedal-locomotion/`  
**Category Configuration** (`_category_.json`):
```json
{
  "label": "Bipedal Locomotion & Whole-Body Control",
  "position": 6
}
```

---

### Chapter 6-1: Foundations of Bipedal Locomotion & Underactuated Robotics
- **Target File**: `ai-book-docs/module6-bipedal-locomotion/6-1-introduction-to-bipedal-locomotion.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 1
  title: Foundations of Bipedal Locomotion & Underactuated Robotics
  description: Historical evolution, underactuation degrees of freedom, intermittent contact dynamics, and orbital stability for bipedal humanoids.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *Historical Evolution of Bipedal Robots*: WABOT-1 (1973), Honda P2/ASIMO, Boston Dynamics Atlas (hydraulic servo-valve vs electric QDD), Agility Cassie/Digit, Unitree G1, Tesla Optimus Gen 2.
  2. *The Physics of Underactuation*: Degrees of underactuation ($\dim(\mathbf{q}) - \dim(\boldsymbol{\tau}) = 6$ for floating base). Passive unactuated contact interactions with flat/uneven terrain.
  3. *Hybrid Dynamical Systems*: Intermittent unilateral contact, continuous stance phases, discrete impact events, guard conditions, and state reset maps.
  4. *Limit Cycles & Orbital Stability*: Poincaré return maps, periodic orbits $\mathbf{x}^* = P(\mathbf{x}^*)$, monodromy matrix eigenvalues (Floquet multipliers $|\lambda_i| < 1$).
  5. *Hardware Architecture Comparison*: Hydraulic vs Quasi-Direct Drive (QDD) vs Strain-Wave actuator bandwidth, transmission transparency, and backdrivability.
- **Graduate-Level Mathematical Formulations**:
  - *Floating-Base Equations of Motion*:
    $$\mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{g}(\mathbf{q}) = \mathbf{S}^T \boldsymbol{\tau} + \sum_{k \in \mathcal{C}} \mathbf{J}_{c, k}^T(\mathbf{q}) \boldsymbol{\lambda}_k$$
    where $\mathbf{q} = [\mathbf{p}_b^T, \boldsymbol{\phi}_b^T, \mathbf{q}_j^T]^T \in SE(3) \times \mathbb{R}^n$, $\mathbf{S} = [\mathbf{0}_{n \times 6}, \mathbf{I}_{n \times n}]$, and $\boldsymbol{\lambda}_k \in \mathbb{R}^3$ are ground reaction contact forces.
  - *Discrete Inelastic Impact Map*:
    $$\begin{bmatrix} \mathbf{M}(\mathbf{q}) & -\mathbf{J}_c^T(\mathbf{q}) \\ \mathbf{J}_c(\mathbf{q}) & \mathbf{0} \end{bmatrix} \begin{bmatrix} \dot{\mathbf{q}}^+ \\ \boldsymbol{\Lambda}_{imp} \end{bmatrix} = \begin{bmatrix} \mathbf{M}(\mathbf{q})\dot{\mathbf{q}}^- \\ \mathbf{0} \end{bmatrix}$$
    where $\boldsymbol{\Lambda}_{imp} = \int_{t^-}^{t^+} \boldsymbol{\lambda}(t) dt$ is the impulsive contact wrench.
  - *Poincaré Map Linearization*:
    $$\delta \mathbf{x}_{k+1} = \left. \frac{\partial P(\mathbf{x})}{\partial \mathbf{x}} \right|_{\mathbf{x}^*} \delta \mathbf{x}_k = \boldsymbol{\Phi}(T, 0) \delta \mathbf{x}_k$$
- **Hardware Profile**:
  - Boston Dynamics Atlas (hydraulic): 500 bar system pressure, 175 N·m knee torque, high power density ($> 5$ kW/kg).
  - Unitree G1: 23-43 DOFs, 35 kg mass, 120 N·m peak knee/hip torque, 1 kHz EtherCAT/CAN-FD bus.
- **Seminal Research Citations**:
  - Vukobratović, M., & Juricic, D. (1969). Contribution to the synthesis of biped gait. *IEEE Trans. Biomed. Eng.*, 16(1), 1–6.
  - Pratt, J. E., & Pratt, G. A. (1998). Intuitive control of a planar bipedal walking robot. *ICRA 1998*, pp. 2014–2021.
  - Kuindersma, S., et al. (2016). Optimization-based locomotion planning, estimation, and control methods for the atlas robot. *Autonomous Robots*, 40(3), 429–455.
- **Runnable Code Block Architecture**:
  - Python hybrid dynamic simulation (`scipy.integrate.solve_ivp`) modeling a planar biped with continuous stance phase integration, terminating at ground impact guard $z_{foot}(\mathbf{q}) = 0$, applying algebraic impact equation to reset velocity vector $\dot{\mathbf{q}}^+$, and iterating across 5 strides.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "Why is a floating-base humanoid robot classified as an underactuated system despite having dozens of joint motors?" -> Options: [A: Joint friction dissipates motor power, B: The 6 DOFs connecting the robot pelvis to the inertial world frame have no direct actuators, C: The battery cannot deliver instantaneous peak current, D: Gearboxes introduce backlash] -> Correct: 1.
  - `q2`: "In Poincaré orbital stability analysis of periodic walking gaits, what condition must the Floquet multipliers (eigenvalues of the monodromy matrix) satisfy for asymptotic stability?" -> Options: [A: All real parts must be negative, B: All eigenvalues must have magnitude strictly less than 1, C: The trace of the matrix must equal zero, D: All eigenvalues must be pure imaginary] -> Correct: 1.

---

### Chapter 6-2: The Zero-Moment Point (ZMP) & 3D Linear Inverted Pendulum Model
- **Target File**: `ai-book-docs/module6-bipedal-locomotion/6-2-zero-moment-point.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 2
  title: The Zero-Moment Point (ZMP) & 3D Linear Inverted Pendulum Model
  description: D'Alembert principle, Center of Pressure equivalence, 3D-LIPM dynamics, and Kajita preview control.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *Physical Definition of the ZMP*: D'Alembert virtual work, resultant gravito-inertial wrench, condition $M_x = 0, M_y = 0$.
  2. *Equivalence Between ZMP and Center of Pressure (COP)*: Proof for planar ground contacts; breakdown on non-coplanar contacts.
  3. *3D Linear Inverted Pendulum Model (3D-LIPM)*: Constant CoM height hypothesis ($z = z_c$), zero angular momentum rate of change ($\dot{\mathbf{L}}_{CoM} = \mathbf{0}$), linear uncoupled $x$-$y$ dynamics.
  4. *Kajita Preview Control (2003)*: Augmenting state with CoM jerk $\dddot{x}$, formulating finite preview horizon $N \approx 1.6$ s, solving discrete algebraic Riccati equation (DARE).
  5. *ZMP Stability Margins & Failure Modes*: Single support polygon vs double support polygon, foot edge roll-off instability.
- **Graduate-Level Mathematical Formulations**:
  - *ZMP Coordinates*:
    $$p_x = \frac{\sum m_i (\ddot{z}_i + g) x_i - \sum m_i \ddot{x}_i z_i - \sum I_{yy, i} \dot{\omega}_{y, i}}{\sum m_i (\ddot{z}_i + g)}$$
  - *3D-LIPM Differential Equations*:
    $$\ddot{x} = \frac{g}{z_c}(x - p_x) = \omega_0^2 (x - p_x), \quad \ddot{y} = \frac{g}{z_c}(y - p_y) = \omega_0^2 (y - p_y), \quad \omega_0 = \sqrt{\frac{g}{z_c}}$$
  - *Discrete-Time Optimal Preview Control Law (Kajita 2003)*:
    State: $\mathbf{x}_k = [x_k, \dot{x}_k, \ddot{x}_k]^T$, input jerk $u_k = \dddot{x}_k$.
    $$u_k = -K_i \sum_{i=0}^k (p_{x, i} - p_{x, i}^{ref}) - \mathbf{K}_x \mathbf{x}_k - \sum_{j=1}^N f_j p_{x, k+j}^{ref}$$
    where preview gains $f_j = (R + \mathbf{B}_d^T \mathbf{P} \mathbf{B}_d)^{-1} \mathbf{B}_d^T (\mathbf{A}_d - \mathbf{B}_d \mathbf{K}_x)^{T (j-1)} \mathbf{C}_d^T Q_e$.
- **Hardware Profile**:
  - Honda ASIMO: 6-axis ankle load cell measuring real-time COP, closing the loop with Kajita preview filter at 200 Hz.
  - Kawada HRP-4: 39 DOFs, 39 kg, utilizing ZMP preview reference to govern lower-body joint trajectory interpolation.
- **Seminal Research Citations**:
  - Kajita, S., et al. (2003). Biped walking pattern generation by using preview control of zero-moment point. *ICRA 2003*, pp. 1620–1626.
  - Vukobratović, M., & Borovac, B. (2004). Zero-moment point—thirty five years of its life. *IJHR*, 1(1), 157–173.
  - Wieber, P.-B. (2006). Trajectory free linear model predictive control for stable walking. *IEEE-RAS Humanoids*, pp. 137–142.
- **Runnable Code Block Architecture**:
  - Python class `ZMPPreviewController` that implements the discrete-time state-space system ($\mathbf{A}_d, \mathbf{B}_d, \mathbf{C}_d$), solves DARE via `scipy.linalg.solve_discrete_are`, computes preview feedforward gains $f_1 \dots f_N$, and generates a smooth CoM trajectory tracking 10 staggered footsteps.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "Under what physical condition does the Zero-Moment Point (ZMP) fail to remain identical to the Center of Pressure (COP)?" -> Options: [A: When walking on flat level terrain, B: When contact surfaces are non-coplanar or the robot interacts with walls/handrails, C: When CoM height is constant, D: When the robot walks at speeds below 0.5 m/s] -> Correct: 1.
  - `q2`: "In the Kajita preview control formulation, why is the input variable chosen as CoM jerk (triple derivative) rather than acceleration?" -> Options: [A: Jerk input ensures continuous acceleration and eliminates instantaneous torque spikes at actuator gearboxes, B: DARE cannot be solved for second-order systems, C: Jerk directly scales motor voltage without back-EMF, D: Humanoid robots have infinite velocity limits] -> Correct: 0.

---

### Chapter 6-3: Divergent Component of Motion (DCM) & Capture Point Step Planning
- **Target File**: `ai-book-docs/module6-bipedal-locomotion/6-3-capture-point-and-dcm.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 3
  title: Divergent Component of Motion (DCM) & Capture Point Step Planning
  description: Instantaneous Capture Point, DCM first-order dynamics, push recovery tri-strategy, and N-step capturability analysis.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *Modal Decomposition of LIPM*: Splitting second-order unstable inverted pendulum dynamics into convergent and divergent first-order modes.
  2. *Instantaneous Capture Point (ICP) & DCM*: Definition of $\boldsymbol{\xi}$; physical meaning as the point where the biped must place its foot to arrest CoM motion.
  3. *Push Recovery Tri-Strategy*: Ankle strategy (COP modulation within foot boundaries for small impulses), Hip strategy (angular momentum injection $\dot{\mathbf{L}}$ for moderate impulses), Stepping strategy (footstep replanning for large impulses).
  4. *Analytical DCM Trajectories*: Backward recursion for footstep sequences, exponential divergence properties, boundary conditions.
  5. *N-Step Capturability (Koolen et al. 2012)*: Viability kernels, 1-step, 2-step, and N-step reachable footstep regions under kinematic joint limits.
- **Graduate-Level Mathematical Formulations**:
  - *DCM State Decomposition*:
    $$\boldsymbol{\xi} = \mathbf{x} + \frac{\dot{\mathbf{x}}}{\omega_0}, \quad \boldsymbol{\eta} = \mathbf{x} - \frac{\dot{\mathbf{x}}}{\omega_0}, \quad \omega_0 = \sqrt{\frac{g}{z_c}}$$
  - *Decoupled Mode Dynamics*:
    $$\dot{\boldsymbol{\xi}} = \omega_0 (\boldsymbol{\xi} - \mathbf{p}), \quad \dot{\boldsymbol{\eta}} = -\omega_0 (\boldsymbol{\eta} - \mathbf{p})$$
  - *Step-Adjustment Push Recovery Law*:
    Given a lateral push at time $t_0$, the updated step placement $\mathbf{p}_{step}$ required to achieve desired end-of-step DCM $\boldsymbol{\xi}_{eos}^{ref}$ is:
    $$\mathbf{p}_{step} = \frac{\boldsymbol{\xi}(t_0) - e^{-\omega_0 (T - t_0)} \boldsymbol{\xi}_{eos}^{ref}}{1 - e^{-\omega_0 (T - t_0)}}$$
  - *N-Step Capturability Region*:
    $$\mathcal{C}_{(1)} = \{ (\mathbf{x}, \dot{\mathbf{x}}) \mid \boldsymbol{\xi}(\mathbf{x}, \dot{\mathbf{x}}) \in \mathcal{S}_{foot} \}$$
- **Hardware Profile**:
  - Boston Dynamics Atlas (IHMC DRC Controller): Captured 100+ pushes during DARPA trials using real-time DCM footstep replanning at 1 kHz.
  - Agility Digit: In-field push recovery utilizing DCM stepping to traverse gravel and unexpected step drops.
- **Seminal Research Citations**:
  - Pratt, J., et al. (2006). Capture point: A step towards translating human-like bipedal locomotion to humanoid robots. *IEEE-RAS Humanoids*, pp. 200–207.
  - Koolen, T., et al. (2012). Capturability-based analysis and walking control. *IJRR*, 31(9), 1094–1113.
  - Englsberger, J., et al. (2015). Three-dimensional bipedal walking control based on Divergent Component of Motion. *IEEE Trans. Robotics*, 31(2), 355–368.
- **Runnable Code Block Architecture**:
  - Python reactive footstep simulator that introduces a sudden lateral force perturbation (200 N for 0.1 s), monitors DCM divergence outside the current support foot, computes an emergency lateral cross-over recovery step $\mathbf{p}_{step}$, and stabilizes the robot within 2 strides.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "What is the physical interpretation of the Divergent Component of Motion (DCM) / Instantaneous Capture Point (ICP)?" -> Options: [A: The geometric center of mass of the pelvis, B: The point on the ground where the robot must step to bring its horizontal CoM velocity to zero, C: The instantaneous center of rotation of the knee joint, D: The center of pressure under the stance heel] -> Correct: 1.
  - `q2`: "How does the time constant $\tau = 1/\omega_0$ of the DCM dynamics change if the robot squats lower (decreasing CoM height $z_c$)?" -> Options: [A: $\tau$ increases, slowing down divergence, B: $\tau$ decreases, causing the system to diverge more rapidly, C: $\tau$ remains invariant to height changes, D: $\tau$ becomes negative] -> Correct: 1.

---

### Chapter 6-4: Model Predictive Control for Legged Locomotion
- **Target File**: `ai-book-docs/module6-bipedal-locomotion/6-4-model-predictive-control.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 4
  title: Model Predictive Control for Legged Locomotion
  description: Single Rigid Body Dynamics (SRBD), convex MPC, contact scheduling, friction cone linearization, and real-time QP solvers.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *Receding Horizon Optimal Control*: Formulation of the dynamic trajectory tracking problem over a finite horizon $N_h \approx 10-20$ steps ($T_h \sim 0.5-1.0$ s).
  2. *Single Rigid Body Dynamics (SRBD)*: Lumping humanoid mass into a single 3D rigid body with composite rotational inertia $\mathbf{I}_G$, actuated by external contact forces.
  3. *Convexification of Angular Dynamics*: Small-angle roll/pitch approximations linearizing rotational dynamics to formulate a strictly Convex Quadratic Program (QP).
  4. *Contact Scheduling & Friction Cones*: Hybrid contact schedules (binary contact vectors), linearizing 3D Coulomb friction cones into 4-sided polyhedral pyramids.
  5. *Real-Time Solvers & Warm-Starting*: Operator Splitting Quadratic Program (OSQP) and qpOASES executing at 250–500 Hz on embedded compute.
- **Graduate-Level Mathematical Formulations**:
  - *SRBD State Equations*:
    $$\dot{\mathbf{p}} = \mathbf{v}, \quad \dot{\mathbf{v}} = \frac{1}{m}\sum_{i=1}^{N_c} \mathbf{f}_i - \mathbf{g}, \quad \dot{\boldsymbol{\Theta}} \approx \boldsymbol{\omega}, \quad \mathbf{I}_G \dot{\boldsymbol{\omega}} \approx \sum_{i=1}^{N_c} (\mathbf{r}_i - \mathbf{p}) \times \mathbf{f}_i$$
  - *State-Space Representation*:
    $$\mathbf{x} = [\boldsymbol{\Theta}^T, \mathbf{p}^T, \boldsymbol{\omega}^T, \mathbf{v}^T, g]^T \in \mathbb{R}^{13}, \quad \mathbf{u} = [\mathbf{f}_1^T, \dots, \mathbf{f}_{N_c}^T]^T \in \mathbb{R}^{3N_c}$$
    $$\dot{\mathbf{x}}(t) = \mathbf{A}_c \mathbf{x}(t) + \mathbf{B}_c(t) \mathbf{u}(t)$$
  - *Condensed QP Formulation*:
    $$\min_{\mathbf{U}} \frac{1}{2}\mathbf{U}^T \mathbf{H} \mathbf{U} + \mathbf{g}^T \mathbf{U} \quad \text{s.t.} \quad \mathbf{C} \mathbf{U} \le \mathbf{d}$$
    where friction pyramid constraints enforce: $|f_{i, x}| \le \mu f_{i, z}$, $|f_{i, y}| \le \mu f_{i, z}$, $f_{min} \le f_{i, z} \le f_{max}$.
- **Hardware Profile**:
  - MIT Cheetah 3 & Mini Cheetah: Groundbreaking deployment of Convex MPC running at 50–250 Hz on Intel Core i7.
  - Unitree H1: Dual onboard Jetson Orin / x86 compute executing Convex MPC with 12-horizon steps solved in $< 3$ ms.
- **Seminal Research Citations**:
  - Di Carlo, J., et al. (2018). Dynamic Locomotion in the MIT Cheetah 3 Through Convex Model-Predictive Control. *IROS 2018*, pp. 1–9.
  - Grandia, R., et al. (2019). Feedback MPC for torque-controlled legged robots. *IROS 2019*, pp. 4730–4737.
  - Bledt, G., et al. (2018). Regularized Predictive Control to Close the Gap Between Simplified and Full-Body Models. *ICRA 2018*, pp. 2641–2648.
- **Runnable Code Block Architecture**:
  - Python Convex MPC solver using `osqp`: sets up sparse dynamics matrices $\mathbf{A}_d, \mathbf{B}_d$, builds the QP cost matrix $\mathbf{H} = 2(\mathbf{B}_{qp}^T \mathbf{Q} \mathbf{B}_{qp} + \mathbf{R})$, applies contact schedule for bipedal walking, solves for optimal ground reaction forces at 250 Hz, and verifies friction cone compliance.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "Why does the Single Rigid Body Dynamics (SRBD) assumption enable convex QP formulation in legged locomotion?" -> Options: [A: It assumes joint angles and leg link inertias are negligible compared to base torso inertia, linearizing force-moment mappings, B: It models all joints as hydraulic dampers, C: It ignores gravity completely, D: It restricts the robot to planar motions] -> Correct: 0.
  - `q2`: "In convex MPC with linearized friction cones, what is the geometric shape of the admissible contact force region for each foot?" -> Options: [A: A sphere, B: A 4-sided inverted pyramid in force space, C: A cylinder along the z-axis, D: A single line] -> Correct: 1.

---

### Chapter 6-5: Hierarchical Whole-Body Control & Operational Space Formulations
- **Target File**: `ai-book-docs/module6-bipedal-locomotion/6-5-whole-body-control.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 5
  title: Hierarchical Whole-Body Control & Operational Space Formulations
  description: Operational space dynamics, null-space projections, strict hierarchy QP formulations, and torque-level control.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *Operational Space Framework*: Decoupling task coordinates, dynamically consistent generalized inverse $\mathbf{J}^{\#} = \mathbf{A}^{-1}\mathbf{J}^T(\mathbf{J}\mathbf{A}^{-1}\mathbf{J}^T)^{-1}$.
  2. *Strict Priority Hierarchy & Null-Space Projections*: Task 1 (Stance foot contact & balance) > Task 2 (Pelvis height & orientation) > Task 3 (Swing foot trajectory) > Task 4 (Posture regularization).
  3. *Null-Space Projector Algebra*: $\mathbf{N}_1 = \mathbf{I} - \mathbf{J}_1^\dagger \mathbf{J}_1$; guaranteeing lower-priority tasks do not perturb higher-priority task accelerations.
  4. *QP-Based Whole-Body Control*: Formulating decision variables $\mathbf{x} = [\ddot{\mathbf{q}}^T, \boldsymbol{\tau}^T, \boldsymbol{\lambda}^T]^T$; unifying equations of motion, torque limits, contact constraints, and friction cones into a 1 kHz QP.
  5. *Singularity & Actuator Saturation Handling*: Damped least squares, torque saturation fallback hierarchies.
- **Graduate-Level Mathematical Formulations**:
  - *Full Floating-Base Equation of Motion Constraint*:
    $$\mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{h}(\mathbf{q}, \dot{\mathbf{q}}) = \mathbf{S}^T \boldsymbol{\tau} + \mathbf{J}_c^T(\mathbf{q})\boldsymbol{\lambda}$$
  - *Rigid Stance Foot Acceleration Constraint*:
    $$\mathbf{J}_c(\mathbf{q})\ddot{\mathbf{q}} + \dot{\mathbf{J}}_c(\mathbf{q})\dot{\mathbf{q}} = \mathbf{0}$$
  - *Hierarchical QP Cost*:
    $$\min_{\ddot{\mathbf{q}}, \boldsymbol{\tau}, \boldsymbol{\lambda}} \sum_{k=1}^K w_k \|\mathbf{J}_k \ddot{\mathbf{q}} + \dot{\mathbf{J}}_k \dot{\mathbf{q}} - \ddot{\mathbf{x}}_k^{des}\|^2 + w_\tau \|\boldsymbol{\tau}\|^2 + w_\lambda \|\boldsymbol{\lambda}\|^2$$
    $$\text{s.t.} \quad \boldsymbol{\tau}_{min} \le \boldsymbol{\tau} \le \boldsymbol{\tau}_{max}, \quad \underline{\mathbf{F}}_c \le \mathbf{C}_c \boldsymbol{\lambda} \le \overline{\mathbf{F}}_c$$
- **Hardware Profile**:
  - PAL Robotics TALOS: 32 DOFs, high-torque strain-wave gears, running 1 kHz TSID (Task Space Inverse Dynamics) based on Pinocchio.
  - Boston Dynamics Atlas (hydraulic): Multi-objective operational space controller prioritizing balance over manipulation tracking.
- **Seminal Research Citations**:
  - Sentis, L., & Khatib, O. (2005). Synthesis of whole-body behaviors through hierarchical control of behavioral primitives. *IJRR*, 24(9), 705–718.
  - Herzog, A., et al. (2016). Momentum control with hierarchical inverse dynamics on a torque-controlled humanoid. *Autonomous Robots*, 40(3), 473–491.
  - Del Prete, A., et al. (2016). Prioritized motion-force control of constrained fully-actuated and underactuated robots. *IEEE Trans. Robotics*, 32(5), 1139–1152.
- **Runnable Code Block Architecture**:
  - Complete Python script using `pinocchio` and `scipy.optimize.linprog`/`osqp` loading a floating-base humanoid model, computing inertia matrix $\mathbf{M}(\mathbf{q})$ and non-linear effects $\mathbf{h}(\mathbf{q}, \dot{\mathbf{q}})$, defining contact and swing foot Jacobians, and solving the 1 kHz WBC QP for balanced dual-stance standing.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "In hierarchical null-space projection control, what mathematical property ensures that task 2 cannot create any acceleration in task 1 coordinates?" -> Options: [A: $\mathbf{J}_1 \mathbf{N}_1 = \mathbf{0}$, B: $\mathbf{J}_1^T \mathbf{N}_1 = \mathbf{I}$, C: $\det(\mathbf{N}_1) = 1$, D: $\mathbf{N}_1 = \mathbf{N}_1^T = -\mathbf{I}$] -> Correct: 0.
  - `q2`: "Why are contact forces $\boldsymbol{\lambda}$ and joint torques $\boldsymbol{\tau}$ included alongside joint accelerations $\ddot{\mathbf{q}}$ as direct decision variables in modern WBC QPs?" -> Options: [A: To eliminate the floating base, B: To enforce actuator torque limits and friction cone inequality constraints directly in the optimization, C: Because the robot does not have joint encoders, D: To bypass the equations of motion] -> Correct: 1.

---

### Chapter 6-6: Deep Reinforcement Learning for Humanoid Locomotion
- **Target File**: `ai-book-docs/module6-bipedal-locomotion/6-6-reinforcement-learning-locomotion.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 6
  title: Deep Reinforcement Learning for Humanoid Locomotion
  description: MDP design, reward shaping, PPO, massively parallel Isaac Lab simulation, and terrain curricula.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *Locomotion as a Markov Decision Process (MDP)*: State observation vector $\mathbf{s}_t \in \mathbb{R}^{d_o}$ (base velocities, projected gravity, joint positions, velocities, past actions), Action vector $\mathbf{a}_t \in \mathbb{R}^{d_a}$ (target PD joint offsets $\mathbf{q}_{target} = \mathbf{q}_{default} + k_a \mathbf{a}_t$).
  2. *Reward Function Engineering Taxonomy*: Positive rewards (linear velocity tracking, heading alignment) vs Regularization penalties (torque magnitude $\|\boldsymbol{\tau}\|^2$, joint acceleration, action rate of change $\|\mathbf{a}_t - \mathbf{a}_{t-1}\|^2$, foot slip, roll/pitch deviation).
  3. *Proximal Policy Optimization (PPO)*: Clipped surrogate objective, Generalized Advantage Estimation (GAE), entropy bonus for exploration.
  4. *Massively Parallel GPU Simulation*: NVIDIA Isaac Lab / `legged_gym` running 4,096+ parallel humanoid agents in PyTorch tensors at $> 100,000$ FPS.
  5. *Terrain Curriculum Scheduling*: Dynamic difficulty adjustment (flat ground $\to$ rough slope $\to$ discrete stairs) based on survival distance.
- **Graduate-Level Mathematical Formulations**:
  - *PPO Clipped Objective*:
    $$L^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\right) \right], \quad r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{old}}(a_t \mid s_t)}$$
  - *Generalized Advantage Estimation (GAE)*:
    $$\hat{A}_t = \sum_{l=0}^\infty (\gamma \lambda)^l \delta_{t+l}^V, \quad \delta_t^V = r_t + \gamma V_\phi(s_{t+1}) - V_\phi(s_t)$$
  - *Complete Humanoid Reward Function*:
    $$R_t = w_{v} \exp\left(-\frac{\|\mathbf{v}_{xy} - \mathbf{v}_{xy}^{cmd}\|^2}{\sigma_v^2}\right) + w_{\omega} \exp\left(-\frac{(\omega_z - \omega_z^{cmd})^2}{\sigma_\omega^2}\right) - w_\tau \|\boldsymbol{\tau}\|^2 - w_{slip} \|\mathbf{v}_{foot, xy}^{contact}\|^2 - w_{\ddot{q}} \|\ddot{\mathbf{q}}\|^2$$
- **Hardware Profile**:
  - Unitree G1: Trained end-to-end in Isaac Gym in under 30 minutes on a single NVIDIA RTX 4090 GPU, achieving stable walking and jogging.
  - Boston Dynamics Electric Atlas: Learning-based controller modules trained with parallel reinforcement learning pipelines.
- **Seminal Research Citations**:
  - Schulman, J., et al. (2017). Proximal Policy Optimization Algorithms. *arXiv:1707.06347*.
  - Rudin, N., et al. (2022). Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning. *Science Robotics*, 7(68), eabk2822.
  - Miki, T., et al. (2022). Learning robust perceptive locomotion for quadrupedal robots in the wild. *Science Robotics*, 7(62), eabk2822.
- **Runnable Code Block Architecture**:
  - PyTorch implementation of the complete PPO actor-critic architecture for humanoids: Actor MLP ($256 \times 256 \times 128$) outputting Gaussian mean joint offsets, Critic MLP predicting state value, vectorized GAE computation, and clipped gradient descent update step.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "In deep RL for humanoid locomotion, why are policy actions almost universally framed as target PD joint positions rather than raw motor torques?" -> Options: [A: Raw torque actions suffer from extreme high-frequency exploration jitter that can destroy physical hardware and destabilize learning, B: Neural networks cannot output negative numbers, C: PD controllers eliminate the need for an actor network, D: Isaac Gym does not support torque control] -> Correct: 0.
  - `q2`: "What is the primary role of the Generalized Advantage Estimation (GAE) hyperparameter $\lambda \in [0, 1]$?" -> Options: [A: It controls the discount factor of future rewards, B: It trades off bias vs variance in the advantage function estimate, C: It scales the entropy bonus, D: It clips the policy gradient] -> Correct: 1.

---

### Chapter 6-7: Sim-to-Real Transfer for Locomotion: Domain Randomization to RMA
- **Target File**: `ai-book-docs/module6-bipedal-locomotion/6-7-sim-to-real-locomotion.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 7
  title: Sim-to-Real Transfer for Locomotion: Domain Randomization to RMA
  description: Reality gap, actuator dynamics modeling, domain randomization, teacher-student distillation, and Rapid Motor Adaptation.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *Deconstructing the Locomotion Reality Gap*: Actuator delay ($10-30$ ms), gearbox compliance and friction, ground softness, battery sag, and unmodeled link flexures.
  2. *Actuator Modeling (Actuator Net)*: Replacing idealized rigid actuators with learned multi-layer perceptron or second-order dyno-fitted transfer functions.
  3. *Domain Randomization (DR) Protocols*: Randomizing masses ($\pm 15\%$), CoM offsets ($\pm 3$ cm), friction $\mu \in [0.2, 1.2]$, motor damping, and communication latency.
  4. *Rapid Motor Adaptation (RMA, Kumar et al. 2021)*:
     - Phase 1: Privileged Teacher $\pi(a_t \mid s_t, e_t)$ conditioned on ground-truth environmental parameters $e_t$.
     - Phase 2: Student Adaptation Network $\phi(z_t \mid s_{t-H:t})$ estimating latent vector $\hat{z}_t$ strictly from proprioceptive history.
  5. *Deployment Architecture*: Exporting trained policies via ONNX Runtime / TensorRT C++ running at 50 Hz, interacting with real-time 1 kHz joint PD loops over CAN-FD.
- **Graduate-Level Mathematical Formulations**:
  - *Actuator Dynamics with Latency*:
    $$\ddot{\tau}_{act} + 2\zeta \omega_n \dot{\tau}_{act} + \omega_n^2 \tau_{act} = \omega_n^2 \tau_{des}(t - \tau_d)$$
  - *Teacher Privileged Encoder*:
    $$\mathbf{z}_t = \mu_{priv}(\mathbf{e}_t), \quad \mathbf{e}_t = [\mu, m_{payload}, \mathbf{p}_{com\_err}, k_p^{scale}, k_d^{scale}]^T \in \mathbb{R}^K$$
  - *Student Temporal Convolutional Adaptation Loss*:
    $$\mathcal{L}_{RMA}(\psi) = \frac{1}{B}\sum_{i=1}^B \|\phi_\psi(\mathbf{s}_{t-H:t}^{(i)}) - \mathbf{z}_t^{(i)}\|^2$$
    where $H \approx 50$ is the history horizon (1.0 second at 50 Hz).
- **Hardware Profile**:
  - Unitree G1: RMA student policy running on onboard Jetson Orin Nano ($< 2$ ms inference per step), walking across foam, slippery plastic, and outdoor asphalt without manual parameter tuning.
- **Seminal Research Citations**:
  - Kumar, A., et al. (2021). RMA: Rapid Motor Adaptation for bipedal locomotion. *Robotics: Science and Systems (RSS)*.
  - Hwangbo, J., et al. (2019). Learning agile robotic locomotion on complex terrain. *Science Robotics*, 4(26), eaau5872.
  - Siekmann, J., et al. (2021). Blind bipedal stair traversal via sim-to-real reinforcement learning. *Robotics: Science and Systems*.
- **Runnable Code Block Architecture**:
  - Complete PyTorch script implementing the RMA Student Adaptation 1D-CNN temporal architecture: takes input tensor `(batch_size, 50, 45)` representing 50 steps of proprioception, passes through 3 layers of 1D convolutions with ReLU, outputs estimated 8D latent vector $\hat{\mathbf{z}}_t$, and benchmarks CPU/GPU inference latency.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "In Rapid Motor Adaptation (RMA), why is privileged environmental information (such as ground friction and payload mass) given only to the Teacher network and not the Student?" -> Options: [A: The privileged information cannot be physically measured by onboard proprioceptive sensors on a real robot in real time, B: The student network does not have enough parameters, C: Friction sensors are too expensive, D: Privileged information destabilizes PPO] -> Correct: 0.
  - `q2`: "What type of neural network layer is most commonly used in the RMA Student adaptation module to process historical sensor streams?" -> Options: [A: 2D Spatial Convolutions, B: 1D Temporal Convolutions or causal self-attention, C: Graph Neural Networks, D: Single-layer linear perceptrons without activation] -> Correct: 1.

---

### Chapter 6-8: Advanced Locomotion: Running, Jumping, Stairs & Neural Parkour
- **Target File**: `ai-book-docs/module6-bipedal-locomotion/6-8-advanced-locomotion-skills.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 8
  title: Advanced Locomotion: Running, Jumping, Stairs & Neural Parkour
  description: Spring-Loaded Inverted Pendulum (SLIP), ballistic flight dynamics, elevation costmaps, and neural parkour policies.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *The Biomechanics of Running*: Aerial flight phases where $\sum \mathbf{f}_c = \mathbf{0}$, ballistic parabolas, touchdown impact attenuation.
  2. *Spring-Loaded Inverted Pendulum (SLIP)*: Compliant leg kinematics, energy storage and return in mechanical springs, apex-to-apex return maps.
  3. *Ballistic Jumping Trajectory Generation*: Three-phase jumping: compression/crouch $\to$ explosive impulse thrust (torque saturation) $\to$ ballistic flight $\to$ compliant touchdown landing.
  4. *Stair & Obstacle Traversal*: 2.5D elevation grid maps from depth cameras/LiDAR, footstep clearance heuristics, swing foot collision avoidance.
  5. *Neural Parkour (Hoeller et al. 2024)*: Vision-conditioned RL policies enabling dynamic vaulting, obstacle leaps, and high-speed gap crossing.
- **Graduate-Level Mathematical Formulations**:
  - *SLIP Stance Dynamics*:
    $$m \ddot{r} = m r \dot{\theta}^2 - k(r - r_0) - m g \cos\theta, \quad m r^2 \ddot{\theta} = -2 m r \dot{r} \dot{\theta} + m g r \sin\theta$$
  - *Flight Phase Ballistic Dynamics*:
    $$\ddot{\mathbf{p}} = -\mathbf{g} \implies \mathbf{p}(t) = \mathbf{p}_{to} + \dot{\mathbf{p}}_{to} t - \frac{1}{2}\mathbf{g} t^2$$
  - *Optimal Takeoff Velocity for Target Gap Clearance ($d, \Delta h$)*:
    $$v_{takeoff} = \sqrt{\frac{g d^2}{2 \cos^2 \alpha (d \tan \alpha - \Delta h)}}$$
- **Hardware Profile**:
  - Boston Dynamics Electric Atlas: Acrobatic backflips, 180-degree turn vaults, and running parkour over elevated platforms.
  - Unitree G1: 0.6 m vertical jump and 1.2 m gap jump with peak knee torque output exceeding 120 N·m.
- **Seminal Research Citations**:
  - Blickhan, R. (1989). The spring-mass model for running and hopping. *Journal of Biomechanics*, 22(11-12), 1217–1227.
  - Hoeller, D., et al. (2024). Neural Parkour for Legged Robots. *Science Robotics*, 9(88), eadi7366.
  - Chignoli, M., et al. (2021). The MIT Humanoid Robot: Design, Motion Planning, and Control For Acrobatic Behaviors. *ICRA 2021*, pp. 602–608.
- **Runnable Code Block Architecture**:
  - Python numerical simulation of a SLIP running model using `scipy.integrate.solve_ivp`: computes transition between stance ODE and ballistic flight ODE, locates apex height via event roots, and verifies periodic limit cycle stability across 10 continuous strides.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "In running and jumping gaits, what fundamental dynamic condition distinguishes the flight phase from the stance phase?" -> Options: [A: In the flight phase, the sum of all external contact forces is identically zero and the CoM accelerates strictly under gravity, B: The robot motors are turned off, C: Joint velocities drop to zero, D: Kinetic energy equals potential energy] -> Correct: 0.
  - `q2`: "What is the primary role of the leg spring stiffness $k$ in the Spring-Loaded Inverted Pendulum (SLIP) model?" -> Options: [A: It limits the robot maximum speed to 1 m/s, B: It temporarily stores kinetic energy during touchdown and returns it during push-off for dynamic self-stabilization, C: It eliminates all angular momentum, D: It removes the need for flight phases] -> Correct: 1.

---

### Chapter 6-9: Gait Analysis, Ground Reaction Forces & Biomechanics
- **Target File**: `ai-book-docs/module6-bipedal-locomotion/6-9-gait-analysis-and-biomechanics.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 9
  title: Gait Analysis, Ground Reaction Forces & Biomechanics
  description: Human gait cycle, ground reaction forces, specific Cost of Transport, and comparative biomechanics.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *The Human Gait Cycle Taxonomy*: 60% Stance (Heel Strike, Loading Response, Midstance, Terminal Stance, Preswing) vs 40% Swing (Initial Swing, Midswing, Terminal Swing).
  2. *Ground Reaction Force (GRF) Dynamics*: Vertical GRF double-peak ("M-shape") profile (1.2 bodyweight at loading and push-off, 0.8 at midstance); anterior-posterior braking/propulsive forces.
  3. *Energetics & Dimensionless Cost of Transport (COT)*: Mechanical COT vs Electrical COT; benchmark comparisons (Human: ~0.08, Cornell Passive Biped: ~0.04, ASIMO: ~1.6, Unitree G1: ~0.5).
  4. *Dynamic Similarity & Froude Number*: Scaling principles across leg lengths and velocities ($Fr = v^2 / (g L_{leg})$); walk-to-run transition at $Fr \approx 0.5$.
  5. *Biomechanics Instrumentation*: Multi-axis force plates, instrumented split-belt treadmills, electromyography (EMG).
- **Graduate-Level Mathematical Formulations**:
  - *Specific Cost of Transport (COT)*:
    $$COT = \frac{E_{total}}{m g d} = \frac{\int_0^T \sum_{i=1}^n \left( |\tau_i(t) \dot{q}_i(t)| + I_i(t)^2 R_i \right) dt}{m g d}$$
  - *Froude Number*:
    $$Fr = \frac{v^2}{g L_{leg}}$$
  - *Gait Symmetry Index (SI)*:
    $$SI = \frac{2 |X_{left} - X_{right}|}{X_{left} + X_{right}} \times 100\%$$
- **Hardware Profile**:
  - Bertec / Kistler 6-axis force plates: measuring 3D ground reaction forces ($F_x, F_y, F_z$) and moments ($M_x, M_y, M_z$) at 1000 Hz.
  - Comparative analysis: Honda ASIMO vs Collins Passive Dynamic Walker vs Boston Dynamics Atlas.
- **Seminal Research Citations**:
  - Winter, D. A. (2009). *Biomechanics and Motor Control of Human Movement* (4th ed.). John Wiley & Sons.
  - Collins, S., et al. (2005). Efficient bipedal robots based on passive-dynamic walkers. *Science*, 307(5712), 1082–1085.
  - Kuo, A. D. (2007). The six determinants of gait and the inverted pendulum analogy. *Human Movement Science*, 26(4), 617–656.
- **Runnable Code Block Architecture**:
  - Python biomechanics processor: parses synthetic 6-axis force plate logs, detects gait events (heel-strike, toe-off), computes vertical and AP ground reaction force butterfly curves, and calculates dimensionless Cost of Transport across 10 strides.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "Why does the vertical ground reaction force (vGRF) exhibit a characteristic double-peak ('M-shape') during normal human walking?" -> Options: [A: The first peak corresponds to initial weight acceptance/braking, while the second corresponds to active ankle push-off propulsion, B: The knees lock twice per stride, C: The arms swing asynchronously, D: The force plate experiences sensor ringing] -> Correct: 0.
  - `q2`: "At approximately what Froude number ($Fr = v^2 / (g L_{leg})$) do bipeds naturally transition from a walking gait to a running gait?" -> Options: [A: $Fr \approx 0.05$, B: $Fr \approx 0.5$, C: $Fr \approx 5.0$, D: $Fr \approx 10.0$] -> Correct: 1.

---

### Chapter 6-10: Motion Capture Retargeting & Adversarial Motion Priors (AMP)
- **Target File**: `ai-book-docs/module6-bipedal-locomotion/6-10-motion-capture-and-reference.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 10
  title: Motion Capture Retargeting & Adversarial Motion Priors (AMP)
  description: MoCap marker setups, AMASS dataset, kinematic retargeting to humanoid URDFs, and AMP reinforcement learning.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *Optical Motion Capture Setup*: Retroreflective marker sets (Plug-in Gait), Vicon/OptiTrack IR strobe cameras, coordinate frames, and occlusion solving.
  2. *The AMASS Motion Dataset*: Architecture of the Archive of Motion Capture as Surface Shapes (SMPL parametric bodies, 40+ datasets unified).
  3. *Kinematic Retargeting Optimization*: Non-linear optimization mapping 3D human skeletal keypoints into humanoid robot joint configurations while respecting joint limits and self-collisions.
  4. *Adversarial Motion Priors (AMP, Peng et al. 2021)*: Discriminator $D(\mathbf{s}, \mathbf{s}')$ trained to distinguish robot transitions from human motion clips; providing style rewards without manual reward engineering.
  5. *Task-AMP Co-Optimization*: Balancing task success (target velocity, obstacle navigation) with natural human motion style.
- **Graduate-Level Mathematical Formulations**:
  - *Retargeting Optimization Problem*:
    $$\min_{\mathbf{q}} \sum_{j \in \mathcal{J}} w_j \|\mathbf{p}_j^{human} - \mathbf{FK}_j(\mathbf{q})\|^2 + w_{reg} \|\mathbf{q} - \mathbf{q}_{nom}\|^2 \quad \text{s.t.} \quad \mathbf{q}_{min} \le \mathbf{q} \le \mathbf{q}_{max}$$
  - *AMP Discriminator Objective (Least-Squares GAN with Gradient Penalty)*:
    $$\min_D \mathbb{E}_{\mathbf{d} \sim \mathcal{M}} \left[(D(\mathbf{d}) - 1)^2\right] + \mathbb{E}_{\mathbf{s} \sim \pi} \left[(D(\mathbf{s}) + 1)^2\right] + \frac{\gamma_{gp}}{2}\mathbb{E}_{\mathbf{d} \sim \mathcal{M}}\left[\|\nabla_\mathbf{d} D(\mathbf{d})\|^2\right]$$
  - *AMP Policy Style Reward*:
    $$r_t^G = \max\left(0, 1 - 0.25 (D(\mathbf{s}_t, \mathbf{s}_{t+1}) - 1)^2\right)$$
- **Hardware Profile**:
  - OptiTrack PrimeX 41 cameras (4.1 MP @ 250 FPS) and Vicon Vantage systems.
  - Unitree H1: Deployed with AMP policies mimicking human martial arts, athletic running, and expressive hand gestures.
- **Seminal Research Citations**:
  - Peng, X. B., et al. (2021). AMP: Adversarial Motion Priors for Stylized Physics-Based Character Animation. *ACM Trans. Graph. (SIGGRAPH)*, 40(4), 1–20.
  - Mahmood, N., et al. (2019). AMASS: Archive of Motion Capture as Surface Shapes. *ICCV 2019*, pp. 5442–5451.
  - Escontrela, A., et al. (2022). Adversarial motion priors make good substitutes for complex reward functions. *IROS 2022*, pp. 25–32.
- **Runnable Code Block Architecture**:
  - Python script using `scipy.optimize` and `pinocchio` that parses a sequence of 3D human skeletal joint positions, solves frame-by-frame inverse kinematics optimization for a humanoid URDF, enforces joint limits, and outputs retargeted joint angle trajectories.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "What is the primary advantage of Adversarial Motion Priors (AMP) over traditional tracking-based reference reward functions (e.g., DeepMimic)?" -> Options: [A: AMP requires zero motion capture data, B: AMP does not require phase-matched time synchronization between the robot and reference clips, allowing the robot to dynamically adapt its timing to terrain obstacles, C: AMP eliminates the policy network, D: AMP only works on quadrupeds] -> Correct: 1.
  - `q2`: "Why is a gradient penalty included in the AMP discriminator training objective?" -> Options: [A: To increase discriminator learning rate, B: To prevent discriminator gradients from exploding or collapsing, ensuring smooth and informative style rewards for the policy, C: To enforce contact constraints, D: To quantize neural weights to 8 bits] -> Correct: 1.

---

## 4. Module 7 Execution Specifications: Dexterous Manipulation & Hand Design
**Module Path**: `ai-book-docs/module7-dexterous-manipulation/`  
**Category Configuration** (`_category_.json`):
```json
{
  "label": "Dexterous Manipulation & Hand Design",
  "position": 7
}
```

---

### Chapter 7-1: Foundations of Dexterous Manipulation & Hand Kinematics
- **Target File**: `ai-book-docs/module7-dexterous-manipulation/7-1-introduction-to-dexterous-manipulation.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 1
  title: Foundations of Dexterous Manipulation & Hand Kinematics
  description: Prehensile vs non-prehensile grasping, human hand anatomy, finger kinematics, and manipulability ellipsoids.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *Taxonomy of Manipulation*: Prehensile (power, precision) vs Non-prehensile (pushing, pivoting, dynamic catching, sliding).
  2. *Human Hand Anatomy*: 27 bones, 34 muscles (intrinsic vs extrinsic), 21 DOFs; the bio-mechanical uniqueness of the opposable thumb (trapeziometacarpal joint).
  3. *Robot Hand Design Spectrum*: Parallel-jaw grippers (Robotiq 2F-85) $\to$ underactuated hands (Barrett Hand) $\to$ fully actuated anthropomorphic hands (Wonik Allegro, Shadow Hand, Tesla Optimus Gen 2 Hand).
  4. *Multi-Finger Kinematic Trees*: Palm base frame $\mathcal{F}_{palm}$, branched serial chains for index, middle, ring, little fingers, and opposable thumb.
  5. *Dexterous Manipulability Ellipsoids*: Yoshikawa manipulability index, fingertip velocity vs force generation capabilities across workspace.
- **Graduate-Level Mathematical Formulations**:
  - *Finger Forward Kinematics (Product of Exponentials)*:
    $$\mathbf{T}_{tip, i}(\boldsymbol{\theta}_i) = \mathbf{T}_{palm}^0 \left( \prod_{j=1}^{n_i} \exp(\hat{\boldsymbol{\xi}}_{i, j} \theta_{i, j}) \right) \mathbf{M}_i$$
  - *Multi-Fingertip Composite Jacobian*:
    $$\mathbf{v}_{tips} = \begin{bmatrix} \mathbf{v}_1 \\ \vdots \\ \mathbf{v}_k \end{bmatrix} = \mathbf{J}_h(\boldsymbol{\theta}) \dot{\boldsymbol{\theta}}, \quad \mathbf{J}_h(\boldsymbol{\theta}) = \text{block\_diag}(\mathbf{J}_1(\boldsymbol{\theta}_1), \dots, \mathbf{J}_k(\boldsymbol{\theta}_k)) \in \mathbb{R}^{3k \times n}$$
  - *Yoshikawa Manipulability Measure*:
    $$w_i = \sqrt{\det(\mathbf{J}_i(\boldsymbol{\theta}_i) \mathbf{J}_i^T(\boldsymbol{\theta}_i))} = \prod_{m=1}^3 \sigma_{i, m}$$
- **Hardware Profile**:
  - Shadow Dexterous Hand: 20 actuated DOFs, 4 underactuated DOFs, 40 antagonistic DC motor tendons in forearm, 4 kg mass.
  - Wonik Robotics Allegro Hand: 16 torque-controlled DOFs (4 fingers $\times$ 4 DOFs), 1.08 kg mass, 1.5 kg payload, 333 Hz CAN bus.
  - Tesla Optimus Gen 2 Hand: 11 DOFs, cable-driven with tactile sensor arrays integrated on all fingertips.
- **Seminal Research Citations**:
  - Cutkosky, M. R. (1989). On grasp choice, grasp models, and the design of hands for manufacturing tasks. *IEEE Trans. Robotics and Automation*, 5(3), 269–279.
  - Bicchi, A. (2000). Hands for dexterous manipulation and robust grasping: a difficult road toward simplicity. *IEEE Trans. Robotics and Automation*, 16(6), 652–662.
  - Napier, J. R. (1956). The prehensile movements of the human hand. *Journal of Bone and Joint Surgery*, 38(4), 902–913.
- **Runnable Code Block Architecture**:
  - Python forward and differential kinematics model of a 4-DOF anthropomorphic robotic finger (metacarpophalangeal abduction/adduction, MCP flexion, proximal interphalangeal PIP flexion, distal interphalangeal DIP flexion): computes spatial Jacobian $\mathbf{J}(\boldsymbol{\theta})$, performs Singular Value Decomposition (SVD), and plots 3D manipulability ellipsoid.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "What is the primary anatomical difference between prehensile and non-prehensile manipulation?" -> Options: [A: Prehensile manipulation requires grasping and securing the object within the hand kinematic chain, whereas non-prehensile manipulation manipulates the object through environmental forces without holding it, B: Non-prehensile manipulation requires 21 DOFs, C: Prehensile manipulation does not use friction, D: Non-prehensile manipulation only works on spheres] -> Correct: 0.
  - `q2`: "If a robotic fingertip operates near a kinematic singularity where $\det(\mathbf{J}\mathbf{J}^T) \to 0$, what happens to its manipulability ellipsoid?" -> Options: [A: It expands uniformly in all directions, B: It collapses along one or more axes, indicating that velocities cannot be generated along singular directions, C: It turns into a sphere, D: It rotates by 90 degrees] -> Correct: 1.

---

### Chapter 7-2: Grasp Theory: Contact Mechanics, Wrench Space & Force Closure
- **Target File**: `ai-book-docs/module7-dexterous-manipulation/7-2-grasp-theory.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 2
  title: Grasp Theory: Contact Mechanics, Wrench Space & Force Closure
  description: Contact models, Grasp Matrix, Form Closure vs Force Closure, Grasp Wrench Space, and Ferrari-Canny metric.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *Contact Mechanics Models*: Point Contact Without Friction (PCWF, 1 DOF), Hard Finger with Coulomb Friction (HF, 3 DOF: normal + 2 tangential forces), Soft Finger Contact (SF, 4 DOF: 3 forces + torsional friction moment).
  2. *The Grasp Matrix $\mathbf{G}$*: Geometric mapping from contact forces to resultant object wrench applied at object center of mass.
  3. *Form Closure vs Force Closure*: Reuleaux kinematic immobilization vs force equilibrium under friction cones; Salisbury theorem on minimal contact points.
  4. *The Grasp Wrench Space (GWS)*: Convex hull of primitive contact wrenches under unit normal force constraints.
  5. *Ferrari-Canny $\epsilon$-Metric*: Mathematical definition of grasp quality as the largest origin-centered hypersphere $\mathcal{B}_\epsilon(\mathbf{0})$ inscribed within the GWS.
- **Graduate-Level Mathematical Formulations**:
  - *Contact Wrench Mapping*:
    $$\mathbf{w}_{c, i} = \begin{bmatrix} \mathbf{f}_i \\ \mathbf{p}_i \times \mathbf{f}_i \end{bmatrix} = \mathbf{G}_i \mathbf{f}_i, \quad \mathbf{G}_i = \begin{bmatrix} \mathbf{I}_{3 \times 3} \\ [\mathbf{p}_i]_\times \end{bmatrix} \in \mathbb{R}^{6 \times 3}$$
  - *Total Object Equilibrium*:
    $$\mathbf{w}_{ext} + \sum_{i=1}^k \mathbf{G}_i \mathbf{f}_i = \mathbf{0} \implies \mathbf{w}_{ext} = -\mathbf{G} \mathbf{f}_c, \quad \mathbf{G} = [\mathbf{G}_1, \dots, \mathbf{G}_k] \in \mathbb{R}^{6 \times 3k}$$
  - *Coulomb Friction Cone & Linearized Primitive Rays*:
    $$\mathcal{F}_i = \{ \mathbf{f}_i \mid f_{i, z} \ge 0, \sqrt{f_{i, x}^2 + f_{i, y}^2} \le \mu f_{i, z} \} \approx \left\{ \sum_{j=1}^m \alpha_{i, j} \mathbf{d}_{i, j} \mid \alpha_{i, j} \ge 0 \right\}$$
  - *Ferrari-Canny $\epsilon$-Metric*:
    $$\epsilon = \max \left\{ r \ge 0 \mid \mathcal{B}_r(\mathbf{0}) \subseteq \text{ConvexHull}\left(\bigcup_{i=1}^k \{ \mathbf{G}_i \mathbf{d}_{i, j} \}_{j=1}^m \right) \right\}$$
- **Hardware Profile**:
  - Robotiq 2F-85 / 2F-140 grippers: Parallel grasp mechanics with high-friction silicone pads ($\mu \approx 0.85$).
  - Wonik Allegro Hand: Hemispherical silicone fingertips providing soft finger contact mechanics for multi-finger grasps.
- **Seminal Research Citations**:
  - Salisbury, J. K., & Roth, B. (1983). Kinematic and force analysis of articulated mechanical hands. *ASME J. Mech. Transm. Autom. Des.*, 105(1), 35–41.
  - Ferrari, C., & Canny, J. (1992). Planning optimal grasps. *ICRA 1992*, pp. 2290–2295.
  - Roa, M. A., & Suárez, R. (2015). Grasp quality measures: review and performance. *Autonomous Robots*, 38(1), 65–88.
- **Runnable Code Block Architecture**:
  - Python grasp analysis package: takes arbitrary 3D mesh contact locations and surface normals, constructs the $6 \times 3k$ Grasp Matrix $\mathbf{G}$, generates 8-sided friction cone rays, computes the 6D Grasp Wrench Space convex hull via `scipy.spatial.ConvexHull`, and calculates the exact Ferrari-Canny $\epsilon$ metric.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "What is the critical distinction between Form Closure and Force Closure in grasp theory?" -> Options: [A: Form closure completely arrests object motion purely through unilateral frictionless geometric constraints, whereas force closure relies on friction forces staying within friction cones, B: Form closure requires rubber pads, C: Force closure requires an infinite number of fingers, D: Form closure only applies to soft deformable objects] -> Correct: 0.
  - `q2`: "What physical quantity does the Ferrari-Canny $\epsilon$-metric represent?" -> Options: [A: The electric current consumed by the hand, B: The magnitude of the worst-case external disturbance wrench that the grasp can resist in any 6D direction without slipping, C: The total mass of the object, D: The distance between fingertips] -> Correct: 1.

---

### Chapter 7-3: Robotic Hand Design: Underactuation, Tendons & Actuator Sizing
- **Target File**: `ai-book-docs/module7-dexterous-manipulation/7-3-robotic-hand-design.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 3
  title: Robotic Hand Design: Underactuation, Tendons & Actuator Sizing
  description: Underactuated adaptive fingers, tendon transmission matrices, Bowden cable Capstan friction, and actuator sizing.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *The Philosophy of Underactuation*: Degrees of freedom ($n$) vs Degrees of actuation ($m < n$); passive mechanical intelligence and adaptive conformity.
  2. *Linkage-Based Underactuated Mechanisms*: Five-bar mechanisms (Robotiq 2F-85), passive springs, transition from precision parallel pinch to enveloping power grasp.
  3. *Tendon-Driven Systems & Transmission Matrices*: Tendon routing matrix $\mathbf{A}$, velocity mapping $\dot{\mathbf{l}} = \mathbf{A} \dot{\boldsymbol{\theta}}$, torque mapping $\boldsymbol{\tau} = \mathbf{A}^T \mathbf{T}$.
  4. *Unilateral Tendon Tension Constraints*: Ensuring positive tensions $\mathbf{T} \ge \mathbf{0}$; $n+1$ tendons required to control $n$ joints (antagonistic tendon routing).
  5. *Bowden Cable Capstan Friction*: Exponential tension loss across curved cable guides; TPU flexure hinges and rapid prototyping.
  6. *Actuator Sizing & Thermal Dissipation*: Coreless DC vs brushless pancake motors (Maxon ECX), planetary gear efficiency, space/weight budgets.
- **Graduate-Level Mathematical Formulations**:
  - *Tendon Kinematics & Statics Mapping*:
    $$\Delta \mathbf{l} = \mathbf{A} \Delta \boldsymbol{\theta}, \quad \boldsymbol{\tau} = \mathbf{A}^T \mathbf{T}, \quad \mathbf{A} \in \mathbb{R}^{m \times n}$$
  - *Tendon Tension Quadratic Program*:
    $$\min_{\mathbf{T}} \frac{1}{2} \|\mathbf{T}\|^2 \quad \text{s.t.} \quad \mathbf{A}^T \mathbf{T} = \boldsymbol{\tau}_{des}, \quad T_{min} \le \mathbf{T} \le T_{max}$$
  - *Capstan Equation for Curved Bowden Sheaths*:
    $$T_{out} = T_{in} \exp\left(-\mu \sum_{j=1}^P |\Delta \phi_j|\right)$$
    where $\mu$ is the cable-sheath friction coefficient and $\sum |\Delta \phi_j|$ is the cumulative bend angle in radians.
- **Hardware Profile**:
  - Robotiq 2F-85: 1 motor actuating 5-bar linkage underactuated mechanism, providing 85 mm stroke and 20–235 N grip force.
  - Shadow Dexterous Hand: 20 Maxon DC motors installed in the forearm driving Dyneema tendon cables routed through Bowden sheaths to hand joints.
  - Yale OpenHand: 3D-printed urethane flexure joints with embedded compliant return springs.
- **Seminal Research Citations**:
  - Dollar, A. M., & Howe, R. D. (2010). The highly adaptive SDM hand: Design and performance evaluation. *IJRR*, 29(5), 585–597.
  - Grebenstein, M., et al. (2011). The DLR Hand Arm System. *ICRA 2011*, pp. 3175–3182.
  - Townsend, W. (2000). The BarrettHand grasper–programmably flexible part handling and assembly. *Industrial Robot*, 27(3), 181–188.
- **Runnable Code Block Architecture**:
  - Python script modeling a 3-joint finger driven by 4 tendon cables: defines the $4 \times 3$ tendon routing matrix $\mathbf{A}$, solves the constrained quadratic program for optimal positive cable tensions satisfying desired joint torques, and computes tension attenuation along a multi-bend Bowden cable path using the Capstan formula.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "Why does an underactuated robotic hand naturally adapt to grasp irregularly shaped objects without requiring external computer vision or motor control loops?" -> Options: [A: The joints automatically lock when power is removed, B: Passive compliance and mechanical linkage constraints allow unconstrained distal joints to conform around the geometry once proximal links establish contact, C: Underactuated hands use soft magnets, D: Tendons have infinite elasticity] -> Correct: 1.
  - `q2`: "According to the Capstan friction equation, if a Bowden cable experiences a cumulative bend angle of $\pi$ radians ($180^\circ$) with a friction coefficient $\mu = 0.2$, what percentage of input tension is transmitted to the output?" -> Options: [A: 100%, B: Approximately 53.3% ($e^{-0.2\pi} \approx 0.533$), C: Exactly 10%, D: 0%] -> Correct: 1.

---

### Chapter 7-4: Optical & Piezoresistive Tactile Sensing: GelSight to High-Density Skins
- **Target File**: `ai-book-docs/module7-dexterous-manipulation/7-4-tactile-sensing.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 4
  title: Optical & Piezoresistive Tactile Sensing: GelSight to High-Density Skins
  description: Elastomer optical sensing, GelSight photometric stereo, piezoresistive arrays, and dynamic slip detection.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *Tactile Transduction Modalities*: Piezoresistive arrays (conductive elastomers, Velostat), capacitive arrays, magnetic Hall-effect arrays (uSkin), and optical elastomer sensors (GelSight, DIGIT, TacTip).
  2. *The GelSight Optical Architecture*: Transparent rigid acrylic plate, compliant silicone elastomer gel, reflective painted elastomeric membrane, multi-color directional RGB LED lighting, micro CMOS camera.
  3. *Photometric Stereo Principle*: Converting pixel color values under known directional illumination vectors into surface gradient fields $(p, q) = (\frac{\partial z}{\partial x}, \frac{\partial z}{\partial y})$.
  4. *Poisson Surface Height Reconstruction*: Fast Fourier Transform (FFT) solution to the Poisson equation for real-time 3D micron-resolution contact geometry.
  5. *Contact Force & Incipient Slip Detection*: Tracking displacement of surface marker dot grids, normal vs shear force decoupling, Coulomb slip criterion $\|\mathbf{f}_{shear}\| \ge \mu f_{normal}$.
- **Graduate-Level Mathematical Formulations**:
  - *Photometric Stereo Reflectance Equation*:
    $$I_k(x, y) = \rho(x, y) \frac{-p(x, y) l_{k, x} - q(x, y) l_{k, y} + l_{k, z}}{\sqrt{p(x, y)^2 + q(x, y)^2 + 1}}, \quad k \in \{R, G, B\}$$
  - *Poisson Integration in Frequency Domain (2D FFT)*:
    $$\nabla^2 z(x, y) = \frac{\partial p}{\partial x} + \frac{\partial q}{\partial y} \implies Z(u, v) = \frac{-j u P(u, v) - j v Q(u, v)}{4\pi^2 (u^2 + v^2)}$$
    $$z(x, y) = \mathcal{F}^{-1}\{ Z(u, v) \}$$
  - *Coulomb Incipient Slip Threshold*:
    $$\frac{\|\mathbf{f}_{shear}\|_2}{f_{normal}} \ge \mu_{static}$$
- **Hardware Profile**:
  - GelSight Mobile / DIGIT (Meta FAIR & GelSight Inc.): Raspberry Pi / Sony IMX sensor with RGB LEDs delivering 60 FPS 1080p tactile images with $< 20\ \mu\text{m}$ spatial resolution.
  - Contactile PapillArray: Optical silicon pillar sensors measuring 3D force vectors and torque per taxel at 1 kHz.
- **Seminal Research Citations**:
  - Johnson, M. K., & Adelson, E. H. (2009). Retrographic sensing for the measurement of surface texture and shape. *CVPR 2009*, pp. 1070–1077.
  - Yuan, W., et al. (2017). GelSight: High-resolution robot tactile system for measuring contact shape and texture. *IEEE Sensors Journal*, 17(9), 2736–2748.
  - Lambeta, M., et al. (2020). DIGIT: A novel design for a low-cost compact high-resolution tactile sensor. *IEEE RA-L*, 5(3), 3838–3845.
- **Runnable Code Block Architecture**:
  - Python/OpenCV script implementing GelSight tactile depth reconstruction: loads RGB tactile contact image, looks up surface normals $(p, q)$ via photometric stereo calibration table, computes divergence $\nabla \cdot [p, q]$, applies 2D FFT Poisson integration to reconstruct a 3D contact height map, and tracks marker displacements to detect incipient slip.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "Why does GelSight use multi-directional RGB LED illumination (e.g. red from left, green from top, blue from right) rather than uniform white illumination?" -> Options: [A: To look aesthetically pleasing, B: Because directional colored illumination allows a single 2D RGB camera frame to simultaneously measure surface gradient components in both horizontal and vertical directions via photometric stereo, C: To heat up the silicone gel, D: To prevent optical reflections] -> Correct: 1.
  - `q2`: "How does an optical tactile sensor detect incipient slip before gross macro-slip occurs across the entire grasp?" -> Options: [A: By monitoring the micro-displacements of tracked surface markers at the outer contact periphery while the central contact region remains stuck, B: By measuring robot battery voltage drop, C: By listening to acoustic microphone hiss, D: By waiting until the object drops completely] -> Correct: 0.

---

### Chapter 7-5: Motion Planning for Manipulation: MoveIt 2, TAMP & RMPs
- **Target File**: `ai-book-docs/module7-dexterous-manipulation/7-5-motion-planning-for-manipulation.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 5
  title: Motion Planning for Manipulation: MoveIt 2, TAMP & RMPs
  description: Configuration space, RRT*, MoveIt 2 architecture, Task and Motion Planning, and Riemannian Motion Policies.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *Configuration Space ($\mathcal{C}$-space) Topology*: Obstacle mapping $\mathcal{C}_{obs}$, free space $\mathcal{C}_{free}$, self-collision geometry, high-dimensional dual-arm manifolds ($14+$ DOFs).
  2. *Sampling-Based Motion Planning*: RRT, RRT-Connect (bidirectional), RRT* (asymptotic optimality with tree rewiring); collision checking with Flexible Collision Library (FCL).
  3. *MoveIt 2 Architecture & Ecosystem*: `move_group` node, Planning Scene Monitor, OMPL plugin interface, Trajectory Execution Manager, ros2_control integration.
  4. *Task and Motion Planning (TAMP)*: Bridging discrete symbolic logic (PDDL, STRIPS) with continuous geometric feasibility samplers; PDDLStream framework.
  5. *Riemannian Motion Policies (RMPs, Ratliff et al. 2018)*: Second-order differential geometry framework combining multiple motion targets, obstacle avoidance, and joint limit repellers into unified joint accelerations.
- **Graduate-Level Mathematical Formulations**:
  - *RRT* Asymptotic Optimality Condition*:
    $$r^*(N) = \gamma_{RRT^*} \left(\frac{\log N}{N}\right)^{1/d}, \quad \text{rewire if } c(x_{near}) > c(x_{new}) + \text{dist}(x_{new}, x_{near})$$
  - *Riemannian Motion Policy (RMP) Pullback*:
    For task map $\mathbf{x} = \phi(\mathbf{q})$, task RMP $(\mathbf{a}_x, \mathbf{M}_x)$ pulls back to configuration space RMP $(\mathbf{a}_q, \mathbf{M}_q)$:
    $$\mathbf{M}_q = \mathbf{J}_\phi^T \mathbf{M}_x \mathbf{J}_\phi, \quad \mathbf{f}_q = \mathbf{J}_\phi^T \mathbf{M}_x (\mathbf{a}_x - \dot{\mathbf{J}}_\phi \dot{\mathbf{q}})$$
  - *RMP Combination*:
    $$\ddot{\mathbf{q}} = \left( \sum_{i} \mathbf{M}_{q, i} \right)^\dagger \left( \sum_{i} \mathbf{f}_{q, i} \right)$$
- **Hardware Profile**:
  - Franka Emika Panda & Universal Robots UR5e: Industry-standard 7-DOF manipulators running MoveIt 2 with OMPL in ROS 2 Jazzy.
  - Dual-arm humanoid manipulators: Boston Dynamics Atlas, Tesla Optimus arms executing bimanual collision-free trajectories.
- **Seminal Research Citations**:
  - Karaman, S., & Frazzoli, E. (2011). Sampling-based algorithms for optimal motion planning. *IJRR*, 30(7), 846–894.
  - Garrett, C. R., et al. (2020). PDDLStream: Integrating symbolic planners and blackbox samplers via optimistic adaptive planning. *ICAPS 2020*, pp. 440–448.
  - Ratliff, N., et al. (2018). Riemannian Motion Policies. *arXiv:1801.02854*.
- **Runnable Code Block Architecture**:
  - Python/MoveIt 2 planning script: initializes `MoveGroupInterface`, populates the `PlanningScene` with 3D collision boxes and cylinders, plans a collision-free dual-arm pick-and-place trajectory using RRT-Connect, validates joint velocity/acceleration limits, and outputs trajectory execution logs.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "What guarantees asymptotic optimality in the RRT* algorithm compared to standard RRT?" -> Options: [A: RRT* uses a neural network, B: RRT* performs local tree rewiring within a shrinking neighborhood ball $r^*(N)$, ensuring the path cost converges to the theoretical optimum as samples $N \to \infty$, C: RRT* only samples straight lines, D: RRT* eliminates collision checking] -> Correct: 1.
  - `q2`: "In Task and Motion Planning (TAMP), why can discrete symbolic planners (like PDDL) not solve manipulation problems alone without geometric samplers?" -> Options: [A: PDDL planners cannot represent logic, B: A discrete symbolic plan (e.g. 'pick mug') may be geometrically unreachable due to kinematic singularities, joint limits, or physical obstacle collisions in continuous $\mathcal{C}$-space, C: PDDL is written in LISP, D: Computers cannot solve graphs] -> Correct: 1.

---

### Chapter 7-6: Learning-Based Manipulation: Grasp Pose Estimation to ACT
- **Target File**: `ai-book-docs/module7-dexterous-manipulation/7-6-learning-based-manipulation.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 6
  title: Learning-Based Manipulation: Grasp Pose Estimation to ACT
  description: 6-DOF grasp synthesis, SE(3)-equivariant networks, Action Chunking with Transformers, and dexterous RL.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *6-DOF Grasp Pose Estimation*: Predicting gripper SE(3) pose and opening width from raw 3D point clouds (GraspNet-1Billion, Contact-GraspNet, AnyGrasp).
  2. *SE(3)-Equivariant Neural Networks*: Geometric deep learning ensuring rotations/translations in 3D scene space map directly to equivariant rotations/translations in output grasp predictions.
  3. *Action Chunking with Transformers (ACT, Zhao et al. 2023)*: Formulating imitation learning as a Conditional VAE (CVAE) sequence-to-sequence problem; predicting chunks of future actions ($k \approx 50-100$) to eliminate compounding error.
  4. *Temporal Ensembling*: Smoothing multi-step predictions across sliding time horizons using exponential decay weighting.
  5. *Dexterous In-Hand Manipulation via RL*: Multi-finger hands (OpenAI Dactyl, Bi-DexHands) learning in-hand cube reorientation and pen spinning via massively parallel Isaac Gym training.
- **Graduate-Level Mathematical Formulations**:
  - *6-DOF Grasp Representation*:
    $$\mathbf{g} = (\mathbf{R}, \mathbf{t}, w, s) \in SO(3) \times \mathbb{R}^3 \times \mathbb{R}^+ \times [0, 1]$$
  - *ACT Conditional VAE Loss*:
    $$\mathcal{L}_{ACT}(\theta, \phi) = \mathbb{E}_{q_\phi(\mathbf{z} \mid \mathbf{a}_{t:t+k}, \mathbf{s}_t)} \left[ \sum_{i=0}^k \|\mathbf{a}_{t+i} - \hat{\mathbf{a}}_{t+i}(\mathbf{z}, \mathbf{s}_t)\|_1 \right] + \beta D_{KL}\left(q_\phi(\mathbf{z} \mid \mathbf{a}_{t:t+k}, \mathbf{s}_t) \parallel p(\mathbf{z})\right)$$
  - *Temporal Ensemble Exponential Blending*:
    $$\mathbf{a}_t = \frac{\sum_{i=0}^m w_i \mathbf{a}_t^{(t-i)}}{\sum_{i=0}^m w_i}, \quad w_i = \exp(-m_{decay} \cdot i)$$
- **Hardware Profile**:
  - ALOHA / Mobile ALOHA: Low-cost bimanual teleoperation system with dual ViperX arms and RealSense RGB-D cameras training ACT policies.
  - Shadow Hand on UR10 robot arm: Physical embodiment executing dexterous in-hand manipulation learned through domain randomization.
- **Seminal Research Citations**:
  - Fang, H.-S., et al. (2020). GraspNet-1Billion: A large-scale benchmark for general object grasping. *CVPR 2020*, pp. 11444–11453.
  - Zhao, T. Z., et al. (2023). Learning fine-grained bimanual manipulation with low-cost hardware. *Robotics: Science and Systems (RSS)*.
  - Chen, Y., et al. (2022). Bi-DexHands: Towards Human-Level Bimanual Dexterous Manipulation with Reinforcement Learning. *NeurIPS 2022*.
- **Runnable Code Block Architecture**:
  - PyTorch implementation of the complete ACT policy architecture: Transformer encoder-decoder network with learned queries, CVAE latent bottleneck, action chunk loss computation for 14-DOF bimanual arm actions, and a temporal ensemble rolling buffer.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "Why does Action Chunking with Transformers (ACT) predict a sequence of future actions (e.g., $k=50$ steps) at once rather than predicting a single step action $a_t$ at each timestep?" -> Options: [A: Predicting single-step actions leads to severe compounding error and causal confusion in imitation learning, whereas action chunking enforces temporal consistency, B: Transformers cannot output vectors smaller than 50 elements, C: Single-step policies require infinite memory, D: Motors cannot accept single-step commands] -> Correct: 0.
  - `q2`: "In SE(3)-equivariant grasp detection networks, what mathematical property holds when the input point cloud $\mathcal{P}$ is rotated by $\mathbf{R} \in SO(3)$?" -> Options: [A: The output grasp orientations rotate by the exact same rotation matrix $\mathbf{R}$, B: The network outputs zero grasps, C: The network must be retrained from scratch, D: The grasp score drops by 50%] -> Correct: 0.

---

### Chapter 7-7: Contact-Rich Assembly: Peg-in-Hole, Spiral Search & Compliance
- **Target File**: `ai-book-docs/module7-dexterous-manipulation/7-7-assembly-and-contact-rich-tasks.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 7
  title: Contact-Rich Assembly: Peg-in-Hole, Spiral Search & Compliance
  description: Peg-in-hole physics, jamming vs wedging, RCC, admittance/impedance control, and spiral search.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *The Mechanics of Peg-in-Hole Assembly*: Contact phases (chamfer crossing, one-point contact, two-point line contact); clearance ratios ($c = (R-r)/R$).
  2. *Jamming vs Wedging (Whitney 1982)*: Jamming (forces/moments in improper ratios causing friction lock; reversible by torque re-orientation) vs Wedging (geometric interference due to elastic deformation; mechanically irreversible).
  3. *Passive Compliance & Remote Center of Compliance (RCC)*: Locating the elastic center of compliance at the peg tip to decouple lateral forces from angular deflections.
  4. *Active Admittance & Impedance Control*: Impedance control (motion input $\to$ force output) vs Admittance control (measured force input $\to$ trajectory modification output: $\mathbf{M}_d \ddot{\mathbf{e}} + \mathbf{D}_d \dot{\mathbf{e}} + \mathbf{K}_d \mathbf{e} = \mathbf{F}_{ext}$).
  5. *Blind Search Strategies*: Archimedean spiral search trajectories combined with downward force drop thresholds to locate hole centers under spatial uncertainty.
  6. *Mason's Hybrid Position/Force Control (1981)*: Task space decomposition via diagonal selection matrix $\mathbf{S}$.
- **Graduate-Level Mathematical Formulations**:
  - *Whitney Jamming Inequality*:
    Jamming occurs during two-point contact when:
    $$\frac{M}{F \cdot r} < \mu \frac{1 + \mu \tan \theta}{\tan \theta - \mu}$$
  - *Whitney Wedging Condition*:
    Wedging occurs when insertion depth $l \le \mu (2r)$ and angular misalignment satisfies:
    $$\theta \ge \frac{c}{\mu}, \quad c = \frac{R - r}{R}$$
  - *Cartesian Admittance Control Law*:
    $$\mathbf{M}_d (\ddot{\mathbf{x}}_{cmd} - \ddot{\mathbf{x}}_d) + \mathbf{D}_d (\dot{\mathbf{x}}_{cmd} - \dot{\mathbf{x}}_d) + \mathbf{K}_d (\mathbf{x}_{cmd} - \mathbf{x}_d) = \mathbf{F}_{ext}$$
    $$\ddot{\mathbf{x}}_{cmd} = \ddot{\mathbf{x}}_d + \mathbf{M}_d^{-1} \left( \mathbf{F}_{ext} - \mathbf{D}_d (\dot{\mathbf{x}}_{cmd} - \dot{\mathbf{x}}_d) - \mathbf{K}_d (\mathbf{x}_{cmd} - \mathbf{x}_d) \right)$$
  - *Archimedean Search Spiral*:
    $$r(\theta) = a + \frac{p}{2\pi} \theta, \quad x(t) = r(\omega t) \cos(\omega t), \quad y(t) = r(\omega t) \sin(\omega t)$$
- **Hardware Profile**:
  - ATI Axia80 / Nano17 6-axis Force/Torque sensors mounted at robot wrist flange (resolution $< 0.1$ N, 1 kHz EtherCAT).
  - KUKA LBR iiwa & Franka Research 3: Joint torque sensors enabling high-bandwidth active Cartesian impedance control for sub-millimeter industrial assembly.
- **Seminal Research Citations**:
  - Whitney, D. E. (1982). Quasi-static assembly of compliantly supported rigid parts. *ASME J. Dyn. Syst. Meas. Control*, 104(1), 65–77.
  - Hogan, N. (1985). Impedance Control: An Approach to Manipulation (Parts I, II, III). *ASME J. Dyn. Syst. Meas. Control*, 107(1), 1–24.
  - Mason, M. T. (1981). Compliance and force control for computer controlled manipulators. *IEEE Trans. SMC*, 11(6), 418–432.
- **Runnable Code Block Architecture**:
  - Python peg-in-hole simulation: models a 6-DOF robot with simulated wrist F/T sensor, executes an Archimedean spiral search on surface contact, detects insertion hole drop from sudden vertical force decrease, aligns peg orientation using active admittance control, and completes insertion without jamming.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "What is the crucial physical difference between 'jamming' and 'wedging' during peg-in-hole assembly?" -> Options: [A: Jamming is caused by friction forces that can be relieved by realigning applied forces/moments, whereas wedging is an irreversible geometric interference caused by elastic material deformation, B: Jamming only occurs with square pegs, C: Wedging happens when the robot runs out of torque, D: There is no difference] -> Correct: 0.
  - `q2`: "How does a Remote Center of Compliance (RCC) device prevent peg jamming during insertion?" -> Options: [A: By actively vibrating the peg at 20 kHz, B: By placing the elastic center of rotation directly at the peg tip so that lateral contact forces produce pure translations rather than rotational tilting, C: By heating the hole, D: By increasing motor current] -> Correct: 1.

---

### Chapter 7-8: Manipulation Benchmarks & Datasets: RoboSuite, ManiSkill & DROID
- **Target File**: `ai-book-docs/module7-dexterous-manipulation/7-8-manipulation-benchmarks.mdx`
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: 8
  title: Manipulation Benchmarks & Datasets: RoboSuite, ManiSkill & DROID
  description: Standardized benchmarks, GPU-parallel simulators, large-scale real-world datasets, and rigorous evaluation protocols.
  ---
  ```
- **Architectural Scope & Section Breakdown**:
  1. *The Evaluation Crisis in Robotics*: Historical fragmentation, lack of standardized physical objects, varying camera placements, unstandardized success metrics.
  2. *Standardized Simulation Benchmark Suites*:
     - RoboSuite: Modular MuJoCo-based benchmark for robot learning with standardized manipulation environments (Lift, Door, NutAssembly, Wipe).
     - ManiSkill3: GPU-parallelized simulator built on SAPIEN/PhysX, rendering thousands of articulated objects at $> 30,000$ FPS.
  3. *Large-Scale Real-World Manipulation Datasets*:
     - DROID (Distributed Robot Interaction Dataset, 2024): 76,000 demonstration trajectories, 350 hours, 564 scenes across 18 labs.
     - BridgeData V2: 60,000 demonstrations across diverse environments for generalizable manipulation.
     - Open X-Embodiment (RT-X): 1M+ trajectories across 22 distinct robot embodiments.
  4. *Humanoid Manipulation Challenges*: AgiBot World Challenge, RoboCup @Home standardized task evaluation.
  5. *Designing Reproducible Evaluation Protocols*: Standardizing randomized object initializations, episode timeout limits, and computing Wilson score confidence intervals on success rates.
- **Graduate-Level Mathematical Formulations**:
  - *Empirical Task Success Rate & Wilson Score 95% Confidence Interval*:
    $$\hat{p} = \frac{1}{N}\sum_{i=1}^N S_i, \quad S_i \in \{0, 1\}$$
    $$CI_{95\%} = \frac{\hat{p} + \frac{z^2}{2N} \pm z\sqrt{\frac{\hat{p}(1-\hat{p})}{N} + \frac{z^2}{4N^2}}}{1 + \frac{z^2}{N}}, \quad z = 1.96$$
  - *Normalized Path Efficiency Ratio*:
    $$\eta_{eff} = \frac{1}{N_{success}} \sum_{i \in \text{Success}} \frac{L_{geodesic}^*(s_0^{(i)}, s_{goal}^{(i)})}{L_{executed}(s_0^{(i)})}$$
- **Hardware Profile**:
  - Franka Emika Panda, UR5e, and AgiBot Raise A1 embodiments deployed across DROID and Open X-Embodiment evaluation protocols.
- **Seminal Research Citations**:
  - Zhu, Y., et al. (2020). robosuite: A Modular Simulation Framework and Benchmark for Robot Learning. *arXiv:2009.12293*.
  - Gu, J., et al. (2023). ManiSkill2: A Unified Benchmark for Generalizable Robot Manipulation. *ICLR 2023*.
  - Khazatsky, A., et al. (2024). DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset. *Robotics: Science and Systems (RSS)*.
  - Padalkar, A., et al. (2024). Open X-Embodiment: Robotic learning datasets and RT-X models. *ICRA 2024*, pp. 15878–15886.
- **Runnable Code Block Architecture**:
  - Python benchmarking harness script: executes automated headless evaluation across 50 seeded trials on a simulated manipulation task, tracks task success conditions, computes Wilson score 95% confidence intervals, and outputs a formatted Markdown evaluation report.
- **Mastery Quiz (`<QuizEngine />`)**:
  - `q1`: "Why is reporting a simple raw success percentage (e.g. '80% success on 10 trials') statistically inadequate for robot manipulation benchmarks?" -> Options: [A: With only 10 trials, the 95% Wilson confidence interval spans from ~49% to ~94%, meaning the claim has massive statistical variance and cannot prove algorithmic superiority, B: Percentages cannot be calculated for integers, C: Benchmarks require at least 1,000,000 trials, D: Neural networks do not follow probability theory] -> Correct: 0.
  - `q2`: "What is the primary contribution of the Open X-Embodiment (RT-X) dataset to robot learning?" -> Options: [A: It proves robots only need 2D images, B: It aggregates over 1 million demonstration trajectories across 22 diverse physical robot embodiments to train cross-embodiment foundation models, C: It replaces ROS 2 with Python scripts, D: It restricts manipulation to parallel-jaw grippers] -> Correct: 1.

---

## 5. Caveats

1. **Solver Dependencies**: Numerical simulations specified in the blueprints require external Python libraries (`pinocchio`, `osqp`, `scipy`, `numpy`, `torch`, `opencv-python`). Downstream author agents must ensure scripts specify imports clearly with standard dependency fallbacks.
2. **GPU Parallel Acceleration**: Chapters 6-6, 6-7, 7-6, and 7-8 involve frameworks (Isaac Lab, PhysX, PyTorch CUDA) that require modern NVIDIA GPUs (RTX 3080/4090/A100) for full-scale execution; the provided runnable code blocks must remain runnable on standard CPU/PyTorch test harnesses for textbook demonstration purposes.
3. **Hardware Protocols**: References to EtherCAT and CAN-FD interfaces on Unitree G1 and Tesla Optimus reflect production specifications; lab exercises simulate these communication buses via POSIX shared memory or software sockets.

---

## 6. Conclusion

This handoff establishes the comprehensive execution blueprint for **18 chapters** across **Module 6 (10 chapters)** and **Module 7 (8 chapters)**. Every single chapter is fully specified with:
- Target file path, frontmatter, and section-by-section outline.
- Complete, graduate-level LaTeX mathematical formulations.
- Industrial hardware embodiment mappings (Unitree G1, Tesla Optimus, Atlas, Shadow Hand, Robotiq 2F-85, GelSight).
- Seminal academic citations across 50+ years of robotics research.
- Full runnable code architectures and complete `<QuizEngine />` question structures.

This specification enables immediate, parallelized drafting by downstream author agents without ambiguity or architectural divergence.

---

## 7. Verification Method

To independently verify this blueprint:
1. **File Path Integrity**: Inspect that every target path adheres to the `ai-book-docs/` hierarchy and matching naming conventions in `specs/010-master-plan-curriculum-expansion/spec.md`.
2. **Mathematical Consistency**: Verify that state-space dimensions, Riccati equations, and optimization constraints are closed and dimensionally consistent across all 18 chapters.
3. **Interactive Component Validation**: Check that all quiz questions adhere to the required JSON schema (`id`, `question`, `options`, `correctIndex`, `explanation`) expected by `<QuizEngine />`.
4. **Docusaurus Build Verification**: Following authoring, run:
   ```bash
   npm run build
   ```
   to confirm zero MDX compilation or frontmatter parsing errors across both modules.
