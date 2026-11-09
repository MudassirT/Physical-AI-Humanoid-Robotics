# Dual-Track E2E Testing Infrastructure Specification

**Document Version**: 1.0.0  
**Target Platform**: Physical AI & Humanoid Robotics Curriculum & Platform  
**Architecture**: Dual-Track (Curriculum Track + Platform & Backend Track)  
**Standard**: Opaque-Box, Requirement-Driven, Zero External Credentials  

---

## 1. Executive Summary & Test Philosophy

This document defines the automated End-to-End (E2E) testing infrastructure for the **12-Module Humanoid Robotics Curriculum & Platform Expansion**. The testing framework establishes rigorous quality gates ensuring both pedagogical perfection across all 110 graduate-level chapters and industrial reliability across the FastAPI/Qdrant backend and Docusaurus 3 frontend.

### 1.1 Core Principles

1. **Opaque-Box Requirement-Driven Verification**:
   - Tests evaluate system behavior strictly through declared public interface contracts, HTTP endpoints, MDX syntactical specifications, and file schemas.
   - Tests verify *what* the system accomplishes, not private implementation internals.

2. **Zero Reliance on External Live API Keys (Hermetic Isolation)**:
   - All tests run completely offline without requiring active OpenAI, Gemini, Cohere, or Qdrant Cloud API credentials.
   - Test fixtures provide deterministic, state-isolated mock doubles replicating the exact wire protocols and schemas of external AI services.

3. **Dual-Track Progressive Testability**:
   - **Track A (Curriculum Track)**: Evaluates all documentation files (`.mdx`), frontmatter metadata, KaTeX mathematical typography, code block syntax, and internal cross-references.
   - **Track B (Platform Track)**: Evaluates FastAPI route behaviors, SSE token streaming, telemetry ingestion, Qdrant payload filtering, and incremental ingestion manifests.
   - **Milestone Gating**: Progressive test execution supports milestone-in-progress validation (M1 platform, M2–M4 curriculum deepening and authoring) up to the comprehensive M5 final release gate.

---

