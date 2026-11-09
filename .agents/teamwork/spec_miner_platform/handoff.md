# Handoff Report — Phase 3: Platform & Infrastructure Upgrades Specification Breakdown

**Agent**: `teamwork_spec_miner` (Platform & Infrastructure)  
**Date**: 2026-11-09T14:27:00Z  
**Target Milestone**: Phase 3 Platform & Infrastructure Upgrades  
**Related Specs**:
- `specs/010-master-plan-curriculum-expansion/spec.md`
- `C:\Users\DELL\.gemini\antigravity-cli\brain\98ff215b-a62a-4d37-839f-7c685594be36\ULTRA_PRO_MAX_MASTER_PLAN.md`
- `.agents/teamwork/ORIGINAL_REQUEST.md`

---

## 1. Observation

Direct code and environment observations gathered during specification probing:

### 1.1 Backend Architecture & Existing Codebase
1. **Application Entrypoint (`backend/app/main.py`)**:
   - Lines 37–43 configure CORS (`allow_origins=["*"]`, `allow_methods=["GET", "POST"]`, `allow_headers=["Content-Type", "Accept"]`).
   - Line 45 includes `chat.router` (`app.include_router(chat.router)`).
   - Lines 48–56 expose `GET /heartbeat` returning `{"status": "alive"}`.
   - Missing routes: no `/analytics` route is currently registered or present in `backend/app/routes/`.
2. **Chat Router (`backend/app/routes/chat.py`)**:
   - Lines 38–71 implement `POST /ask`, accepting `ChatQuery(query_text: str)` and returning `ChatResponse(answer_text: str, retrieved_sources: List[str])`.
   - Execution is purely synchronous/unary: `agent_service.ask_agent(query.query_text)`.
   - Streaming SSE support is completely absent; no `StreamingResponse` from `fastapi.responses` is used.
   - Lines 77–90 implement `GET /health` returning `HealthStatus(status="ok")`.
   - Lines 97–124 implement `POST /retrieval-test` returning `RetrievalTestResponse(chunks=...)`.
3. **Agent Service (`backend/app/agent/agent_service.py`)**:
   - Uses `google-genai` SDK (`genai.Client(api_key=settings.GEMINI_API_KEY)`), model `gemini-2.5-flash` (lines 44, 104).
   - Implements a tool-calling loop (max 5 turns) calling `retrieve_chunks` tool (lines 47–71, 112–160).
   - Currently calls `self.gemini_client.models.generate_content(...)` (line 195); does not support `generate_content_stream(...)` for token streaming.
   - Does not accept any `module_filter` parameter in `ask_agent` or in `retrieve_chunks` tool schema.
4. **Retriever Service (`backend/app/retriever/retriever_service.py`)**:
   - `retrieve_chunks(query_text: str, top_k: int = 5) -> list[ContentChunk]` (line 74).
   - Generates 1024-dimension embeddings via Cohere `embed-english-v3.0` with `input_type="search_query"` (line 63).
   - Performs Qdrant search via `self.qdrant_client.query_points(collection_name=..., query=..., limit=top_k, with_payload=True)` (lines 95–100).
   - There is NO filter passed to `query_points`: no `models.Filter` or module scoping is implemented.
5. **Data Models (`backend/app/models/models.py`) & Schemas (`backend/app/schemas/chat_models.py`)**:
   - `Document` model in `backend/app/models/models.py` only defines: `text: str`, `source_url: str`, `title: str`, `chunk_index: int`. It lacks `module: str`, `chapter: str`, and `content_hash: str`.
   - `ChatQuery` in `backend/app/schemas/chat_models.py` only defines `query_text: str = Field(..., min_length=1)`. It lacks `stream: Optional[bool] = False` and `module_filter: Optional[str] = None`.
