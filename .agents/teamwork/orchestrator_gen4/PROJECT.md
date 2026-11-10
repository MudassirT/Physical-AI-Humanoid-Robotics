# Project: Production-Grade Humanoid Robotics Curriculum & Platform Expansion

## Architecture

The project delivers an advanced, graduate-level physical AI & humanoid robotics curriculum (110 chapters across 12 modules) powered by a Docusaurus 3 / MDX 3 frontend and a FastAPI / Qdrant / Gemini RAG backend.

```
                          ┌────────────────────────────┐
                          │   Docusaurus 3 Frontend    │
                          │     (ai-book-docs/)        │
                          └─────────────┬──────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
┌─────────────────────┐      ┌────────────────────┐      ┌─────────────────────┐
│  Curriculum Modules │      │ Interactive React  │      │ MathJax / KaTeX     │
│  M1–M12 (110 docs)  │      │ - ChapterProgress  │      │ - remark-math@6     │
│  - Frontmatter      │      │ - QuizEngine       │      │ - rehype-katex@7    │
│  - LaTeX equations  │      │ - FloatingAssistant│      │ - katex.min.css     │
│  - Runnable code    │      │ - 12-Module Sidebar│      │                     │
└─────────────────────┘      └──────────┬─────────┘      └─────────────────────┘
                                        │ REST / SSE
                                        ▼
                          ┌────────────────────────────┐
                          │     FastAPI Backend        │
                          │        (backend/)          │
                          └─────────────┬──────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
┌─────────────────────┐      ┌────────────────────┐      ┌─────────────────────┐
│  Streaming /ask     │      │ Telemetry /analytics│     │ Qdrant Vector Store │
│  - SSE event stream │      │ - POST event ingest│      │ - Module filtering  │
│  - Token generation │      │ - GET aggregates   │      │ - Hash auto-ingest  │
│  - Unary fallback   │      │ - JSONL file log   │      │ - Cohere embeddings │
└─────────────────────┘      └────────────────────┘      └─────────────────────┘
```

---

## Feature Inventory

| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | KaTeX Math Configuration | Install remark-math@6, rehype-katex@7, KaTeX CSS in Docusaurus | M1 | Survey Miner 2 |
| 2 | 12-Module Sidebar & Navigation | Register M1–M12 and all 110 chapters in `ai-book-docs/sidebar.ts` and navbar | M1 | Survey Miner 2 |
| 3 | Interactive Chapter Progress Component | `src/components/ChapterProgress/` tracking completed chapters via localStorage | M1 | Survey Miner 2 |
| 4 | Interactive Quiz Engine Component | `src/components/QuizEngine/` multi-choice quiz with explanations and scoring | M1 | Survey Miner 2 |
| 5 | Backend SSE Streaming `/ask` | Real-time SSE token stream (`event: sources`, `token`, `done`, `error`) | M1 | Survey Miner 2 |
| 6 | Backend Telemetry `/analytics` | `POST /analytics` & `GET /analytics` storing JSONL event metrics | M1 | Survey Miner 2 |
| 7 | Qdrant Module Filter | Payload `module` field and filter in `RetrieverService.retrieve_chunks` | M1 | Survey Miner 2 |
| 8 | Incremental Hash Auto-Ingestion | SHA-256 change detection manifest in `backend/ingest_docs.py` | M1 | Survey Miner 2 |
| 9 | M1 Deepening & New Chapters | Enhance 1-1..1-10; Author 1-11..1-14 (ros2_control, DDS, PREEMPT_RT, telemetry) | M2 | Survey Miner 1 |
| 10 | M2 Deepening & New Chapters | Enhance 2-1..2-5; Author 2-6..2-10 (URDF/SDF, Featherstone, SDG, Drake, DT loop) | M2 | Survey Miner 1 |
| 11 | M3 Deepening & New Chapters | Enhance 3-1..3-5; Author 3-6..3-10 (cuVSLAM, semantic vision, F/T, fusion, INT8) | M2 | Survey Miner 1 |
| 12 | M4 Deepening & New Chapters | Enhance 4-1..4-5; Author 4-6..4-10 (VLA architectures, diffusion, ACT, RLAIF, safety)| M2 | Survey Miner 1 |
| 13 | Module 6 Authoring | 10 chapters on Bipedal Locomotion (ZMP, 3D-LIPM, DCM, MPC, WBC, RL, Sim2Real) | M3 | Survey Miner 1 |
| 14 | Module 7 Authoring | 8 chapters on Dexterous Manipulation (Grasp theory, hand design, GelSight, MoveIt) | M3 | Survey Miner 1 |
| 15 | Module 8 Authoring | 10 chapters on Robot Learning & RL (PPO, SAC, continuous, Isaac Lab, World models)| M3 | Survey Miner 1 |
| 16 | Module 9 Authoring | 8 chapters on Sim-to-Real Transfer (Reality gap, ADR, sysID, RMA, fine-tuning) | M3 | Survey Miner 1 |
| 17 | Module 10 Authoring | 8 chapters on Hardware Architecture (Mechanics, actuators, FOC, EtherCAT, Jetson)| M4 | Survey Miner 1 |
| 18 | Module 11 Authoring | 6 chapters on Safety, Ethics & Deployment (ISO standards, SIL, pHRI, ethics, OTA)| M4 | Survey Miner 1 |
| 19 | Module 12 Authoring | 6 chapters on Capstone Projects & Frontiers (4 capstones, frontiers, roadmap, bib)| M4 | Survey Miner 1 |
| 20 | E2E Build & Test Verification | `npm run build`, `npm run typecheck`, backend `pytest`, backend `ruff` | M5 | Survey Explorer 3 |