## 2. 4-Tier Test Suite Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          4-Tier Dual-Track Test Suite                           │
├───────────────────────────────────────┬─────────────────────────────────────────┤
│ Track A: Curriculum Verification     │ Track B: Platform & Backend Services    │
├───────────────────────────────────────┼─────────────────────────────────────────┤
│ Tier 1: Feature Coverage              │ Tier 1: Feature Coverage                │
│ - MDX YAML frontmatter validity       │ - Health, heartbeat & retrieval-test    │
│ - Mandatory title & sidebar_position  │ - Unary /ask question answering         │
│ - Balanced $...$ & $$...$$ KaTeX tags │ - SSE streaming /ask protocol           │
│ - 110-chapter master plan inventory   │ - /analytics POST telemetry ingestion   │
│ - Code block language identifiers     │ - /analytics GET metrics reporting      │
├───────────────────────────────────────┼─────────────────────────────────────────┤
│ Tier 2: Boundary & Corner Cases       │ Tier 2: Boundary & Corner Cases         │
│ - Unescaped curly braces in MDX text  │ - Empty and whitespace-only queries     │
│ - Complex LaTeX (matrices, Greek)     │ - Ultra-long query payloads (>10K chars)│
│ - Non-breaking spaces and unicode     │ - Invalid module filter fallbacks       │
│ - Deeply nested markdown structures   │ - Malformed analytics JSON & types      │
│ - Missing optional frontmatter fields │ - Rapid concurrent telemetry writes     │
├───────────────────────────────────────┼─────────────────────────────────────────┤
│ Tier 3: Cross-Feature Interactions    │ Tier 3: Cross-Feature Interactions      │
│ - Module category JSON hierarchy      │ - QuizEngine -> /analytics dispatch     │
│ - Code snippet - equation alignment   │ - ChapterProgress -> /analytics dispatch│
│ - Chapter citation link integrity     │ - Filtered /ask -> Qdrant scoped query  │
│                                       │ - Incremental ingestion dirty checking  │
├───────────────────────────────────────┼─────────────────────────────────────────┤
│ Tier 4: Real-World Scenarios          │ Tier 4: Real-World Scenarios            │
│ - Complete 110-chapter link resolver  │ - Full RAG pipeline flow (Query ->      │
│ - Zero dead internal links/anchors    │   Retriever -> Stream -> Done event)    │
│ - Docusaurus production config audit  │ - Concurrency under telemetry load      │
│ - KaTeX CDN stylesheet verification   │ - Deterministic UUID5 point IDs         │
└───────────────────────────────────────┴─────────────────────────────────────────┘
```

### 2.1 Tier 1: Feature Coverage
- **Objective**: Verify that every documented feature, endpoint, and content unit exists and obeys its base contract.
- **Curriculum Scope**:
  - Validates that every `.mdx` file starts with valid YAML frontmatter containing `title` and `sidebar_position`.
  - Verifies that math expressions have matching opening and closing delimiters (`$` for inline, `$$` for block).
  - Checks for the existence of all 110 curriculum chapters against the authoritative 12-module master plan.
- **Backend Scope**:
  - `GET /heartbeat`: Verifies liveness response `{"status": "alive"}`.
  - `GET /health`: Verifies operational health status `{"status": "ok"}`.
  - `POST /ask` (Unary): Verifies 200 OK with `ChatResponse` schema (`answer_text`, `retrieved_sources`).
  - `POST /ask` (Streaming): Verifies 200 OK with `text/event-stream` returning ordered events (`event: sources`, `event: token`*, `event: done`).
  - `POST /analytics`: Verifies 200/201 response with `AnalyticsResponse` schema (`status: "recorded"`, `event_id: str`).
  - `GET /analytics`: Verifies 200 OK returning `AnalyticsSummary` aggregates.

### 2.2 Tier 2: Boundary & Corner Cases
- **Objective**: Ensure resilience against malformed inputs, edge cases, and unexpected system stress.
- **Curriculum Scope**:
  - Detects unescaped JSX curly braces outside code fences and math blocks which trigger MDX v3 compiler crashes.
  - Validates complex LaTeX constructs: matrices (`\begin{bmatrix} ... \end{bmatrix}`), tensors, piecewise functions (`\begin{cases}`), and Greek symbols.
- **Backend Scope**:
  - `POST /ask` with empty query `""` or whitespace `"   "` -> Expects HTTP 422 Unprocessable Entity.
  - `POST /ask` with ultra-long query (10,000+ characters) -> Successfully handled without memory leak or unhandled exception.
  - `POST /ask` with unknown module filter (e.g., `"module999"`) -> Graceful fallback to global search or empty chunk handling without server crash.
  - `POST /analytics` with invalid `event_type` (e.g. `"button_hover"`) -> Expects HTTP 422.
  - `POST /analytics` with empty JSON body `{}` -> Expects HTTP 422.
  - High-concurrency telemetry logging: Simulates 50 simultaneous asynchronous event posts ensuring no corrupted lines in `backend/logs/analytics.jsonl`.

### 2.3 Tier 3: Cross-Feature Interactions
- **Objective**: Validate the contracts between distinct architectural modules and client-server workflows.
- **Workflows Verified**:
  1. **QuizEngine -> Backend Telemetry**: Verifies that the JSON payload emitted upon quiz completion matches the schema expected by `POST /analytics` (`event_type: "quiz_score"`).
  2. **ChapterProgress -> Backend Telemetry**: Verifies that chapter completion toggles generate valid `POST /analytics` events (`event_type: "progress_update"`).
  3. **Module-Scoped Retrieval Integration**: Verifies that passing `module_filter` in `ChatQuery` causes `RetrieverService` to construct a Qdrant `models.Filter` matching `models.FieldCondition(key="module", match=models.MatchValue(value=...))`.
  4. **Incremental Ingestion Change Detection**: Verifies that `backend/ingest_docs.py` computes SHA-256 file hashes, skips unmodified files, updates modified chunks, and prunes deleted chapters.

### 2.4 Tier 4: Real-World Scenarios
- **Objective**: Validate integrated real-world end-to-end execution.
- **Scenarios Verified**:
  1. **Curriculum-Wide Internal Link Integrity**: Parses all markdown links across all chapters and asserts that zero links point to non-existent chapters, missing files, or invalid document anchors.
  2. **Docusaurus Production Configuration Audit**: Validates `docusaurus.config.ts` for presence of `remark-math@^6`, `rehype-katex@^7`, and KaTeX CDN stylesheet links.
  3. **End-to-End RAG Stream Pipeline**: Simulates a full user interaction lifecycle: query submission -> vector chunk retrieval -> prompt synthesis -> streaming token generator -> event stream consumption -> completion validation.

---

## 3. Authoritative 110-Chapter Master Curriculum Matrix

The complete curriculum comprises **110 chapters across 12 modules** plus the introductory treatise:

| Module | Title | Chapter Count | Directory Path |
|:---|:---|:---:|:---|
| **Intro** | Foundations of Physical AI | 1 | `ai-book-docs/intro.mdx` |
| **Module 1** | The Robotic Nervous System (ROS 2) | 14 | `ai-book-docs/module1-ros2/` (`1-1` to `1-14`) |
| **Module 2** | The Digital Twin (Gazebo & Unity) | 10 | `ai-book-docs/module2-digital-twin/` (`2-1` to `2-10`) |
| **Module 3** | The AI-Robot Brain (NVIDIA Isaac) | 10 | `ai-book-docs/module3-ai-robot-brain/` (`3-1` to `3-10`) |
| **Module 4** | Vision-Language-Action (VLA) Systems | 10 | `ai-book-docs/module4-vla/` (`4-1` to `4-10`) |
| **Module 5** | Humanoid Kinematics & Dynamics | 10 | `ai-book-docs/module5-kinematics-dynamics/` (`5-1` to `5-10`) |
| **Module 6** | Bipedal Locomotion & Whole-Body Control | 10 | `ai-book-docs/module6-bipedal-locomotion/` (`6-1` to `6-10`) |
| **Module 7** | Dexterous Manipulation & Hand Design | 8 | `ai-book-docs/module7-dexterous-manipulation/` (`7-1` to `7-8`) |
| **Module 8** | Robot Learning & Reinforcement Learning | 10 | `ai-book-docs/module8-robot-learning/` (`8-1` to `8-10`) |
| **Module 9** | Sim-to-Real Transfer & Domain Randomization | 8 | `ai-book-docs/module9-sim-to-real/` (`9-1` to `9-8`) |
| **Module 10** | Hardware Architecture & Embedded Systems | 8 | `ai-book-docs/module10-hardware-architecture/` (`10-1` to `10-8`) |
| **Module 11** | Safety, Ethics & Deployment | 6 | `ai-book-docs/module11-safety-ethics/` (`11-1` to `11-6`) |
| **Module 12** | Capstone Projects & Research Frontiers | 6 | `ai-book-docs/module12-capstone-frontiers/` (`12-1` to `12-6`) |
| **Total** | **Full Curriculum Expansion** | **110 Chapters** (+ 1 Intro) | **111 Total MDX Documents** |

---

## 4. Test Suite Execution & Runner Instructions

### 4.1 Running Tests via Pytest (Backend Environment)

All automated tests are integrated with `pytest` inside the Python 3.13 backend environment:

```powershell
# Navigate to backend directory
cd backend

