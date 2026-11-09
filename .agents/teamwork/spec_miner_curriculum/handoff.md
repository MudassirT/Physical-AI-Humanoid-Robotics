# Curriculum Expansion Specification Mining Report (v4.0 Definitive Inventory)

**State Folder**: `C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\spec_miner_curriculum\`  
**Date**: 2026-11-09T14:25:00Z  
**Author**: Specification Miner Agent  
**Parent Conversation ID**: `9c96a791-1769-4c88-9445-500c157ed676`  
**Authoritative Sources**:
1. `specs/010-master-plan-curriculum-expansion/spec.md`
2. `C:\Users\DELL\.gemini\antigravity-cli\brain\98ff215b-a62a-4d37-839f-7c685594be36\ULTRA_PRO_MAX_MASTER_PLAN.md`
3. `C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\ORIGINAL_REQUEST.md`
4. Codebase inspection of `ai-book-docs/`, `package.json`, `docusaurus.config.ts`, `backend/`

---

## 1. Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Phase 1: M1 Depth | Module 1 Existing Enhancements | Graduate-level deepening of 10 existing ROS 2 chapters | Existing MDX files (1-1 to 1-10) | Enhanced MDX chapters with DDS math, RTPS traces, SROS2, and schedulers | MDX syntax error if KaTeX/Mermaid malformed | `spec.md` § Phase 1, `ULTRA_PRO_MAX` § Phase 1 |
| 2 | Phase 1: M1 New | Module 1 Expansion (4 chapters) | 4 new chapters (`1-11` to `1-14`) covering ros2_control, DDS internals, PREEMPT_RT, and diagnostics | Hardware interface specs, kernel configs, tracing metrics | `1-11` through `1-14` MDX files | Missing RT kernel symbols, EtherCAT sync timeouts | `spec.md` § Module 1, `ULTRA_PRO_MAX` § Module 1 |
| 3 | Phase 1: M2 Depth | Module 2 Existing Enhancements | Deepening 5 Gazebo/Unity chapters with LCP contact physics, IMU Allan deviation, and shader graphs | Existing MDX files (2-1 to 2-5) | Enhanced MDX chapters with LCP math, noise modeling, and evaluation rubrics | Solver divergence on singular mass matrices | `spec.md` § Phase 1, `ULTRA_PRO_MAX` § Module 2 |
| 4 | Phase 1: M2 New | Module 2 Expansion (5 chapters) | 5 new chapters (`2-6` to `2-10`) covering URDF/SDF, Featherstone ABA, SDG Replicator, Drake/MuJoCo, and DT loop | CAD meshes, multi-body kinematics, Isaac Replicator graphs | `2-6` through `2-10` MDX files | Penetration depth explosion, non-convex mesh collisions | `spec.md` § Module 2, `ULTRA_PRO_MAX` § Module 2 |
| 5 | Phase 1: M3 Depth | Module 3 Existing Enhancements | Deepening 5 NVIDIA Isaac chapters with CUDA architecture, PhysX 5 articulations, and Capture Point math | Existing MDX files (3-1 to 3-5) | Enhanced MDX chapters with Jetson benchmarks, NITROS memory maps, and 3D grid maps | Memory copy thrashing, VSLAM feature tracking loss | `spec.md` § Phase 1, `ULTRA_PRO_MAX` § Module 3 |
| 6 | Phase 1: M3 New | Module 3 Expansion (5 chapters) | 5 new chapters (`3-6` to `3-10`) covering cuVSLAM, semantic segmentation (SAM 2), F/T sensing, sensor fusion (UKF/Factor Graph), and TensorRT FP8 deployment | Stereo pairs, 6-axis F/T loads, point clouds, ONNX models | `3-6` through `3-10` MDX files | Degenerate feature geometry, INT8 quantization drift | `spec.md` § Module 3, `ULTRA_PRO_MAX` § Module 3 |
| 7 | Phase 1: M4 Depth | Module 4 Existing Enhancements | Deepening 5 VLA chapters with RT-1/2/π0 timeline, Whisper latency, SayCan CoT, and SpatialVLM | Existing MDX files (4-1 to 4-5) | Enhanced MDX chapters with flow matching math, token schemas, and PDDL generation | Out-of-vocabulary action tokens, hallucinated affordances | `spec.md` § Phase 1, `ULTRA_PRO_MAX` § Module 4 |
| 8 | Phase 1: M4 New | Module 4 Expansion (5 chapters) | 5 new chapters (`4-6` to `4-10`) covering Foundation Architectures, Diffusion Policies, ACT Imitation, RLAIF, and Safe Deployment | Open X-Embodiment dataset, multi-modal prompt, robot state | `4-6` through `4-10` MDX files | Compounding covariate shift, diffusion generation latency | `spec.md` § Module 4, `ULTRA_PRO_MAX` § Module 4 |
| 9 | Phase 2: M6 New | Module 6 Bipedal Locomotion (10 chapters) | Definitive 10-chapter module (`6-1` to `6-10`) covering ZMP, 3D-LIPM, Capture Point/DCM, Convex MPC, Whole-Body QP Control, RL (`legged_gym`), Sim-to-Real, Parkour, Biomechanics, and MoCap AMP | Floating-base states, ground contact forces, heightmaps | 10 new MDX files in `module6-bipedal-locomotion/` | Dynamic tipping, foot slip, friction cone violation | `spec.md` § Module 6, `ULTRA_PRO_MAX` § Module 6 |
| 10 | Phase 2: M7 New | Module 7 Dexterous Manipulation (8 chapters) | 8-chapter module (`7-1` to `7-8`) covering Grasp Theory, Hand Design, GelSight Tactile Sensing, MoveIt 2 / TAMP, Learning (ACT/Bi-DexHands), Peg-in-Hole Assembly, and Benchmarks | Multi-finger kinematics, tactile images, object poses | 8 new MDX files in `module7-dexterous-manipulation/` | Force-closure infeasibility, peg wedging/jamming | `spec.md` § Module 7, `ULTRA_PRO_MAX` § Module 7 |
| 11 | Phase 2: M8 New | Module 8 Robot Learning & RL (10 chapters) | 10-chapter module (`8-1` to `8-10`) covering MDP/Bellman, PPO/SAC/TD3, Continuous Control, Parallel Isaac Lab, Curriculum Learning, Offline RL (CQL/IQL), Model-Based (Dreamer V3), Meta-RL (MAML), Safe RL (CBF), and Evaluation | Environmental state, reward functions, demonstrations | 10 new MDX files in `module8-robot-learning/` | Reward hacking, policy collapse, unsafe joint velocity | `spec.md` § Module 8, `ULTRA_PRO_MAX` § Module 8 |
| 12 | Phase 2: M9 New | Module 9 Sim-to-Real Transfer (8 chapters) | 8-chapter module (`9-1` to `9-8`) covering Reality Gap metrics, Domain Randomization (ADR), System Identification (LuGre), Privileged Learning (RMA), Adaptation Modules, Real-World Fine-Tuning, Transfer Benchmarks, and Digital Twin Loops | Real telemetry, sim states, excitation trajectories | 8 new MDX files in `module9-sim-to-real/` | Policy transfer collapse, unmodeled actuator delay | `spec.md` § Module 9, `ULTRA_PRO_MAX` § Module 9 |
| 13 | Phase 2: M10 New | Module 10 Hardware Architecture (8 chapters) | 8-chapter module (`10-1` to `10-8`) covering Humanoid Mechanical Design, Actuators (QDD/Harmonic/SEA), FOC & SVPWM Motor Control, EtherCAT/CAN-FD, Jetson Compute, Sensor Hardware, FreeRTOS Firmware, and System Bring-up | Power budgets, motor curves, bus timing, thermal limits | 8 new MDX files in `module10-hardware-architecture/` | Bus contention, gate driver shoot-through, thermal trip | `spec.md` § Module 10, `ULTRA_PRO_MAX` § Module 10 |
| 14 | Phase 2: M11 New | Module 11 Safety, Ethics & Deployment (6 chapters) | 6-chapter module (`11-1` to `11-6`) covering ISO Standards (10218, 15066, 13849), SIL 1-4 Architecture, Momentum Observer pHRI, AI Ethics & Law, Differential Privacy, and Fleet DevOps (OTA/Grafana) | Collision forces, risk matrices, telemetry streams | 6 new MDX files in `module11-safety-ethics/` | Dangerous failure without diagnostic coverage, ISO breach | `spec.md` § Module 11, `ULTRA_PRO_MAX` § Module 11 |
| 15 | Phase 2: M12 New | Module 12 Capstone & Frontiers (6 chapters) | 6-chapter module (`12-1` to `12-6`) covering 4 Full-Stack Capstone Projects, Research Frontiers in Locomotion, Embodied AI World Models (3DGS/GR00T), Future Roadmap 2030, Open-Source Contributions, and Annotated 200+ Bibliography | End-to-end task specs, research papers, community datasets | 6 new MDX files in `module12-capstone-frontiers/` | Infeasible student scope, broken external URLs | `spec.md` § Module 12, `ULTRA_PRO_MAX` § Module 12 |
| 16 | Phase 3: Backend | Streaming SSE & Telemetry Services | FastAPI endpoints `/ask` (SSE token streaming), `/analytics` (usage metrics), and module-filtered Qdrant retrieval | HTTP requests with user questions and module filters | Server-Sent Event stream, JSON analytics, filtered vector results | Vector store timeout, invalid module ID fallback | `spec.md` § R3, `ULTRA_PRO_MAX` § Phase 3 |
| 17 | Phase 3: Frontend | Docusaurus Navigation & Interactive Components | Autogenerated or explicit sidebar wiring all 12 modules, KaTeX math integration, `<Quiz>` engine, and `<ChapterProgress>` tracker | MDX documentation tags, user localStorage interaction | Rendered interactive UI, math equations, completion rings | MDX JSX compilation errors on raw math symbols | `spec.md` § R3, `ULTRA_PRO_MAX` § Phase 3 |

---

## 2. Edge Cases

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | KaTeX Syntax in MDX | Inline `$R \in SO(3)$` with unescaped curly brackets `{3x3}` or `<` | In MDX v3, curly braces outside code blocks or KaTeX plugins are parsed as JSX expressions, throwing build errors (`Unexpected token`). Must be wrapped inside code fences or configured with `remark-math` + `rehype-katex`. |
| 2 | Existing Module 5 Status | Requesting creation of Module 5 | `module5-kinematics-dynamics` was already authored in v2.3 with 10 complete chapters (`5-1` to `5-10`). Re-authoring would overwrite completed work. Phase 2 strictly targets Modules 6 through 12. |
| 3 | Docusaurus Sidebar Autogeneration | New module directories without `_category_.json` | Docusaurus defaults to directory names without order. Each new module directory (`module6` through `module12`) requires a `_category_.json` specifying `label` and `position` (6 to 12). |
| 4 | Large Python/C++ Code Snippets | Scripts exceeding 100 lines inside MDX | Docusaurus Prism syntax highlighter handles long code blocks cleanly, but tabs/spaces must remain consistent to avoid markdown indentation confusion. |
| 5 | Interactive MDX Components | Rendering `<Quiz id="6-2-zmp" />` before component is created | MDX compiler throws `ReferenceError: Quiz is not defined` if `<Quiz />` is placed in MDX without a global MDX component provider or explicit import. |
| 6 | Unit Testing without External Services | `pytest` run against `/ask` or Qdrant | Test suite must mock `openai.AsyncOpenAI` and `qdrant_client.QdrantClient` so CI/local builds pass without live network credentials. |

---

## 3. Phase 1 (M1–M4): Deepen Existing Modules Inventory

### 3.1 Existing 25 Chapters to Enhance in M1, M2, M3, M4

#### Module 1: The Robotic Nervous System (ROS 2) — 10 Existing Chapters
1. **`ai-book-docs/module1-ros2/1-1-introduction.mdx`**
   - **Current Title**: Introduction to the Robotic Nervous System
   - **Mathematical Derivations**: Network bandwidth calculation for humanoid telemetry:
     $$\text{Bandwidth (Mbps)} = \sum_{i=1}^N f_i \times S_i \times 8 \times 10^{-6}$$
     where $f_i$ is sampling frequency (1 kHz joint state, 60 Hz dual 1080p RGB-D), and $S_i$ is serialized payload size in bytes.
   - **Hardware Breakdowns**: Communication channel bandwidth: 1 Gbps onboard Ethernet vs 100 Mbps EtherCAT vs 8 Mbps CAN-FD.
   - **Research Citations**: Quigley et al. (2009) *ROS: an open-source Robot Operating System*; Macenski et al. (2022) *Robot Operating System 2: Design, architecture, and uses in the wild* (Science Robotics).
   - **Code Examples**: Complete Python telemetry calculation script computing total system network load and buffer sizing.

2. **`ai-book-docs/module1-ros2/1-2-ros2-core-concepts.mdx`**
   - **Current Title**: Core Concepts & Communication Primitives
   - **Mathematical Derivations**: RTPS wire-level reliability protocol: ACKNACK sequence window probability of packet loss; DDS discovery message overhead.
   - **Hardware Breakdowns**: Network Interface Cards (NIC), Ethernet PHY transceivers, hardware multicast filtering on robot switch.
   - **Research Citations**: OMG DDS v1.4 Specification; DDSI-RTPS v2.3 Protocol Standard.
   - **Code Examples**: Complete QoS profile definition in Python and C++ demonstrating `ReliabilityPolicy.BEST_EFFORT` for 1 kHz IMU streams vs `DURABILITY_TRANSIENT_LOCAL` for PID gain parameters.

3. **`ai-book-docs/module1-ros2/1-3-ros2-workspace.mdx`**
   - **Current Title**: Workspace Setup & Modern Build Systems
   - **Mathematical Derivations**: Dependency graph resolution acyclic verification; compilation time scaling $O(V + E)$ in Colcon build execution.
   - **Hardware Breakdowns**: ARM64 cross-compilation toolchains targeting NVIDIA Jetson AGX Orin (Cortex-A78AE).
   - **Research Citations**: Colcon Architecture RFC; Open Robotics REP-2000 (ROS 2 Releases and Target Platforms).
   - **Code Examples**: `devcontainer.json` and Dockerfile for multi-stage ARM64 cross-compilation with `colcon build --symlink-install --mixin release`.

4. **`ai-book-docs/module1-ros2/1-4-nodes.mdx`**
   - **Current Title**: Execution Models & Node Architecture
   - **Mathematical Derivations**: Worst-Case Execution Time (WCET) bounds under SingleThreaded vs MultiThreaded vs StaticSingleThreaded executors; queuing delay under Poisson message arrivals.
   - **Hardware Breakdowns**: Symmetric Multi-Processing (SMP) CPU core assignment, cache line bouncing, L1/L2 cache misses during context switches.
   - **Research Citations**: Casini et al. (2019) *Response-Time Analysis of ROS 2 Processing Chains under Reservation-Based Scheduling*; Blass et al. (2021).
   - **Code Examples**: Multi-threaded C++ node isolating real-time balance control callbacks in a `MutuallyExclusive` callback group with dedicated executor thread.

5. **`ai-book-docs/module1-ros2/1-5-topics.mdx`**
   - **Current Title**: Topics & Zero-Copy Middleware
   - **Mathematical Derivations**: Latency comparison model: standard TCP loopback vs POSIX shared memory ring buffers; serialized CDR alignment math.
   - **Hardware Breakdowns**: DMA controller, unified memory architecture (UMA) on Jetson AGX Orin vs discrete GPU PCIe bus bottlenecks.
   - **Research Citations**: Staschulat et al. (2021) *Complete Latency Analysis of Message Communication in ROS 2*; Eclipse Iceoryx True Zero-Copy Architecture.
   - **Code Examples**: Runnable C++ ROS 2 publisher using `rclcpp::LoanedMessage` and Iceoryx shared memory for 60 Hz 4K point cloud publishing.

6. **`ai-book-docs/module1-ros2/1-6-services.mdx`**
   - **Current Title**: Services & Remote Procedure Calls
   - **Mathematical Derivations**: Exponential backoff and jitter formula:
     $$T_{retry} = \min(T_{max}, T_{base} \times 2^{k}) + \text{Uniform}(0, \delta)$$
   - **Hardware Breakdowns**: Power Distribution Unit (PDU) relays, contactors, actuator bus pre-charge circuits triggered via service calls.
   - **Research Citations**: Pardo-Castellote (2001) *OMG Data-Distribution Service: Architectural Overview*.
   - **Code Examples**: Asynchronous C++ ROS 2 service client with deadline timers, non-blocking `future.wait_for`, and timeout cancellation.

7. **`ai-book-docs/module1-ros2/1-7-actions.mdx`**
   - **Current Title**: Actions & Long-Horizon Goal Execution
   - **Mathematical Derivations**: Finite State Machine (FSM) reachability matrix; feedback throttling frequency divider formula:
     $$f_{feedback} = \frac{f_{control}}{K_{div}}$$
   - **Hardware Breakdowns**: Bipedal footstep execution hardware interlocks; emergency braking solenoids.
   - **Research Citations**: Open Robotics Action Design REP-141; Sentis et al. (2010).
   - **Code Examples**: Full ROS 2 action server in Python managing a `NavigateFootsteps.action` goal with preemption, live progress feedback, and abort triggers.

8. **`ai-book-docs/module1-ros2/1-8-parameters.mdx`**
   - **Current Title**: Parameters & Dynamic Reconfiguration
   - **Mathematical Derivations**: PID controller discretization (bilinear Tustin transform):
     $$u[k] = u[k-1] + K_p (e[k] - e[k-1]) + K_i \frac{T_s}{2} (e[k] + e[k-1]) + \frac{K_d}{T_s} (e[k] - 2e[k-1] + e[k-2])$$
   - **Hardware Breakdowns**: Actuator digital signal processors (DSP), non-volatile EEPROM gain storage.
   - **Research Citations**: Ang, Chong, & Li (2005) *PID control system analysis, design, and technology*.
   - **Code Examples**: Parameter callback node validating joint limits and dynamically updating PID stiffness/damping gains without dropping control cycles.

9. **`ai-book-docs/module1-ros2/1-9-rclpy-rclcpp.mdx`**
   - **Current Title**: Client Libraries (rclcpp vs rclpy)
   - **Mathematical Derivations**: Python Global Interpreter Lock (GIL) latency jitter distribution; C++ memory allocation latency histogram ($O(1)$ pool vs $O(N)$ heap).
   - **Hardware Breakdowns**: Real-time POSIX timers (`timer_create`, `CLOCK_MONOTONIC_RAW`), MMU page fault traps.
   - **Research Citations**: Barbalace et al. (2008) *Real-Time Extensions for Python: A Survey*; Real-Time Linux Collaborative Project (Linux Foundation).
   - **Code Examples**: Real-time C++ node using `mlockall(MCL_CURRENT | MCL_FUTURE)`, `sched_setscheduler(SCHED_FIFO, 98)`, and custom TLSF static memory allocator.

10. **`ai-book-docs/module1-ros2/1-10-best-practices.mdx`**
    - **Current Title**: Production Best Practices & SROS2
    - **Mathematical Derivations**: Elliptic Curve Cryptography (ECDSA P-256) encryption overhead and signature verification latency bounds.
    - **Hardware Breakdowns**: Hardware Security Modules (HSM), TPM 2.0 chips on industrial humanoid SBCs.
    - **Research Citations**: White et al. (2019) *SROS2: Usable Cyber Security Tools for Mechanism Design in Robotics*; NIST SP 800-57.
    - **Code Examples**: End-to-end SROS2 PKI governance generation script (`sros2 create_keystore`, `create_enclave`) and automated policy enforcement profile.

---

#### Module 2: The Digital Twin (Gazebo & Unity) — 5 Existing Chapters
1. **`ai-book-docs/module2-digital-twin/2-1-introduction-to-digital-twins.mdx`**
   - **Current Title**: Introduction to Digital Twins & Co-Simulation
   - **Mathematical Derivations**: Co-simulation latency budget inequality:
     $$\Delta t_{sim\_step} \le \Delta t_{wall\_clock} - (\tau_{transport} + \tau_{render} + \tau_{bridge})$$
   - **Hardware Breakdowns**: GPU rendering nodes (NVIDIA RTX 4090 / L40S) vs physics server compute blades; 10GbE co-sim bridge interfaces.
   - **Research Citations**: Grieves & Vickers (2017) *Digital Twin: Mitigating Unpredictable, Undesirable Emergent Behavior in Complex Systems*; ISO 23247.
   - **Code Examples**: Co-simulation latency benchmark script measuring jitter between Gazebo physics clock and external ROS 2 controller.

2. **`ai-book-docs/module2-digital-twin/2-2-gazebo-simulation-engine.mdx`**
   - **Current Title**: Physics Engines & Gazebo Harmonic Architecture
   - **Mathematical Derivations**: Linear Complementarity Problem (LCP) formulation for rigid body contact:
     $$\mathbf{w} = \mathbf{A} \boldsymbol{\lambda} + \mathbf{b}, \quad \mathbf{w} \ge 0, \quad \boldsymbol{\lambda} \ge 0, \quad \mathbf{w}^T \boldsymbol{\lambda} = 0$$
     Coulomb friction pyramid cone linearization.
   - **Hardware Breakdowns**: Multi-core CPU cache alignment for spatial tree traversals; SIMD AVX-512 acceleration in ODE/DART.
   - **Research Citations**: Featherstone (2008) *Rigid Body Dynamics Algorithms*; Stewart & Trinkle (1996) *An implicit time-stepping method for rigid body dynamics with inelastic collisions and Coulomb friction*.
   - **Code Examples**: Gazebo Harmonic world SDF configuration with custom DART solver parameters (iterations, step size `0.001`, sor factor).

3. **`ai-book-docs/module2-digital-twin/2-3-sensor-simulation.mdx`**
   - **Current Title**: High-Fidelity Sensor Simulation
   - **Mathematical Derivations**: Continuous-time IMU stochastic noise model:
     $$\tilde{\boldsymbol{\omega}}(t) = \boldsymbol{\omega}(t) + \mathbf{b}(t) + \boldsymbol{\eta}_v(t), \quad \dot{\mathbf{b}}(t) = \boldsymbol{\eta}_u(t)$$
     Allan variance random walk and bias instability parameters.
   - **Hardware Breakdowns**: Optical sensors (CMOS rolling vs global shutter), MEMS capacitive accelerometers.
   - **Research Citations**: Woodman (2007) *An introduction to inertial navigation*; El-Sheimy et al. (2008).
   - **Code Examples**: Python script injecting calibrated Gaussian white noise, random walk bias, and beam-divergence dropouts into simulated LiDAR data.

4. **`ai-book-docs/module2-digital-twin/2-4-unity-for-high-fidelity-visuals.mdx`**
   - **Current Title**: Photorealistic Simulation with Unity HDRP
   - **Mathematical Derivations**: Coordinate frame transformation between ROS (Right-Handed Z-Up) and Unity (Left-Handed Y-Up):
     $$\mathbf{p}_{ROS} = \begin{bmatrix} 0 & 0 & 1 \\ -1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix} \mathbf{p}_{Unity}$$
   - **Hardware Breakdowns**: Real-time ray-tracing RT Cores, DLSS 3.5 tensor frame generation on workstation GPUs.
   - **Research Citations**: Unity Technologies (2020) *Robotics Perception Package Architecture*; Juliani et al. (2018) *Unity: A General Platform for Intelligent Agents*.
   - **Code Examples**: C# Unity component integrating `ROS-TCP-Connector` to stream synthetic RGB-D images and ground-truth bounding box metadata over ROS 2 topics.

5. **`ai-book-docs/module2-digital-twin/2-5-hands-on-exercises.mdx`**
   - **Current Title**: Hands-On Exercises & Lab Verification
   - **Mathematical Derivations**: Tracking error Root Mean Square Error (RMSE) metric and energy expenditure integral.
   - **Hardware Breakdowns**: HIL interface cards, virtual CAN adapters (`vcan0`).
   - **Research Citations**: ASME V&V 40 (Verification and Validation in Computational Modeling).
   - **Code Examples**: Automated Python grading harness validating robot gait stability, tip-over margin, and ground reaction force feasibility in Gazebo.

---

#### Module 3: The AI-Robot Brain (NVIDIA Isaac) — 5 Existing Chapters
1. **`ai-book-docs/module3-ai-robot-brain/3-1-introduction-to-isaac-platform.mdx`**
   - **Current Title**: Introduction to NVIDIA Isaac Platform
   - **Mathematical Derivations**: Roofline computational model for Jetson Orin compute engines:
     $$\text{Operational Intensity} = \frac{\text{FLOPs}}{\text{DRAM Bytes Loaded}}$$
   - **Hardware Breakdowns**: NVIDIA Jetson family teardown: Orin Nano (40 TOPS) vs Orin NX (100 TOPS) vs AGX Orin (275 TOPS) vs Thor (2000+ FP4 TOPS); Deep Learning Accelerators (DLA).
   - **Research Citations**: NVIDIA Corporation (2022) *NVIDIA Jetson AGX Orin Architecture Whitepaper*.
   - **Code Examples**: Command-line and Python script configuring Jetson power profiles (`nvpmodel -m 0`, `jetson_clocks`) and querying thermal states.

2. **`ai-book-docs/module3-ai-robot-brain/3-2-isaac-sim-for-humanoids.mdx`**
   - **Current Title**: Isaac Sim Architecture & Articulation Physics
   - **Mathematical Derivations**: PhysX 5 articulation reduced coordinate Baumgarte stabilization:
     $$\ddot{\mathbf{q}}_{corr} = -2 \alpha \dot{\mathbf{q}} - \beta^2 \mathbf{q}$$
   - **Hardware Breakdowns**: RTX GPU streaming multiprocessors (SMs), Omniverse Nucleus distributed asset servers.
   - **Research Citations**: NVIDIA PhysX 5 SDK Documentation; Macklin et al. (2014) *Unified particle physics for real-time applications*.
   - **Code Examples**: Python Omniverse script loading a USD humanoid model, setting joint drive stiffness/damping, and creating OmniGraph publisher nodes.

3. **`ai-book-docs/module3-ai-robot-brain/3-3-isaac-ros-perception-pipeline.mdx`**
   - **Current Title**: Isaac ROS, NITROS & Hardware-Accelerated Perception
   - **Mathematical Derivations**: Memory bus throughput reduction formula under zero-copy pointer negotiation:
     $$\Delta B = (N_{subscribers} + 1) \times (\text{Width} \times \text{Height} \times \text{Channels} \times \text{BytesPerPixel}) \times \text{FPS}$$
   - **Hardware Breakdowns**: Unified memory controller, hardware optical flow accelerators (OFA), hardware stereo disparity engine (NVCOMP).
   - **Research Citations**: NVIDIA Isaac ROS NITROS Architecture Specification; REP-2007 Type Adaptation.
   - **Code Examples**: C++ ROS 2 composite launch file running hardware-accelerated Isaac ROS stereo disparity and cuVSLAM on Jetson AGX Orin.

4. **`ai-book-docs/module3-ai-robot-brain/3-4-nav2-for-bipedal-movement.mdx`**
   - **Current Title**: Nav2 Adaptation for Legged Locomotion
   - **Mathematical Derivations**: Capture Point footstep reachability boundary:
     $$\mathbf{x}_{cp} = \mathbf{x}_{com} + \frac{\dot{\mathbf{x}}_{com}}{\omega_0}, \quad \omega_0 = \sqrt{\frac{g}{z_0}}$$
     $ARA^*$ heuristic weight calculation for non-holonomic 3D elevation lattice.
   - **Hardware Breakdowns**: Livox Mid-360 LiDAR, IMU time-sync hardware PPS line.
   - **Research Citations**: Macenski et al. (2020) *The Marathon 2: A Navigation System*; Pratt et al. (2006) *Capture Point*.
   - **Code Examples**: Nav2 custom behavior tree XML configuration invoking footstep planning plugins and 3D elevation costmap layers.

5. **`ai-book-docs/module3-ai-robot-brain/3-5-hands-on-exercises.mdx`**
   - **Current Title**: Hands-On Exercises & Lab Projects
   - **Mathematical Derivations**: Localization Absolute Trajectory Error (ATE) and Relative Pose Error (RPE) mathematical formulas.
   - **Hardware Breakdowns**: Intel RealSense D455 depth camera calibration target rig.
   - **Research Citations**: Sturm et al. (2012) *A benchmark for the evaluation of RGB-D SLAM systems*.
   - **Code Examples**: Complete Python verification script computing ATE RMSE comparing cuVSLAM estimated trajectory against OptiTrack ground truth.

---

#### Module 4: Vision-Language-Action (VLA) Systems — 5 Existing Chapters
1. **`ai-book-docs/module4-vla/4-1-introduction-to-vla-systems.mdx`**
   - **Current Title**: Foundations of Vision-Language-Action (VLA) Systems
   - **Mathematical Derivations**: Autoregressive next-token prediction over joint vision-language-action sequence:
     $$\mathcal{L}_{VLA}(\theta) = -\sum_{t=1}^T \log P_\theta(a_t \mid \mathbf{I}_{1:t}, \mathbf{l}, a_{<t})$$
   - **Hardware Breakdowns**: Onboard PCIe accelerators (Dual NVIDIA Orin AGX 64GB vs server-class H100 inference clusters).
   - **Research Citations**: Brohan et al. (2022) *RT-1: Robotics Transformer for Real-World Control at Scale*; Brohan et al. (2023) *RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control*; Kim et al. (2024) *OpenVLA*.
   - **Code Examples**: PyTorch snippet tokenizing 7-DOF robot delta actions into discrete bins $[-1, 1] \rightarrow [0, 255]$ and decoding back to Cartesian velocities.

2. **`ai-book-docs/module4-vla/4-2-voice-to-action-pipeline.mdx`**
   - **Current Title**: Voice-to-Action Pipeline: Whisper & Real-Time ASR
   - **Mathematical Derivations**: CTC (Connectionist Temporal Classification) loss and Beam Search decoding probability score:
     $$\text{Score}(Y) = \sum_{t=1}^T \log P(y_t \mid y_{<t}, X) + \alpha \log P_{LM}(Y) + \beta \text{Length}(Y)$$
   - **Hardware Breakdowns**: Circular microphone array (ReSpeaker USB 4-Mic), hardware acoustic echo cancellation (AEC) DSP.
   - **Research Citations**: Radford et al. (2023) *Robust Speech Recognition via Large-Scale Weak Supervision* (Whisper).
   - **Code Examples**: Real-time streaming Whisper Python client piping microphone audio chunks to low-latency intent parser with ROS 2 publisher.

3. **`ai-book-docs/module4-vla/4-3-cognitive-planning-with-llms.mdx`**
   - **Current Title**: Cognitive Task Planning with Large Language Models
   - **Mathematical Derivations**: Affordance-grounded scoring in SayCan:
     $$P(\text{action } a) = P_{LLM}(a \mid \text{instruction}) \times P_{Value}(a \mid \text{state})$$
   - **Hardware Breakdowns**: Edge NPU/GPU memory footprint for 8B model quantized to 4-bit AWQ/GGUF (5.2 GB VRAM).
   - **Research Citations**: Ahn et al. (2022) *Do As I Can, Not As I Say: Grounding Language in Robotic Affordances* (SayCan); Huang et al. (2022) *Language Models as Zero-Shot Planners*.
   - **Code Examples**: Complete Python LangChain / Pydantic structured output script generating validated PDDL domain and problem files from human commands.

4. **`ai-book-docs/module4-vla/4-4-multimodal-interaction.mdx`**
   - **Current Title**: Multimodal Physical Interaction & Visual Question Answering
   - **Mathematical Derivations**: 3D spatial coordinate projection from 2D pixel coordinates and camera intrinsic matrix $\mathbf{K}$:
     $$\mathbf{P}_{3D} = Z \cdot \mathbf{K}^{-1} \begin{bmatrix} u \\ v \\ 1 \end{bmatrix}$$
   - **Hardware Breakdowns**: Wide-angle stereo camera mast, pan-tilt head gimbal servos.
   - **Research Citations**: Chen et al. (2024) *SpatialVLM: Endowing Vision-Language Models with Spatial Reasoning*.
   - **Code Examples**: Python script querying Gemini 2.5 Pro with an RGB-D camera frame to identify object grasping affordances and return 3D bounding coordinates.

5. **`ai-book-docs/module4-vla/4-5-hands-on-exercises.mdx`**
   - **Current Title**: Hands-On Exercises & VLA Benchmark Evaluation
   - **Mathematical Derivations**: Success weighted by Path Length (SPL) metric:
     $$\text{SPL} = \frac{1}{N} \sum_{i=1}^N S_i \frac{l_i}{\max(p_i, l_i)}$$
   - **Hardware Breakdowns**: Physical test arena (tabletop workspace, standardized YCB object sets).
   - **Research Citations**: Anderson et al. (2018) *Evaluation Measures for Object Goal Navigation*; Calli et al. (2015) *The YCB object and model set*.
   - **Code Examples**: Automated Python test suite evaluating VLA policy execution across 10 randomized manipulation trials in simulation.

---

### 3.2 Exact List of 19 New Chapters Across M1–M4

#### Module 1: The Robotic Nervous System (ROS 2) — 4 New Chapters
1. **`ai-book-docs/module1-ros2/1-11-ros2-control.mdx`**
   - **Title**: ros2_control Hardware Abstraction & Real-Time Controller Management
   - **Learning Objectives**: Master `hardware_interface` C++ architecture, configure `controller_manager`, author custom EtherCAT/CAN-FD actuator plugins, and execute hard real-time 1 kHz joint position/velocity/effort loops.
   - **Mathematical Formulas**: Actuator transmission reduction math $\tau_{joint} = N \cdot \tau_{motor} \cdot \eta$, stiffness/damping effort command:
     $$\tau = K_p (q_{des} - q) + K_d (\dot{q}_{des} - \dot{q}) + \tau_{ff}$$
   - **Hardware Components Covered**: EtherCAT master boards, Maxon EPOS4 / Elmo Gold Twitter drives, CAN-FD micro-controllers.
   - **Code Topics**: C++ `hardware_interface::SystemInterface` plugin implementation, ROS 2 controller spawner launch files, `ros2_control.xacro` URDF tags.

2. **`ai-book-docs/module1-ros2/1-12-dds-internals.mdx`**
   - **Title**: DDS & RTPS Protocol Deep Dive: Wire-Level Anatomy & Determinism
   - **Learning Objectives**: Analyze DDSI-RTPS wire packets, master Participant Discovery Protocol (PDP) and Endpoint Discovery Protocol (EDP), evaluate DDS vendor implementations for 1 kHz humanoid loops.
   - **Mathematical Formulas**: Packet drop probability model under UDP multicast saturation; ACKNACK latency window bounds:
     $$T_{resend\_max} = T_{heartbeat} + RTT + T_{acknack}$$
   - **Hardware Breakdowns**: Managed industrial switches (Moxa, Cisco Industrial Ethernet), hardware IGMP snooping.
   - **Code Topics**: XML configuration profiles for CycloneDDS and FastDDS tuning shared memory transports, Wireshark `.pcapng` capture analysis scripts.

3. **`ai-book-docs/module1-ros2/1-13-real-time-linux.mdx`**
   - **Title**: Real-Time Linux (PREEMPT_RT) Kernel Architecture & Optimization
   - **Learning Objectives**: Compile and tune a PREEMPT_RT patched Linux kernel, configure CPU isolation and thread pinning, prevent priority inversion with PI-mutexes, benchmark deterministic control latency.
   - **Mathematical Formulas**: Worst-case thread scheduling latency:
     $$L_{wc} = t_{interrupt\_off\_max} + t_{context\_switch} + t_{timer\_overhead}$$
   - **Hardware Components Covered**: NVIDIA Jetson AGX Orin, Intel Core i7-13700E industrial SBC, high-resolution hardware timers (`HPET`, `TSC`).
   - **Code Topics**: Bash/kernel config scripts (`isolcpus=2,3`, `nohz_full=2,3`, `rcu_nocbs=2,3`), C++ POSIX thread initialization (`pthread_attr_setschedparam`), latency profiling with `cyclictest`.

4. **`ai-book-docs/module1-ros2/1-14-ros2-diagnostics-and-monitoring.mdx`**
   - **Title**: System Diagnostics, Observability & Fleet Telemetry
   - **Learning Objectives**: Build comprehensive robot health monitoring systems, trace ROS 2 communication pipelines with LTTng, integrate Prometheus metrics and Grafana live dashboards.
   - **Mathematical Formulas**: Exponential moving average (EMA) for joint temperature and packet loss:
     $$S_t = \alpha Y_t + (1 - \alpha) S_{t-1}$$
   - **Hardware Components Covered**: Actuator thermistors, bus voltage monitors, emergency E-stop status contactors.
   - **Code Topics**: Custom `diagnostic_updater` Python/C++ node, `ros2_tracing` instrumentation session scripts, Prometheus metrics exporter for ROS 2.

---

#### Module 2: The Digital Twin (Gazebo & Unity) — 5 New Chapters
5. **`ai-book-docs/module2-digital-twin/2-6-urdf-and-sdf-mastery.mdx`**
   - **Title**: URDF, SDF & Xacro Mastery for High-DOF Humanoid Robots
   - **Learning Objectives**: Master unified robot description formats, calculate spatial inertia tensors from CAD meshes, formulate complex humanoid kinematic trees using Xacro macros.
   - **Mathematical Formulas**: Parallel Axis Theorem (Steiner's theorem) for spatial inertia:
     $$\mathbf{I}_{new} = \mathbf{I}_{cm} + m ((\mathbf{d}^T\mathbf{d})\mathbf{I}_{3\times 3} - \mathbf{d}\mathbf{d}^T)$$
   - **Hardware Components Covered**: 28-DOF humanoid structural links (pelvis, thigh, shank, torso, clavicle, forearm).
   - **Code Topics**: Complete modular Xacro template for humanoid arms and legs, MeshLab/OpenSCAD inertia computation scripts, SDF model generation.

6. **`ai-book-docs/module2-digital-twin/2-7-physics-engine-deep-dive.mdx`**
   - **Title**: Multi-Body Dynamics & Contact Physics Engine Internals
   - **Learning Objectives**: Derive Featherstone's Articulated Body Algorithm (ABA), understand contact LCP formulations, compare MuJoCo, DART, Bullet, and Drake contact solvers.
   - **Mathematical Formulas**: Featherstone's ABA recursion:
     $$\mathbf{I}^A_i = \mathbf{I}_i + \sum_{c} \mathbf{X}^* \left( \mathbf{I}^A_c - \frac{\mathbf{I}^A_c \mathbf{S}_c \mathbf{S}_c^T \mathbf{I}^A_c}{\mathbf{S}_c^T \mathbf{I}^A_c \mathbf{S}_c} \right) \mathbf{X}$$
   - **Hardware Components Covered**: Contact soles, polyurethane rubber bumpers, mechanical hard-stops.
   - **Code Topics**: Python implementation of Featherstone's forward dynamics ABA algorithm, solver benchmark harness comparing MuJoCo vs DART.

7. **`ai-book-docs/module2-digital-twin/2-8-synthetic-data-generation.mdx`**
   - **Title**: Synthetic Data Generation (SDG) & Isaac Sim Replicator
   - **Learning Objectives**: Build automated procedural synthetic data generation pipelines, execute domain randomization across visual and physical properties, export annotated multimodal datasets.
   - **Mathematical Formulas**: Domain Randomization parameter distribution sampling:
     $$\boldsymbol{\xi} \sim \mathcal{U}(\boldsymbol{\xi}_{min}, \boldsymbol{\xi}_{max}), \quad \mathcal{L}_{sim2real} = \mathbb{E}_{\boldsymbol{\xi}} [\mathcal{L}(\theta; \boldsymbol{\xi})]$$
   - **Hardware Components Covered**: RTX Ada Lovelace rendering GPUs, fast NVMe scratch storage.
   - **Code Topics**: Python Isaac Sim Replicator script generating 50,000 randomized RGB-D frames with automatic 2D/3D bounding boxes, segmentation masks, and COCO json export.

8. **`ai-book-docs/module2-digital-twin/2-9-drake-and-mujoco.mdx`**
   - **Title**: Advanced Physics Solvers for Control Research: Drake & MuJoCo
   - **Learning Objectives**: Formulate trajectory optimization problems in Drake with SNOPT/IPOPT, build high-speed reinforcement learning environments in MuJoCo with `dm_control`.
   - **Mathematical Formulas**: Direct Collocation trajectory optimization formulation:
     $$\min_{\mathbf{x}, \mathbf{u}} \int_0^T L(\mathbf{x}, \mathbf{u}) dt \quad \text{s.t.} \quad \dot{\mathbf{x}}_k = \mathbf{f}(\mathbf{x}_k, \mathbf{u}_k), \quad \mathbf{g}(\mathbf{x}_k, \mathbf{u}_k) \le 0$$
   - **Hardware Components Covered**: Kinematic test benches, robotic arms and planar biped test-rigs.
   - **Code Topics**: PyDrake DirectCollocation trajectory optimization script solving biped swing-leg trajectory; MuJoCo XML tendon-actuated hand setup.

9. **`ai-book-docs/module2-digital-twin/2-10-digital-twin-data-loop.mdx`**
   - **Title**: Closing the Real↔Sim Digital Twin Feedback Loop
   - **Learning Objectives**: Establish bidirectional data synchronization between physical humanoids and digital twins, deploy Hardware-in-the-Loop (HIL) test suites, implement OTA controller updates.
   - **Mathematical Formulas**: Extended Kalman Filter (EKF) residual state correction:
     $$\mathbf{K}_k = \mathbf{P}_k^- \mathbf{H}_k^T (\mathbf{H}_k \mathbf{P}_k^- \mathbf{H}_k^T + \mathbf{R}_k)^{-1}, \quad \hat{\mathbf{x}}_k = \hat{\mathbf{x}}_k^- + \mathbf{K}_k (\mathbf{z}_k - \mathbf{h}(\hat{\mathbf{x}}_k^-))$$
   - **Hardware Components Covered**: High-speed telemetry radios (Wi-Fi 6E / 5G Industrial), real-time physical telemetry loggers.
   - **Code Topics**: Full Python/ROS 2 shadow robot node mirroring real physical joint states into Isaac Sim in real-time, detecting tracking divergences.

---

#### Module 3: The AI-Robot Brain (NVIDIA Isaac) — 5 New Chapters
10. **`ai-book-docs/module3-ai-robot-brain/3-6-cuvslam-and-state-estimation.mdx`**
    - **Title**: Visual-Inertial Odometry & State Estimation with cuVSLAM
    - **Learning Objectives**: Implement GPU-accelerated stereo visual-inertial odometry, integrate preintegrated IMU factors on Lie manifolds, resolve localization drift through factor graphs.
    - **Mathematical Formulas**: IMU preintegration on $SO(3)$ manifold (Forster et al. 2017):
      $$\Delta \mathbf{R}_{ij} = \prod_{k=i}^{j-1} \text{Exp}((\tilde{\boldsymbol{\omega}}_k - \mathbf{b}_i^g) \Delta t)$$
    - **Hardware Components Covered**: Stereolabs ZED X, Intel RealSense D455, InvenSense ICM-42688-P 6-axis IMU.
    - **Code Topics**: ROS 2 launch file configuring Isaac ROS cuVSLAM with custom IMU noise matrices, GTSAM factor graph optimization script.

11. **`ai-book-docs/module3-ai-robot-brain/3-7-semantic-perception.mdx`**
    - **Title**: Semantic Perception, 6-DOF Pose Estimation & Open-Vocabulary Detection
    - **Learning Objectives**: Deploy foundation vision models on robots, execute zero-shot open-vocabulary object detection with Grounding DINO, estimate 6-DOF object poses with FoundationPose.
    - **Mathematical Formulas**: Point-to-plane ICP error minimization for 6-DOF pose refinement:
      $$\min_{\mathbf{R}, \mathbf{t}} \sum_{i} \left( ( \mathbf{R} \mathbf{p}_i + \mathbf{t} - \mathbf{q}_i ) \cdot \mathbf{n}_i \right)^2$$
    - **Hardware Components Covered**: Jetson Orin DLA cores, global-shutter RGB-D cameras.
    - **Code Topics**: TensorRT deployment script for NanoOWL / Grounding DINO, FoundationPose inference ROS 2 node publishing `geometry_msgs/PoseStamped`.

12. **`ai-book-docs/module3-ai-robot-brain/3-8-force-torque-sensing.mdx`**
    - **Title**: Tactile, Contact & 6-Axis Force-Torque Sensing
    - **Learning Objectives**: Process multi-axis force-torque sensor data, build robust foot-contact state machines, estimate external wrenches using motor current disturbance observers (DOB).
    - **Mathematical Formulas**: Disturbance Observer (DOB) external torque estimation:
      $$\hat{\boldsymbol{\tau}}_{ext} = \mathbf{L} (\boldsymbol{\tau}_{cmd} - \mathbf{M}(q)\ddot{q} - \mathbf{C}(q,\dot{q})\dot{q} - \mathbf{g}(q))$$
    - **Hardware Components Covered**: ATI Gamma 6-axis F/T sensors, Robotiq FT 300, strain-gauge sole load cells.
    - **Code Topics**: C++ foot contact state machine filtering raw F/T data with Schmitt triggers, publishing `ContactState` messages.

13. **`ai-book-docs/module3-ai-robot-brain/3-9-multi-sensor-fusion.mdx`**
    - **Title**: Probabilistic Multi-Sensor Fusion & Factor Graph SLAM
    - **Learning Objectives**: Formulate nonlinear multi-sensor fusion, combine LiDAR, camera, and IMU data (LVIO-SAM), tune ROS 2 `robot_localization` for floating-base humanoids.
    - **Mathematical Formulas**: Unscented Transform sigma points:
      $$\boldsymbol{\chi}_0 = \bar{\mathbf{x}}, \quad \boldsymbol{\chi}_i = \bar{\mathbf{x}} \pm \left( \sqrt{(n + \lambda)\mathbf{P}} \right)_i$$
    - **Hardware Components Covered**: Livox Mid-360 LiDAR, stereo camera, dual IMUs (torso + pelvis), wheel/foot odometry.
    - **Code Topics**: Complete `robot_localization` dual-EKF configuration YAML, custom Ceres / GTSAM factor graph optimization node.

14. **`ai-book-docs/module3-ai-robot-brain/3-10-edge-inference-optimization.mdx`**
    - **Title**: Edge AI Inference Optimization with TensorRT & INT8 Quantization
    - **Learning Objectives**: Optimize neural network execution for low latency on Jetson AGX Orin, execute INT8 post-training calibration, partition workloads across GPU Tensor Cores and DLAs.
    - **Mathematical Formulas**: Symmetric INT8 quantization mapping:
      $$x_{quant} = \text{clip}\left(\left\lfloor \frac{x}{s} \right\rceil, -128, 127\right), \quad s = \frac{\max(|x|)}{127}$$
      Kullback-Leibler (KL) divergence calibration.
    - **Hardware Components Covered**: NVIDIA Jetson AGX Orin 64GB, DLA0/DLA1 accelerators, NVLink.
    - **Code Topics**: Complete Python TensorRT builder script converting PyTorch model to ONNX, running entropy calibrator, and executing asynchronous execution engine.

---

#### Module 4: Vision-Language-Action (VLA) Systems — 5 New Chapters
15. **`ai-book-docs/module4-vla/4-6-foundation-model-architectures.mdx`**
    - **Title**: VLA Foundation Model Architectures: Vision Encoders to Action Heads
    - **Learning Objectives**: Deconstruct leading VLA models (OpenVLA, π0, Octo), analyze vision encoders (SigLIP, DinoV2), master action tokenization vs continuous action heads.
    - **Mathematical Formulas**: Cross-attention query-key-value mechanism in multimodal transformers:
      $$\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(\frac{\mathbf{Q} \mathbf{K}^T}{\sqrt{d_k}}\right) \mathbf{V}$$
    - **Hardware Components Covered**: Data center training clusters (8×H100 SXM5), edge inference rigs.
    - **Code Topics**: PyTorch model definition of a vision-language cross-attention module connecting SigLIP vision tokens to Llama 3 backbone with continuous MLP action head.

16. **`ai-book-docs/module4-vla/4-7-diffusion-policies.mdx`**
    - **Title**: Diffusion Policies & Flow Matching for Multimodal Robot Control
    - **Learning Objectives**: Understand score-based generative modeling for robot control, implement Diffusion Policy (Chi et al. 2023), master Conditional Flow Matching (CFM) on action spaces.
    - **Mathematical Formulas**: Conditional Flow Matching objective:
      $$\mathcal{L}_{CFM}(\theta) = \mathbb{E}_{t, x_0 \sim p_0, x_1 \sim p_1} \left[ \| v_\theta(x_t, t, c) - (x_1 - x_0) \|^2 \right]$$
      where $x_t = t x_1 + (1 - t) x_0$.
    - **Hardware Components Covered**: High-frequency robot control interfaces (50 Hz action chunking).
    - **Code Topics**: Complete PyTorch implementation of a 1D Temporal U-Net Diffusion Policy training script for robot reaching and grasping.

17. **`ai-book-docs/module4-vla/4-8-imitation-learning.mdx`**
    - **Title**: Imitation Learning, Action Chunking (ACT) & Teleoperation
    - **Learning Objectives**: Collect high-quality humanoid demonstration datasets, mitigate compounding covariate shift, implement Action Chunking with Transformers (ACT).
    - **Mathematical Formulas**: ACT Conditional Variational Autoencoder (CVAE) loss:
      $$\mathcal{L}_{ACT} = \sum_{t=1}^k \|\mathbf{a}_t - \hat{\mathbf{a}}_t\|_1 + \beta D_{KL}\left( q(\mathbf{z} \mid \mathbf{a}_{1:k}, \bar{\mathbf{o}}) \,\Big\|\, p(\mathbf{z} \mid \bar{\mathbf{o}}) \right)$$
    - **Hardware Components Covered**: Bilateral teleoperation exoskeletons, 3D SpaceMouse, Apple Vision Pro spatial trackers.
    - **Code Topics**: LEROBOT dataset loader and ACT transformer policy training script in PyTorch with temporal action ensembling.

18. **`ai-book-docs/module4-vla/4-9-reward-shaping-and-rlaif.mdx`**
    - **Title**: Reward Shaping, Preference Learning & RL from AI Feedback (RLAIF)
    - **Learning Objectives**: Train reward models from human ranking preferences, leverage Vision-Language Models as automated reward critics (Eureka / RLAIF), enforce Lyapunov safety constraints.
    - **Mathematical Formulas**: Bradley-Terry preference model for trajectory comparisons:
      $$P(\tau_1 \succ \tau_2) = \frac{\exp\left(\sum_t R(s_t^1, a_t^1)\right)}{\exp\left(\sum_t R(s_t^1, a_t^1)\right) + \exp\left(\sum_t R(s_t^2, a_t^2)\right)}$$
    - **Hardware Components Covered**: Automated cloud evaluation clusters.
    - **Code Topics**: Python script using Gemini API as an automated reward evaluator for humanoid manipulation trajectories in simulation.

19. **`ai-book-docs/module4-vla/4-10-deployment-and-safety.mdx`**
    - **Title**: Production VLA Deployment, Safety Filtering & Out-of-Distribution Detection
    - **Learning Objectives**: Deploy closed-loop VLA policies with real-time error recovery, detect out-of-distribution visual inputs with Monte Carlo Dropout, enforce deterministic kinematic safety filters.
    - **Mathematical Formulas**: Epistemic uncertainty quantification via predictive entropy:
      $$\mathcal{H}[y \mid x, \mathcal{D}] = -\sum_{c} \bar{p}_c \log \bar{p}_c, \quad \bar{p}_c = \frac{1}{M}\sum_{m=1}^M P(y=c \mid x, \mathbf{w}^{(m)})$$
    - **Hardware Components Covered**: Dual-channel safety override hardware, emergency hardware brakes.
    - **Code Topics**: C++ safety filter node wrapping a Python VLA policy, clamping joint velocities, enforcing torque limits, and falling back to safe posture if uncertainty spikes.

---

## 4. Phase 2 (M6–M12): 56 Brand-New Modules & Chapters Inventory

### Module 6: Bipedal Locomotion & Whole-Body Control (`ai-book-docs/module6-bipedal-locomotion/`) — 10 Chapters
1. **`module6-bipedal-locomotion/6-1-introduction-to-bipedal-locomotion.mdx`**
   - **Title**: Foundations of Bipedal Locomotion & Underactuated Robotics
   - **Key Concepts**: Historical evolution (WABOT-1, Honda ASIMO, Boston Dynamics Atlas, Tesla Optimus); underactuation index; intermittent hybrid contact dynamics; Poincaré map orbital stability.
   - **Mathematical Equations**: Floating-base equations of motion:
     $$\mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{g}(\mathbf{q}) = \mathbf{S}^T \boldsymbol{\tau} + \mathbf{J}_c^T \boldsymbol{\lambda}$$
     where $\mathbf{S} = [\mathbf{0}_{n \times 6}, \mathbf{I}_{n \times n}]$ selects actuated joints.
   - **Algorithms/Code**: Hybrid dynamical system simulation in Python with event-based foot impact detection.
   - **Research Citations**: Vukobratović & Juricic (1969); Pratt & Pratt (1998); Kuindersma et al. (2016).

2. **`module6-bipedal-locomotion/6-2-zero-moment-point.mdx`**
   - **Title**: The Zero-Moment Point (ZMP) & 3D Linear Inverted Pendulum Model
   - **Key Concepts**: D'Alembert principle; Center of Pressure (COP); 3D-LIPM assumptions; Kajita preview control with look-ahead window; flat-ground constraints.
   - **Mathematical Equations**: 3D-LIPM equations:
     $$p_{zmp, x} = x - \frac{z_c}{g}\ddot{x}, \quad p_{zmp, y} = y - \frac{z_c}{g}\ddot{y}$$
     Discrete-time optimal preview control law:
     $$u_k = -K_i \sum_{i=0}^k e_i - K_x \mathbf{x}_k - \sum_{j=1}^N F_j p^{ref}_{k+j}$$
   - **Algorithms/Code**: Complete Kajita Preview Controller simulation in Python plotting CoM trajectory tracking against reference ZMP footsteps.
   - **Research Citations**: Kajita et al. (2003) *Biped walking pattern generation by using preview control of zero-moment point*; Vukobratović & Borovac (2004).

3. **`module6-bipedal-locomotion/6-3-capture-point-and-dcm.mdx`**
   - **Title**: Divergent Component of Motion (DCM) & Capture Point Step Planning
   - **Key Concepts**: Instantaneous Capture Point (ICP); Divergent Component of Motion decomposition; push recovery tri-strategy (ankle, hip, step); N-step capturability analysis.
   - **Mathematical Equations**: DCM definition and first-order unstable dynamics:
     $$\boldsymbol{\xi} = \mathbf{x}_{com} + \frac{\dot{\mathbf{x}}_{com}}{\omega_0}, \quad \dot{\boldsymbol{\xi}} = \omega_0 (\boldsymbol{\xi} - \mathbf{p}_{zmp}), \quad \omega_0 = \sqrt{\frac{g}{z_c}}$$
     Step adjustment formula: $\Delta \mathbf{p}_{step} = \boldsymbol{\xi}_{eos} - \mathbf{p}_{zmp}$.
   - **Algorithms/Code**: Reactive push-recovery footstep replanner script in Python simulating sudden lateral impulsive forces.
   - **Research Citations**: Pratt et al. (2006); Koolen et al. (2012) *Capturability-based analysis and walking control*; Englsberger et al. (2015).

4. **`module6-bipedal-locomotion/6-4-model-predictive-control.mdx`**
   - **Title**: Model Predictive Control for Legged Locomotion
   - **Key Concepts**: Receding horizon optimal control; Single Rigid Body Dynamics (SRBD); convex QP formulation; contact scheduling; real-time warm-start solvers (OSQP, qpOASES).
   - **Mathematical Equations**: SRBD linear state-space dynamics:
     $$\frac{d}{dt}\begin{bmatrix} \mathbf{p} \\ \dot{\mathbf{p}} \\ \mathbf{R} \\ \boldsymbol{\omega} \end{bmatrix} = \begin{bmatrix} \dot{\mathbf{p}} \\ \frac{1}{m}\sum \mathbf{f}_i - \mathbf{g} \\ \mathbf{R}[\boldsymbol{\omega}]_\times \\ \mathbf{I}_G^{-1}\left(\sum (\mathbf{r}_i - \mathbf{p}) \times \mathbf{f}_i\right) \end{bmatrix}$$
     Convex QP cost: $\min_{\mathbf{f}} \sum_{k} \|\mathbf{x}_k - \mathbf{x}_k^{ref}\|_{\mathbf{Q}}^2 + \|\mathbf{f}_k\|_{\mathbf{R}}^2$ s.t. friction cones.
   - **Algorithms/Code**: 500 Hz Convex MPC locomotion solver implemented with `osqp-python`.
   - **Research Citations**: Di Carlo et al. (2018) *Dynamic Locomotion in the MIT Cheetah 3 Through Convex Model-Predictive Control*; Grandia et al. (2019).

5. **`module6-bipedal-locomotion/6-5-whole-body-control.mdx`**
   - **Title**: Hierarchical Whole-Body Control & Operational Space Formulations
   - **Key Concepts**: Multi-objective priority hierarchy (null-space projection); QP-based Whole-Body Control (WBC); joint torque limits and contact friction cone constraints.
   - **Mathematical Equations**: Hierarchical null-space projection:
     $$\boldsymbol{\tau} = \mathbf{J}_1^T \mathbf{F}_1 + \mathbf{N}_1^T (\mathbf{J}_2^T \mathbf{F}_2 + \mathbf{N}_2^T \boldsymbol{\tau}_0), \quad \mathbf{N}_i = \mathbf{I} - \mathbf{J}_i^\dagger \mathbf{J}_i$$
     QP formulation with decision variables $\mathbf{x} = [\ddot{\mathbf{q}}^T, \boldsymbol{\tau}^T, \boldsymbol{\lambda}^T]^T$.
   - **Algorithms/Code**: C++ / Python WBC implementation using Pinocchio and OSQP for floating-base humanoid balance.
   - **Research Citations**: Sentis & Khatib (2005) *Synthesis of whole-body behaviors through hierarchical control of behavioral primitives*; Herzog et al. (2016).

6. **`module6-bipedal-locomotion/6-6-reinforcement-learning-locomotion.mdx`**
   - **Title**: Deep Reinforcement Learning for Humanoid Locomotion
   - **Key Concepts**: MDP formulation for bipedal balancing; reward function engineering; PPO algorithm; massively parallel simulation with Isaac Lab / `legged_gym`; terrain curriculum scheduling.
   - **Mathematical Equations**: PPO clipped objective with generalized advantage estimation (GAE):
     $$L^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\right) \right]$$
     Reward function: $R = w_v R_{vel} + w_\omega R_{ang} - w_\tau \|\boldsymbol{\tau}\|^2 - w_a \|\ddot{\mathbf{q}}\|^2$.
   - **Algorithms/Code**: Complete Isaac Lab training script executing PPO across 4096 parallel humanoid environments.
   - **Research Citations**: Schulman et al. (2017) *Proximal Policy Optimization Algorithms*; Rudin et al. (2022) *Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning*.

7. **`module6-bipedal-locomotion/6-7-sim-to-real-locomotion.mdx`**
   - **Title**: Sim-to-Real Transfer for Locomotion: Domain Randomization to RMA
   - **Key Concepts**: Reality gap in bipedal systems; actuator dynamic modeling (Actuator Net); Rapid Motor Adaptation (RMA) two-stage architecture; deploying neural policies to Unitree G1.
   - **Mathematical Equations**: RMA Teacher-Student loss formulation:
     $$\mathcal{L}_{student} = \|\phi(\mathbf{s}_{t-H:t}) - \mathbf{z}_t^{priv}\|^2$$
     where $\mathbf{z}_t^{priv}$ is the latent vector estimated by the privileged teacher network.
   - **Algorithms/Code**: Complete RMA student adaptation module in PyTorch and C++ deployment bridge for physical robot deployment.
   - **Research Citations**: Kumar et al. (2021) *RMA: Rapid Motor Adaptation for Bipedal Locomotion*; Hwangbo et al. (2019) *Learning agile robotic locomotion on complex terrain* (Science Robotics).

8. **`module6-bipedal-locomotion/6-8-advanced-locomotion-skills.mdx`**
   - **Title**: Advanced Locomotion: Running, Jumping, Stairs & Neural Parkour
   - **Key Concepts**: Spring-Loaded Inverted Pendulum (SLIP) model; ballistic jumping flight phases; stair climbing with elevation costmaps; agile parkour policies.
   - **Mathematical Equations**: SLIP model flight-stance dynamics:
     $$m \ddot{r} = m r \dot{\theta}^2 - k(r - r_0) - m g \cos\theta, \quad m r^2 \ddot{\theta} = -2 m r \dot{r} \dot{\theta} + m g r \sin\theta$$
   - **Algorithms/Code**: Ballistic jumping trajectory optimizer and neural parkour policy runner in Python.
   - **Research Citations**: Blickhan (1989) *The spring-mass model for running and hopping*; Hoeller et al. (2024) *Neural Parkour for Legged Robots* (Science Robotics).

9. **`module6-bipedal-locomotion/6-9-gait-analysis-and-biomechanics.mdx`**
   - **Title**: Gait Analysis, Ground Reaction Forces & Biomechanics
   - **Key Concepts**: Biological human gait cycle (heel strike, foot flat, midstance, push-off, swing); Ground Reaction Force (GRF) butterfly diagrams; dimensionless Cost of Transport (COT); ankle elasticity.
   - **Mathematical Equations**: Dimensionless Specific Cost of Transport:
     $$COT = \frac{E}{m g d} = \frac{\int_0^T P_{electrical}(t) dt}{m g d}$$
     Froude number for dynamically similar walking: $Fr = \frac{v^2}{g l_{leg}}$.
   - **Algorithms/Code**: Gait data analysis script computing joint power, GRF symmetry index, and COT from force plate logs.
   - **Research Citations**: Winter (2009) *Biomechanics and Motor Control of Human Movement*; Collins et al. (2005) *Efficient bipedal robots based on passive-dynamic walkers* (Science).

10. **`module6-bipedal-locomotion/6-10-motion-capture-and-reference.mdx`**
    - **Title**: Motion Capture Retargeting & Adversarial Motion Priors (AMP)
    - **Key Concepts**: Optical MoCap marker sets (Helen Hayes / Plug-in Gait); AMASS dataset; Adversarial Motion Priors (AMP); kinematic retargeting to humanoid joint limits.
    - **Mathematical Equations**: AMP discriminator adversarial objective:
      $$\min_D \mathbb{E}_{\mathbf{d} \sim \mathcal{D}^{MoCap}} \left[ (D(\mathbf{d}) - 1)^2 \right] + \mathbb{E}_{\mathbf{s} \sim \pi} \left[ (D(\mathbf{s}) + 1)^2 \right]$$
      Retargeting optimization: $\min_{\mathbf{q}} \|\mathbf{x}_{human}^{MoCap} - \mathbf{x}_{robot}^{FK}(\mathbf{q})\|^2 + \lambda \|\mathbf{q} - \mathbf{q}_{neutral}\|^2$.
    - **Algorithms/Code**: Python script retargeting AMASS BVH human motion clips to humanoid URDF joint angles.
    - **Research Citations**: Peng et al. (2021) *AMP: Adversarial Motion Priors for Stylized Physics-Based Character Animation*; Mahmood et al. (2020) *AMASS: Archive of Motion Capture as Surface Shapes*.

---

### Module 7: Dexterous Manipulation & Hand Design (`ai-book-docs/module7-dexterous-manipulation/`) — 8 Chapters
11. **`module7-dexterous-manipulation/7-1-introduction-to-dexterous-manipulation.mdx`**
    - **Title**: Foundations of Dexterous Manipulation & Hand Kinematics
    - **Key Concepts**: Prehensile vs non-prehensile grasping; power vs precision grasps; human hand anatomy (21 DOFs) vs robot hands (6–24 DOFs); challenge spectrum (pick-and-place $\rightarrow$ in-hand reorientation $\rightarrow$ deformable manipulation).
    - **Mathematical Equations**: Hand configuration space $\mathcal{C}_{hand} \subset \mathbb{R}^n$; finger kinematic Jacobian:
      $$\mathbf{v}_{tip} = \mathbf{J}_{finger}(\boldsymbol{\theta}) \dot{\boldsymbol{\theta}}$$
    - **Algorithms/Code**: Hand workspace reachability simulation script computing dexterous manipulability ellipsoids.
    - **Research Citations**: Cutkosky (1989) *On grasp choice, grasp models, and the design of hands for manufacturing tasks*; Bicchi (2000).

12. **`module7-dexterous-manipulation/7-2-grasp-theory.mdx`**
    - **Title**: Grasp Theory: Contact Mechanics, Wrench Space & Force Closure
    - **Key Concepts**: Contact models (frictionless, hard finger with friction, soft finger); Grasp Matrix $\mathbf{G}$; Form Closure vs Force Closure; Grasp Wrench Space (GWS); Ferrari-Canny $\epsilon$-metric.
    - **Mathematical Equations**: Grasp equilibrium:
      $$\mathbf{w}_{ext} = -\mathbf{G} \mathbf{f}_c, \quad \mathbf{G} = [\mathbf{G}_1, \dots, \mathbf{G}_k] \in \mathbb{R}^{6 \times m}$$
      Ferrari-Canny metric: $\epsilon = \max \{ r \mid \mathcal{B}_r(\mathbf{0}) \subseteq \text{ConvexHull}(\cup \mathbf{w}_i) \}$.
    - **Algorithms/Code**: Python grasp quality evaluation module using `scipy.spatial.ConvexHull` to compute Ferrari-Canny $\epsilon$ metric on 3D meshes.
    - **Research Citations**: Salisbury & Roth (1983); Ferrari & Canny (1992) *Planning optimal grasps*; Roa & Suárez (2015).

13. **`module7-dexterous-manipulation/7-3-robotic-hand-design.mdx`**
    - **Title**: Robotic Hand Design: Underactuation, Tendons & Actuator Sizing
    - **Key Concepts**: Underactuated self-adaptive fingers (Robotiq 2F-85); fully articulated multi-finger hands (Shadow Dexterous Hand); tendon routing matrices; Capstan friction; TPU flexure joints.
    - **Mathematical Equations**: Tendon kinematic transmission matrix $\mathbf{A}$:
      $$\Delta \mathbf{l} = \mathbf{A} \Delta \boldsymbol{\theta}, \quad \boldsymbol{\tau} = \mathbf{A}^T \mathbf{T}$$
      Capstan equation for Bowden cable friction: $T_{out} = T_{in} e^{-\mu \theta_{wrap}}$.
    - **Algorithms/Code**: Tendon tension-to-joint torque optimization solver in Python.
    - **Research Citations**: Dollar & Howe (2010) *The highly adaptive SDM hand*; Grebenstein et al. (2011) *The DLR hand arm system*.

14. **`module7-dexterous-manipulation/7-4-tactile-sensing.mdx`**
    - **Title**: Optical & Piezoresistive Tactile Sensing: GelSight to High-Density Skins
    - **Key Concepts**: Optical elastomer sensors (GelSight, DIGIT); photometric stereo reconstruction; piezoresistive array skins; normal and shear force decoupling; dynamic slip detection.
    - **Mathematical Equations**: Photometric stereo surface gradient reconstruction:
      $$I_k(x, y) = \rho \frac{-p l_{x, k} - q l_{y, k} + l_{z, k}}{\sqrt{p^2 + q^2 + 1}}$$
      Slip criterion: $\|\mathbf{f}_{shear}\| \ge \mu f_{normal}$.
    - **Algorithms/Code**: GelSight 3D contact depth reconstruction script using OpenCV and Python.
    - **Research Citations**: Johnson & Adelson (2009); Yuan et al. (2017) *GelSight: High-resolution robot tactile system*; Lambeta et al. (2020) *DIGIT*.

15. **`module7-dexterous-manipulation/7-5-motion-planning-for-manipulation.mdx`**
    - **Title**: Motion Planning for Manipulation: MoveIt 2, TAMP & RMPs
    - **Key Concepts**: Configuration space $\mathcal{C}_{free}$ mapping; sampling-based planning (RRT*, BiRRT); MoveIt 2 planning pipeline; Task and Motion Planning (TAMP) with PDDLStream; Riemannian Motion Policies (RMP).
    - **Mathematical Equations**: RRT* rewiring radius:
      $$r^*(\text{card}(V)) = \gamma_{RRT^*} \left(\frac{\log(\text{card}(V))}{\text{card}(V)}\right)^{1/d}$$
      Riemannian Motion Policy pullback: $\mathbf{f}_M = \mathbf{J}^T \mathbf{M} (\ddot{\mathbf{x}}_{des} - \dot{\mathbf{J}}\dot{\mathbf{q}})$.
    - **Algorithms/Code**: MoveIt 2 C++ planning client executing collision-free dual-arm pick-and-place trajectories.
    - **Research Citations**: Karaman & Frazzoli (2011) *Sampling-based algorithms for optimal motion planning*; Garrett et al. (2020) *PDDLStream*; Ratliff et al. (2018).

16. **`module7-dexterous-manipulation/7-6-learning-based-manipulation.mdx`**
    - **Title**: Learning-Based Manipulation: Grasp Pose Estimation to ACT
    - **Key Concepts**: 6-DOF grasp synthesis from point clouds (GraspNet-1Billion, Contact-GraspNet); SE(3)-equivariant networks; Action Chunking with Transformers (ACT); dexterous in-hand manipulation RL (Bi-DexHands).
    - **Mathematical Equations**: 6-DOF grasp likelihood score:
      $$s(\mathbf{T}_g \mid \mathcal{P}) = \sigma(\text{MLP}(\mathbf{z}_{pointcloud}, \mathbf{T}_g))$$
    - **Algorithms/Code**: ACT bimanual policy training script using PyTorch and LEROBOT dataset format.
    - **Research Citations**: Fang et al. (2020) *GraspNet-1Billion*; Zhao et al. (2023) *Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware* (ACT); Chen et al. (2022) *Bi-DexHands*.

17. **`module7-dexterous-manipulation/7-7-assembly-and-contact-rich-tasks.mdx`**
    - **Title**: Contact-Rich Assembly: Peg-in-Hole, Spiral Search & Compliance
    - **Key Concepts**: Peg-in-hole contact physics (jamming vs wedging); passive compliance (Remote Center of Compliance RCC); active admittance control; spiral search algorithms; Mason's hybrid position/force control.
    - **Mathematical Equations**: Mechanical Admittance model:
      $$\mathbf{M}_d (\ddot{\mathbf{x}} - \ddot{\mathbf{x}}_d) + \mathbf{D}_d (\dot{\mathbf{x}} - \dot{\mathbf{x}}_d) + \mathbf{K}_d (\mathbf{x} - \mathbf{x}_d) = \mathbf{F}_{ext}$$
      Mason selection matrix: $\mathbf{v} = \mathbf{S} \dot{\mathbf{x}}$, $\mathbf{f} = (\mathbf{I} - \mathbf{S}) \mathbf{F}$.
    - **Algorithms/Code**: Python/Gazebo peg-in-hole assembly controller executing spiral search and impedance insertion.
    - **Research Citations**: Hogan (1985) *Impedance Control: An Approach to Manipulation*; Mason (1981); Whitney (1982) *Quasi-static assembly of compliantly supported rigid parts*.

18. **`module7-dexterous-manipulation/7-8-manipulation-benchmarks.mdx`**
    - **Title**: Manipulation Benchmarks & Datasets: RoboSuite, ManiSkill & DROID
    - **Key Concepts**: Standardized benchmarks (RoboSuite, ManiSkill3); large-scale real-world datasets (DROID, BridgeData V2, Open X-Embodiment); AgiBot World Challenge; designing reproducible evaluation protocols.
    - **Mathematical Equations**: Grasp success rate:
      $$S = \frac{1}{N_{trials}}\sum_{i=1}^{N_{trials}} \mathbb{I}(\text{task completed within } T_{max})$$
    - **Algorithms/Code**: Automated evaluation script executing benchmark trials on ManiSkill3 with headless GPU rendering.
    - **Research Citations**: Zhu et al. (2020) *robosuite: A Modular Simulation Framework for Robot Learning*; Khazatsky et al. (2024) *DROID: A Large-Scale Robot Manipulation Dataset*.

---

### Module 8: Robot Learning & Reinforcement Learning (`ai-book-docs/module8-robot-learning/`) — 10 Chapters
19. **`module8-robot-learning/8-1-foundations-of-reinforcement-learning.mdx`**
    - **Title**: Theoretical Foundations of Reinforcement Learning & Dynamic Programming
    - **Key Concepts**: Markov Decision Process (MDP); Bellman Expectation and Optimality Equations; Policy Iteration and Value Iteration; Monte Carlo sampling; Temporal Difference learning (TD(0), TD($\lambda$)).
    - **Mathematical Equations**: Bellman Optimality Equation:
      $$V^*(s) = \max_a \sum_{s', r} P(s', r \mid s, a) [r + \gamma V^*(s')], \quad Q^*(s, a) = \sum_{s', r} P(s', r \mid s, a) [r + \gamma \max_{a'} Q^*(s', a')]$$
    - **Algorithms/Code**: Python implementation of Value Iteration and TD($\lambda$) with eligibility traces.
    - **Research Citations**: Sutton & Barto (2018) *Reinforcement Learning: An Introduction*; Bellman (1957).

20. **`module8-robot-learning/8-2-deep-rl-algorithms.mdx`**
    - **Title**: Deep RL Algorithms for Robotics: PPO, SAC & TD3
    - **Key Concepts**: Deep Q-Networks (DQN); Policy Gradient Theorem; REINFORCE; Actor-Critic; PPO clipped objective; Soft Actor-Critic (SAC) maximum entropy; Twin Delayed DDPG (TD3).
    - **Mathematical Equations**: SAC maximum entropy objective:
      $$J(\pi) = \sum_{t=0}^T \mathbb{E}_{(s_t, a_t) \sim \rho_\pi} [r(s_t, a_t) + \alpha \mathcal{H}(\pi(\cdot \mid s_t))]$$
      Automatic temperature tuning loss: $J(\alpha) = \mathbb{E}_{a_t \sim \pi_t} [-\alpha (\log \pi_t(a_t \mid s_t) + \bar{\mathcal{H}})]$.
    - **Algorithms/Code**: Clean PyTorch implementation of SAC with continuous Gaussian policy and target smoothing.
    - **Research Citations**: Haarnoja et al. (2018) *Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning*; Fujimoto et al. (2018) *Addressing Function Approximation Error in Actor-Critic (TD3)*.

21. **`module8-robot-learning/8-3-rl-for-continuous-control.mdx`**
    - **Title**: RL for Continuous Control: Action Space Design & Reward Engineering
    - **Key Concepts**: Continuous action space parameterization (squashed Gaussian); joint positions vs velocity offsets vs torques; potential-based reward shaping; reward hacking mitigation; privileged critic architectures.
    - **Mathematical Equations**: Potential-based reward shaping invariance theorem (Ng et al. 1999):
      $$F(s, a, s') = \gamma \Phi(s') - \Phi(s)$$
      Squashed Gaussian policy log-likelihood: $\log \pi(a \mid s) = \log \mu(u \mid s) - \sum_{i} \log(1 - \tanh^2(u_i))$.
    - **Algorithms/Code**: Continuous control SAC training script in `dm_control` for humanoid reaching.
    - **Research Citations**: Ng, Harada, & Russell (1999) *Policy invariance under reward transformations*; Peng et al. (2018) *DeepMimic*.

22. **`module8-robot-learning/8-4-massively-parallel-training.mdx`**
    - **Title**: Massively Parallel GPU Training: Isaac Gym & Isaac Lab
    - **Key Concepts**: Vectorized GPU physics simulation (PhysX, Warp); tensor-based memory architectures; scaling to 10,000+ parallel environments; mixed-precision FP16 rollouts; Ray RLlib multi-node scaling.
    - **Mathematical Equations**: Simulation throughput scaling:
      $$\text{Throughput (FPS)} = \frac{N_{environments} \times N_{steps}}{\Delta t_{wall\_clock}}$$
    - **Algorithms/Code**: Full Isaac Lab training configuration script spinning up 4096 parallel environments for bipedal locomotion.
    - **Research Citations**: Makoviychuk et al. (2021) *Isaac Gym: High Performance GPU-Based Physics Simulation for Robot Learning*; Mittal et al. (2023) *Orbit*.

23. **`module8-robot-learning/8-5-curriculum-learning.mdx`**
    - **Title**: Curriculum Learning & Procedural Environment Generation
    - **Key Concepts**: Automatic Curriculum Learning (ACL); Absolute Learning Progress (ALP-GMM); PAIRED unsupervised environment design; procedural terrain synthesis (Perlin noise, diamond-square).
    - **Mathematical Equations**: Regret in PAIRED:
      $$\text{Regret}(\boldsymbol{\theta}) = \max_{\pi^*} V(\pi^*, \boldsymbol{\theta}) - V(\pi^{agent}, \boldsymbol{\theta})$$
    - **Algorithms/Code**: Progressive terrain curriculum manager and Perlin heightmap generator in Python.
    - **Research Citations**: Portelas et al. (2020) *Teacher algorithms for curriculum learning*; Dennis et al. (2020) *Emergent Complexity and Zero-shot Transfer via Unsupervised Environment Design*.

24. **`module8-robot-learning/8-6-offline-rl-and-imitation.mdx`**
    - **Title**: Offline Reinforcement Learning & Sequence Modeling
    - **Key Concepts**: Learning from fixed datasets; out-of-distribution action overestimation; Conservative Q-Learning (CQL); Implicit Q-Learning (IQL); Decision Transformer (autoregressive sequence modeling).
    - **Mathematical Equations**: CQL penalty loss:
      $$\min_Q \alpha \cdot \left( \mathbb{E}_{s \sim \mathcal{D}, a \sim \mu}[\exp(Q(s, a))] - \mathbb{E}_{(s, a) \sim \mathcal{D}}[Q(s, a)] \right) + \frac{1}{2}\mathcal{L}_{TD}(Q)$$
    - **Algorithms/Code**: PyTorch implementation of IQL training on D4RL locomotion trajectory datasets.
    - **Research Citations**: Kumar et al. (2020) *Conservative Q-Learning for Offline Reinforcement Learning*; Kostrikov, Nair, & Levine (2021) *Offline Reinforcement Learning with Implicit Q-Learning*; Chen et al. (2021) *Decision Transformer*.

25. **`module8-robot-learning/8-7-model-based-rl.mdx`**
    - **Title**: Model-Based RL & World Models: Dreamer V3 & MBPO
    - **Key Concepts**: Latent dynamics models; Recurrent State Space Model (RSSM); Dreamer V3; Model-Based Policy Optimization (MBPO); probabilistic ensembles (PETS); imagination rollouts for real humanoids.
    - **Mathematical Equations**: RSSM variational lower bound (ELBO):
      $$\mathcal{L} = \mathbb{E}_{q} \left[ \sum_t -\log p(x_t \mid h_t, z_t) -\log p(r_t \mid h_t, z_t) + D_{KL}(q(z_t \mid h_t, x_t) \parallel p(z_t \mid h_t)) \right]$$
    - **Algorithms/Code**: PyTorch implementation of a latent world model and imagination policy optimization loop.
    - **Research Citations**: Hafner et al. (2023) *Mastering Diverse Domains through World Models (DreamerV3)*; Janner et al. (2019) *When to Trust Your Model: Model-Based Policy Optimization*.

26. **`module8-robot-learning/8-8-multi-task-and-meta-learning.mdx`**
    - **Title**: Multi-Task & Meta-Reinforcement Learning: MAML to Context Policies
    - **Key Concepts**: Shared representation learning; task conditioning; Model-Agnostic Meta-Learning (MAML); RL2 recurrent meta-RL; context-conditioned adaptive policies.
    - **Mathematical Equations**: MAML gradient update:
      $$\boldsymbol{\theta}^* = \arg\min_{\boldsymbol{\theta}} \sum_{\mathcal{T}_i} \mathcal{L}_{\mathcal{T}_i}(\boldsymbol{\theta} - \alpha \nabla_{\boldsymbol{\theta}} \mathcal{L}_{\mathcal{T}_i}(\boldsymbol{\theta}))$$
    - **Algorithms/Code**: Python meta-RL training harness adapting locomotion across varied friction and slope parameters.
    - **Research Citations**: Finn, Abbeel, & Levine (2017) *Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks*; Duan et al. (2016) *RL$^2$*.

27. **`module8-robot-learning/8-9-safe-reinforcement-learning.mdx`**
    - **Title**: Safe Reinforcement Learning & Control Barrier Functions
    - **Key Concepts**: Constrained MDPs (CMDP); Lagrangian dual relaxation; Constrained Policy Optimization (CPO); Control Barrier Functions (CBF); forward invariant safe sets; real-time safety filter wrappers.
    - **Mathematical Equations**: Control Barrier Function condition:
      $$\dot{h}(\mathbf{x}, \mathbf{u}) = \frac{\partial h}{\partial \mathbf{x}} \mathbf{f}(\mathbf{x}) + \frac{\partial h}{\partial \mathbf{x}} \mathbf{g}(\mathbf{x})\mathbf{u} \ge -\gamma(h(\mathbf{x}))$$
      where safe set $\mathcal{C} = \{\mathbf{x} \mid h(\mathbf{x}) \ge 0\}$.
    - **Algorithms/Code**: CBF-QP safety filter wrapping a neural locomotion policy in Python to guarantee non-tipping.
    - **Research Citations**: Achiam et al. (2017) *Constrained Policy Optimization*; Ames et al. (2019) *Control Barrier Functions: Theory and Applications*.

28. **`module8-robot-learning/8-10-evaluation-and-benchmarking.mdx`**
    - **Title**: Evaluation Methodologies, Statistical Rigor & Reproducibility
    - **Key Concepts**: Statistical significance in deep RL; seed variance; Interquartile Mean (IQM); stratified bootstrap confidence intervals; experiment tracking (MLflow, Weights & Biases); NeurIPS RL checklist.
    - **Mathematical Equations**: Interquartile Mean (IQM) calculation:
      $$\text{IQM} = \frac{1}{0.5 N} \sum_{i=\lfloor 0.25 N \rfloor + 1}^{\lfloor 0.75 N \rfloor} x_{(i)}$$
    - **Algorithms/Code**: Python evaluation harness calculating stratified bootstrap confidence intervals and generating performance profile plots.
    - **Research Citations**: Agarwal et al. (2021) *Deep Reinforcement Learning at the Edge of the Statistical Precipice*; Henderson et al. (2018) *Deep Reinforcement Learning that Matters*.

---

### Module 9: Sim-to-Real Transfer & Domain Randomization (`ai-book-docs/module9-sim-to-real/`) — 8 Chapters
29. **`module9-sim-to-real/9-1-the-reality-gap.mdx`**
    - **Title**: Anatomy of the Reality Gap: Physics, Perception & Latency
    - **Key Concepts**: Discrepancy taxonomy (unmodeled friction, motor inductance, gear backlash, contact compliance, lighting, sensor noise, bus latency); distribution distance metrics (Wasserstein distance).
    - **Mathematical Equations**: Wasserstein-1 distance between sim and real state distributions:
      $$\mathcal{W}_1(\mathbb{P}_{sim}, \mathbb{P}_{real}) = \inf_{\gamma \in \Pi} \mathbb{E}_{(\mathbf{x}, \mathbf{y}) \sim \gamma}[\|\mathbf{x} - \mathbf{y}\|]$$
    - **Algorithms/Code**: Python script computing Wasserstein distance between simulated and physical IMU/joint telemetry trajectories.
    - **Research Citations**: Tobin et al. (2017); Kadian et al. (2020) *Sim2Real Predictivity: Does Evaluation in Simulation Predict Real-World Performance?*.

30. **`module9-sim-to-real/9-2-domain-randomization.mdx`**
    - **Title**: Domain Randomization & Adaptive Domain Randomization (ADR)
    - **Key Concepts**: Physics parameter distributions (mass, friction, damping, latency); uniform vs log-uniform sampling; OpenAI Dactyl 128-parameter breakthrough; Adaptive Domain Randomization (ADR).
    - **Mathematical Equations**: Robust MDP expected return:
      $$J(\pi) = \mathbb{E}_{\boldsymbol{\xi} \sim P(\boldsymbol{\Xi})} \left[ \mathbb{E}_{\tau \sim \pi(\boldsymbol{\xi})} \left[ \sum_{t=0}^T \gamma^t R(s_t, a_t) \right] \right]$$
    - **Algorithms/Code**: Isaac Lab domain randomization configuration script setting up physical parameter distributions.
    - **Research Citations**: Akkaya et al. (2019) *Solving Rubik's Cube with a Robot Hand* (OpenAI ADR); Peng et al. (2018).

31. **`module9-sim-to-real/9-3-system-identification.mdx`**
    - **Title**: System Identification: Rigid Body Parameters & Nonlinear Friction
    - **Key Concepts**: Classical least-squares system identification; base inertial parameters; actuator frequency sweep Bode plots; nonlinear friction modeling (Coulomb, Stribeck, LuGre).
    - **Mathematical Equations**: Identification regression matrix:
      $$\mathbf{Y}(\mathbf{q}, \dot{\mathbf{q}}, \ddot{\mathbf{q}}) \boldsymbol{\Phi} = \boldsymbol{\tau}$$
      LuGre friction model: $\tau_f = \sigma_0 z + \sigma_1 \dot{z} + \sigma_2 \dot{q}$, $\dot{z} = \dot{q} - \frac{|\dot{q}|}{g(\dot{q})} z$.
    - **Algorithms/Code**: Python least-squares identification script processing trajectory logs to extract link masses and friction coefficients.
    - **Research Citations**: Gautier & Khalil (1990); Swevers et al. (1997) *Optimal robot excitation and identification*.

32. **`module9-sim-to-real/9-4-privileged-learning.mdx`**
    - **Title**: Privileged Learning: Asymmetric Actor-Critic & RMA
    - **Key Concepts**: Teacher-student distillation; privileged information access in sim (exact ground height, friction, push forces); Asymmetric Actor-Critic; Rapid Motor Adaptation (RMA); DreamWaQ visual distillation.
    - **Mathematical Equations**: Distillation loss with privileged context vector $\mathbf{e}$:
      $$\mathcal{L} = \mathbb{E} \left[ D_{KL}\left(\pi_{teacher}(\cdot \mid \mathbf{s}_t, \mathbf{e}_t) \,\Big\|\, \pi_{student}(\cdot \mid \mathbf{s}_t, \mathbf{z}_t)\right) \right] + \lambda \|\mathbf{z}_t - \mathbf{h}(\mathbf{e}_t)\|^2$$
    - **Algorithms/Code**: Two-stage RMA training pipeline in PyTorch with teacher policy training and student trajectory encoder distillation.
    - **Research Citations**: Kumar et al. (2021) *RMA: Rapid Motor Adaptation*; Nahrendra et al. (2023) *DreamWaQ*.

33. **`module9-sim-to-real/9-5-adaptation-modules.mdx`**
    - **Title**: Online Adaptation Modules: Temporal Convolutions to Transformers
    - **Key Concepts**: Recursive Bayesian inference; online particle filters; Temporal Convolutional Networks (TCN); causal Transformers; zero-shot transfer vs test-time adaptation.
    - **Mathematical Equations**: Recursive Least Squares (RLS) parameter update:
      $$\mathbf{K}_t = \frac{\mathbf{P}_{t-1}\boldsymbol{\phi}_t}{\lambda + \boldsymbol{\phi}_t^T \mathbf{P}_{t-1}\boldsymbol{\phi}_t}, \quad \hat{\boldsymbol{\theta}}_t = \hat{\boldsymbol{\theta}}_{t-1} + \mathbf{K}_t(y_t - \boldsymbol{\phi}_t^T \hat{\boldsymbol{\theta}}_{t-1})$$
    - **Algorithms/Code**: PyTorch TCN adaptation module predicting external payload mass from a 50-step joint history window.
    - **Research Citations**: Yu et al. (2017) *Preparing for the Unknown: Learning a Universal Policy with Online System Identification*; Arndt et al. (2020).

34. **`module9-sim-to-real/9-6-real-world-fine-tuning.mdx`**
    - **Title**: Real-World Fine-Tuning: Safe Exploration & Offline-to-Online RL
    - **Key Concepts**: Hardware safety during fine-tuning (safety tether, torque threshold interception); Model-Based RL (PETS) on hardware; offline pre-training $\rightarrow$ online fine-tuning; Human-in-the-Loop corrections.
    - **Mathematical Equations**: Conservative online policy regularization:
      $$\max_\theta \mathbb{E}[R(\tau)] - \beta D_{KL}(\pi_\theta \parallel \pi_{sim})$$
    - **Algorithms/Code**: Real-world deployment script with automatic emergency torque limit safety interception for Unitree G1.
    - **Research Citations**: Haarnoja et al. (2018) *Learning to Walk via Deep Reinforcement Learning* (Real Minitaur); Smith et al. (2022) *A Walk in the Park*.

35. **`module9-sim-to-real/9-7-transfer-benchmarks.mdx`**
    - **Title**: Sim-to-Real Transfer Benchmarks & Cross-Morphology Retargeting
    - **Key Concepts**: Policy Transfer Degradation Ratio (PTDR); standardized community benchmarks (RealRobot Challenge); cross-morphology retargeting (Cassie $\rightarrow$ Digit, Unitree A1 $\rightarrow$ G1); object generalization.
    - **Mathematical Equations**: Policy Transfer Degradation Ratio:
      $$\text{PTDR} = 1 - \frac{J_{real}(\pi)}{J_{sim}(\pi)}$$
    - **Algorithms/Code**: Benchmark evaluation pipeline computing degradation ratios across sim and physical trials.
    - **Research Citations**: Wüthrich et al. (2020) *TriFinger: An Open-Source Robot for Learning Dexterous Manipulation*; Julian et al. (2020).

36. **`module9-sim-to-real/9-8-digital-twin-feedback-loop.mdx`**
    - **Title**: Differentiable Simulation & Automated Real-to-Sim Calibration
    - **Key Concepts**: Differentiable physics engines (MuJoCo MJX, Brax); gradient-based parameter calibration through simulation; neural-augmented simulation (hybrid physics + residual ML); closed digital twin sync.
    - **Mathematical Equations**: Gradient-based parameter estimation:
      $$\frac{\partial \mathcal{L}}{\partial \boldsymbol{\theta}} = \sum_{t=1}^T \frac{\partial \mathcal{L}}{\partial \mathbf{s}_t^{sim}} \frac{\partial \mathbf{s}_t^{sim}}{\partial \boldsymbol{\theta}}$$
    - **Algorithms/Code**: JAX parameter optimization script tuning MuJoCo MJX model parameters directly against real trajectory data using Adam.
    - **Research Citations**: Todorov et al. (2024) *MuJoCo MJX: High-performance physics simulation in JAX*; Freeman et al. (2021) *Brax*.

---

### Module 10: Hardware Architecture & Embedded Systems (`ai-book-docs/module10-hardware-architecture/`) — 8 Chapters
37. **`module10-hardware-architecture/10-1-humanoid-mechanical-design.mdx`**
    - **Title**: Humanoid Mechanical Architecture & Structural Optimization
    - **Key Concepts**: Anthropomorphic vs functional optimization; DOF allocation; kinematic topology (serial chains vs parallel 4-bar linkages); CoM optimization; material selection (Aluminum 7075-T6, Carbon Fiber, Titanium 6Al-4V); teardowns (Tesla Optimus Gen 2, Unitree G1, Digit).
    - **Mathematical Equations**: Swinging limb rotational inertia:
      $$I_{axis} = \sum_i (I_{cm, i} + m_i d_i^2)$$
    - **Algorithms/Code**: Python mass property tool computing humanoid limb mass distribution, total CoM, and inertia tensor from CAD export.
    - **Research Citations**: Wisse et al. (2007); Tsagarakis et al. (2017) *COMANoid: An athletic humanoid robot*; Tesla AI Day (2022/2023).

38. **`module10-hardware-architecture/10-2-actuator-technologies.mdx`**
    - **Title**: Actuator Technologies: Quasi-Direct Drive, Harmonic Drives & SEAs
    - **Key Concepts**: Motor fundamentals (BLDC torque constant $K_t$, back-EMF $K_e$); Quasi-Direct Drive (QDD); Strain Wave / Harmonic Drive; Series Elastic Actuators (SEA); hydraulic systems; actuator trade-off selection matrix.
    - **Mathematical Equations**: Actuator reflected inertia and SEA force output:
      $$I_{reflected} = N^2 I_{rotor}, \quad F_{SEA} = k_s \left(\frac{x_{motor}}{N} - x_{joint}\right)$$
    - **Algorithms/Code**: Actuator sizing and thermal dissipation calculation tool evaluating RMS torque for walking trajectories.
    - **Research Citations**: Seok et al. (2015) *Design principles for energy-efficient legged locomotion and actuation* (MIT Cheetah); Pratt & Williamson (1995) *Series Elastic Actuators*.

39. **`module10-hardware-architecture/10-3-power-electronics-and-motor-control.mdx`**
    - **Title**: Power Electronics, FOC Motor Control & Battery Systems
    - **Key Concepts**: Field Oriented Control (FOC); Clarke and Park transforms; Space Vector PWM (SVPWM); 20 kHz current control loop; GaN gate drivers; dead-time insertion; Battery Management Systems (BMS); 48V vs 24V bus architecture.
    - **Mathematical Equations**: Clarke and Park transformations:
      $$\begin{bmatrix} I_\alpha \\ I_\beta \end{bmatrix} = \frac{2}{3} \begin{bmatrix} 1 & -\frac{1}{2} & -\frac{1}{2} \\ 0 & \frac{\sqrt{3}}{2} & -\frac{\sqrt{3}}{2} \end{bmatrix} \begin{bmatrix} I_a \\ I_b \\ I_c \end{bmatrix}, \quad \begin{bmatrix} I_d \\ I_q \end{bmatrix} = \begin{bmatrix} \cos\theta & \sin\theta \\ -\sin\theta & \cos\theta \end{bmatrix} \begin{bmatrix} I_\alpha \\ I_\beta \end{bmatrix}$$
    - **Algorithms/Code**: Embedded C implementation of an FOC inner current control loop with SVPWM voltage generation.
    - **Research Citations**: Mohan, Undeland, & Robbins (2003) *Power Electronics*; Texas Instruments FOC Reference Guide.

40. **`module10-hardware-architecture/10-4-communication-buses.mdx`**
    - **Title**: Deterministic Communication Buses: EtherCAT, CAN-FD & High-Speed Links
    - **Key Concepts**: Deterministic real-time industrial networks; EtherCAT (processing on-the-fly, $\le 250\,\mu\text{s}$ cycle time); CAN-FD (8 Mbit/s, 64-byte payload); RS-485 legacy; PCIe & MIPI CSI-2 camera interfaces; humanoid wiring harness design.
    - **Mathematical Equations**: CAN-FD bus utilization formula:
      $$U = \frac{\sum_{i} (N_{bits, i} \cdot f_{m, i})}{\text{BaudRate}}$$
    - **Algorithms/Code**: C++ ROS 2 node using Simple Open EtherCAT Master (SOEM) reading 28 joint encoders at 1 kHz.
    - **Research Citations**: Robert Bosch GmbH (2012) *CAN with Flexible Data-Rate Specification*; Beckhoff Automation (2018) *EtherCAT Communication Manual*.

41. **`module10-hardware-architecture/10-5-compute-platforms.mdx`**
    - **Title**: Heterogeneous Compute Platforms: Jetson AGX Orin, NPUs & FPGAs
    - **Key Concepts**: Embedded compute architecture; Jetson family comparison (Orin NX vs AGX Orin vs Thor); Tensor Cores, DLA, and PVA; alternative platforms (Qualcomm RB5, Rockchip RK3588); FPGA co-processors; multi-board power budgeting (15W to 75W).
    - **Mathematical Equations**: Roofline attainable performance model:
      $$\text{Attainable Performance} = \min(\text{Peak GFLOPS}, \text{Memory Bandwidth} \times \text{Operational Intensity})$$
    - **Algorithms/Code**: Jetson power profile manager and DLA offload benchmarking script in Python.
    - **Research Citations**: NVIDIA Jetson AGX Orin Architecture Brief (2022); Williams, Waterman, & Patterson (2009) *Roofline*.

42. **`module10-hardware-architecture/10-6-sensor-hardware.mdx`**
    - **Title**: Sensor Hardware Integration: Cameras, IMUs, LiDARs & F/T Sensors
    - **Key Concepts**: Sensor teardown (OAK-D, ZED X, RealSense D455); MEMS IMUs (ICM-42688-P, BMI088); Solid-state LiDAR (Livox Mid-360); 6-axis F/T sensors (ATI Gamma); hardware clock synchronization (IEEE 1588 PTP, PPS triggers).
    - **Mathematical Equations**: Allan variance decomposition formula:
      $$\sigma^2_y(\tau) = \frac{N^2}{\tau} + \frac{B^2 2\ln 2}{\pi} + \frac{K^2 \tau}{3}$$
    - **Algorithms/Code**: Python Allan deviation computation tool processing raw IMU stationary data to extract noise parameters.
    - **Research Citations**: Allan (1966); El-Sheimy et al. (2008); IEEE 1588-2019 Standard.

43. **`module10-hardware-architecture/10-7-real-time-embedded-software.mdx`**
    - **Title**: Real-Time Embedded Firmware: FreeRTOS, STM32 & Motor Drives
    - **Key Concepts**: Microcontroller firmware architecture; FreeRTOS task prioritization; ISR latency minimization; STM32G4 / TI C2000; EtherCAT slave (LAN9252); safety-critical programming patterns (MISRA C:2012, IEC 61508 SIL 2); HIL testing.
    - **Mathematical Equations**: Rate Monotonic Scheduling (RMS) utilization bound:
      $$U = \sum_{i=1}^n \frac{C_i}{T_i} \le n (2^{1/n} - 1)$$
    - **Algorithms/Code**: Complete FreeRTOS C motor control task loop with deterministic 1 kHz timer and EtherCAT sync interrupt.
    - **Research Citations**: Liu & Layland (1973); FreeRTOS Reference Manual; IEC 61508 Functional Safety Standard.

44. **`module10-hardware-architecture/10-8-system-integration-and-testing.mdx`**
    - **Title**: System Integration, Bring-Up, Thermal Management & Reliability
    - **Key Concepts**: Whole-body bring-up sequencing (logic $\rightarrow$ sensors $\rightarrow$ high-voltage bus); joint homing calibration; hardware E-stop interlocks; EMI/EMC shielding; thermal management (heat pipes, active fans); MTBF estimation; automated testing fixtures.
    - **Mathematical Equations**: Mean Time Between Failures:
      $$\text{MTBF} = \frac{1}{\sum \lambda_i} = \frac{T_{total}}{N_{failures}}, \quad \Delta T = P_{dissipated} \times R_{\theta, total}$$
    - **Algorithms/Code**: Automated joint health diagnostic and sequential bring-up verification test script in ROS 2.
    - **Research Citations**: MIL-HDBK-217F; Ott (2009) *Electromagnetic Compatibility Engineering*.

---

### Module 11: Safety, Ethics & Deployment (`ai-book-docs/module11-safety-ethics/`) — 6 Chapters
45. **`module11-safety-ethics/11-1-robot-safety-standards.mdx`**
    - **Title**: Global Robot Safety Standards: ISO 10218, ISO/TS 15066 & ISO 13849
    - **Key Concepts**: Global safety regulations; ISO 10218-1/2; ISO/TS 15066 collaborative robot speed-force limits; ISO 13849 Performance Levels (PL a–e); IEC 62061; ANSI/RIA R15.08; regulatory gap analysis for untethered humanoids.
    - **Mathematical Equations**: Collaborative impact kinetic energy transfer:
      $$E = \frac{1}{2} m_{red} v_{rel}^2, \quad m_{red} = \left(\frac{1}{m_{robot}} + \frac{1}{m_{human}}\right)^{-1}$$
    - **Algorithms/Code**: Dynamic Speed and Separation Monitoring (SSM) compliance checking calculator in Python.
    - **Research Citations**: ISO 10218-1:2011; ISO/TS 15066:2016; ISO 13849-1:2023.

46. **`module11-safety-ethics/11-2-functional-safety-architecture.mdx`**
    - **Title**: Functional Safety Architecture: SIL Ratings, Redundancy & FMEA
    - **Key Concepts**: Safety Integrity Levels (SIL 1–4); dual-channel redundant architecture (1oo2, 2oo2 voting); safety PLCs; hardware watchdogs; fail-safe states (gravity compensation, electromechanical brakes); FMEA and Fault Tree Analysis (FTA).
    - **Mathematical Equations**: Probability of Dangerous Failure per Hour:
      $$PFH = \lambda_{DD} + \frac{1}{2}\beta \lambda_D, \quad DC = \frac{\sum \lambda_{DD}}{\sum \lambda_{D, total}}$$
    - **Algorithms/Code**: Dual-channel cross-monitoring heartbeat node in C++/ROS 2.
    - **Research Citations**: IEC 61508; Storey (1996) *Safety-Critical Computer Systems*.

47. **`module11-safety-ethics/11-3-human-robot-interaction-safety.mdx`**
    - **Title**: Physical Human-Robot Interaction (pHRI) Safety & Collision Detection
    - **Key Concepts**: Sensorless collision detection using generalized momentum observers; Power and Force Limiting (PFL); active impedance control; voice/gesture E-stop; Hall's social proxemics; dual-channel hardware/software E-stops.
    - **Mathematical Equations**: Generalized momentum observer residual:
      $$\mathbf{r}(t) = \mathbf{K}_I \left( \mathbf{p}(t) - \int_0^t (\boldsymbol{\tau} + \mathbf{C}^T \dot{\mathbf{q}} - \mathbf{g} + \mathbf{r}) dt \right), \quad \|\mathbf{r}\| > \tau_{thresh} \implies \text{Collision}$$
    - **Algorithms/Code**: Python/C++ momentum observer for sensorless collision detection and emergency compliance stop.
    - **Research Citations**: De Luca & Mattone (2005) *Sensorless robot collision detection and hybrid force/motion control*; Haddadin et al. (2017).

48. **`module11-safety-ethics/11-4-ethics-of-autonomous-humanoids.mdx`**
    - **Title**: Ethics of Autonomous Humanoids: Labor, Liability & Bias
    - **Key Concepts**: IEEE Ethically Aligned Design; labor displacement economics; workplace ergonomics vs human replacement; privacy in homes/workplaces; algorithmic bias in face/gesture recognition; liability assignment; EU AI Act and US EO 14110.
    - **Mathematical Equations**: Demographic Statistical Parity Difference:
      $$SPD = P(\hat{Y}=1 \mid D=\text{unprivileged}) - P(\hat{Y}=1 \mid D=\text{privileged})$$
    - **Algorithms/Code**: Bias detection and demographic fairness evaluation harness for robot vision pipelines.
    - **Research Citations**: IEEE Global Initiative (2019) *Ethically Aligned Design*; Acemoglu & Restrepo (2020) *Robots and Jobs*; EU AI Act (2024).

49. **`module11-safety-ethics/11-5-privacy-and-data-governance.mdx`**
    - **Title**: Privacy Engineering & Data Governance for Embodied Agents
    - **Key Concepts**: Data minimization; edge-only inference (zero raw video egress); differential privacy in federated robot learning; GDPR compliance; automated face/license-plate redaction; adversarial physical attacks.
    - **Mathematical Equations**: $(\epsilon, \delta)$-Differential Privacy condition:
      $$P(\mathcal{M}(D) \in S) \le e^\epsilon P(\mathcal{M}(D') \in S) + \delta$$
    - **Algorithms/Code**: Real-time edge video anonymization pipeline blurring human faces before semantic processing.
    - **Research Citations**: Dwork & Roth (2014) *The Algorithmic Foundations of Differential Privacy*; McMahan et al. (2017).

50. **`module11-safety-ethics/11-6-deployment-operations.mdx`**
    - **Title**: Deployment Operations: Fleet Management, OTA Updates & Digital Shadows
    - **Key Concepts**: RoboOps fleet management; Over-The-Air (OTA) firmware and policy deployment; A/B testing in physical robotics; digital twin synchronized shadows; Grafana/Prometheus telemetry; incident response; CE/UL certification; Agility Digit warehouse case study.
    - **Mathematical Equations**: Fleet availability metric:
      $$A = \frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}}$$
    - **Algorithms/Code**: Prometheus metrics exporter node for ROS 2 streaming joint temperature, motor current, and policy latency.
    - **Research Citations**: Kim et al. (2020) *Continuous Integration and Deployment for Robotics*; Agility Robotics (2023) *Digit Whitepaper*.

---

### Module 12: Capstone Projects & Research Frontiers (`ai-book-docs/module12-capstone-frontiers/`) — 6 Chapters
51. **`module12-capstone-frontiers/12-1-capstone-project-guide.mdx`**
    - **Title**: Humanoid Robotics Capstone Projects: Comprehensive Guide
    - **Key Concepts**: Tiered capstone projects (Beginner to Research); 4 full-stack projects: (1) Autonomous Tabletop VLA Manipulation, (2) Perceptive Bipedal Stair Climbing with RL, (3) Natural Language Voice-Commanded Mobile Assistant, (4) Bilateral VR Teleoperation with Force Feedback; grading rubrics and evaluation pipelines.
    - **Mathematical Equations**: Latency budget allocation:
      $$\tau_{total} = \tau_{perception} (30\,\text{ms}) + \tau_{planning} (50\,\text{ms}) + \tau_{WBC} (1\,\text{ms}) \le 100\,\text{ms}$$
    - **Algorithms/Code**: Full capstone project skeleton integrating ROS 2, Isaac Lab trained policy, and FastAPI cognitive bridge.
    - **Research Citations**: Open X-Embodiment Collaboration (2023); Gu et al. (2023) *ManiSkill2*.

52. **`module12-capstone-frontiers/12-2-research-frontiers-locomotion.mdx`**
    - **Title**: Research Frontiers in Locomotion: Parkour, Loco-Manipulation & Extreme Environments
    - **Key Concepts**: Extreme parkour and acrobatic agility (MIT Cheetah, ETH Neural Parkour); loco-manipulation (simultaneous balance and manipulation); compliant soft robotics; exoskeletons; extreme environment operations (OceanOne underwater humanoid); 20 unsolved locomotion challenges.
    - **Mathematical Equations**: Whole-body angular momentum regulation:
      $$\dot{\mathbf{L}}_G = \sum_{i} (\mathbf{p}_i - \mathbf{p}_G) \times \mathbf{f}_i$$
    - **Algorithms/Code**: Angular momentum regulation whole-body controller for jump landing stabilization.
    - **Research Citations**: Khatib et al. (2016) *OceanOne: A Robotic Avatar for Oceanic Exploration*; Hoeller et al. (2024).

53. **`module12-capstone-frontiers/12-3-research-frontiers-ai.mdx`**
    - **Title**: Research Frontiers in Physical AI: World Models, NeRFs & 3D Gaussian Splatting
    - **Key Concepts**: Generative world models for robotics (Dreamer V3, GAIA-1); embodied foundation models (NVIDIA Project GR00T, OpenVLA); Neural Radiance Fields (NeRF); 3D Gaussian Splatting (3DGS) for real-time scene synthesis; CLIP-based reward shaping; 20 open AI challenges.
    - **Mathematical Equations**: 3D Gaussian Splatting radiance field formulation:
      $$G(\mathbf{x}) = \exp\left(-\frac{1}{2}(\mathbf{x} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})\right), \quad \boldsymbol{\Sigma} = \mathbf{R} \mathbf{S} \mathbf{S}^T \mathbf{R}^T$$
    - **Algorithms/Code**: Real-time 3D Gaussian Splatting trajectory evaluation script in Python.
    - **Research Citations**: Kerbl et al. (2023) *3D Gaussian Splatting for Real-Time Radiance Field Rendering*; Mildenhall et al. (2020) *NeRF*; NVIDIA Project GR00T (2024).

54. **`module12-capstone-frontiers/12-4-the-future-of-humanoid-robotics.mdx`**
    - **Title**: The Future of Humanoid Robotics: 2025–2030 Technology Roadmap
    - **Key Concepts**: Strategic 2025–2030 roadmap; industrial and domestic adoption milestones; commercial ecosystem (Boston Dynamics, Figure AI, 1X, Tesla, Sanctuary, Apptronik, Unitree); Goldman Sachs market forecast (\$38B+ by 2035); Moravec's paradox resolution; robotic scaling laws.
    - **Mathematical Equations**: Chinchilla-style robotic data-compute scaling law:
      $$L(N, D) = \frac{A}{N^\alpha} + \frac{B}{D^\beta} + E$$
    - **Algorithms/Code**: Robotic scaling law parameter regression and data requirements projection script in Python.
    - **Research Citations**: Moravec (1988) *Mind Children*; Goldman Sachs Equity Research (2023) *The Humanoid Robot: A Global Multi-Billion Market*.

55. **`module12-capstone-frontiers/12-5-contributing-to-open-source.mdx`**
    - **Title**: Contributing to Open-Source Robotics & Research Communities
    - **Key Concepts**: Open-source robotics ecosystem (ROS 2, Isaac Lab, LeRobot, MuJoCo MJX, Pinocchio); contribution workflows (RFCs, PR etiquette, CI/CD); writing research papers for premier conferences (ICRA, IROS, CoRL, RSS, NeurIPS); spinning out robotics startups from open-source IP.
    - **Mathematical Equations**: H-index and citation graph connectivity calculations.
    - **Algorithms/Code**: Automated Git subtree and CI testing template for robotics open-source contributions.
    - **Research Citations**: Open Robotics Foundation Community Guidelines; IEEE RAS Author Resources.

56. **`module12-capstone-frontiers/12-6-reference-and-bibliography.mdx`**
    - **Title**: Definitive Annotated Bibliography & Reference Compendium
    - **Key Concepts**: Curated 200+ paper annotated bibliography spanning 1969 to 2025; seminal textbooks; top university graduate courses (MIT 6.832, Stanford CS329, CMU 16-831); public dataset index (Open X-Embodiment, AMASS, DROID); hardware supplier index.
    - **Mathematical Equations**: Full BibTeX database schema and citation network topology.
    - **Algorithms/Code**: BibTeX citation search and verification utility in Python.
    - **Research Citations**: Comprehensive cross-index of all 200+ cited works.

---

## 5. MDX Formatting, KaTeX & Component Specifications

### 5.1 Frontmatter Standards
Every `.mdx` file must begin with valid YAML frontmatter:
```yaml
---
sidebar_position: [integer, e.g. 1 to 14]
title: "[Complete Chapter Title]"
description: "[1-2 sentence concise summary of chapter concepts, algorithms, and hardware]"
---
```

### 5.2 KaTeX / LaTeX Syntax Rules
1. **Inline Math**: `$x_{zmp} = x - \frac{z_c}{g}\ddot{x}$`
   - Must not contain spaces immediately after opening `$` or before closing `$`.
2. **Display / Block Math**:
   ```latex
   $$
   \mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{g}(\mathbf{q}) = \mathbf{S}^T \boldsymbol{\tau} + \mathbf{J}_c^T \boldsymbol{\lambda}
   $$
   ```
3. **MDX Character Escaping**:
   - In MDX v3, curly braces `{` and `}` outside of code blocks are treated as JSX expression delimiters.
   - Inside KaTeX `$...$` and `$$...$$`, Docusaurus with `remark-math` preserves LaTeX `{...}`. However, in plain markdown text or headings, never use raw `{...}` or `<...>` without backticks or code blocks.
   - Matrix blocks must use valid LaTeX environments: `\begin{bmatrix} ... \end{bmatrix}` or `\begin{pmatrix} ... \end{pmatrix}`.

### 5.3 Diagrams & Code Blocks
1. **Mermaid Diagrams**: Fenced with ````mermaid ... ````:
   - Use `flowchart TD` or `flowchart TB` or `flowchart LR`.
   - Node labels with special characters must be enclosed in double quotes: `NodeA["Node Title (Math: \tau)"]`.
2. **Code Blocks**: Specify language identifier (`python`, `cpp`, `bash`, `yaml`, `text`, `json`).
   - Runnable snippets should include `if __name__ == "__main__":` blocks or full function signatures.

### 5.4 Interactive Components
1. **Admonitions / Callouts**:
   ```markdown
   > [!NOTE]
   > Descriptive pedagogical guidance or historical context.

   > [!IMPORTANT]
   > Critical physical hardware limits or stability warnings.

   > [!TIP]
   > Practical tuning tips and debugging advice.
   ```
2. **Interactive Quiz Engine**:
   - Tag: `<Quiz id="module6-bipedal-locomotion/6-2-zmp" />`
   - Backed by JSON question schemas in `static/quizzes/` or component props.
3. **Chapter Progress Tracker**:
   - Integrated into Docusaurus theme layout or embedded via `<ChapterProgress />`.

---

## 6. Standard 5-Component Handoff

### 1. Observation
- Verified authoritative specifications:
  - `specs/010-master-plan-curriculum-expansion/spec.md`: 951 lines detailing all 12 modules, 100+ chapters, per-chapter quality criteria, lab projects, and research citations.
  - `C:\Users\DELL\.gemini\antigravity-cli\brain\98ff215b-a62a-4d37-839f-7c685594be36\ULTRA_PRO_MAX_MASTER_PLAN.md`: 633 lines detailing v4.0 target architecture, exact chapter count progression (35 existing $\rightarrow$ 54 Phase 1 $\rightarrow$ 110 v4.0 Target), backend SSE/telemetry endpoints, frontend quiz engine, and KaTeX integration.
  - `C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\ORIGINAL_REQUEST.md`: 61 lines detailing requirements R1 through R4.
- Codebase verification:
  - Modules 1–4 currently exist in `ai-book-docs/` with 10, 5, 5, 5 chapters respectively (25 existing chapters).
  - Module 5 exists in `ai-book-docs/module5-kinematics-dynamics/` with 10 chapters completed (`5-1` to `5-10`).
  - Modules 6–12 do not yet exist in `ai-book-docs/`.
  - `docusaurus.config.ts` has `aiBookSidebar` referencing `sidebar.ts`, which uses `autogenerated` mode.
  - `package.json` contains `@docusaurus/core: ^3.10.2` and needs `remark-math` and `rehype-katex` for LaTeX math.
  - Backend has FastAPI structure in `backend/app/` with tests in `backend/tests/`.

### 2. Logic Chain
1. **Phase 1 Scope**: The master plan requires enhancing 25 existing chapters across M1–M4 and authoring 19 new chapters (4 in M1, 5 in M2, 5 in M3, 5 in M4). Total chapters in M1–M4 becomes $14 + 10 + 10 + 10 = 44$.
2. **Module 5 Status**: Module 5 has already been implemented with 10 chapters. Attempting to author Module 5 in Phase 2 would duplicate effort; Phase 2 authoring starts from Module 6 (`module6-bipedal-locomotion`) through Module 12 (`module12-capstone-frontiers`).
3. **Phase 2 Scope**: Total new chapters across M6–M12 is exactly 56: M6 (10) + M7 (8) + M8 (10) + M9 (8) + M10 (8) + M11 (6) + M12 (6) = 56 chapters.
4. **Platform & MDX Dependencies**: Because Docusaurus compiles MDX via MDX v3, any mathematical equations using `{}` or `<` must either be protected within code blocks or rendered via KaTeX once `remark-math` and `rehype-katex` are installed in Phase 3. Frontmatter must strictly define `sidebar_position` and `title` to ensure autogenerated sidebars render correctly.

### 3. Caveats
- No actual chapter code or markdown has been implemented during this turn; this report serves as a read-only, authoritative specification discovery deliverable.
- Hardware requirements (e.g. Jetson Orin, Unitree G1, EtherCAT drives) described in chapters are pedagogical and lab-specifications; code blocks must run on standard developer machines or simulation fixtures without requiring physical hardware.
- KaTeX plugins (`remark-math`, `rehype-katex`) and interactive React components (`<Quiz />`, `<ChapterProgress />`) are part of Phase 3 platform upgrades; chapters authored in Phases 1 & 2 must adhere to MDX v3 JSX compatibility rules.

### 4. Conclusion
The curriculum expansion blueprint is fully surveyed and cataloged:
- **Phase 1**: 25 existing chapters to enhance with graduate-level math, hardware specs, citations, and runnable code; 19 brand-new chapters to author across Modules 1–4.
- **Phase 2**: 56 brand-new chapters to author across Modules 6 through 12.
- **Phase 3**: Backend SSE streaming, telemetry `/analytics`, module retrieval, incremental auto-ingest; frontend sidebar wiring, KaTeX rendering, quiz engine, and progress tracker.
The planning and authoring subagents now have an exhaustive, unambiguous reference inventory.

### 5. Verification Method
1. Inspect this inventory file directly:
   `Get-Content C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\spec_miner_curriculum\handoff.md`
2. Cross-verify chapter lists against `specs/010-master-plan-curriculum-expansion/spec.md` and `ULTRA_PRO_MAX_MASTER_PLAN.md`.
3. Verify existing module count and files:
   `Get-ChildItem ai-book-docs -Directory`
