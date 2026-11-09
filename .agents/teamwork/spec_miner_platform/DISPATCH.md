## 2026-11-09T14:16:48Z

You are a teamwork_spec_miner assigned to survey the platform and infrastructure specifications and architecture.
Read ORIGINAL_REQUEST.md at: C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\ORIGINAL_REQUEST.md

Your state folder is:
C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\spec_miner_platform\
Create this folder if needed and write your progress.md and handoff.md there.

Your mission:
Investigate authoritative sources and existing code regarding Phase 3: Platform & Infrastructure Upgrades:
1. `specs/010-master-plan-curriculum-expansion/spec.md`
2. `C:\Users\DELL\.gemini\antigravity-cli\brain\98ff215b-a62a-4d37-839f-7c685594be36\ULTRA_PRO_MAX_MASTER_PLAN.md`
3. Existing backend in `src/` and `tests/`
4. Existing frontend in `ai-book-docs/`

Produce a detailed specification breakdown in your handoff report covering:
- Backend Upgrades:
  * SSE Streaming `/ask` endpoint: request format, streaming response format (SSE events: tokens, sources, done), error handling, backward compatibility.
  * `/analytics` endpoint: schema, event tracking (page views, queries, quiz scores, progress updates), storage or handling mechanism, validation.
  * Qdrant Retrieval Module Filtering: payload structure, filter syntax by `module` (e.g. `module1`, `module6`), fallback if no module specified, index payload schema.
  * Incremental hash-based auto-ingestion pipeline: CLI command/script, SHA-256 hash tracking (e.g., manifest or metadata), detection of modified/added/deleted files, batching, Qdrant upserting/deletion logic.
- Frontend Upgrades:
  * Sidebar configuration: structure of `ai-book-docs/sidebar.ts` or `sidebars.ts`, ordering of all 12 modules and all chapters.
  * KaTeX / MathJax configuration: Docusaurus config (`docusaurus.config.ts`), `remark-math` and `rehype-katex` plugins, CSS inclusion (`katex.min.css`), testing math rendering.
  * Interactive Chapter Progress component: state persistence (localStorage), completion toggling, progress bar / indicator, integration into MDX pages.
  * Interactive Quiz Engine component: schema for quiz questions (multiple choice, explanations), rendering, scoring, persistence, telemetry to `/analytics`.
- Testing & Verification Requirements:
  * Pytest fixtures and mocks for OpenAI and Qdrant in `tests/`.
  * Ruff linting standards.
  * Docusaurus build verification (`npm run build`).

Deliver a complete handoff report (`handoff.md`) in your state folder and notify with send_message.
