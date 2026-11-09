# Handoff Report: Empirical Challenge of Backend Platform Upgrades (Milestone M1)

**Agent**: `challenger_platform_2`  
**Role**: `critic`, `specialist` (Empirical Challenger)  
**Date**: 2026-11-09T15:05:00Z  
**Verdict**: **REJECT** (Blocking Quality Gate Failure in E2E Test Suite)

---

## 1. Observation

### 1.1 Test Suite Execution Failures
When running the required verification commands:

1. **Unified E2E Runner Command**:
   ```powershell
   python run_e2e_tests.py
   ```
   **Result**: Exited with code `1`.
   ```text
   ================================== FAILURES ===================================
   ____________ TestTier1BackendCoverage.test_ask_sse_streaming_mode _____________

   self = <tests.e2e.test_tier1_backend_coverage.TestTier1BackendCoverage object at 0x000002E3EBA9C510>
   test_client = <starlette.testclient.TestClient object at 0x000002E3EBBCC2B0>

       def test_ask_sse_streaming_mode(self, test_client: TestClient):
           payload = {"query_text": "Explain ZMP preview control", "stream": True}
           response = test_client.post("/ask", json=payload, headers={"Accept": "text/event-stream"})
           ...
   >       assert "event: token" in stream_text or "token" in stream_text, (
               "SSE stream must include token chunk events"
           )
   E       AssertionError: SSE stream must include token chunk events
   E       assert ('event: token' in 'event: sources\ndata: {"sources": [...]}\n\nevent: error\ndata: {"error": "429 RESOURCE_EXHAUSTED. {\'error\': {\'code\': 429, \'message\': \'You exceeded your current quota, please check your plan and billing details... Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash... Please retry in 16h59m21s.\'..."}\n\n' or 'token' in ...)

   FAILED tests/e2e/test_tier1_backend_coverage.py::TestTier1BackendCoverage::test_ask_sse_streaming_mode
   =================== 1 failed, 27 passed, 1 warning in 2.52s ===================
   [E2E Runner] Completed in 7.63s with exit code 1
   ```

2. **Full Pytest Suite Command**:
   ```powershell
   cd backend
   uv run pytest -v
   ```
   **Result**: Exited with code `1`.
   ```text
   FAILED tests/e2e/test_tier1_backend_coverage.py::TestTier1BackendCoverage::test_ask_sse_streaming_mode
   ================= 1 failed, 106 passed, 7 warnings in 13.39s ==================
   ```

3. **Linter Command**:
   ```powershell
   cd backend
   uv run ruff check .
   ```
   **Result**: Exited with code `0` (`All checks passed!`).

### 1.2 Root Cause in Test Suite Code
- In `backend/tests/e2e/test_tier1_backend_coverage.py` lines 59–85:
  ```python
  def test_ask_sse_streaming_mode(self, test_client: TestClient):
      payload = {
          "query_text": "Explain ZMP preview control",
          "stream": True,
      }
      response = test_client.post(
          "/ask",
          json=payload,
          headers={"Accept": "text/event-stream"},
      )
  ```
  Unlike `test_ask_unary_mode` (lines 40–58 in the same file), which properly uses `with patch("app.routes.chat.agent_service.ask_agent", return_value=mock_response):`, `test_ask_sse_streaming_mode` has **zero mocks** for `agent_service.ask_agent_stream` or the Gemini API client (`mock_gemini_client`).
- Consequently, `test_ask_sse_streaming_mode` makes an unmocked live HTTP request over the internet to Google GenAI (`generativelanguage.googleapis.com/generate_content_free_tier_requests`).
- Because the free tier quota is 20 requests/day, once 20 requests are reached, Google returns HTTP 429 RESOURCE_EXHAUSTED. The endpoint catches this and yields `event: error\ndata: {"error": "429 RESOURCE_EXHAUSTED..."}\n\n`. The test assertion expecting `event: token` fails.
- This directly contradicts the requirement in `ORIGINAL_REQUEST.md` (R4: *"without requiring live external API credentials... pytest passes with all tests green using mock fixtures"*) and the claim in `TEST_READY.md` (*"Hermetic Test Doubles (Zero Live API Keys)... 100% pass rate"*).