6. **Ingestion Pipeline (`backend/ingest_docs.py`)**:
   - Currently crawls all `*.mdx` in `ai-book-docs/**` (line 61).
   - Uses `TextProcessor(chunk_size=350, chunk_overlap=50)` (line 64).
   - Generates embeddings with Cohere in batches of 64 (line 91).
   - Calls `vector_store.create_collection()`, which executes `client.recreate_collection(...)`—completely dropping and recreating the collection on every run (line 107 in `ingest_docs.py`, line 22 in `vector_store.py`).
   - Assigns point IDs using sequential loop indices `id=i` (line 111).
   - Lacks any content hash tracking (SHA-256), change detection manifest, incremental upserting, or targeted deletion.
7. **Test Suite & Tooling Verification**:
   - Running `cd backend; uv run pytest` passed all 41 test cases in 21.23 seconds.
   - Running `cd backend; uv run ruff check .` returned `All checks passed!`.
   - Test suite uses mock fixtures (`conftest.py`, `test_agent_service.py`, `test_retriever_service.py`) without requiring live external API credentials.

### 1.2 Frontend Architecture & Existing Codebase
1. **Docusaurus Version & Dependencies (`package.json`)**:
   - Docusaurus core: `@docusaurus/core@^3.10.2`, `@docusaurus/preset-classic@^3.10.2`.
   - React version: `react@^19.0.0`, `react-dom@^19.0.0`.
   - Math plugins: `remark-math` and `rehype-katex` are NOT currently installed in `package.json`.
2. **Docusaurus Configuration (`docusaurus.config.ts`)**:
   - Lines 123–131 load `@docusaurus/plugin-content-docs` with `id: 'ai-book'`, `path: 'ai-book-docs'`, `sidebarPath: require.resolve('./ai-book-docs/sidebar.ts')`.
   - Lines 271–297: `navbar.items` dropdown only lists Modules 1–5 (`module1-ros2`, `module2-digital-twin`, `module3-ai-robot-brain`, `module4-vla`, `module5-kinematics-dynamics`). Modules 6–12 are missing.
   - Lines 314–340: `footer.links` only lists Modules 1–5.
   - Missing: no `remarkPlugins` or `rehypePlugins` configured in docs plugin; no KaTeX CSS stylesheet configured in `stylesheets`.
3. **Sidebar Files (`ai-book-docs/sidebar.ts` vs `sidebars.ts`)**:
   - Root `sidebars.ts` is empty (`const sidebars: SidebarsConfig = {};`).
   - Active sidebar is `ai-book-docs/sidebar.ts`, which currently has:
     ```typescript
     const sidebars: SidebarsConfig = {
       aiBookSidebar: ['intro', { type: 'autogenerated', dirName: '.' }],
     };
     ```
   - Requires explicit or structured category definitions for all 12 modules and 110 chapters to guarantee exact chapter ordering (e.g. `1-1` to `1-14`, `2-1` to `2-10`, `6-1` to `6-10`, etc.).
4. **Existing Frontend Components (`src/components/`)**:
   - `FloatingAssistant/FloatingAssistant.tsx`: Currently fetches `/ask` via unary POST `fetch(...)` (lines 266–273). Has predefined quick prompts for Modules 1–4 only. Does not handle SSE events.
   - `ChatWidget/ChatWidget.tsx`: Landing page widget with unary `/ask` fetch.
   - `ReadingProgressBar/ReadingProgressBar.tsx`: 60 FPS transform-based scroll progress bar mounted in `src/theme/Root.tsx`.
   - Missing components: `src/components/ChapterProgress/` and `src/components/QuizEngine/` do not exist.
5. **Build Verification**:
   - Running `npm run build` completed cleanly: `[SUCCESS] Generated static files in "build"`.
   - Running `npm run typecheck` completed cleanly with exit code 0.

---

## 2. Logic Chain

From the observed state to the required platform and infrastructure architecture:

```
[Observations: Missing SSE, No Analytics, No Qdrant Filter, Full Ingestion Wipe, Missing Sidebar M6-M12, Missing KaTeX, Missing Progress/Quiz Components]
       │
       ▼
[Backend Upgrades]
 ├── 1. Streaming SSE /ask:
 │      - Request: ChatQuery with optional `stream: bool = False`, `module_filter: Optional[str] = None`
 │      - If stream=True or Accept=text/event-stream -> StreamingResponse yielding SSE events:
 │          * event: sources -> JSON list of retrieved URLs
 │          * event: token -> text token chunks from Gemini streaming API
 │          * event: done -> {"done": true, "total_sources": N}
 │          * event: error -> {"error": "..."}
 │      - Backward compatibility: If stream=False, return unary ChatResponse JSON with status 200.
 │
 ├── 2. Telemetry /analytics Endpoint:
 │      - POST /analytics: accepts AnalyticsEvent(event_type, timestamp, session_id, module_id, chapter_id, data)
 │      - Event types: "page_view", "query", "quiz_score", "progress_update"
 │      - Storage: Append-only JSON Lines in backend/logs/analytics.jsonl
 │      - GET /analytics: returns aggregate metrics (total queries, popular modules, quiz pass rates)
 │
 ├── 3. Qdrant Module-Aware Retrieval:
 │      - Update Document payload: add `module` (e.g. "module1", "module6"), `chapter`, `content_hash`
 │      - RetrieverService: build qdrant_client.models.Filter(must=[FieldCondition(key="module", match=MatchValue(value=module_filter))])
 │      - Fallback: when module_filter is None/empty, perform global semantic search across all modules
 │
 └── 4. Incremental Hash-Based Ingestion:
        - Manifest file backend/.ingest_manifest.json stores { file_path: { sha256, chunk_ids, count, updated_at } }
        - Added files: chunk, embed, upsert to Qdrant, record in manifest
        - Modified files: delete old points by ID, chunk, embed, upsert new points, update manifest
        - Deleted files: delete old points from Qdrant, remove entry from manifest
        - Unmodified files: skip (0 Cohere embedding calls)
        - Deterministic IDs: UUID5 based on namespace + f"{rel_path}:{chunk_index}"
       │
       ▼
[Frontend Upgrades]
 ├── 5. Sidebar & Navigation for 12 Modules:
 │      - Update `ai-book-docs/sidebar.ts`: 12 module categories + intro, chapters ordered 1-1..1-14, 2-1..2-10, etc.
 │      - Update `docusaurus.config.ts`: navbar dropdown items and footer links for all 12 modules
 │
 ├── 6. KaTeX LaTeX Math Configuration:
 │      - Install remark-math@^6.0.0 and rehype-katex@^7.0.1 in package.json
 │      - Add remarkPlugins: [remarkMath] and rehypePlugins: [rehypeKatex] to docs plugin in docusaurus.config.ts
 │      - Add KaTeX CSS CDN stylesheet link to stylesheets in docusaurus.config.ts
 │
 ├── 7. Interactive Chapter Progress Component:
 │      - Component in src/components/ChapterProgress/
 │      - Persist state in localStorage ("robotics_chapter_progress")
 │      - Mark as Complete toggle button, module progress ring/bar, overall completion indicator
 │      - Dispatches "progress_update" to /analytics
 │
 └── 8. Interactive Quiz Engine Component:
        - Component in src/components/QuizEngine/
        - Schema: QuizData { id, title, module, questions: [{ id, question, options, correctIndex, explanation }] }
        - Features: Radio selection, immediate pedagogical feedback, scoring, retake option
        - Persist results in localStorage ("robotics_quiz_scores")
        - Dispatches "quiz_score" to /analytics
       │
       ▼
[Testing & Verification]
 ├── Mock fixtures for Gemini/OpenAI, Cohere, and Qdrant in backend/tests/
 ├── Ruff lint compliance (target py311, line-length 100)
 └── Clean Docusaurus build (npm run build with 0 broken links and 0 errors)
```

---

## 3. Detailed Specifications by Subsystem

### 3.1 Backend: SSE Streaming `/ask` Endpoint
- **Request Format**:
  ```json
  POST /ask
  Headers:
    Content-Type: application/json
    Accept: text/event-stream  (or application/json)
  Body:
  {
    "query_text": "What is the Zero-Moment Point (ZMP)?",
    "module_filter": "module6",
    "stream": true
  }
  ```