# Execute all E2E tests
uv run pytest tests/e2e -v

# Execute specific tiers
uv run pytest tests/e2e/test_tier1_curriculum_coverage.py -v
uv run pytest tests/e2e/test_tier1_backend_coverage.py -v
uv run pytest tests/e2e/test_tier2_boundary_corner_cases.py -v
uv run pytest tests/e2e/test_tier3_cross_feature_interactions.py -v
uv run pytest tests/e2e/test_tier4_real_world_scenarios.py -v

# Execute with strict 110-chapter presence requirement (Milestone 5 Gate)
$env:STRICT_110="1"; uv run pytest tests/e2e/test_tier1_curriculum_coverage.py -v
```

### 4.2 Running Tests via Unified Root Test Runner

A standalone cross-platform Python runner `run_e2e_tests.py` is available at project root:

```powershell
# Run all tiers with unified summary report
uv run --directory backend python ../run_e2e_tests.py --all

# Run curriculum validation only
uv run --directory backend python ../run_e2e_tests.py --curriculum-only

# Run backend services validation only
uv run --directory backend python ../run_e2e_tests.py --backend-only

# Run specific tier
uv run --directory backend python ../run_e2e_tests.py --tier 1
```

### 4.3 Pass/Fail Criteria & CI/CD Quality Gates

| Gate Metric | Threshold | Consequence on Failure |
|:---|:---:|:---|
| **Pytest Pass Rate** | 100% of applicable tests | Immediate build break; deployment blocked |
| **MDX Syntax Errors** | 0 allowed | Compilation failure; PR blocked |
| **Unescaped JSX Curlys** | 0 allowed | Build failure; PR blocked |
| **Broken Math Tags** | 0 allowed | Typography defect; PR blocked |
| **Dead Internal Links** | 0 allowed | Navigation defect; PR blocked |
| **Ruff Code Violations** | 0 allowed | Lint failure; PR blocked |

---

## 5. Mock Architecture & Isolation Details

All tests use strictly isolated fixtures defined in `backend/tests/e2e/conftest.py`:
- **Qdrant Mock**: Intercepts `query_points`, `upsert`, and `delete` calls, returning canned `models.ScoredPoint` or `models.QueryResponse` objects matching real vector search behavior.
- **Gemini Mock**: Implements both `generate_content` (unary) and `generate_content_stream` (yielding token chunk objects).
- **Cohere Mock**: Returns fixed 1024-dimensional normalized float vectors for arbitrary text queries without network traffic.
- **Telemetry Sandbox**: Redirects JSONL log writes to a temporary directory (`tempfile.TemporaryDirectory`) cleaned up automatically after each test.