### 1.3 Adversarial Platform Stress Testing Observations
A dedicated stress test suite (`backend/tests/test_adversarial_platform_m1.py`, 17 tests) was authored and executed:

1. **SSE Streaming Protocol (`POST /ask`)**:
   - `test_sse_wire_format_exact_compliance`: Confirmed framing is strictly `event: <name>\ndata: <json>\n\n` with exact double newline terminators. Headers include `Cache-Control: no-cache`, `Connection: keep-alive`, and `X-Accel-Buffering: no`.
   - `test_sse_error_event_formatting_on_stream_failure`: When the token generator encounters a mid-stream exception, it safely yields `event: error\ndata: {"error": "..."}\n\n` without server crash.
   - `test_sse_client_early_disconnect_resilience`: Simulated abrupt client connection termination after 2 chunks. Generator closes cleanly without deadlock, lingering tasks, or server corruption.
   - `test_unary_mode_fallback_stream_false`: Confirmed `stream=False` (or omitted) with `Accept: application/json` returns standard JSON `ChatResponse(answer_text, retrieved_sources)`.
   - `test_sse_tokens_with_newlines_and_special_characters`: Tokens containing multiline code blocks, embedded newlines, and unicode emojis are safely escaped inside JSON payloads without breaking SSE framing.

2. **Telemetry Endpoint (`/analytics`)**:
   - `test_analytics_high_concurrency_rapid_fire`: Concurrently executed 200 requests across 25 parallel threads. Confirmed that due to `threading.Lock()` serialization in `app/routes/analytics.py:77-80`, exactly 200 lines were written, every single line is 100% valid JSON, and zero line interleaving occurred.
   - `test_analytics_validation_oversized_payloads`: Rejects oversized fields (`session_id > 128`, `module_id > 64`, `chapter_id > 128`) with HTTP 422 Unprocessable Entity.
   - `test_analytics_validation_missing_and_malformed`: Rejects missing `event_type`, non-dict `data`, and empty bodies with HTTP 422.
   - `test_analytics_unknown_event_types_handled`: Accepts custom string event types without error.
   - `test_analytics_summary_corrupted_lines_resilience`: `GET /analytics` skips unparseable/corrupted lines gracefully without raising HTTP 500.
   - `test_analytics_summary_non_numeric_and_null_quiz_scores`: Robustly calculates average quiz scores by ignoring `None`, string, or missing scores.

3. **Qdrant Filtering & Incremental Ingestion**:
   - `test_qdrant_module_filter_nonexistent_module`: Passing `module_filter="module99"` builds `FieldCondition(key="module", match=MatchValue(value="module99"))` and returns `[]` without error.
   - `test_qdrant_module_filter_all_and_none_variations`: Passing `None`, `"all"`, `"ALL"`, `"none"`, or `""` passes `query_filter=None` for global search.
   - `test_qdrant_module_filter_dash_and_whitespace_normalization`: Strings like `"  module6-bipedal-locomotion  "` are normalized to `"module6"`.
   - `test_qdrant_module_filter_injection_safety`: SQL/shell injection strings are safely passed as literal values inside `MatchValue` without injection risk.
   - `test_incremental_ingestion_lifecycle_simulation`:
     - Untouched file (matching SHA-256): 0 embedding recomputations performed.
     - Modified file (mismatched SHA-256): old point IDs deleted from Qdrant, new embeddings generated and upserted.
     - New file: new embeddings generated and upserted into Qdrant and manifest.
     - Deleted file: obsolete point IDs deleted from Qdrant and pruned from manifest.
   - `test_incremental_ingestion_corrupted_manifest_resilience`: Truncated/corrupted manifest file is handled gracefully by starting fresh.

---

## 2. Logic Chain

1. **Requirement R4 & Test Gate Contract**:
   - `ORIGINAL_REQUEST.md` (R4) dictates: *"Verify backend functionality... using local test fixtures and repository build tools without requiring live external API credentials: Run backend verification via pytest... pytest passes with all tests green using mock fixtures"*.
   - The user dispatch instruction mandates running `python run_e2e_tests.py` and `cd backend; uv run pytest -v`.