- **SSE Stream Protocol**:
  Content-Type: `text/event-stream; charset=utf-8`
  Cache-Control: `no-cache`
  Connection: `keep-alive`

  Stream Event Sequence:
  1. **Sources Event** (emitted as soon as retrieval completes):
     ```
     event: sources
     data: {"sources": ["/ai-book/module6-bipedal-locomotion/6-2-zero-moment-point"]}
     \n\n
     ```
  2. **Token Events** (emitted as tokens are generated by LLM stream):
     ```
     event: token
     data: {"token": "The "}
     \n\n
     event: token
     data: {"token": "Zero-Moment "}
     \n\n
     ```
  3. **Done Event** (emitted when generation concludes):
     ```
     event: done
     data: {"done": true, "total_sources": 1}
     \n\n
     ```
  4. **Error Event** (emitted on stream generation failure):
     ```
     event: error
     data: {"error": "Retrieval service timeout."}
     \n\n
     ```
- **Backward Compatibility**:
  If `stream` is `false` (default) and `Accept` header is not `text/event-stream`, the endpoint returns the existing JSON response:
  ```json
  {
    "answer_text": "The Zero-Moment Point (ZMP) is...",
    "retrieved_sources": ["/ai-book/module6-bipedal-locomotion/6-2-zero-moment-point"]
  }
  ```

### 3.2 Backend: `/analytics` Telemetry Endpoint
- **Pydantic Schemas**:
  ```python
  from enum import Enum
  from typing import Any, Dict, Optional
  from pydantic import BaseModel, Field

  class EventType(str, Enum):
      PAGE_VIEW = "page_view"
      QUERY = "query"
      QUIZ_SCORE = "quiz_score"
      PROGRESS_UPDATE = "progress_update"

  class AnalyticsEvent(BaseModel):
      event_type: EventType
      timestamp: Optional[str] = None  # ISO-8601 string; server auto-populates if None
      session_id: Optional[str] = Field(None, max_length=128)
      module_id: Optional[str] = Field(None, max_length=64)
      chapter_id: Optional[str] = Field(None, max_length=128)
      data: Dict[str, Any] = Field(default_factory=dict)

  class AnalyticsResponse(BaseModel):
      status: str = "recorded"
      event_id: str

  class AnalyticsSummary(BaseModel):
      total_events: int
      event_counts: Dict[str, int]
      total_queries: int
      popular_modules: Dict[str, int]
      average_quiz_scores: Dict[str, float]
  ```
- **Storage**:
  File: `backend/logs/analytics.jsonl`.
  Appends single-line JSON records using non-blocking file I/O or background task.
- **Endpoints**:
  - `POST /analytics` — Records incoming telemetry event. Returns `201 Created` or `200 OK`.
  - `GET /analytics` — Reads log file and returns aggregated `AnalyticsSummary`.

### 3.3 Backend: Qdrant Retrieval Module Filtering
- **Payload Schema in Qdrant**:
  ```json
  {
    "text": "The 3D Linear Inverted Pendulum Model...",
    "source_url": "/ai-book/module6-bipedal-locomotion/6-2-zero-moment-point",
    "title": "Zero-Moment Point (ZMP)",
    "chunk_index": 2,
    "module": "module6",
    "chapter": "6-2-zero-moment-point",
    "content_hash": "a1b2c3d4..."
  }
  ```
- **Filter Syntax in `RetrieverService.retrieve_chunks`**:
  ```python
  from qdrant_client import models

  query_filter = None
  if module_filter and module_filter.lower() != "all":
      # Normalize e.g. "module6-bipedal-locomotion" -> "module6" or direct match
      norm_module = module_filter.split("-")[0] if "-" in module_filter else module_filter
      query_filter = models.Filter(
          must=[
              models.FieldCondition(
                  key="module",
                  match=models.MatchValue(value=norm_module),
              )
          ]
      )

  search_result = self.qdrant_client.query_points(
      collection_name=self.collection_name,
      query=query_embedding,
      query_filter=query_filter,
      limit=top_k,
      with_payload=True,
  )
  ```
- **Fallback**: If `module_filter` is `None`, empty, or `"all"`, `query_filter` is `None`, performing an unrestricted search across the entire curriculum.