---

## Milestones

| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Platform & Infrastructure Upgrades | Backend SSE streaming, `/analytics`, Qdrant module filtering, incremental ingestion; Frontend KaTeX plugins, Chapter Progress, Quiz Engine, 12-Module Sidebar | none | DONE |
| M2 | Phase 1: Deepen Modules 1–4 | Enhance 25 existing chapters with graduate-level math, hardware specs, citations, code; Author 19 new chapters across M1–M4 | M1 | DONE |
| M3 | Phase 2: Author Modules 6–9 | Author 36 new chapters in M6 (Locomotion, 10 ch), M7 (Manipulation, 8 ch), M8 (Robot Learning, 10 ch), M9 (Sim-to-Real, 8 ch) | M1, M2 | DONE |
| M4 | Phase 2: Author Modules 10–12 | Author 20 new chapters in M10 (Hardware, 8 ch), M11 (Safety & Ethics, 6 ch), M12 (Capstones & Frontiers, 6 ch) | M3 | IN_PROGRESS |
| M5 | E2E Testing, Quality Gates & Forensic Audit | Clean `npm run build`, `pytest` (100% pass), `ruff check .` clean, link validation, forensic integrity audit | M1, M2, M3, M4 | PLANNED |

### Key Outputs of Completed Milestones:
- **Milestone M1**:
  - Frontend: `remark-math@6`, `rehype-katex@7`, KaTeX CSS in `docusaurus.config.ts`, `ai-book-docs/sidebar.ts` with 12 modules, `src/components/ChapterProgress/` and `src/components/QuizEngine/` components, `FloatingAssistant` SSE stream support.
  - Backend: `StreamingResponse` on `POST /ask` with SSE event protocol, `POST /analytics` & `GET /analytics` with `backend/logs/analytics.jsonl` persistence, Qdrant payload & `module_filter` query filtering in `RetrieverService`, SHA-256 incremental hash auto-ingestion in `backend/ingest_docs.py`.
  - Testing: 107/107 pytest tests passing, 28/28 E2E tests passing, 0 ruff errors, `npm run build` static production assets generated cleanly with 0 broken links.
