# Technical Exploration & Blueprint Handoff: Module 3 (NVIDIA Isaac) & Module 4 (Vision-Language-Action Systems)

**State Folder**: `C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\teamwork_explorer_m2_2\`  
**Date**: 2026-11-09T15:45:00Z  
**Author**: Teamwork Explorer Subagent (`teamwork_explorer_m2_2`)  
**Parent Agent**: Orchestrator (`9c96a791-1769-4c88-9445-500c157ed676`)  
**Scope**: Milestone M2 Phase 1 Deepening & Authoring for Module 3 (NVIDIA Isaac) and Module 4 (VLA Systems)  

---

## 1. Observation

A systematic forensic inspection was conducted across the existing chapters in `ai-book-docs/module3-ai-robot-brain/` (5 chapters) and `ai-book-docs/module4-vla/` (5 chapters), as well as the master specifications in `specs/010-master-plan-curriculum-expansion/spec.md` and `.agents/teamwork/spec_miner_curriculum/handoff.md`.

### 1.1 Existing File Inventory & Current State

| Chapter Path | Lines | Current Title | Current State & Gaps Observed |
|:---|:---:|:---|:---|
| `ai-book-docs/module3-ai-robot-brain/3-1-introduction-to-isaac-platform.mdx` | 89 | The NVIDIA Isaac Ecosystem & Physical AI Architecture | High-level architectural overview. Lacks the **Roofline computational model** derivation for Jetson Orin/Thor, CUDA execution hierarchy (warps, streaming multiprocessors, tensor cores), hardware acceleration engines (DLA, PVA, OFA, NVCOMP), and power profile configuration scripts. |
| `ai-book-docs/module3-ai-robot-brain/3-2-isaac-sim-for-humanoids.mdx` | 142 | Isaac Sim, Synthetic Data & Massively Parallel RL | Uses plain markdown `text` code fences for PPO math (lines 55–67: `J(theta) = E[...]`). Lacks **PhysX 5 Reduced Coordinate Articulation (RCA)** mathematical derivations (Baumgarte stabilization, generalized coordinate dynamics $\mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}\dot{\mathbf{q}} + \mathbf{g} = \boldsymbol{\tau}$), Lula kinematics solver internals, and USD OmniGraph action graph Python scripts. |
| `ai-book-docs/module3-ai-robot-brain/3-3-isaac-ros-perception-pipeline.mdx` | 124 | Isaac ROS, NITROS & Hardware-Accelerated Perception | Text block equation for VIO (lines 52–54: `min_X [ sum ||r_imu||^2 + ... ]`). Lacks mathematical memory bus throughput reduction equations for zero-copy NITROS vs standard ROS 2 serialization, type negotiation state machine (REP-2007/REP-2009), cuDNN vs TensorRT execution pipelines, and SGBM vs deep stereo math. |
| `ai-book-docs/module3-ai-robot-brain/3-4-nav2-for-bipedal-movement.mdx` | 151 | Nav2 for Bipedal Locomotion & Footstep Planning | Uses plain `text` code blocks for slope/roughness (lines 49–61) and Capture Point (lines 73–85: `x_CP = x_CoM + dx_CoM / omega_0`). Lacks 3D-LIPM orbital energy conservation derivations, ARA* heuristic footstep lattice formulation with cost function $f(s) = g(s) + \epsilon \cdot h(s)$, QP Whole-Body Control formulation in LaTeX, and complete Nav2 behavior tree XML. |
| `ai-book-docs/module3-ai-robot-brain/3-5-hands-on-exercises.mdx` | 333 | Hands-On Project: Complete Isaac Perception-to-Locomotion Loop | Contains 1 capstone project. Lacks the **10 graded lab project specifications**, mathematical derivations of Absolute Trajectory Error (ATE) and Relative Pose Error (RPE), camera/IMU hardware calibration rig procedures, and automated grading rubrics. |
| `ai-book-docs/module4-vla/4-1-introduction-to-vla-systems.mdx` | 208 | Foundations of Vision-Language-Action (VLA) Systems | High-level taxonomy. Mathematical formulas in plain `text` block (lines 62–67, 76–84). Lacks formal LaTeX autoregressive VLA loss derivation, discrete binning quantization error analysis, comprehensive timeline (RT-1 to $\pi_0$), and continuous flow matching vs discrete tokenization comparative math. |
| `ai-book-docs/module4-vla/4-2-voice-to-action-pipeline.mdx` | 267 | The Voice-to-Action Pipeline: Streaming Audio to Motor Intent | Contains Whisper + Silero VAD implementation. Lacks Connectionist Temporal Classification (CTC) loss derivation, Beam Search probability scoring formula, acoustic delay-and-sum beamformer math, ego-noise spectral subtraction formulation, and NVIDIA Riva FastConformer streaming benchmarks. |
| `ai-book-docs/module4-vla/4-3-cognitive-planning-with-llms.mdx` | 247 | Cognitive Planning & Grounding with Large Language Models | Covers SayCan conceptually. Uses plain `text` block for argmax scoring (lines 70–73). Lacks formal affordance-grounded scoring derivations, PDDL mathematical representation, automated PDDL domain/problem generation via LLMs, and edge NPU memory profiling for quantized LLMs (AWQ/GGUF). |
| `ai-book-docs/module4-vla/4-4-multimodal-interaction.mdx` | 200 | Multimodal Interaction: Vision, Deictic Gestures, and 3D Affordances | Pointing ray formulas in plain `text` blocks (lines 75–96). Lacks formal camera projective geometry derivations ($\mathbf{P}_{3D} = Z \mathbf{K}^{-1} [u, v, 1]^T$), frustum culling on $SE(3)$, FoundationPose 6-DOF tracking math, and pan-tilt gimbal camera kinematics. |
| `ai-book-docs/module4-vla/4-5-hands-on-exercises.mdx` | 418 | Capstone Project: Voice-Grounded Humanoid Manipulation Pipeline | Contains 1 capstone voice listener project. Lacks the **10 graded lab project specifications**, Success weighted by Path Length (SPL) metric derivation, YCB object benchmark protocols, and multi-trial automated grading harness. |

### 1.2 Target Expansion Scope
As mandated in `specs/010-master-plan-curriculum-expansion/spec.md`:
1. **Module 3**: 5 existing chapters enhanced + 5 brand-new chapters:
   - `3-6-cuvslam-and-state-estimation.mdx`
   - `3-7-semantic-perception.mdx`
   - `3-8-force-torque-sensing.mdx`
   - `3-9-multi-sensor-fusion.mdx`
   - `3-10-edge-inference-optimization.mdx`
2. **Module 4**: 5 existing chapters enhanced + 5 brand-new chapters:
   - `4-6-foundation-model-architectures.mdx`
   - `4-7-diffusion-policies.mdx`
   - `4-8-imitation-learning.mdx`
   - `4-9-reward-shaping-and-rlaif.mdx`
   - `4-10-deployment-and-safety.mdx`

---

## 2. Logic Chain

1. **Pedagogical Requirement**: The curriculum is designed for graduate students and robotics research engineers. Explaining algorithms using plain text or hand-waving code blocks fails to provide the rigorous mathematical foundations needed to understand convergence, stability margins, and hardware limitations.
2. **Mathematical Formulation (LaTeX)**: Docusaurus 3 is configured with `remark-math@6` and `rehype-katex@7`. Equations must be written in KaTeX syntax (`$ ... $` for inline, `$$ ... $$` for blocks). Plain text equations (e.g., `J(theta) = E[...]`) must be converted to standard mathematical notation ($\mathcal{J}(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^T \gamma^t r(s_t, a_t) \right]$).
3. **Hardware Grounding**: Humanoid robots operate under tight power and thermal envelopes (15W–60W on Jetson AGX Orin, sub-100W on Jetson Thor). Real-time bipedal balance demands sub-millisecond control loops (1 kHz), while perception must achieve 30–60 Hz with sub-20 ms glass-to-action latency. The blueprints must detail memory bandwidth (GB/s), PCIe bus limits, sensor synchronization (PPS, PTP/IEEE 1588), and silicon accelerator blocks (DLA, Tensor Cores, OFA, PVA).
4. **Seminal Research Citations**: To meet graduate-level scholarship standards, each chapter must cite peer-reviewed foundational literature (author, year, paper title, conference/journal), connecting theory to empirical research.
5. **Runnable Code Engineering**: Code snippets must not be fragmented pseudo-code. They must be complete, syntactically valid Python (with type annotations and docstrings) or modern C++20 nodes implementing standard ROS 2 and PyTorch interfaces.

---

## 3. Caveats

1. **Read-Only Investigation**: As an explorer subagent, this report establishes blueprints and architectural specifications. Actual file authoring in `ai-book-docs/` will be carried out by authoring agents during Milestone M2 execution.
2. **MDX v3 Syntax Constraints**: In Docusaurus 3 / MDX 3, curly braces `{` and `}` outside of code blocks or KaTeX math delimiters are parsed as JSX expressions and cause build failures. All mathematical sets and indices with curly braces must be placed inside LaTeX delimiters (e.g., `$\{q_i\}_{i=1}^N$`) or code fences.
3. **Hardware Simulation**: Code examples referencing physical Jetson Orin registers (`nvpmodel`, `tegrastats`) or hardware cameras (ZED X, RealSense D455) must provide software fallbacks and mock structures so that unit tests pass in headless CI environments without physical sensors.

---

## 4. Conclusion: Complete Blueprints for Module 3 & Module 4

---

### Part A: Module 3 Existing Chapters Enhancement Blueprints (3-1 to 3-5)

#### Chapter 3-1: The NVIDIA Isaac Ecosystem & Physical AI Architecture (`3-1-introduction-to-isaac-platform.mdx`)
- **Learning Objectives**:
  - Understand the end-to-end hardware-software stack from Omniverse simulation to edge Jetson execution.
  - Formulate the computational roofline model for robotics workloads on modern GPU architectures.
  - Evaluate trade-offs between CPU execution, GPU CUDA cores, Deep Learning Accelerators (DLA), and Programmable Vision Accelerators (PVA).
- **Mathematical Formulations (LaTeX)**:
  - **Roofline Computational Model**:
    $$\text{Attainable Performance (TFLOPS)} = \min \left( P_{peak}, \; I \times B_{peak} \right)$$
    where $I$ is Operational Intensity ($\text{FLOPs/byte}$) and $B_{peak}$ is memory bandwidth ($\text{GB/s}$).
  - **Memory Transfer Bottleneck Model**:
    $$T_{comm} = \alpha + \frac{S}{B_{PCIe}} + T_{sync}$$
    where $\alpha$ is latency overhead, $S$ is frame payload size in bytes, and $B_{PCIe}$ is PCIe bandwidth (PCIe Gen4 x8 $\approx 15.75 \text{ GB/s}$).
- **Hardware Breakdowns**:
  - **Jetson AGX Orin 64GB**: 2048-core NVIDIA Ampere GPU with 64 Tensor Cores; 12-core Arm Cortex-A78AE CPU; 2x NVDLA 2.0 engines (combined 275 INT8 TOPS); 204.8 GB/s 256-bit LPDDR5 memory; TDP 15W–60W.
  - **Jetson Thor**: Blackwell GPU architecture with 5th Gen Tensor Cores & Transformer Engine; 14-core Arm Neoverse-V3AE CPU; 1000+ FP4/FP8 TOPS; >500 GB/s LPDDR5X.
  - **Hardware Accelerator Engines**: DLA (offloads CNN/Transformer inference, freeing GPU), PVA (fixed-function optical flow & stereo disparity), NVENC/NVDEC (H.264/H.265 hardware video codecs).
- **Seminal Citations**:
  - Williams, S., Waterman, A., & Patterson, D. (2009). *Roofline: an insightful visual performance model for multicore architectures*. Communications of the ACM, 52(4), 65-76.
  - NVIDIA Corporation. (2022). *NVIDIA Jetson AGX Orin Architecture Whitepaper*.
  - Kirk, D. B., & Hwu, W. M. W. (2016). *Programming Massively Parallel Processors: A Hands-on Approach*. Morgan Kaufmann.
- **Runnable Code Example**:
  - Python script querying Jetson power states via `tegrastats` API or sysfs, parsing thermal zones, and calculating actual operational intensity of an edge inference workload.

---

#### Chapter 3-2: Isaac Sim, Synthetic Data & Massively Parallel RL (`3-2-isaac-sim-for-humanoids.mdx`)
- **Learning Objectives**:
  - Derive the dynamics of PhysX 5 Reduced Coordinate Articulations (RCA) and contrast with maximal coordinate formulations.
  - Understand GPU tensor sharing between PhysX 5 GPU and PyTorch tensors without host memory transfers.
  - Formulate domain randomization distributions and programmatic scene graph generation via Omniverse Replicator.
- **Mathematical Formulations (LaTeX)**:
  - **Reduced Coordinate Forward Dynamics**:
    $$\mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{g}(\mathbf{q}) = \boldsymbol{\tau} + \mathbf{J}_c^T \boldsymbol{\lambda}$$
    where $\mathbf{M}(\mathbf{q}) \in \mathbb{R}^{n \times n}$ is the generalized inertia matrix computed via the Articulated Body Algorithm (ABA) in $O(n)$ time.
  - **Baumgarte Joint Constraint Stabilization**:
    $$\ddot{\mathbf{C}}(\mathbf{q}) + 2 \alpha \dot{\mathbf{C}}(\mathbf{q}) + \beta^2 \mathbf{C}(\mathbf{q}) = \mathbf{0}$$
    where $\alpha, \beta$ are damping and stiffness stabilization parameters preventing constraint drift.
  - **PPO Clipped Surrogate Locomotion Objective**:
    $$\mathcal{L}^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\theta)\hat{A}_t, \; \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t \right) \right]$$
    where $r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{old}}(a_t \mid s_t)}$.
- **Hardware Breakdowns**:
  - Workstation GPU: Dual NVIDIA RTX 4090 / RTX 6000 Ada with 48 GB VRAM.
  - Memory Bus: NVLink interconnect (900 GB/s bidirectional) for distributed multi-GPU simulation.
  - Physics Execution: 4,096 parallel environments stepping at 1,000 Hz consuming ~14 GB VRAM.
- **Seminal Citations**:
  - Rudin, N., Hoeller, D., Reist, P., & Hutter, M. (2022). *Learning to walk in minutes using massively parallel deep reinforcement learning*. Science Robotics, 7(66), eabk2822.
  - Featherstone, R. (2008). *Rigid Body Dynamics Algorithms*. Springer Science & Business Media.
  - Macklin, M., Storey, K., Lu, M., Terdiman, P., Chentanez, N., Jeschke, S., & Müller, M. (2020). *Small steps in physics simulation*. ACM Transactions on Graphics (TOG), 39(6), 1-14.
- **Runnable Code Example**:
  - Standalone Omniverse Python script configuring a 28-DOF humanoid articulation in Isaac Sim, setting joint drive stiffness/damping, and attaching GPU tensor buffers for vectorized observation extraction.

---

#### Chapter 3-3: Isaac ROS, NITROS & Hardware-Accelerated Perception (`3-3-isaac-ros-perception-pipeline.mdx`)
- **Learning Objectives**:
  - Master the architecture of NVIDIA Isaac Transport for ROS (NITROS) and understand REP-2007 Type Adaptation & REP-2009 Type Negotiation.
  - Derive the memory throughput savings achieved by zero-copy CUDA pointer passing versus standard ROS 2 serialization.
  - Implement a composable ROS 2 perception graph executing hardware-accelerated stereo rectification and inference.
- **Mathematical Formulations (LaTeX)**:
  - **Memory Throughput Reduction**:
    Standard ROS 2 pipeline bandwidth consumption across $K$ subscriber nodes:
    $$B_{std} = (K + 1) \cdot (W \times H \times C \times b) \cdot f_{cam}$$
    where $W, H$ are frame dimensions, $C$ channels, $b$ bytes per pixel, and $f_{cam}$ framerate.  
    Under NITROS zero-copy IPC:
    $$B_{nitros} = (W \times H \times C \times b) \cdot f_{cam} \quad (\text{Direct DMA to VRAM; } O(1) \text{ pointer swaps})$$
    yielding a reduction factor of $\frac{B_{std}}{B_{nitros}} = K + 1$.
  - **Semi-Global Matching (SGM) Disparity Energy**:
    $$E(D) = \sum_{\mathbf{p}} C(\mathbf{p}, D(\mathbf{p})) + \sum_{\mathbf{q} \in \mathcal{N}_\mathbf{p}} P_1 \cdot \mathbb{I}[|D(\mathbf{p}) - D(\mathbf{q})| = 1] + \sum_{\mathbf{q} \in \mathcal{N}_\mathbf{p}} P_2 \cdot \mathbb{I}[|D(\mathbf{p}) - D(\mathbf{q})| > 1]$$
- **Hardware Breakdowns**:
  - Camera Interfaces: Dual GMSL2 (Gigabit Multimedia Serial Link 2) automotive camera inputs @ 6 Gbps per lane, bypassing USB host controller latency.
  - Programmable Vision Accelerator (PVA): 7-way VLIW vector processors offloading stereo SGBM and corner detection with <2W power draw.
  - Jetson Unified Memory Architecture (UMA): Eliminates discrete PCIe transfers between CPU and GPU.
- **Seminal Citations**:
  - Hirschmüller, H. (2007). *Stereo processing by semiglobal matching and mutual information*. IEEE Transactions on Pattern Analysis and Machine Intelligence, 30(2), 328-341.
  - Open Robotics. (2021). *REP-2007: Type Adaptation - Enabling zero-copy in ROS 2*.
  - Macenski, S., Foote, T., Gerkey, B., Lalancette, C., & Woodall, W. (2022). *Robot Operating System 2: Design, architecture, and uses in the wild*. Science Robotics, 7(66), eabm6074.
- **Runnable Code Example**:
  - Complete C++ ROS 2 Composable Node implementing `NitrosImage` custom type adaptation and demonstrating zero-copy CUDA kernel invocation on received image pointers.

---

#### Chapter 3-4: Nav2 for Bipedal Locomotion & Footstep Planning (`3-4-nav2-for-bipedal-movement.mdx`)
- **Learning Objectives**:
  - Contrast 2D planar costmaps with 3D multi-layered elevation maps for legged mobility.
  - Derive the 3D Linear Inverted Pendulum Model (3D-LIPM) and Capture Point (CP) dynamic step-recovery formulations.
  - Configure the Anytime Repairing A* ($ARA^*$) footstep lattice planner within the Nav2 framework.
- **Mathematical Formulations (LaTeX)**:
  - **3D-LIPM Orbital Energy Conservation**:
    $$\ddot{x} = \omega_0^2 (x - p_x), \quad \omega_0 = \sqrt{\frac{g}{z_c}}$$
    $$E_{orbital} = \frac{1}{2} \dot{x}^2 - \frac{g}{2 z_c} x^2 = \text{constant}$$
  - **Instantaneous Capture Point (ICP)**:
    $$\mathbf{x}_{cp} = \mathbf{x}_{com} + \frac{\dot{\mathbf{x}}_{com}}{\omega_0}$$
    If external push disturbance $\Delta \mathbf{v}$ occurs, the required capture footstep position is:
    $$\mathbf{p}_{foot}^* = \mathbf{x}_{cp} + \frac{\Delta \mathbf{v}}{\omega_0}$$
  - **ARA\* Heuristic Footstep Lattice Cost**:
    $$f_\epsilon(s) = g(s) + \epsilon \cdot h(s), \quad \epsilon > 1$$
    gradually decreasing $\epsilon \to 1.0$ as computation time permits to guarantee suboptimality bounds $\le \epsilon$.
- **Hardware Breakdowns**:
  - 3D Terrain Sensors: Livox Mid-360 3D LiDAR (360° horizontal FOV, non-repetitive scanning) + RealSense D455 depth camera.
  - Time-Synchronization: Hardware PPS (Pulse-Per-Second) triggering camera global shutters and IMU sampling @ 1 kHz.
- **Seminal Citations**:
  - Pratt, J., Carff, J., Drakunov, S., & Goswami, A. (2006). *Capture point: A step towards agile humanoid locomotion*. IEEE-RAS International Conference on Humanoid Robots (Humanoids).
  - Kajita, S., Kanehiro, F., Kaneko, K., Fujiwara, K., Harada, K., & Hirukawa, H. (2003). *Biped walking pattern generation by using preview control of zero-moment point*. IEEE International Conference on Robotics and Automation (ICRA).
  - Likhachev, M., Gordon, G. J., & Thrun, S. (2003). *ARA\*: Anytime A\* with provable bounds on sub-optimality*. Advances in Neural Information Processing Systems (NeurIPS).
- **Runnable Code Example**:
  - Complete Python footstep planner calculating dynamically stable left/right step sequences across an obstacle field using Capture Point bounds and generating Nav2 `nav_msgs/Path` messages.

---

#### Chapter 3-5: Hands-On Exercises & Lab Projects (`3-5-hands-on-exercises.mdx`)
- **Learning Objectives**:
  - Execute 10 rigorous, graded laboratory exercises covering the entire Module 3 curriculum.
  - Implement mathematical benchmarks for visual odometry accuracy: Absolute Trajectory Error (ATE) and Relative Pose Error (RPE).
  - Build automated verification harnesses testing real-time ROS 2 node execution against reference baselines.
- **Mathematical Formulations (LaTeX)**:
  - **Absolute Trajectory Error (ATE RMSE)**:
    $$\mathbf{E}_k = \mathbf{Q}_k^{-1} \mathbf{S} \mathbf{P}_k, \quad \text{ATE}_{RMSE} = \sqrt{\frac{1}{N} \sum_{k=1}^N \|\text{trans}(\mathbf{E}_k)\|^2}$$
    where $\mathbf{P}_{1:N} \in SE(3)$ is the estimated trajectory, $\mathbf{Q}_{1:N} \in SE(3)$ is the ground-truth trajectory, and $\mathbf{S}$ is the optimal rigid alignment transformation via Umeyama's method.
  - **Relative Pose Error (RPE)**:
    $$\Delta \mathbf{E}_{i} = \left( \mathbf{Q}_i^{-1} \mathbf{Q}_{i+\Delta t} \right)^{-1} \left( \mathbf{P}_i^{-1} \mathbf{P}_{i+\Delta t} \right)$$
- **Hardware Breakdowns**:
  - OptiTrack PrimeX 13 motion capture system (12 cameras, 240 FPS sub-millimeter tracking).
  - Calibration Target: Monocular and stereo checkerboard / AprilTag grid rig with precision micrometer mounts.
- **Seminal Citations**:
  - Sturm, J., Engelhard, N., Endres, F., Burgard, W., & Cremers, D. (2012). *A benchmark for the evaluation of RGB-D SLAM systems*. IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS).
  - Umeyama, S. (1991). *Least-squares estimation of transformation parameters between two point patterns*. IEEE Transactions on Pattern Analysis and Machine Intelligence, 13(4), 376-380.
- **Detailed 10-Project Blueprint Catalog**:
  1. *Project 3.1: Jetson AGX Orin Hardware & Roofline Benchmark* (Profile memory bandwidth and Tensor Core TFLOPS).
  2. *Project 3.2: Isaac Sim Humanoid Articulation Setup* (Load 28-DOF URDF, convert to USD with PhysX 5 RCAs).
  3. *Project 3.3: Replicator Domain Randomization Pipeline* (Generate 10k photorealistic frames with COCO bounding boxes).
  4. *Project 3.4: NITROS Zero-Copy Composable Perception Node* (Write C++ node processing 1080p stereo at 60 Hz).
  5. *Project 3.5: cuVSLAM Tuning for Dynamic Walking* (Tune IMU noise covariances to eliminate walking impact drift).
  6. *Project 3.6: 3D GridMap Elevation Layer Integration* (Build point-cloud filter computing slope and roughness).
  7. *Project 3.7: Capture Point Reactive Step Replanner* (Simulate lateral impulse pushes and trigger emergency footsteps).
  8. *Project 3.8: Hierarchical QP Whole-Body Controller* (Solve contact wrench distribution across dual support feet).
  9. *Project 3.9: Nav2 Behavior Tree Custom Footstep Action Plugin* (Author Nav2 BT node invoking gait generator).
  10. *Project 3.10: Full-Stack Autonomy Capstone* (Navigate humanoid across 15m obstacle course to grasp target).
- **Runnable Code Example**:
  - Complete Python trajectory evaluation harness reading estimated odometry and ground-truth CSV logs, computing Umeyama alignment, and generating publication-quality ATE/RPE error plots.

---

### Part B: Module 3 Brand-New Chapters Blueprints (3-6 to 3-10)

#### Chapter 3-6: Visual-Inertial Odometry & State Estimation with cuVSLAM (`3-6-cuvslam-and-state-estimation.mdx`)
- **Title**: Visual-Inertial Odometry & State Estimation with cuVSLAM
- **Learning Objectives**:
  - Derive the continuous-time IMU kinematic model and its discrete integration on the $SO(3)$ Lie group.
  - Implement IMU preintegration theory on manifold (Forster et al.) to prevent re-integrating IMU measurements during optimization.
  - Construct a tightly coupled factor graph combining visual reprojection factors and preintegrated IMU factors using GTSAM.
  - Mitigate feature tracking degradation in low-texture corridors and during high-acceleration footstep impacts.
- **Mathematical Formulations (LaTeX)**:
  - **IMU Preintegration on $SO(3)$**:
    $$\Delta \mathbf{R}_{ij} = \prod_{k=i}^{j-1} \text{Exp} \left( (\tilde{\boldsymbol{\omega}}_k - \mathbf{b}_i^g - \boldsymbol{\eta}_k^{gd}) \Delta t \right)$$
    $$\Delta \mathbf{v}_{ij} = \sum_{k=i}^{j-1} \Delta \mathbf{R}_{ik} (\tilde{\mathbf{a}}_k - \mathbf{b}_i^a - \boldsymbol{\eta}_k^{ad}) \Delta t$$
    $$\Delta \mathbf{p}_{ij} = \sum_{k=i}^{j-1} \left( \Delta \mathbf{v}_{ik} \Delta t + \frac{1}{2} \Delta \mathbf{R}_{ik} (\tilde{\mathbf{a}}_k - \mathbf{b}_i^a - \boldsymbol{\eta}_k^{ad}) \Delta t^2 \right)$$
  - **First-Order Bias Update**:
    $$\Delta \mathbf{R}_{ij}(\mathbf{b}_i^g) \approx \Delta \bar{\mathbf{R}}_{ij} \text{Exp} \left( \frac{\partial \Delta \bar{\mathbf{R}}_{ij}}{\partial \mathbf{b}^g} \delta \mathbf{b}_i^g \right)$$
  - **Visual Reprojection Residual Factor**:
    $$\mathbf{r}_{proj}(\mathbf{x}_i, \mathbf{l}_j) = \pi \left( \mathbf{R}_i^T (\mathbf{l}_j - \mathbf{p}_i) \right) - \tilde{\mathbf{z}}_{ij}$$
    where $\pi([X, Y, Z]^T) = [f_x \frac{X}{Z} + c_x, \; f_y \frac{Y}{Z} + c_y]^T$.
- **Hardware Breakdowns**:
  - Stereo Cameras: Stereolabs ZED X Stereo Camera (GMSL2, global shutter, 1920x1200 @ 60 FPS, 12cm baseline).
  - IMU: InvenSense ICM-42688-P (6-axis high-performance MEMS IMU, ultra-low noise: $2.8 \, \mu g/\sqrt{\text{Hz}}$, gyro noise: $0.0038^\circ/s/\sqrt{\text{Hz}}$).
  - Compute Target: Jetson AGX Orin DLA + Ampere GPU running cuVSLAM @ 60 Hz with <8 ms latency.
- **Seminal Citations**:
  - Forster, C., Carlone, L., Shen, S., & Scaramuzza, D. (2017). *On-manifold preintegration for real-time visual--inertial odometry*. IEEE Transactions on Robotics, 33(1), 1-21.
  - Qin, T., Li, P., & Shen, S. (2018). *VINS-Mono: A robust and versatile monocular visual-inertial state estimator*. IEEE Transactions on Robotics, 34(4), 1004-1020.
  - Mur-Artal, R., & Tardós, J. D. (2017). *ORB-SLAM2: An open-source SLAM system for monocular, stereo, and RGB-D cameras*. IEEE Transactions on Robotics, 33(5), 1255-1262.
- **Runnable Code Example**:
  - Complete Python GTSAM factor graph optimization script setting up prior factors, between factors, IMU preintegration factors, and optimizing state trajectories over a simulated walking motion.

---

#### Chapter 3-7: Semantic Perception, 6-DOF Pose Estimation & Open-Vocabulary Detection (`3-7-semantic-perception.mdx`)
- **Title**: Semantic Perception, 6-DOF Pose Estimation & Open-Vocabulary Detection
- **Learning Objectives**:
  - Deploy zero-shot open-vocabulary detectors (Grounding DINO, NanoOWL) on edge robotics silicon.
  - Implement promptable instance segmentation with Segment Anything 2 (SAM 2) for dynamic robotic scenes.
  - Estimate and track 6-DOF object poses in real time using FoundationPose and MegaPose without object-specific CAD retraining.
  - Fuse semantic instance masks with 3D point clouds to build real-time 3D semantic scene graphs.
- **Mathematical Formulations (LaTeX)**:
  - **Open-Vocabulary Cross-Modal Contrastive Alignment**:
    $$\mathcal{L}_{align} = -\log \frac{\exp(\mathbf{v}_i^T \mathbf{t}_j / \tau)}{\sum_k \exp(\mathbf{v}_i^T \mathbf{t}_k / \tau)}$$
    where $\mathbf{v}_i$ is the normalized visual token embedding from the image backbone and $\mathbf{t}_j$ is the language token embedding from the text encoder.
  - **6-DOF Pose Refinement Loss (FoundationPose)**:
    $$\min_{\mathbf{R} \in SO(3), \mathbf{t} \in \mathbb{R}^3} \sum_{k=1}^M \rho \left( \left\| \mathbf{p}_k^{rend}(\mathbf{R}, \mathbf{t}) - \mathbf{p}_k^{obs} \right\|_2 \right)$$
    using robust Huber loss $\rho(\cdot)$ and rendering-and-comparing neural field representations.
- **Hardware Breakdowns**:
  - Vision Processing: Jetson AGX Orin utilizing FP8 Tensor Cores via TensorRT-LLM and ONNX Runtime CUDA Execution Provider.
  - Video Stream: 4K 30 FPS RGB-D camera stream processed with sub-35 ms latency using INT8 quantized Grounding DINO.
- **Seminal Citations**:
  - Liu, S., Zeng, Z., Ren, T., Li, F., Zhang, H., Yang, J., ... & Zhang, L. (2023). *Grounding DINO: Marrying DINO with grounded pre-training for open-vocabulary object detection*. arXiv preprint arXiv:2303.05499.
  - Ravi, N., Gabeur, V., Hu, Y. T., Hu, R., Ryali, C., Ma, T., ... & Feichtenhofer, C. (2024). *SAM 2: Segment Anything in High Quality Videos*. arXiv preprint arXiv:2408.00714.
  - Wen, B., Tremblay, J., Blukis, V., Tyree, S., Müller, T., Evans, A., ... & Fox, D. (2024). *FoundationPose: Unified 6D pose estimation and tracking of novel objects*. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR).
- **Runnable Code Example**:
  - Python ROS 2 node executing TensorRT-accelerated open-vocabulary object detection, extracting 3D oriented bounding boxes ($SE(3)$ pose + extents) from registered depth clouds, and publishing `vision_msgs/Detection3DArray`.

---

#### Chapter 3-8: Tactile, Contact & 6-Axis Force-Torque Sensing (`3-8-force-torque-sensing.mdx`)
- **Title**: Tactile, Contact & 6-Axis Force-Torque Sensing
- **Learning Objectives**:
  - Master the operating principles of 6-axis strain-gauge force/torque sensors and optical tactile sensors (GelSight, DIGIT).
  - Formulate foot-contact detection algorithms using load cells and Schmitt-trigger contact state machines.
  - Design a Generalized Momentum-based Disturbance Observer (DOB) to estimate external wrenches without distal sensors.
  - Implement force-controlled assembly primitives (peg-in-hole) with active admittance control.
- **Mathematical Formulations (LaTeX)**:
  - **Generalized Momentum Disturbance Observer (DOB)**:
    Let robot generalized momentum be $\mathbf{p} = \mathbf{M}(\mathbf{q})\dot{\mathbf{q}}$. Its time derivative is:
    $$\dot{\mathbf{p}} = \boldsymbol{\tau} + \mathbf{C}^T(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} - \mathbf{g}(\mathbf{q}) + \boldsymbol{\tau}_{ext}$$
    The estimated external torque $\hat{\boldsymbol{\tau}}_{ext}$ is governed by:
    $$\hat{\boldsymbol{\tau}}_{ext} = \mathbf{K}_O \left( \mathbf{p}(t) - \int_0^t \left( \boldsymbol{\tau} + \mathbf{C}^T \dot{\mathbf{q}} - \mathbf{g} + \hat{\boldsymbol{\tau}}_{ext} \right) dt - \mathbf{p}(0) \right)$$
    where $\mathbf{K}_O > 0$ is a diagonal observer gain matrix guaranteeing first-order error convergence: $\dot{\mathbf{e}} + \mathbf{K}_O \mathbf{e} = \mathbf{0}$.
  - **Admittance Control Law**:
    $$\mathbf{M}_d (\ddot{\mathbf{x}}_c - \ddot{\mathbf{x}}_d) + \mathbf{D}_d (\dot{\mathbf{x}}_c - \dot{\mathbf{x}}_d) + \mathbf{K}_d (\mathbf{x}_c - \mathbf{x}_d) = \mathbf{F}_{ext}$$
    where $\mathbf{M}_d, \mathbf{D}_d, \mathbf{K}_d$ are desired virtual inertia, damping, and stiffness matrices.
- **Hardware Breakdowns**:
  - 6-Axis F/T Sensors: ATI Axia80 EtherCAT (payload $\pm 500 \text{ N}$, torque $\pm 20 \text{ Nm}$, resolution $0.1 \text{ N}$, 8 kHz sample rate) mounted on humanoid ankles and wrists.
  - Tactile Fingers: GelSight wedge sensor with 4-megapixel CMOS sensor tracking 3D surface elastomeric deformations.
- **Seminal Citations**:
  - De Luca, A., & Mattone, R. (2005). *Sensorless robot collision detection and hybrid force/motion control*. IEEE International Conference on Robotics and Automation (ICRA).
  - Yuan, W., Dong, S., & Adelson, E. H. (2017). *GelSight: High-resolution robot tactile system for estimating geometry and force*. Sensors, 17(12), 2762.
  - Hogan, N. (1985). *Impedance control: An approach to manipulation*. ASME Journal of Dynamic Systems, Measurement, and Control, 107(1), 1-24.
- **Runnable Code Example**:
  - C++ ROS 2 real-time controller node implementing the momentum-based disturbance observer and admittance compliance loop running in a 1 kHz RTOS thread.

---

#### Chapter 3-9: Probabilistic Multi-Sensor Fusion & Factor Graph SLAM (`3-9-multi-sensor-fusion.mdx`)
- **Title**: Probabilistic Multi-Sensor Fusion & Factor Graph SLAM
- **Learning Objectives**:
  - Derive the Kalman Filter family: linear KF, Extended Kalman Filter (EKF), and Unscented Kalman Filter (UKF).
  - Formulate nonlinear factor graph SLAM and contrast smoothing with filtering.
  - Implement tightly coupled LiDAR-Inertial-Visual Odometry (LIVO) for humanoid floating-base state estimation.
  - Configure the ROS 2 `robot_localization` dual-EKF architecture for industrial humanoid deployments.
- **Mathematical Formulations (LaTeX)**:
  - **Unscented Transform Sigma Point Generation**:
    For state dimension $n$ and covariance $\mathbf{P}$:
    $$\boldsymbol{\chi}_0 = \bar{\mathbf{x}}$$
    $$\boldsymbol{\chi}_i = \bar{\mathbf{x}} + \left( \sqrt{(n + \lambda)\mathbf{P}} \right)_i, \quad i = 1, \dots, n$$
    $$\boldsymbol{\chi}_{i+n} = \bar{\mathbf{x}} - \left( \sqrt{(n + \lambda)\mathbf{P}} \right)_i, \quad i = 1, \dots, n$$
    where scaling parameter $\lambda = \alpha^2(n + \kappa) - n$.
  - **Factor Graph Nonlinear Least Squares**:
    $$\mathcal{X}^* = \arg\min_{\mathcal{X}} \sum_{i} \left\| \mathbf{r}_{prior}(\mathbf{x}_i) \right\|_{\boldsymbol{\Sigma}_i}^2 + \sum_{k} \left\| \mathbf{r}_{odom}(\mathbf{x}_k, \mathbf{x}_{k+1}) \right\|_{\boldsymbol{\Lambda}_k}^2 + \sum_{j} \left\| \mathbf{r}_{meas}(\mathbf{x}_j, \mathbf{z}_j) \right\|_{\boldsymbol{\Omega}_j}^2$$
    solved via Levenberg-Marquardt or iSAM2 (incremental smoothing and mapping).
- **Hardware Breakdowns**:
  - Sensors: Livox Mid-360 LiDAR (200k pts/sec), Dual Bosch BMI085 IMUs (one in pelvis, one in head), wheel/joint motor encoders, and wheel contact switches.
  - Bus Topology: Isolated Gigabit Ethernet VLANs for LiDAR point clouds, PTP (IEEE 1588v2) master clock synchronizer guaranteeing sub-microsecond timestamp alignment.
- **Seminal Citations**:
  - Julier, S. J., & Uhlmann, J. K. (2004). *Unscented filtering and nonlinear estimation*. Proceedings of the IEEE, 92(3), 401-422.
  - Kaess, M., Ranganathan, A., & Dellaert, F. (2008). *iSAM: Incremental smoothing and mapping*. IEEE Transactions on Robotics, 24(6), 1365-1378.
  - Shan, T., Englot, B., Meyers, D., Wang, W., Ratti, C., & Rus, D. (2020). *LIO-SAM: Tightly-coupled lidar inertial odometry via smoothing and mapping*. IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS).
- **Runnable Code Example**:
  - Complete ROS 2 `robot_localization` dual-EKF configuration file (`ekf_local.yaml` and `ekf_global.yaml`) alongside a Python node verifying covariance consistency using normalized innovation squared (NIS) tests.

---

#### Chapter 3-10: Edge AI Inference Optimization with TensorRT & INT8 Quantization (`3-10-edge-inference-optimization.mdx`)
- **Title**: Edge AI Inference Optimization with TensorRT & INT8 Quantization
- **Learning Objectives**:
  - Understand the complete TensorRT compilation pipeline: ONNX parsing, layer and tensor fusion, kernel auto-tuning, and engine serialization.
  - Derive post-training quantization (PTQ) mathematics: uniform symmetric quantization, dynamic range clipping, and KL-divergence calibration.
  - Profile and optimize Vision Transformer (ViT) attention blocks using FP8/INT8 Tensor Cores.
  - Author a multi-stream asynchronous inference worker pipeline utilizing dual Deep Learning Accelerators (DLA) and GPU concurrently.
- **Mathematical Formulations (LaTeX)**:
  - **Uniform Symmetric INT8 Quantization**:
    $$q = \text{clip} \left( \left\lfloor \frac{x}{s} \right\rceil, \; -128, \; 127 \right), \quad s = \frac{\max(|x|)}{127}$$
  - **Kullback-Leibler (KL) Divergence Calibration**:
    $$D_{KL}(P \parallel Q) = \sum_{i=1}^{N} P(i) \log \left( \frac{P(i)}{Q(i)} \right)$$
    where $P$ is the reference FP32 activation histogram and $Q$ is the candidate quantized INT8 distribution expanded back to FP32 bins. The optimal clipping threshold $T^*$ minimizes $D_{KL}(P \parallel Q)$.
- **Hardware Breakdowns**:
  - Compute Engines: Jetson AGX Orin 64GB with 64 Tensor Cores supporting INT8, FP8, and FP16 math; Dual NVDLA 2.0 engines operating at 1.4 GHz.
  - Thermal Envelope: Power profile tuning using `nvpmodel` (Mode 0: MAXN 60W vs Mode 1: 50W vs Mode 2: 30W vs Mode 3: 15W).
- **Seminal Citations**:
  - NVIDIA Corporation. (2023). *NVIDIA TensorRT Developer Guide: Low-Precision Inference*.
  - Jacob, B., Kligys, S., Chen, B., Zhu, M., Tang, M., Howard, A., ... & Adam, H. (2018). *Quantization and training of neural networks for efficient integer-arithmetic-only inference*. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR).
  - Micikevicius, P., Stosic, D., Burgess, N., Cornea, M., Dubey, P., Fasih, A., ... & Wu, H. (2022). *FP8 formats for deep learning*. arXiv preprint arXiv:2209.05433.
- **Runnable Code Example**:
  - Complete Python script implementing a custom TensorRT `IInt8EntropyCalibrator2` class, compiling a vision transformer ONNX model to an INT8 engine, and running asynchronous double-buffered CUDA inference streams.

---

### Part C: Module 4 Existing Chapters Enhancement Blueprints (4-1 to 4-5)

#### Chapter 4-1: Foundations of Vision-Language-Action (VLA) Systems (`4-1-introduction-to-vla-systems.mdx`)
- **Learning Objectives**:
  - Trace the historical evolution of robotic policies from modular pipelines to end-to-end VLA models (RT-1, RT-2, OpenVLA, Octo, $\pi_0$).
  - Compare action space representations: joint angles, Cartesian end-effector velocities, delta actions, and impedance parameters.
  - Analyze the trade-offs between discrete action tokenization and continuous diffusion/flow-matching action heads.
- **Mathematical Formulations (LaTeX)**:
  - **Joint VLA Autoregressive Negative Log-Likelihood**:
    $$\mathcal{L}_{VLA}(\theta) = -\sum_{t=1}^T \log P_\theta(\mathbf{a}_t \mid \mathbf{I}_{1:t}, \; \mathbf{l}, \; \mathbf{a}_{<t})$$
    where $\mathbf{I}_{1:t}$ are visual frames, $\mathbf{l}$ is the language instruction, and $\mathbf{a}_t \in \mathbb{R}^D$ is the robot action vector.
  - **Discretized Action Quantization**:
    $$\text{bin}_i = \text{clip} \left( \left\lfloor \frac{a_i - a_i^{min}}{a_i^{max} - a_i^{min}} \cdot (K - 1) \right\rceil, \; 0, \; K - 1 \right)$$
    with reconstruction $\hat{a}_i = a_i^{min} + \frac{\text{bin}_i}{K - 1}(a_i^{max} - a_i^{min})$.
- **Hardware Breakdowns**:
  - Edge Inference Rig: Dual NVIDIA Jetson AGX Orin 64GB connected via high-speed 10GbE running 7B parameter models @ 10 Hz.
  - Training Cluster: 64x NVIDIA H100 SXM5 80GB GPUs with 3.2 Tbps InfiniBand interconnect.
- **Seminal Citations**:
  - Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Ding, M., ... & Zitkovich, B. (2022). *RT-1: Robotics Transformer for real-world control at scale*. arXiv preprint arXiv:2212.06817.
  - Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Chen, K., ... & Zitkovich, B. (2023). *RT-2: Vision-Language-Action models transfer web knowledge to robotic control*. arXiv preprint arXiv:2307.15818.
  - Kim, M. J., Pertsch, K., Xiao, T., Goodrich, B., Lee, M. H., Sadigh, D., & Levine, S. (2024). *OpenVLA: An open-source vision-language-action model*. arXiv preprint arXiv:2406.09246.
- **Runnable Code Example**:
  - PyTorch module implementing an action tokenizer/detokenizer with continuous-to-discrete binning, out-of-bounds clipping, and inverse mapping with tensor unit tests.

---

#### Chapter 4-2: The Voice-to-Action Pipeline: Streaming Audio to Motor Intent (`4-2-voice-to-action-pipeline.mdx`)
- **Learning Objectives**:
  - Design acoustic preprocessing pipelines for high-noise humanoid platforms (beamforming, acoustic echo cancellation, motor ego-noise notch filtering).
  - Derive Connectionist Temporal Classification (CTC) loss and beam search decoding algorithms.
  - Implement low-latency streaming ASR using Whisper and NVIDIA Riva Conformer-CTC.
  - Build structured Pydantic intent parsers translating raw transcripts into validated ROS 2 Action goals.
- **Mathematical Formulations (LaTeX)**:
  - **Delay-and-Sum Beamforming**:
    $$y(t) = \sum_{m=1}^M w_m \, x_m(t - \tau_m)$$
    where $\tau_m = \frac{\mathbf{d}_m \cdot \mathbf{u}}{c}$ is the acoustic propagation delay for microphone position $\mathbf{d}_m$, target direction $\mathbf{u}$, and speed of sound $c \approx 343 \text{ m/s}$.
  - **Connectionist Temporal Classification (CTC) Loss**:
    $$\mathcal{L}_{CTC} = -\log P(\mathbf{l} \mid \mathbf{x}) = -\log \sum_{\boldsymbol{\pi} \in \mathcal{B}^{-1}(\mathbf{l})} P(\boldsymbol{\pi} \mid \mathbf{x}), \quad P(\boldsymbol{\pi} \mid \mathbf{x}) = \prod_{t=1}^T y_{\pi_t}^t$$
    where $\mathcal{B}$ is the collapse operator removing duplicate consecutive characters and blank tokens $\epsilon$.
  - **Beam Search Decoding Score**:
    $$\text{Score}(\mathbf{y}) = \sum_{t=1}^{|\mathbf{y}|} \log P(y_t \mid y_{<t}, \mathbf{x}) + \alpha \log P_{LM}(\mathbf{y}) + \beta |\mathbf{y}|$$
- **Hardware Breakdowns**:
  - Microphones: ReSpeaker USB 4-Mic Circular Array / XMOS XVF3510 voice processor with hardware AEC.
  - Compute Latency: NVIDIA Riva Conformer-CTC on Jetson Orin running with Real-Time Factor (RTF) $\le 0.03$, latency to first token $< 120 \text{ ms}$.
- **Seminal Citations**:
  - Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., & Sutskever, I. (2023). *Robust speech recognition via large-scale weak supervision*. International Conference on Machine Learning (ICML).
  - Graves, A., Fernández, S., Gomez, F., & Schmidhuber, J. (2006). *Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks*. International Conference on Machine Learning (ICML).
  - Gulati, A., Qin, J., Chiu, C. C., Parmar, N., Zhang, Y., Yu, J., ... & Pang, R. (2020). *Conformer: Convolution-augmented Transformer for speech recognition*. Interspeech.
- **Runnable Code Example**:
  - Asynchronous Python ROS 2 node using `asyncio` and `pydantic` to stream microphone audio, transcribe via local streaming Whisper, parse into a typed `RobotTaskAction` schema, and dispatch to a ROS 2 Action Server.

---

#### Chapter 4-3: Cognitive Planning & Grounding with Large Language Models (`4-3-cognitive-planning-with-llms.mdx`)
- **Learning Objectives**:
  - Solve the physical grounding problem using affordance verification and SayCan probability scoring.
  - Formulate classical symbolic planning using PDDL (Planning Domain Definition Language) and generate valid PDDL models via LLMs.
  - Construct reactive Behavior Trees (BTs) from generated task plans with dynamic error recovery.
  - Profile edge LLM inference memory footprints under 4-bit AWQ and GGUF quantization.
- **Mathematical Formulations (LaTeX)**:
  - **SayCan Joint Affordance Selection Law**:
    $$a^* = \arg\max_{a \in \mathcal{A}} \left[ \alpha \log P_{LLM}(a \mid \text{instruction}) + \beta \log P_{affordance}(a \mid \mathbf{s}) \right]$$
    where $P_{affordance}(a \mid \mathbf{s})$ is evaluated via a learned Value Function $V(s) \in [0, 1]$ or geometric reachability filter.
  - **PDDL State Transition Semantics**:
    A planning problem is a tuple $\Pi = \langle \mathcal{P}, \mathcal{A}, s_0, g \rangle$. An action $a = \langle \text{pre}(a), \text{add}(a), \text{del}(a) \rangle$ is applicable in state $s$ if $\text{pre}(a) \subseteq s$, producing next state:
    $$\delta(s, a) = (s \setminus \text{del}(a)) \cup \text{add}(a)$$
- **Hardware Breakdowns**:
  - Embedded NPU: Jetson AGX Orin 64GB running Llama 3 8B Instruct quantized to 4-bit AWQ consuming ~5.4 GB VRAM with 35 tokens/sec generation throughput.
- **Seminal Citations**:
  - Ahn, M., Brohan, A., Brown, N., Chebotar, Y., Cortes, O., David, B., ... & Zitkovich, B. (2022). *Do as I can, not as I say: Grounding language in robotic affordances*. arXiv preprint arXiv:2204.01691 (SayCan).
  - Huang, W., Abbeel, P., Pathak, D., & Mordatch, I. (2022). *Language models as zero-shot planners: Extracting actionable knowledge for embodied agents*. International Conference on Machine Learning (ICML).
  - Lin, J., Tang, J., Tang, H., Yang, S., Dang, X., & Han, S. (2023). *AWQ: Activation-aware weight quantization for LLM compression and acceleration*. arXiv preprint arXiv:2306.00978.
- **Runnable Code Example**:
  - Complete Python script generating validated PDDL problem definitions from natural language prompts, feeding them to the `pyperplan` symbolic planner, and translating the resulting plan into a PyTrees Behavior Tree.

---

#### Chapter 4-4: Multimodal Interaction: Vision, Deictic Gestures, and 3D Affordances (`4-4-multimodal-interaction.mdx`)
- **Learning Objectives**:
  - Reconcile pointing gestures and spoken deictic references (*"pick that up"*) into 3D Cartesian coordinates.
  - Formulate 3D pointing ray-casting and conical frustum object intersection in $SE(3)$.
  - Integrate Vision-Language Models (e.g., Gemini 2.5 Pro Vision API) for zero-shot object affordance reasoning.
  - Track 6-DOF object grasping frames using FoundationPose.
- **Mathematical Formulations (LaTeX)**:
  - **Camera Perspective Pinhole Projection**:
    $$\mathbf{p}_{img} = \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = \frac{1}{Z} \mathbf{K} \, \mathbf{P}_{cam}, \quad \mathbf{K} = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}$$
    Inverse projection back to 3D camera frame: $\mathbf{P}_{cam} = Z \cdot \mathbf{K}^{-1} [u, v, 1]^T$.
  - **3D Pointing Ray & Conical Scoring**:
    Normalized pointing direction from human shoulder $\mathbf{p}_s$ through index fingertip $\mathbf{p}_f$:
    $$\hat{\mathbf{d}} = \frac{\mathbf{p}_f - \mathbf{p}_s}{\|\mathbf{p}_f - \mathbf{p}_s\|}, \quad \mathbf{r}(t) = \mathbf{p}_f + t \hat{\mathbf{d}}, \; t \ge 0$$
    Candidate object score for centroid $\mathbf{o}_i$:
    $$S(\mathbf{o}_i) = w_{angle} \exp \left( -\frac{\theta_i^2}{2 \sigma_\theta^2} \right) + w_{dist} \exp \left( -\frac{(d_i^\perp)^2}{2 \sigma_d^2} \right) + w_{sem} P_{VLM}(\text{target} \mid \mathbf{I}, \mathbf{o}_i)$$
    where $\theta_i = \arccos \left( \frac{(\mathbf{o}_i - \mathbf{p}_f) \cdot \hat{\mathbf{d}}}{\|\mathbf{o}_i - \mathbf{p}_f\|} \right)$ and $d_i^\perp = \| (\mathbf{o}_i - \mathbf{p}_f) - ((\mathbf{o}_i - \mathbf{p}_f)\cdot\hat{\mathbf{d}})\hat{\mathbf{d}} \|$.
- **Hardware Breakdowns**:
  - Pan-Tilt Head: 2-DOF dynamically stabilized camera gimbal with harmonic drive servos and 19-bit absolute encoders.
  - Depth Sensors: Intel RealSense D455 stereo camera mounted on robot forehead.
- **Seminal Citations**:
  - Chen, B., Xu, Z., Kirmani, S., Ichter, B., Dai, F., & Song, S. (2024). *SpatialVLM: Endowing vision-language models with spatial reasoning capabilities*. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR).
  - Wen, B., Tremblay, J., Blukis, V., Tyree, S., Müller, T., Evans, A., ... & Fox, D. (2024). *FoundationPose: Unified 6D pose estimation and tracking of novel objects*. CVPR.
  - Kirillov, A., Mintun, E., Ravi, N., Mao, H., Rolland, C., Gustafson, L., ... & Dollár, P. (2023). *Segment anything*. IEEE/CVF International Conference on Computer Vision (ICCV).
- **Runnable Code Example**:
  - Complete Python ROS 2 node receiving human 3D skeletal keypoints from `tf2`, casting pointing rays into an organized point cloud, identifying the target candidate object, and returning its $SE(3)$ grasp transform.

---

#### Chapter 4-5: Hands-On Exercises & VLA Benchmark Evaluation (`4-5-hands-on-exercises.mdx`)
- **Learning Objectives**:
  - Execute 10 comprehensive laboratory projects spanning the full VLA stack.
  - Implement standardized robotics benchmark metrics: Task Success Rate (SR) and Success weighted by Path Length (SPL).
  - Evaluate multimodal policies against standard object datasets (YCB, Google Scanned Objects).
  - Deploy automated evaluation harnesses in simulation with randomized initial conditions.
- **Mathematical Formulations (LaTeX)**:
  - **Success weighted by Path Length (SPL)**:
    $$\text{SPL} = \frac{1}{N} \sum_{i=1}^N S_i \frac{l_i}{\max(p_i, \; l_i)}$$
    where $N$ is the number of evaluation episodes, $S_i \in \{0, 1\}$ is binary task success, $l_i$ is the shortest path ground-truth trajectory length, and $p_i$ is the actual path length traversed by the robot.
- **Hardware Breakdowns**:
  - Standardized Test Environment: 1.2m x 0.8m tabletop workspace, calibrated Franka Emika Panda arm or dual-arm Unitree humanoid torso.
  - Object Set: Standardized 77-piece YCB Object and Model Set.
- **Seminal Citations**:
  - Anderson, P., Wu, Q., Teney, D., Bruce, J., Johnson, M., Sünderhauf, N., ... & van den Hengel, A. (2018). *On evaluation measures for embodied agent search and navigation*. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR).
  - Calli, B., Walsman, A., Singh, A., Srinivasa, S., Abbeel, P., & Dollar, A. M. (2015). *Benchmarking in manipulation research: The YCB object and model set and benchmarking protocols*. IEEE Robotics & Automation Magazine, 22(3), 36-52.
- **Detailed 10-Project Blueprint Catalog**:
  1. *Project 4.1: Robot Action Tokenizer & Inverter* (Author 7-DOF discrete binning module with sub-millimeter precision).
  2. *Project 4.2: Acoustic Beamforming & Noise Suppression* (Implement 4-channel delay-and-sum beamformer for microphone array).
  3. *Project 4.3: Streaming ASR with Voice Activity Detection* (Build real-time Whisper streaming pipeline with Silero VAD).
  4. *Project 4.4: Structured Intent Parser with Pydantic* (Extract task parameters from ambiguous spoken commands).
  5. *Project 4.5: SayCan Affordance Scorer* (Evaluate value functions for 20 simulated manipulation primitives).
  6. *Project 4.6: Automated PDDL Plan Generator* (Translate natural language instructions into verifiable PDDL domains).
  7. *Project 4.7: 3D Deictic Pointing Ray Grounding* (Project human skeletal rays to select tabletop target objects).
  8. *Project 4.8: Multimodal Visual Question Answering* (Query Gemini 2.5 API with RGB-D frames for robot situational reasoning).
  9. *Project 4.9: Closed-Loop Grasp Failure Recovery* (Detect grasp slipping via tactile feedback and trigger BT re-planning).
  10. *Project 4.10: Full-Stack Voice-to-Grasp Capstone* (Execute end-to-end voice-commanded pick, carry, and place in simulation).
- **Runnable Code Example**:
  - Complete Python benchmark evaluation script running 20 randomized simulation episodes, recording trajectory execution paths, calculating SPL, and generating benchmark summary statistics.

---

### Part D: Module 4 Brand-New Chapters Blueprints (4-6 to 4-10)

#### Chapter 4-6: VLA Foundation Model Architectures: Vision Encoders to Action Heads (`4-6-foundation-model-architectures.mdx`)
- **Title**: VLA Foundation Model Architectures: Vision Encoders to Action Heads
- **Learning Objectives**:
  - Deconstruct state-of-the-art VLA architectures: OpenVLA, Octo, and $\pi_0$.
  - Evaluate vision backbones (SigLIP, DinoV2, CLIP ViT-L/14) and LLM backbones (PaLM-E, Llama 3, Gemma 2).
  - Understand action head designs: Autoregressive discrete tokens, Continuous MLPs, Diffusion heads, and Flow Matching heads.
  - Master multi-embodiment training across the Open X-Embodiment dataset (900k+ trajectories).
- **Mathematical Formulations (LaTeX)**:
  - **Vision-Language Cross-Attention Formulation**:
    Given visual patch tokens $\mathbf{X}_v \in \mathbb{R}^{N_v \times d}$ and language tokens $\mathbf{X}_l \in \mathbb{R}^{N_l \times d}$:
    $$\mathbf{Q} = \mathbf{X}_l \mathbf{W}_Q, \quad \mathbf{K} = [\mathbf{X}_l; \mathbf{X}_v] \mathbf{W}_K, \quad \mathbf{V} = [\mathbf{X}_l; \mathbf{X}_v] \mathbf{W}_V$$
    $$\text{CrossAttention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left( \frac{\mathbf{Q} \mathbf{K}^T}{\sqrt{d_k}} \right) \mathbf{V}$$
  - **Action Chunking Parameterization**:
    Instead of predicting single-step actions $a_t$, predict an action chunk horizon $H$:
    $$\mathbf{A}_{t:t+H} = [\mathbf{a}_t, \; \mathbf{a}_{t+1}, \; \dots, \; \mathbf{a}_{t+H-1}] \in \mathbb{R}^{H \times D}$$
- **Hardware Breakdowns**:
  - Training Infrastructure: 8x NVIDIA H100 SXM5 with 640 GB aggregate VRAM executing DeepSpeed ZeRO-3 and FlashAttention-2.
  - Edge Inference: NVIDIA Jetson AGX Orin running 7B parameter models with KV-cache optimization and INT4 activation quantization.
- **Seminal Citations**:
  - Padalkar, A., Pooley, A., Jain, A., Bewley, A., Herzog, A., Irpan, A., ... & Zitkovich, B. (2024). *Open X-Embodiment: Robotic learning datasets and RT-X models*. IEEE Transactions on Robotics.
  - Octo Model Team, Ghosh, D., Walke, H., Pertsch, K., Black, K., Zheng, O. Y., ... & Levine, S. (2024). *Octo: An open-source generalist robot policy*. Robotics: Science and Systems (RSS).
  - Oquab, M., Darcet, T., Moutakanni, T., Vo, H. V., Szafraniec, M., Khalidov, V., ... & Bojanowski, P. (2023). *Dinov2: Learning robust visual features without supervision*. arXiv preprint arXiv:2304.07193.
- **Runnable Code Example**:
  - Complete PyTorch neural network definition connecting a pretrained SigLIP vision transformer to a lightweight Transformer decoder with an action projection head predicting $H=16$ chunked continuous actions.

---

#### Chapter 4-7: Diffusion Policies & Flow Matching for Multimodal Robot Control (`4-7-diffusion-policies.mdx`)
- **Title**: Diffusion Policies & Flow Matching for Multimodal Robot Control
- **Learning Objectives**:
  - Derive the mathematics of score-based generative modeling (DDPM, DDIM) applied to continuous robotic action spaces.
  - Implement Diffusion Policy (Chi et al. 2023) using 1D Temporal Convolutional Networks (TCN) and Transformer backbones.
  - Formulate Continuous Flow Matching (CFM) on action manifolds and analyze the $\pi_0$ flow matching action expert.
  - Apply temporal action chunk ensembling and receding-horizon execution to guarantee smooth, jitter-free joint motions.
- **Mathematical Formulations (LaTeX)**:
  - **Denoising Diffusion Probabilistic Model (DDPM) Action Loss**:
    $$\mathcal{L}_{DDPM}(\theta) = \mathbb{E}_{t \sim \mathcal{U}(1, T), \; \mathbf{a}_0 \sim q(\mathbf{a}_0), \; \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left[ \left\| \boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta(\sqrt{\bar{\alpha}_t}\mathbf{a}_0 + \sqrt{1 - \bar{\alpha}_t}\boldsymbol{\epsilon}, \; t, \; \mathbf{c}) \right\|^2 \right]$$
    where $\mathbf{c} = f_{enc}(\mathbf{I}, \mathbf{l})$ is the conditioning embedding.
  - **Conditional Flow Matching (CFM) Formulation ($\pi_0$)**:
    Let linear probability path between Gaussian noise $x_0 \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ and data $x_1 = \mathbf{a}$ be:
    $$x_t = (1 - t) x_0 + t x_1, \quad t \in [0, 1]$$
    The target vector field is $u_t(x \mid x_1) = x_1 - x_0$. The CFM training objective is:
    $$\mathcal{L}_{CFM}(\theta) = \mathbb{E}_{t, x_0, x_1} \left[ \left\| v_\theta(x_t, t, \mathbf{c}) - (x_1 - x_0) \right\|^2 \right]$$
  - **Temporal Ensembling Weighting**:
    Overlapping action predictions for time $t$ from historical prediction chunks are blended via exponential weights:
    $$\hat{\mathbf{a}}_t = \frac{\sum_{i=1}^m w_i \mathbf{a}_t^{(i)}}{\sum_{i=1}^m w_i}, \quad w_i = \exp(-k \cdot (t - t_0^{(i)}))$$
- **Hardware Breakdowns**:
  - Control Frequency: 50 Hz closed-loop inference loop running 10-step DPM-Solver or Euler integration on Jetson AGX Orin Tensor Cores.
- **Seminal Citations**:
  - Chi, C., Feng, S., Pan, Y., Eric, Z., Cousineau, N., Burchfiel, B., & Song, S. (2023). *Diffusion policy: Visuomotor policy learning via action diffusion*. Robotics: Science and Systems (RSS).
  - Lipman, Y., Chen, R. T., Ben-Hamu, H., Nicklas, M., & Le, M. (2022). *Flow matching for generative modeling*. arXiv preprint arXiv:2210.02747.
  - Black, K., Wang, Z., Wan, W., Shen, B., Le, M., & Levine, S. (2024). *$\pi_0$: A Vision-Language-Action Flow Model for Generalist Robotics*. Physical Intelligence Technical Report.
- **Runnable Code Example**:
  - Complete, self-contained PyTorch implementation of a 1D Temporal U-Net Diffusion Policy training loop with Conditional Flow Matching vector field inference.

---

#### Chapter 4-8: Imitation Learning, Action Chunking (ACT) & Teleoperation (`4-8-imitation-learning.mdx`)
- **Title**: Imitation Learning, Action Chunking (ACT) & Teleoperation
- **Learning Objectives**:
  - Analyze compounding errors in behavioral cloning ($O(T^2)$ error bound) and understand DAgger mitigation.
  - Master humanoid teleoperation setups: bilateral exoskeletons, SpaceMouse, and spatial trackers (Apple Vision Pro, Meta Quest 3).
  - Implement Action Chunking with Transformers (ACT) using Conditional Variational Autoencoders (CVAE).
  - Leverage Hugging Face's LeRobot framework for standardized dataset recording, training, and deployment.
- **Mathematical Formulations (LaTeX)**:
  - **Behavioral Cloning Compounding Error Bound (Ross & Bagnell)**:
    Under $T$-step horizon with single-step error rate $\epsilon$:
    $$\mathbb{E} \left[ \sum_{t=1}^T c(s_t, \pi_\theta(s_t)) \right] \le C_{max} \cdot \epsilon T^2$$
  - **ACT Conditional Variational Autoencoder (CVAE) Loss**:
    $$\mathcal{L}_{ACT}(\theta, \phi) = \sum_{t=1}^k \left\| \mathbf{a}_t - \hat{\mathbf{a}}_t \right\|_1 + \beta \cdot D_{KL}\left( q_\phi(\mathbf{z} \mid \mathbf{a}_{1:k}, \bar{\mathbf{o}}) \;\Big\|\; p(\mathbf{z} \mid \bar{\mathbf{o}}) \right)$$
    where latent variable $\mathbf{z} \sim \mathcal{N}(\boldsymbol{\mu}_\phi, \boldsymbol{\Sigma}_\phi)$ encodes high-level motion style, and prior $p(\mathbf{z} \mid \bar{\mathbf{o}}) = \mathcal{N}(\mathbf{0}, \mathbf{I})$ during inference.
- **Hardware Breakdowns**:
  - Teleoperation Hardware: Dual GELLO 7-DOF passive exoskeleton arms or dual 3Dconnexion SpaceMouse Pro controllers; Apple Vision Pro WebRTC teleoperation bridge streaming spatial hand poses at 90 Hz.
  - Dataset Storage: High-throughput NVMe RAID storing HDF5 demonstration episodes with multi-view 1080p video streams.
- **Seminal Citations**:
  - Zhao, T. Z., Kumar, V., Levine, S., & Finn, C. (2023). *Learning fine-grained bimanual manipulation with low-cost hardware*. arXiv preprint arXiv:2304.13705 (ACT).
  - Ross, S., Gordon, G., & Bagnell, D. (2011). *A reduction of imitation learning and structured prediction to no-regret online learning*. Proceedings of the Fourteenth International Conference on Artificial Intelligence and Statistics (AISTATS).
  - Cadene, R., Alibert, S., Tuleu, A., & Wolf, T. (2024). *LeRobot: State-of-the-art machine learning for real-world robotics in PyTorch*. Hugging Face.
- **Runnable Code Example**:
  - Complete PyTorch training script implementing the ACT CVAE loss, transformer encoder-decoder action chunk predictor, and HDF5 demonstration loader.

---

#### Chapter 4-9: Reward Shaping, Preference Learning & RL from AI Feedback (RLAIF) (`4-9-reward-shaping-and-rlaif.mdx`)
- **Title**: Reward Shaping, Preference Learning & RL from AI Feedback (RLAIF)
- **Learning Objectives**:
  - Understand the limitations of manual reward engineering for complex humanoid skills.
  - Formulate preference learning using the Bradley-Terry ranking model for robot trajectory comparisons.
  - Implement Reinforcement Learning from AI Feedback (RLAIF) using multimodal LLMs as automated code and reward critics (Eureka / DrEureka).
  - Enforce formal safety constraints using Control Barrier Functions (CBFs) in reward optimization.
- **Mathematical Formulations (LaTeX)**:
  - **Bradley-Terry Trajectory Preference Model**:
    The probability that trajectory $\tau_1$ is preferred to $\tau_2$ given learned reward model $R_\psi$:
    $$P(\tau_1 \succ \tau_2) = \frac{\exp\left(\sum_{t} R_\psi(s_t^1, a_t^1)\right)}{\exp\left(\sum_{t} R_\psi(s_t^1, a_t^1)\right) + \exp\left(\sum_{t} R_\psi(s_t^2, a_t^2)\right)}$$
    Cross-entropy loss over human preference dataset $\mathcal{D}$:
    $$\mathcal{L}_{pref}(\psi) = -\mathbb{E}_{(\tau_1, \tau_2, y) \sim \mathcal{D}} \left[ y \log P(\tau_1 \succ \tau_2) + (1 - y) \log P(\tau_2 \succ \tau_1) \right]$$
  - **Control Barrier Function (CBF) Safety Constraint**:
    For safe set $\mathcal{C} = \{s \mid h(s) \ge 0\}$, dynamic safety is guaranteed if:
    $$\dot{h}(s, a) \ge -\gamma(h(s)), \quad \gamma > 0$$
- **Hardware Breakdowns**:
  - Evaluator Rig: Cloud GPU cluster running parallel Isaac Lab simulation instances evaluating candidate reward functions generated by LLM critics in real time.
- **Seminal Citations**:
  - Ma, Y. J., Liang, W., Wang, G., Huang, D. A., Bastani, O., Jayaraman, D., ... & Fan, L. (2023). *Eureka: Human-level reward design via coding large language models*. arXiv preprint arXiv:2310.12931.
  - Christiano, P. F., Leike, J., Brown, T., Martic, M., Legg, S., & Amodei, D. (2017). *Deep reinforcement learning from human preferences*. Advances in Neural Information Processing Systems (NeurIPS).
  - Ames, A. D., Xu, X., Grizzle, J. W., & Tabuada, P. (2016). *Control barrier function based quadratic programming with application to bipedal robotic walking*. IEEE Transactions on Automatic Control, 62(8), 3861-3876.
- **Runnable Code Example**:
  - Python script orchestrating an automated RLAIF loop: querying Gemini 2.5 API with simulation telemetry, generating refined reward functions, and evaluating PPO training curves.

---

#### Chapter 4-10: Production VLA Deployment, Safety Filtering & Out-of-Distribution Detection (`4-10-deployment-and-safety.mdx`)
- **Title**: Production VLA Deployment, Safety Filtering & Out-of-Distribution Detection
- **Learning Objectives**:
  - Architect robust closed-loop execution systems bridging neural foundation policies and deterministic hardware interfaces.
  - Implement real-time Out-of-Distribution (OOD) visual detection using Monte Carlo Dropout and predictive entropy.
  - Construct kinematic and dynamic safety filter shields enforcing joint limits, velocity caps, and collision envelopes.
  - Evaluate end-to-end VLA autonomy on industrial benchmarks: LIBERO, RoboSuite, and AgiBot World.
- **Mathematical Formulations (LaTeX)**:
  - **Predictive Entropy for Epistemic Uncertainty Quantification**:
    Given $M$ stochastic forward passes with Monte Carlo Dropout $\mathbf{W}^{(m)} \sim q(\mathbf{W})$:
    $$\bar{p}_c = \frac{1}{M} \sum_{m=1}^M P(y = c \mid \mathbf{x}, \mathbf{W}^{(m)})$$
    $$\mathcal{H}[\mathbf{y} \mid \mathbf{x}, \mathcal{D}] = -\sum_{c=1}^C \bar{p}_c \log \bar{p}_c$$
    If $\mathcal{H}[\mathbf{y} \mid \mathbf{x}, \mathcal{D}] > H_{threshold}$, the safety supervisor halts motor dispatch and triggers conversational clarification.
  - **Kinematic Shielding Quadratic Program (QP)**:
    $$\min_{\mathbf{u} \in \mathbb{R}^n} \frac{1}{2} \|\mathbf{u} - \mathbf{u}_{VLA}\|^2 \quad \text{s.t.} \quad \mathbf{q}_{min} \le \mathbf{q} + \mathbf{u} \Delta t \le \mathbf{q}_{max}, \quad |\mathbf{u}| \le \dot{\mathbf{q}}_{max}, \quad \mathbf{J}_c \mathbf{u} \ge -\eta (\mathbf{d} - d_{safe})$$
- **Hardware Breakdowns**:
  - Safety Hardware: Dual-channel Category 3 / PL d functional safety interlock relays (Pilz PNOZ) connected to hardware dynamic motor braking circuits.
  - Onboard Telemetry: Real-time black-box flight recorder logging 1 kHz joint states and camera frames to NVMe storage.
- **Seminal Citations**:
  - Gal, Y., & Ghahramani, Z. (2016). *Dropout as a Bayesian approximation: Representing model uncertainty in deep learning*. International Conference on Machine Learning (ICML).
  - Liu, B., Liu, Y., Zhu, X., & Stone, P. (2023). *LIBERO: Benchmarking knowledge transfer for lifelong robot learning*. Advances in Neural Information Processing Systems (NeurIPS).
  - ISO. (2016). *ISO/TS 15066:2016 Robots and robotic devices — Collaborative robots*. International Organization for Standardization.
- **Runnable Code Example**:
  - Complete C++ real-time safety filter wrapper node intercepting incoming VLA action vectors, solving a quadratic program (OSQP) to enforce joint velocity/torque/collision limits, and publishing safe `trajectory_msgs/JointTrajectory` commands.

---

## 5. Verification Method

To verify these blueprints independently and validate future chapter authoring:

1. **KaTeX Delimiter Syntax Compliance**:
   - Verify every mathematical formula uses either `$ ... $` (inline) or `$$ ... $$` (block).
   - Verify no unescaped curly braces exist in raw markdown headings or text (e.g., use `$\{q_i\}_{i=1}^N$` or code blocks).
2. **Docusaurus Static Compilation**:
   - Run `npm run build` in the repository root. Static production assets must compile with zero broken links, zero JSX reference errors, and clean KaTeX rendering.
3. **Backend Service Integrity**:
   - Run `pytest` across `backend/tests/` to guarantee mock vector retrieval and SSE streaming remain intact.
   - Run `ruff check .` to verify zero Python linting or syntax errors.
4. **Invalidation Conditions**:
   - Any chapter authored without explicit LaTeX mathematical derivations ($...$ and $$...$$).
   - Any chapter omitting concrete hardware silicon/sensor breakdowns.
   - Any chapter lacking peer-reviewed research citations (author, year, title, venue).
   - Any chapter including non-runnable pseudo-code rather than syntactically valid code blocks.