### 3.4 Backend: Incremental Hash-Based Auto-Ingestion Pipeline
- **CLI Command**:
  `cd backend && uv run python ingest_docs.py [--incremental] [--force] [--dry-run]`
- **Manifest File**: `backend/.ingest_manifest.json`
  ```json
  {
    "ai-book-docs/module6-bipedal-locomotion/6-2-zero-moment-point.mdx": {
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "chunk_ids": [
        "c81d4e2e-bcf2-11e6-869b-7fa663f21000",
        "c81d4e2e-bcf2-11e6-869b-7fa663f21001"
      ],
      "chunk_count": 2,
      "updated_at": "2026-11-09T14:20:00Z"
    }
  }
  ```
- **Change Detection Logic**:
  1. Scan all `.mdx` files in `ai-book-docs/`.
  2. Compute SHA-256 for each file's content.
  3. Compare against `backend/.ingest_manifest.json`:
     - **New File**: Present on disk, absent in manifest -> Chunk text, generate embeddings with Cohere, upsert points with deterministic IDs to Qdrant, record in manifest.
     - **Modified File**: Present in manifest, but SHA-256 mismatch -> Delete old point IDs from Qdrant (`client.delete(points_selector=PointIdsList(points=old_chunk_ids))`), re-chunk, generate new embeddings, upsert new points, update manifest.
     - **Deleted File**: In manifest, absent on disk -> Delete old point IDs from Qdrant, remove entry from manifest.
     - **Unmodified File**: SHA-256 matches manifest -> Skip embedding generation completely.
- **Deterministic Point ID Generation**:
  ```python
  import uuid
  NAMESPACE_MODULE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
  point_id = str(uuid.uuid5(NAMESPACE_MODULE, f"{rel_path}:{chunk_index}"))
  ```

### 3.5 Frontend: Sidebar Configuration for All 12 Modules
- **File**: `ai-book-docs/sidebar.ts`
- **Structure**:
  Must register:
  1. `intro`: `ai-book/intro`
  2. `module1`: Module 1: The Robotic Nervous System (ROS 2) (Chapters 1-1 through 1-14)
  3. `module2`: Module 2: The Digital Twin (Gazebo & Unity) (Chapters 2-1 through 2-10)
  4. `module3`: Module 3: The AI-Robot Brain (NVIDIA Isaac) (Chapters 3-1 through 3-10)
  5. `module4`: Module 4: Vision-Language-Action (VLA) Systems (Chapters 4-1 through 4-10)
  6. `module5`: Module 5: Humanoid Kinematics & Dynamics (Chapters 5-1 through 5-10)
  7. `module6`: Module 6: Bipedal Locomotion & Whole-Body Control (Chapters 6-1 through 6-10)
  8. `module7`: Module 7: Dexterous Manipulation & Hand Design (Chapters 7-1 through 7-8)
  9. `module8`: Module 8: Robot Learning & Reinforcement Learning (Chapters 8-1 through 8-10)
  10. `module9`: Module 9: Sim-to-Real Transfer & Domain Randomization (Chapters 9-1 through 9-8)
  11. `module10`: Module 10: Hardware Architecture & Embedded Systems (Chapters 10-1 through 10-8)
  12. `module11`: Module 11: Safety, Ethics & Deployment (Chapters 11-1 through 11-6)
  13. `module12`: Module 12: Capstone Projects & Research Frontiers (Chapters 12-1 through 12-6)
- **Navbar & Footer Updates in `docusaurus.config.ts`**:
  Update `navbar.items` dropdown from 5 to all 12 modules; update `footer.links` to include all modules.

### 3.6 Frontend: KaTeX / MathJax Configuration
- **NPM Packages**:
  `npm install remark-math@^6.0.0 rehype-katex@^7.0.1`
- **`docusaurus.config.ts` Plugin Configuration**:
  ```typescript
  import remarkMath from 'remark-math';
  import rehypeKatex from 'rehype-katex';

  // In plugins -> @docusaurus/plugin-content-docs:
  {
    id: 'ai-book',
    path: 'ai-book-docs',
    routeBasePath: 'ai-book',
    sidebarPath: require.resolve('./ai-book-docs/sidebar.ts'),
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
  }
  ```