- **Milestone M2**:
  - Module 1 (14 chapters): 10 enhanced chapters + 4 new (`1-11-ros2-control`, `1-12-dds-internals`, `1-13-real-time-linux`, `1-14-ros2-diagnostics-and-monitoring`).
  - Module 2 (10 chapters): 5 enhanced chapters + 5 new (`2-6-urdf-and-sdf-mastery`, `2-7-physics-engine-deep-dive`, `2-8-synthetic-data-generation`, `2-9-drake-and-mujoco`, `2-10-digital-twin-data-loop`).
  - Module 3 (10 chapters): 5 enhanced chapters + 5 new (`3-6-cuvslam-and-state-estimation`, `3-7-semantic-perception`, `3-8-force-torque-sensing`, `3-9-multi-sensor-fusion`, `3-10-edge-inference-optimization`).
  - Module 4 (10 chapters): 5 enhanced chapters + 5 new (`4-6-foundation-model-architectures`, `4-7-diffusion-policies`, `4-8-imitation-learning`, `4-9-reward-shaping-and-rlaif`, `4-10-deployment-and-safety`).
  - Quality & Testing: All 44 chapters verified with graduate-level LaTeX math, hardware specs, citations, runnable code, `<ChapterProgress />` and `<QuizEngine />`.
  - Hermeticity: 121/121 backend pytest tests passing 100% offline with zero live network calls. 28/28 E2E tests passing. 0 ruff errors. Production `npm run build` passes with 0 broken links. Gate Iteration 4: PASS.

---

## Interface Contracts

### 1. Backend SSE Streaming Protocol (`POST /ask`)
- **Headers**: `Accept: text/event-stream` or `stream: true` in body
- **Events**:
  - `event: sources\ndata: {"sources": ["/ai-book/moduleX/..."]}\n\n`
  - `event: token\ndata: {"token": "..."}\n\n`
  - `event: done\ndata: {"done": true, "total_sources": N}\n\n`
  - `event: error\ndata: {"error": "..."}\n\n`
- **Fallback**: Unary JSON `ChatResponse(answer_text, retrieved_sources)` when `stream=false`

### 2. Backend Telemetry Schema (`POST /analytics`, `GET /analytics`)
- **Payload**:
  - `event_type`: "page_view" | "query" | "quiz_score" | "progress_update"
  - `timestamp`: ISO-8601 string
  - `session_id`: Optional string
  - `module_id`: Optional string
  - `chapter_id`: Optional string
  - `data`: Dict[str, Any]
- **Log storage**: `backend/logs/analytics.jsonl`

### 3. Qdrant Payload & Filter Contract
- **Payload fields**: `text`, `source_url`, `title`, `chunk_index`, `module`, `chapter`, `content_hash`
- **Filter**: `models.Filter(must=[FieldCondition(key="module", match=MatchValue(value=module_filter))])`

### 4. Frontend MDX & Component Contract
- **KaTeX math**: `$math$` for inline, `$$math$$` for block. No unescaped curly braces in headings or body text.
- **Frontmatter**:
  ```yaml
  ---
  sidebar_position: <int>
  title: "<Full Title>"
  description: "<Concise Summary>"
  ---
  ```
- **Category Files**: Each module directory has `_category_.json` with `label` and `position`.

---

## Code Layout

- Frontend:
  - `ai-book-docs/`: Markdown / MDX documentation files organized by module folder (`module1-ros2` to `module12-capstone-frontiers`).
  - `ai-book-docs/sidebar.ts`: Master navigation definition.
  - `docusaurus.config.ts`: Site configuration, plugin setup (remark-math, rehype-katex), stylesheets.
  - `src/components/`: React interactive components (`ChapterProgress`, `QuizEngine`, `FloatingAssistant`).
- Backend:
  - `backend/app/main.py`: FastAPI application entrypoint, middleware, router inclusions.
  - `backend/app/routes/`: Route handlers (`chat.py`, `analytics.py`).
  - `backend/app/agent/agent_service.py`: LLM agent logic with token streaming generator.
  - `backend/app/retriever/retriever_service.py`: Qdrant search with module filtering.
  - `backend/app/schemas/chat_models.py`: Pydantic request/response schemas.
  - `backend/ingest_docs.py`: Incremental hash-based auto-ingestion CLI script.
  - `backend/tests/`: Pytest fixtures and test modules.