2. **Failure Trace**:
   - Both commands terminate with non-zero exit code `1` due to `test_tier1_backend_coverage.py::TestTier1BackendCoverage::test_ask_sse_streaming_mode`.
   - The test failure was directly traced to a missing mock for `agent_service.ask_agent_stream` or the Gemini API client.
   - The unmocked test attempts a live network request to Google GenAI, hits the free-tier rate limit (429 RESOURCE_EXHAUSTED), and fails the assertion `assert "event: token" in stream_text`.
3. **Hermeticity Violation**:
   - `TEST_READY.md` claimed the entire suite was 100% green and completely hermetic with zero reliance on live credentials.
   - In reality, the test harness has a live API leak, making CI/CD and offline verification unreliable.
4. **Implementation Quality vs. Test Harness Quality**:
   - The backend implementation itself (`chat.py`, `analytics.py`, `retriever_service.py`, `ingest_docs.py`) passed all 17 adversarial stress tests and is robust.
   - However, because the project's standard verification commands (`python run_e2e_tests.py` and `pytest -v`) fail with exit code 1, the milestone fails its acceptance gate.

---

## 3. Caveats

1. **Implementation Code Quality**: The underlying backend feature code is well-designed and passed all adversarial edge cases (high-concurrency rapid fire, line interleaving, SSE double newlines, client disconnects, incremental hashing).
2. **Scope of Defect**: The bug is located in the test file `backend/tests/e2e/test_tier1_backend_coverage.py`, specifically lines 59–85, where mocking was omitted.
3. **No Code Modification Constraint**: Per the agent role constraints (*"Review-only — do NOT modify implementation code"*, *"Report any failures as findings — do NOT fix them yourself"*), this agent did not modify `test_tier1_backend_coverage.py`. The defect is reported for resolution by the appropriate agent (`test_writer_infra` or worker).

---

## 4. Conclusion

**Verdict: REJECT**

The Backend Platform Upgrades (Milestone M1) cannot be approved until the E2E test harness is fixed to be hermetic.

### Actionable Remediation Required:
In `backend/tests/e2e/test_tier1_backend_coverage.py`, update `test_ask_sse_streaming_mode` to mock `agent_service.ask_agent_stream` (analogous to `test_agent_stream.py` and `test_ask_unary_mode`) or mock `agent_service.gemini_client`:

```python
    def test_ask_sse_streaming_mode(self, test_client: TestClient):
        fake_events = [
            ("sources", {"sources": ["/ai-book/module6-bipedal-locomotion/6-2-zero-moment-point"]}),
            ("token", {"token": "ZMP preview control regulates com trajectory."}),
            ("done", {"done": True, "total_sources": 1}),
        ]
        with patch("app.routes.chat.agent_service.ask_agent_stream", return_value=iter(fake_events)):
            payload = {
                "query_text": "Explain ZMP preview control",
                "stream": True,
            }
            response = test_client.post(
                "/ask",
                json=payload,
                headers={"Accept": "text/event-stream"},
            )
            ...
```

Once this mock is added, both `python run_e2e_tests.py` and `cd backend; uv run pytest -v` will pass 100% hermetically without live external API calls.

---

## 5. Verification Method

To independently verify this finding:

1. **Reproduce the Live API Leak & Failure**:
   ```powershell
   python run_e2e_tests.py
   ```
   **Expected**: Exit code `1`, failing at `tests/e2e/test_tier1_backend_coverage.py::TestTier1BackendCoverage::test_ask_sse_streaming_mode` with Google GenAI 429 RESOURCE_EXHAUSTED.

2. **Verify Adversarial Stress Suite**:
   ```powershell
   cd backend
   uv run pytest tests/test_adversarial_platform_m1.py -v
   ```
   **Expected**: 17 passed in ~4s.

3. **Verify Linter Cleanliness**:
   ```powershell
   cd backend
   uv run ruff check .
   ```
   **Expected**: `All checks passed!`