- **KaTeX Stylesheet**:
  ```typescript
  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css',
      type: 'text/css',
      integrity: 'sha384-nB0miv6/jRmo5UMMR1wu3Gz6NLsoTkbqJghGIsx//Rlm+ZU03BU6SQNC66uf4l5+',
      crossorigin: 'anonymous',
    },
  ],
  ```

### 3.7 Frontend: Interactive Chapter Progress Component
- **Component File**: `src/components/ChapterProgress/ChapterProgress.tsx`
- **CSS Module**: `src/components/ChapterProgress/styles.module.css`
- **Capabilities**:
  - `localStorage` key: `robotics_chapter_progress` storing array of completed chapter IDs.
  - "Mark as Complete" / "Completed ✓" button with smooth visual transition.
  - Chapter progress bar indicator showing module progress (`X / Y Chapters (Z%)`) and overall curriculum progress.
  - Optional dispatch: posts a telemetry event to `/analytics` (`event_type="progress_update"`).
  - Can be embedded in MDX directly or injected via theme layout.

### 3.8 Frontend: Interactive Quiz Engine Component
- **Component File**: `src/components/QuizEngine/QuizEngine.tsx`
- **CSS Module**: `src/components/QuizEngine/styles.module.css`
- **Quiz Schema**:
  ```typescript
  export interface QuizOption {
    id: string;
    text: string;
  }

  export interface QuizQuestion {
    id: string;
    question: string;
    options: string[];
    correctIndex: number;
    explanation: string;
  }

  export interface QuizProps {
    quizId: string;
    title?: string;
    moduleId?: string;
    questions: QuizQuestion[];
    passThreshold?: number; // e.g. 0.70
  }
  ```
- **Capabilities**:
  - Interactive multiple choice question selector.
  - Submit button with instant pedagogical feedback (correct option highlighted green, incorrect selected highlighted red, explanation revealed).
  - Score tally and pass/fail badge.
  - "Retake Quiz" button to reset state.
  - State persisted to `localStorage` (`robotics_quiz_results`).
  - Automatic dispatch of quiz metrics to `POST /analytics` (`event_type="quiz_score"`).

---

