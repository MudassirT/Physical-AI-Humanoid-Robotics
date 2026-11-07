# Changelog

All notable changes to the **Physical AI & Humanoid Robotics** platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
