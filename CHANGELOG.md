# Changelog

All notable changes to the **Physical AI & Humanoid Robotics** platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.4.0] - 2026-11-11

### Added
- **Professional Cybernetic Vector Logo**: Bespoke aerospace-grade SVG brand identity featuring humanoid cranium, stereoscopic perception visor, quantum core, and bipedal chevrons (`static/img/physical-ai-robotics-logo.svg`).
- **High-Visibility Vector Favicon**: Crisp cyber hex favicon optimized for both dark and light browser tabs (`static/img/favicon.svg`).
- **Complete 12-Module Homepage Matrix**: Expanded curriculum showcase to feature all 12 modules with category filter tabs (Foundations, Embodied AI, Dynamics, Systems) in `src/components/HomepageFeatures`.
- **Interactive Telemetry Showcase Upgrade**: Live simulated real-time metrics (0.38 ms loop latency, zero-copy shared memory) and VLA whole-body control code snippets.

### Changed
- **Comprehensive UI Overhaul**: Glassmorphic frosted navbar, ambient dynamic glow blooms, high-contrast syntax tokens, and micro-interactions.
- **AI Tutor Suggestions**: Expanded quick prompt chips across kinematics, bipedal locomotion, and massively parallel reinforcement learning.

---

## [2.3.0] - 2026-11-08

