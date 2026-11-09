## 2026-11-09T14:30:57Z
You are a teamwork_worker assigned to implement the Backend Platform & Infrastructure Upgrades (Milestone M1).
Read ORIGINAL_REQUEST.md at: C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\ORIGINAL_REQUEST.md
Read PROJECT.md at: C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\orchestrator\PROJECT.md
Read the platform spec handoff at: C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\spec_miner_platform\handoff.md

Your state folder is:
C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\worker_backend_platform\
Create this folder if needed and write your progress.md and handoff.md there.

Exclusive Write Ownership:
- `backend/app/routes/chat.py`
- `backend/app/routes/analytics.py`
- `backend/app/main.py`
- `backend/app/agent/agent_service.py`
- `backend/app/retriever/retriever_service.py`
- `backend/app/schemas/chat_models.py`
- `backend/app/models/models.py`
- `backend/ingest_docs.py`
- `backend/tests/**`
DO NOT modify any frontend files (`ai-book-docs/`, `src/`, `package.json`, etc.).

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Tasks to implement:
1. **Pydantic Schemas & Data Models**:
   - In `backend/app/schemas/chat_models.py`:
     * Add `stream: Optional[bool] = False` and `module_filter: Optional[str] = None` to `ChatQuery`.
     * Add `AnalyticsEvent(event_type: str, timestamp: Optional[str], session_id: Optional[str], module_id: Optional[str], chapter_id: Optional[str], data: dict)`, `AnalyticsResponse`, and `AnalyticsSummary`.
   - In `backend/app/models/models.py`:
     * Add `module: Optional[str] = None`, `chapter: Optional[str] = None`, and `content_hash: Optional[str] = None` to `Document` and `ContentChunk`.
2. **SSE Streaming for `/ask`**:
   - In `backend/app/agent/agent_service.py`:
     * Implement streaming generation (e.g. `ask_agent_stream(query_text: str, module_filter: Optional[str] = None)`).
     * Yields events or token chunks: first retrieved sources, then tokens, then completion signal.
     * Keep `ask_agent(...)` synchronous unary method intact for backward compatibility.
   - In `backend/app/routes/chat.py`:
     * When `query.stream is True` or `request.headers.get("accept") == "text/event-stream"`, return `StreamingResponse(..., media_type="text/event-stream")`.
     * Emit compliant SSE format:
       `event: sources\ndata: {"sources": [...]}\n\n`
       `event: token\ndata: {"token": "..."}\n\n`
       `event: done\ndata: {"done": true, "total_sources": N}\n\n`
       `event: error\ndata: {"error": "..."}\n\n`
     * When `query.stream is False`, return standard unary `ChatResponse(answer_text, retrieved_sources)`.
3. **Telemetry Endpoint (`/analytics`)**:
   - Create `backend/app/routes/analytics.py`:
     * `POST /analytics`: Accepts `AnalyticsEvent`, validates fields, appends record as single-line JSON to `backend/logs/analytics.jsonl` (ensure directory exists). Returns `AnalyticsResponse(status="recorded", event_id=...)`.
     * `GET /analytics`: Reads `backend/logs/analytics.jsonl`, computes aggregate metrics (total events, event counts, popular modules, quiz scores), returns `AnalyticsSummary`.
   - In `backend/app/main.py`: Include `analytics.router` (`app.include_router(analytics.router)`).
4. **Qdrant Retrieval Module Filtering**:
   - In `backend/app/retriever/retriever_service.py`:
     * Update `retrieve_chunks(query_text: str, top_k: int = 5, module_filter: Optional[str] = None) -> list[ContentChunk]`.
     * If `module_filter` is provided (e.g., "module1" or "module6"), build a `qdrant_client.models.Filter(must=[FieldCondition(key="module", match=MatchValue(value=norm_module))])`.
     * Pass `query_filter` to `qdrant_client.query_points(...)`.
     * If `module_filter` is None or empty or "all", `query_filter=None` (global search fallback).
5. **Incremental Hash-Based Auto-Ingestion**:
   - Update `backend/ingest_docs.py`:
     * Support `--incremental`, `--force`, `--dry-run` CLI options.
     * Compute SHA-256 for each `.mdx` file.
     * Maintain manifest `backend/.ingest_manifest.json` tracking `{ file_path: { sha256, chunk_ids, count, updated_at } }`.
     * Use deterministic UUID5 for chunk point IDs: `uuid.uuid5(uuid.NAMESPACE_DNS, f"{rel_path}:{chunk_index}")`.
     * For new files: embed and upsert points; add to manifest.
     * For modified files: delete old point IDs from Qdrant, embed and upsert new points; update manifest.
     * For deleted files: delete old point IDs from Qdrant; remove from manifest.
     * For unchanged files: skip embedding generation completely.
     * Ensure payloads include `module` (extracted from parent folder name e.g. "module1", "module6"), `chapter` (filename), and `content_hash`.
6. **Testing & Verification**:
   - In `backend/tests/`: Add comprehensive tests covering:
     * Unary `/ask` and streaming SSE `/ask` (using mock LLM/retriever fixtures).
     * `POST /analytics` and `GET /analytics`.
     * `retrieve_chunks` with and without `module_filter`.
     * Incremental ingestion hashing logic.
   - Run verification:
     * `cd backend; uv run pytest -v` (ensure all tests pass 100%).
     * `cd backend; uv run ruff check .` (ensure 0 lint errors).
   - Document commands and test outcomes in `handoff.md`. Notify with `send_message`.