## 4. Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Backend | SSE Streaming `/ask` | Real-time token streaming endpoint using FastAPI `StreamingResponse` | `ChatQuery` with `stream=True` or `Accept: text/event-stream` | SSE stream: `sources`, `token`, `done` | Emits `event: error` with detail JSON, status 500 if unhandled | `specs/010-master-plan`, `ULTRA_PRO_MAX`, `backend/app/routes/chat.py` |
| 2 | Backend | Unary `/ask` (Backward Compat) | Non-streaming question answering for legacy or synchronous clients | `ChatQuery` with `stream=False` | `ChatResponse(answer_text, retrieved_sources)` | HTTP 422 for validation, 500 for runtime exceptions | `backend/app/routes/chat.py`, existing unit tests |
| 3 | Backend | Telemetry Ingestion (`POST /analytics`) | Ingests telemetry events from frontend components | `AnalyticsEvent(event_type, timestamp, session_id, module_id, chapter_id, data)` | `AnalyticsResponse(status="recorded", event_id)` | HTTP 422 on invalid event_type or malformed payload | `ULTRA_PRO_MAX` §3.3, `ORIGINAL_REQUEST.md` R3 |
| 4 | Backend | Analytics Aggregates (`GET /analytics`) | Summarizes stored telemetry logs for monitoring | Query params: optional `module`, `since` | `AnalyticsSummary` with counts, popular modules, quiz pass rates | HTTP 500 if log file unreadable; returns empty summary if no logs | `ULTRA_PRO_MAX` §3.3 |
| 5 | Backend | Qdrant Module Filtering | Restricts semantic vector search to specified module payload | `query_text: str`, `module_filter: Optional[str]`, `top_k: int` | List of `ContentChunk` from requested module | Falls back to global search if `module_filter` is null/empty | `specs/010-master-plan`, `ULTRA_PRO_MAX` §3.4 |
| 6 | Backend | Incremental Hash Ingestion | CLI pipeline detecting MDX changes via SHA-256 hash manifest | Command flags: `--incremental`, `--force`, `--dry-run` | Console logs, updated `.ingest_manifest.json`, Qdrant upserts/deletes | Skips unchanged files; rolls back on fatal connection errors | `backend/ingest_docs.py`, `ULTRA_PRO_MAX` §3.2 |
| 7 | Frontend | 12-Module Sidebar | Structured navigation for all 12 modules and 110 chapters | `SidebarsConfig` in `ai-book-docs/sidebar.ts` | Complete hierarchical sidebar in Docusaurus | Throws build error if referenced MDX doc ID missing | `specs/010-master-plan` §🗺️, `ULTRA_PRO_MAX` §3.6 |
| 8 | Frontend | KaTeX LaTeX Math | Native MDX LaTeX math formula rendering (`$...$` and `$$...$$`) | LaTeX expressions in MDX files | Rendered HTML with math typography | Falls back to raw text or build warning on invalid LaTeX syntax | `ULTRA_PRO_MAX` §3.8, `ORIGINAL_REQUEST.md` |
| 9 | Frontend | Chapter Progress Component | Client-side completion tracking and progress indicator | Chapter ID/URL, user toggle click | Updated UI badge, localStorage state, `/analytics` event | Graceful fallback if `localStorage` disabled or quota exceeded | `ULTRA_PRO_MAX` §3.7, `ORIGINAL_REQUEST.md` |
| 10 | Frontend | Quiz Engine Component | Client-side interactive quiz evaluation with explanation display | Array of `QuizQuestion` objects | Interactive quiz cards, score percentage, pass/fail badge | Validates option selection before submit; logs telemetry fail silently | `ULTRA_PRO_MAX` §3.9, `ORIGINAL_REQUEST.md` |
| 11 | Frontend | Streaming Floating Assistant | AI assistant chat drawer streaming tokens in real time | User query, SSE response stream | Real-time word-by-word message bubbles + clickable sources | Shows error message card with retry button on network failure | `src/components/FloatingAssistant/FloatingAssistant.tsx`, `ULTRA_PRO_MAX` §3.10 |
| 12 | Test/Infra | Local Pytest Mocks & Fixtures | Mocks external APIs (Gemini, Cohere, Qdrant) for deterministic CI | Pytest runner (`pytest -v`) | 100% green test suite | Fails test if API called without mock | `backend/tests/conftest.py`, `backend/tests/test_routes.py` |

---

## 5. Edge Cases

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | SSE `/ask` | Client disconnects before generation finishes | Async generator should catch `asyncio.CancelledError` or client disconnect without crashing server. |
| 2 | SSE `/ask` | Streaming requested with empty `query_text` | Pydantic validation rejects with HTTP 422 before opening SSE stream. |
| 3 | Qdrant Module Filter | Querying non-existent module (e.g. `module=module99`) | Qdrant returns 0 points; agent responds with standard fallback: "I could not find relevant information in the book..." |
| 4 | Qdrant Module Filter | Querying with `module=all` or `None` | Query filter is bypassed; retriever searches across all 12 modules globally. |
| 5 | Incremental Ingestion | File deleted from `ai-book-docs/` | Pipeline queries manifest for deleted file's `chunk_ids`, deletes them from Qdrant, and prunes manifest entry. |
| 6 | Incremental Ingestion | MDX file modified without changing total chunk count | SHA-256 changes; pipeline deletes old chunk IDs and upserts new embeddings, avoiding stale text. |
| 7 | Incremental Ingestion | Cohere API rate limit or network failure midway | Script fails cleanly; manifest is saved atomically per successful file to prevent inconsistent state. |
| 8 | `/analytics` | Large or malformed JSON payload in `data` | Pydantic limits field sizes and validates types; rejects malformed requests with HTTP 422. |
| 9 | `/analytics` | Concurrency: multiple simultaneous analytics requests | Append-only file writing with thread lock or async mutex avoids interleaved line corruption. |
| 10 | Chapter Progress | Browser private browsing mode (`localStorage` blocked) | In-memory fallback state prevents JavaScript runtime exceptions; UI remains interactive. |
| 11 | Quiz Engine | User submits quiz without answering all questions | Submit button disabled or prompts user with visual alert to answer all questions. |
| 12 | KaTeX Math | Broken LaTeX syntax (e.g. unclosed bracket `$\tau = \frac{1}{2$`) | Docusaurus build or rehype-katex will fail build if `throwOnError: true`; setting `throwOnError: false` allows graceful rendering with warning. |