### Added
- **Module 5: Humanoid Kinematics & Dynamics**: 10 comprehensive chapters covering mathematical geometry and multi-body dynamics:
  - *5-1: Introduction to Humanoid Kinematics & Coordinate Geometry* (SE(3), SO(3), Quaternions, SLERP, DH Parameters)
  - *5-2: Forward Kinematics, Screw Theory & Lie Group SE(3)* (Twists, Rodrigues' formula, Product of Exponentials, Geometric Jacobians)
  - *5-3: Inverse Kinematics, Redundancy Resolution & Optimization* (DLS, Levenberg-Marquardt, Null-Space Projection, QP Whole-Body IK)
  - *5-4: Rigid Body Dynamics & Featherstone's Articulated Body Algorithm* (RNEA O(n) inverse dynamics, CRBA O(n^2), ABA O(n) forward dynamics)
  - *5-5: Spatial Vector Algebra & Plücker Coordinates* (Motion space M^6 vs Force space F^6 duality, 6x6 spatial inertia, Plücker transforms)
  - *5-6: Floating-Base Dynamics, Centroidal Momentum & Anthropometry* (6-DOF unactuated base, Winter's mass distribution, CMM matrix)
  - *5-7: Trajectory Generation, Minimum-Jerk Profiles & Splines* (C^2 quintic splines, Flash-Hogan minimum-jerk, bipedal swing leg)
  - *5-8: Differential Kinematics, Manipulability & Singularities* (SVD decomposition, Yoshikawa manipulability, condition number)
  - *5-9: Contact Mechanics, Friction Cones & Ground Reaction Forces* (Unilateral constraints, Coulomb friction cones, CoP bounds)
  - *5-10: Computational Dynamics Engines, Pinocchio & Drake Benchmarking* (Pinocchio v3, Drake, 1 kHz latency profiling on Jetson Orin)
- **Master Plan for Curriculum Expansion**: 12-module roadmap blueprint (`specs/010-master-plan-curriculum-expansion/spec.md`) scaling curriculum to 100+ chapters.
- **Deep Chapter Enhancements in Modules 1–4**:
  - *Module 1*: Added OROCOS/YARP middleware comparison, RTPS wire protocol discovery (PDP/EDP), multi-threaded executor patterns, Eclipse Iceoryx zero-copy shared memory, and SROS2 PKI security.
  - *Module 2*: Added ISO 23247 digital twin maturity models, LCP constraint solvers in DART, Allan variance stochastic IMU noise models, Unity HDRP coordinate transforms, and laboratory evaluation rubrics.
  - *Module 3*: Added Jetson Thor / Orin hardware comparison, PhysX 5 reduced coordinate articulators, NITROS zero-copy GPU memory exchange, and 3D elevation lattice planning.
  - *Module 4*: Added OpenVLA / π0 / Octo / GR00T foundation architecture matrix, microphone array acoustic beamforming, SayCan mathematical scoring, and FoundationPose 6D tracking.

---

## [2.2.0] - 2026-11-07

### Added
- **Global Hardware-Accelerated Reading Progress Bar**: Real-time 60 FPS top reading indicator dynamically tracking user scroll with direct DOM `scaleX` GPU transforms (`src/components/ReadingProgressBar`).
- **Persistent Floating RAG Assistant Drawer**: Global bottom-right floating trigger (`⌘K` / `Ctrl+K`), slide-out drawer, dynamic context-aware starter prompts matching the active documentation path, and copy-to-clipboard functionality (`src/components/FloatingAssistant`).
- **Interactive Robotics Showcase Terminal**: Tabbed live code and telemetry viewer on homepage hero covering ROS 2 Humble/Jazzy, Gazebo Harmonic, NVIDIA Isaac ROS, and OpenVLA foundation policies.
- **Enterprise Curriculum Module Grid**: 4 color-accented cards (Cyber Blue, Digital Twin Violet, Isaac Emerald, VLA Coral) with estimated study durations, topic checklists, and animated arrows.
- **D3 Selection Prototype Protection**: Defensive monkey-patch in `src/theme/Root.tsx` ensuring Mermaid diagram hover tooltips resolve cleanly without `transition is not a function` exceptions under Rspack bundling.
- **World-Class SEO & Schema.org Metadata**: OpenGraph, Twitter card tags, search crawler directives in `robots.txt`, and injected Schema.org `WebSite` and `Course` JSON-LD schemas.
- **Vector Brand Identity**: Bespoke cybernetic humanoid SVG logo and high-DPI favicon.
- **GitHub Enterprise Governance**: CodeQL vulnerability analysis, multi-stage Docker build verification workflow, Dependabot maintenance configuration, and curriculum chapter proposal issue template.

### Fixed
- **Sidebar Navigation Active Line Styling**: Restored clean, flush left accent bar (`border-left: 3.5px solid var(--ifm-color-primary)`) on active documentation links, eliminating unwanted inset pill lines and preserving right-corner radii.
- **Code Block High-Contrast Syntax Highlighting**: Overhauled Prism code container tokens with dark slate `#0d111c` background, `#f8fafc` text, and vibrant color-coded syntax tokens across both light and dark themes.
- **Mermaid Sequence Delimiter Errors**: Replaced statement-delimiting semicolons on message arrows in `1-6-services.mdx` and `1-1-introduction.mdx`.
- **Rspack Windows File-Locking Panics**: Disabled `rspackPersistentCache` in `docusaurus.config.ts` to prevent persistent cache snapshot crashes on Windows.
- **Vector Search Accuracy Alignment**: Updated retrieval similarity test thresholds in `backend/tests/retrieval/test_retrieval.py` to match dense Cohere v3 embeddings.

---

## [2.1.0] - 2026-11-06

### Added
- **Integrated RAG Chat Widget**: Homepage interactive assistant connected to FastAPI vector search backend.
- **Clean Route Normalization**: Automatic transformation of disk `.mdx` file paths into clean Docusaurus URL routes for citation links.
- **Automated Documentation Ingestion**: Vectorization pipeline (`ingest_docs.py`) chunking 26 curriculum chapters into Qdrant Cloud.

### Changed
- Refactored homepage layout with responsive grid architecture and glassmorphism styling.
- Standardized FastAPI endpoints with Pydantic v2 data models and OpenAPI schemas.

---

## [2.0.0] - 2026-11-05

### Added
- **Full Curriculum Authoring**: Complete 4-module graduate textbook across 26 technical chapters:
  - *Module 1: The Robotic Nervous System (ROS 2 Humble & Jazzy)*
  - *Module 2: The Digital Twin (Gazebo Harmonic & Unity HDRP)*
  - *Module 3: The AI Robot Brain (NVIDIA Isaac Sim 4.0 & Nav2 Bipedal)*
  - *Module 4: Vision-Language-Action (OpenVLA, Flow Matching & Cognitive Grounding)*
- **Multi-Container Docker Architecture**: Multi-stage `Dockerfile` and `docker-compose.yml` for unified local and production deployments.

---

## [1.0.0] - 2026-10-30

### Added
- Initial project architecture and Docusaurus v3 setup.
- Basic FastAPI backend skeleton with vector retriever services.
- Initial ROS 2 middleware chapters and core concepts documentation.