---

## 6. Caveats

1. **Mock vs Production Credentials**: In the current test environment, tests pass using local mock fixtures. Production ingestion against Qdrant Cloud requires live `QDRANT_API_KEY`, `QDRANT_URL`, and `COHERE_API_KEY` in `backend/.env`.
2. **Docusaurus ESM Packaging**: Docusaurus 3 uses MDX 3 (ESM-only). `remark-math` must be version 6 and `rehype-katex` must be version 7; older version 3/4 packages will fail with ESM module import errors.
3. **Sidebar File Location**: The active sidebar configuration is `ai-book-docs/sidebar.ts`, explicitly configured in `docusaurus.config.ts` line 129. The root `sidebars.ts` is not loaded by the `@docusaurus/plugin-content-docs` instance. Updates must target `ai-book-docs/sidebar.ts`.

---

## 7. Conclusion

Phase 3 Platform & Infrastructure Upgrades require specific enhancements across 4 backend areas, 4 frontend areas, and the testing harness:
1. **Backend**:
   - `backend/app/routes/chat.py` and `backend/app/agent/agent_service.py`: Add SSE streaming with `StreamingResponse` for `/ask`, while preserving unary JSON output for backward compatibility.
   - `backend/app/routes/analytics.py` & `backend/app/schemas/chat_models.py`: Implement telemetry ingestion (`POST /analytics`) and reporting (`GET /analytics`), storing events in `backend/logs/analytics.jsonl`.
   - `backend/app/retriever/retriever_service.py` & `backend/app/models/models.py`: Support `module` metadata filtering in Qdrant searches.
   - `backend/ingest_docs.py`: Upgrade to an incremental hash-based pipeline with SHA-256 change detection and deterministic UUID5 point IDs.
2. **Frontend**:
   - `ai-book-docs/sidebar.ts` & `docusaurus.config.ts`: Register all 12 modules and all 110 chapters in numerical order; update navigation dropdowns and footer.
   - `package.json` & `docusaurus.config.ts`: Install and configure `remark-math@^6.0.0`, `rehype-katex@^7.0.1`, and the KaTeX CSS CDN link.
   - `src/components/ChapterProgress/`: Implement client-side chapter tracking with `localStorage` persistence and `/analytics` dispatch.
   - `src/components/QuizEngine/`: Implement interactive multiple-choice quiz evaluation with explanation display, score calculation, and `/analytics` telemetry.
3. **Verification**:
   - Pytest fixtures in `backend/tests/` verifying all endpoints (unary, SSE streaming, analytics, module-filtered retrieval).
   - Clean linting (`ruff check .`) and clean production build (`npm run build`).

---

## 8. Verification Method

To independently verify the discoveries and requirements:
1. **Backend Unit & Integration Tests**:
   ```powershell
   cd backend
   uv run pytest -v
   ```
   *Expected outcome*: 41 existing tests pass. Upgraded test suite must cover SSE streaming `/ask`, `/analytics`, and module-filtered retrieval.
2. **Backend Linting**:
   ```powershell
   cd backend
   uv run ruff check .
   ```
   *Expected outcome*: All checks pass with 0 errors.
3. **Frontend Production Build**:
   ```powershell
   npm run build
   ```
   *Expected outcome*: Static files generated in `build/` with 0 broken links and 0 errors.
4. **Frontend TypeScript Typechecking**:
   ```powershell
   npm run typecheck
   ```
   *Expected outcome*: Exits with code 0.
