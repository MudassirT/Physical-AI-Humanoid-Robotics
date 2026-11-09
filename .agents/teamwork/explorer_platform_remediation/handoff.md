# Forensic Remediation Strategy & Plan — Milestone M1 Platform Upgrades

**Agent**: `explorer_platform_remediation`  
**Mission**: Formulate an exact, robust, step-by-step remediation plan addressing all forensic audit and challenger findings.  
**Mode**: Read-Only Explorer / Synthesizer  
**Date**: 2026-11-09T15:10:00Z  

---

## 1. Observation

### 1.1 Empirical Audit Failure: Live API Leak in Test Suite
Direct execution of the end-to-end test suite via `python run_e2e_tests.py` and `cd backend; uv run pytest tests/e2e/test_tier1_backend_coverage.py` consistently fails with exit code `1`:

```text
FAILED tests/e2e/test_tier1_backend_coverage.py::TestTier1BackendCoverage::test_ask_sse_streaming_mode
AssertionError: SSE stream must include token chunk events
assert ('event: token' in 'event: sources\ndata: {"sources": [...]}\n\nevent: error\ndata: {"error": "429 RESOURCE_EXHAUSTED. {\'error\': {\'code\': 429, \'message\': \'You exceeded your current quota, please check your plan and billing details... Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash... Please retry in 16h51m30s.\'..."}\n\n' or 'token' in ...)
```

#### Detailed Call Trace & Root Cause
- **File**: `backend/tests/e2e/test_tier1_backend_coverage.py` lines 59–85:
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
- **Contrast**: `test_ask_unary_mode` in the same class (lines 40–58) mocks the agent:
  ```python
  with patch("app.routes.chat.agent_service.ask_agent", return_value=mock_response):
      ...
  ```
- **Mechanism**:
  1. `test_client.post("/ask", ...)` hits the FastAPI handler in `backend/app/routes/chat.py:51`.
  2. Because `stream: True`, `ask()` invokes `sse_event_generator()` (lines 72–84), which calls `agent_service.ask_agent_stream(...)`.
  3. `agent_service.ask_agent_stream` (in `backend/app/agent/agent_service.py:361–366`) executes:
     `stream_fn = getattr(self.gemini_client.models, "generate_content_stream", None)`
  4. `self.gemini_client` is initialized with live environment credentials from `settings.GEMINI_API_KEY`. It dispatches live HTTPS requests to `https://generativelanguage.googleapis.com`.
  5. The Google GenAI free tier has a daily limit of 20 requests per model. Once exhausted, Google returns HTTP 429 `RESOURCE_EXHAUSTED`.
  6. In `ask_agent_stream:404–406`, the exception is caught and yielded as `("error", {"error": str(exc)})`.
  7. The endpoint emits `event: error\ndata: {"error": "429..."}\n\n` instead of `event: token`.
  8. `assert "event: token" in stream_text` fails.
  9. This violates Requirement R4 of `ORIGINAL_REQUEST.md` (*"without requiring live external API credentials"*) and refutes the attestation in `TEST_READY.md` claiming hermetic zero-live-key execution.

---

### 1.2 Lint Errors in Backend Test Suite
Challenger 1 identified 3 `ruff` errors in `backend/tests/test_adversarial_platform_m1.py`:
1. `tests/test_adversarial_platform_m1.py:10:1: I001 [*] Import block is un-sorted or un-formatted`
2. `tests/test_adversarial_platform_m1.py:18:37: F401 [*] app.agent.agent_service.AgentService imported but unused`
3. `tests/test_adversarial_platform_m1.py:21:37: F401 [*] app.schemas.chat_models.ContentChunk imported but unused`

- **Verification**: `cd backend; uv run ruff check .` currently exits with code 0 (`All checks passed!`) because unused imports were pruned and import formatting was resolved. However, exact instructions are documented to maintain zero lint violations.

---

### 1.3 Frontend Component Edge Cases

#### A. `src/components/ChapterProgress/ChapterProgress.tsx`
1. **Undefined `chapterId` Crash**:
   - Lines 20–27:
     ```typescript
     function normalizeModuleId(chapterId: string, explicitModuleId?: string): string {
       if (explicitModuleId) return explicitModuleId;
       const match = chapterId.match(/^(\d+)-/);
       if (match) return `module${match[1]}`;
       const prefixMatch = chapterId.match(/^(module\d+)/i);
       if (prefixMatch) return prefixMatch[1].toLowerCase();
       return 'general';
     }
     ```
   - When rendered without `chapterId` (e.g. `<ChapterProgress />`), `chapterId.match(...)` throws `TypeError: Cannot read properties of undefined (reading 'match')`, crashing the entire React render tree.
2. **Prefix Matching Collision Bug**:
   - Lines 114–120:
     ```typescript
     const modulePrefixNum = moduleId.replace(/\D/g, '');
     const moduleCompletedCount = completedChapters.filter((id) => {
       if (modulePrefixNum) {
         return id.startsWith(`${modulePrefixNum}-`) || id.includes(`module${modulePrefixNum}`);
       }
       return id.includes(moduleId);
     }).length;
     ```
   - If `moduleId` is `"module1"`, `modulePrefixNum` is `"1"`.
   - `id.includes(`module${modulePrefixNum}`)` checks `id.includes('module1')`.
   - In JavaScript:
     - `'module10-1'.includes('module1') === true`
     - `'module11-2'.includes('module1') === true`
     - `'module12-1'.includes('module1') === true`
   - When a student completes chapters in Module 10, 11, or 12, Module 1's progress bar erroneously increments.

#### B. `src/components/QuizEngine/QuizEngine.tsx`
1. **Null / Non-Array `questions` Prop Crash**:
   - Lines 34, 71, 108, 150:
     ```typescript
     export function QuizEngine({ ..., questions = [], ... }: QuizProps)
     ...
     if (questions.length === 0)
     ```
   - In JavaScript/TypeScript, default parameters only substitute `undefined`. If `null` is passed (e.g. `<QuizEngine questions={null as any} />`), `questions` remains `null`.
   - Accessing `questions.length` throws `TypeError: Cannot read properties of null (reading 'length')`.
2. **Duplicate Question IDs Block Submission**:
   - Lines 40, 62–71, 107–116, 215–220:
     ```typescript
     const [selectedOptions, setSelectedOptions] = useState<Record<string, number>>({});
     ...
     const handleSelectOption = (questionId: string, optionIndex: number) => {
       setSelectedOptions((prev) => ({ ...prev, [questionId]: optionIndex }));
     };
     const answeredCount = Object.keys(selectedOptions).length;
     const isAllAnswered = questions.length > 0 && answeredCount === questions.length;
     ```
   - If a quiz author supplies duplicate question IDs (e.g. `id: "q1"`, `id: "q1"` or unassigned IDs), answering the second question overwrites the first question's entry in `selectedOptions`.
   - `Object.keys(selectedOptions).length` can never equal `questions.length`.
   - `isAllAnswered` is permanently `false`, and the Submit button (`disabled={!isAllAnswered}`) is permanently disabled.
3. **Defensive LocalStorage Number / Non-Object Parsing**:
   - Line 127: `const existing = raw ? JSON.parse(raw) : {}; existing[quizId] = ...`
   - If `raw` in localStorage is primitive (e.g. `"123"`), `JSON.parse` returns a number, and `existing[quizId] = ...` throws `TypeError: Cannot create property on number '123'`.

---

### 1.4 MDX Escaped Curly Braces in Module 5
- **File**: `ai-book-docs/module5-kinematics-dynamics/5-4-rigid-body-dynamics.mdx` line 163:
  ```markdown
  | **Cholesky (M^{-1})** | Naive Forward Dynamics via Matrix Inversion | `O(n^3)` | 180 us | Offline analysis, small kinematic chains |
  ```
- **Compiled AST**:
  ```javascript
  _jsxs(_components.strong, {
    children: ["Cholesky (M^", -1, ")"]
  })
  ```
- Because `{ -1 }` is not enclosed in LaTeX `$...$` delimiters or inline code ticks `` `...` ``, MDX 3 parses it as a JSX expression containing the JavaScript integer `-1`. It renders as broken plain text `Cholesky (M^-1)` rather than LaTeX math superscript.

---

## 2. Logic Chain

1. **Integrity Mandate**: `ORIGINAL_REQUEST.md` (R4) dictates that backend functionality must be verified using local fixtures without requiring live external API credentials, and that `pytest` and `ruff check .` must pass cleanly.
2. **Failure Trace**: `python run_e2e_tests.py` and `pytest tests/e2e` fail strictly because `test_ask_sse_streaming_mode` lacks a test double for `agent_service.ask_agent_stream` or the Gemini SDK client. Adding a hermetic mock double (as is already done for unary mode in `test_ask_unary_mode` and for streaming in `test_agent_stream.py`) eliminates the live API leak, ensures 100% offline test execution, and turns all 28 tests green.
3. **Static Quality**: The 3 ruff errors (`I001`, `F401`) were caused by extraneous imports (`AgentService`, `ContentChunk`) and unformatted import blocks in `test_adversarial_platform_m1.py`. Removing the unused imports and applying standard isort sorting resolves the linter cleanly.
4. **Component Robustness**:
   - In `ChapterProgress.tsx`, guarding `chapterId` with `if (!chapterId) return 'general'` prevents uncaught `TypeError`.
   - Replacing `.includes('module1')` with regex `/^module1([^0-9]|$)/` eliminates the prefix collision with `module10`, `module11`, and `module12`.
   - In `QuizEngine.tsx`, defensive array checking (`Array.isArray(questions) ? questions : []`) prevents null dereferencing. Deduplicating and disambiguating question IDs prevents key collision in state and unblocks submission.
5. **MDX Mathematical Correctness**: Wrapping `M^{-1}` in LaTeX math delimiters `$M^{-1}$` instructs the MDX/KaTeX pipeline (`remark-math@6` and `rehype-katex@7`) to render the mathematical superscript as `<span class="katex">` without JSX expression evaluation conflicts.

---

## 3. Caveats

- **Read-Only Scope**: In strict accordance with the explorer archetype, this agent has NOT modified any source files or test scripts. The exact patches and step-by-step remediation plan below are prepared for the implementing agents.
- **Pre-authoring Status of Modules 6–12**: The 74 new chapters for Modules 6–12 are scheduled for authoring in Milestones M2–M4. The navigation sidebar and navbar fallback to `/ai-book/intro` for unauthored chapters was verified and is expected behavior.
- **Ruff Cleanliness**: The ruff check on backend code currently passes cleanly (`All checks passed!`); the remediation steps provide the formal guarantee to prevent regression.

---

## 4. Conclusion & Actionable Remediation Plan

### Remediation Step 1: Hermetic Mock for `test_ask_sse_streaming_mode`

**Target File**: `backend/tests/e2e/test_tier1_backend_coverage.py`  
**Lines**: 59–85  
**Action**: Wrap the test request with a hermetic mock of `app.routes.chat.agent_service.ask_agent_stream`.

#### Exact Patch:
```python
<<<<
    def test_ask_sse_streaming_mode(self, test_client: TestClient):
        """
        Verify POST /ask in SSE streaming mode yields ordered event stream:
        event: sources -> event: token* -> event: done
        """
        # Check if route handles streaming
        payload = {
            "query_text": "Explain ZMP preview control",
            "stream": True,
        }

        # Test request with SSE accept header
        response = test_client.post(
            "/ask",
            json=payload,
            headers={"Accept": "text/event-stream"},
        )
====
    def test_ask_sse_streaming_mode(self, test_client: TestClient):
        """
        Verify POST /ask in SSE streaming mode yields ordered event stream:
        event: sources -> event: token* -> event: done
        """
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

            # Test request with SSE accept header
            response = test_client.post(
                "/ask",
                json=payload,
                headers={"Accept": "text/event-stream"},
            )
>>>>
```

*Alternative (Service-Level Mock with `mock_gemini_client` fixture)*:
```python
    def test_ask_sse_streaming_mode(self, test_client: TestClient, mock_gemini_client):
        fake_chunks = [
            ContentChunk(
                chunk_id="chunk-test-1",
                source_url="/ai-book/module6-bipedal-locomotion/6-2-zero-moment-point",
                original_text="ZMP preview control regulates com trajectory.",
                score=0.95,
                module="module6",
                chapter="6-2-zero-moment-point",
            )
        ]
        with patch.object(app.routes.chat.agent_service, "gemini_client", mock_gemini_client), \
             patch.object(app.routes.chat.agent_service.retriever_service, "retrieve_chunks", return_value=fake_chunks):
            payload = {"query_text": "Explain ZMP preview control", "stream": True}
            response = test_client.post("/ask", json=payload, headers={"Accept": "text/event-stream"})
            ...
```
*Recommendation*: The generator patch (`with patch("app.routes.chat.agent_service.ask_agent_stream", return_value=iter(fake_events))`) is recommended because it cleanly mirrors `test_ask_unary_mode` in the same class and focuses on verifying the FastAPI SSE streaming route protocol without external coupling.

---

### Remediation Step 2: Ensure Linter Cleanliness in `test_adversarial_platform_m1.py`

**Target File**: `backend/tests/test_adversarial_platform_m1.py`  
**Lines**: 10–25  
**Action**: Maintain sorted imports and omit unused imports (`AgentService`, `ContentChunk`).

#### Exact Import Block:
```python
import concurrent.futures
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.retriever.retriever_service import RetrieverService
from ingest_docs import (
    compute_file_hash,
    plan_ingestion,
    run_ingestion,
)
```

---

### Remediation Step 3: Hardening Frontend Components

#### A. Patch `src/components/ChapterProgress/ChapterProgress.tsx`
**Action**: Guard `normalizeModuleId` against `undefined` and replace prefix substring check with regex word boundary.

```typescript
// 1. Guard normalizeModuleId (lines 20-27)
function normalizeModuleId(chapterId?: string, explicitModuleId?: string): string {
  if (explicitModuleId) return explicitModuleId;
  if (!chapterId) return 'general';
  const match = chapterId.match(/^(\d+)-/);
  if (match) return `module${match[1]}`;
  const prefixMatch = chapterId.match(/^(module\d+)/i);
  if (prefixMatch) return prefixMatch[1].toLowerCase();
  return 'general';
}

// 2. Guard ChapterProgressProps (lines 5-9)
export interface ChapterProgressProps {
  chapterId?: string;
  moduleId?: string;
  totalChapters?: number;
}

// 3. Guard handleToggle (lines 87-89)
const handleToggle = () => {
  if (!chapterId) return;
  const nextCompleted = !completed;
  ...
};

// 4. Exact Module Matching without Prefix Collision (lines 114-121)
const modulePrefixNum = moduleId.replace(/\D/g, '');
const moduleCompletedCount = completedChapters.filter((id) => {
  if (modulePrefixNum) {
    const isNumPrefix = id.startsWith(`${modulePrefixNum}-`);
    const isModulePrefix = new RegExp(`^module${modulePrefixNum}([^0-9]|$)`, 'i').test(id);
    return isNumPrefix || isModulePrefix;
  }
  return id.includes(moduleId);
}).length;
```

#### B. Patch `src/components/QuizEngine/QuizEngine.tsx`
**Action**: Defensively sanitize `questions`, disambiguate duplicate question IDs, and guard localStorage JSON parsing.

```typescript
export function QuizEngine({
  quizId,
  title = 'Chapter Mastery Check',
  moduleId = 'general',
  questions = [],
  passThreshold = 70,
}: QuizProps): React.JSX.Element {
  const isBrowser = useIsBrowser();
  const normalizedThreshold = passThreshold <= 1 ? Math.round(passThreshold * 100) : passThreshold;

  // Defensively normalize questions and guarantee unique question IDs
  const safeQuestions = React.useMemo(() => {
    if (!Array.isArray(questions)) return [];
    const seenIds = new Set<string>();
    return questions.map((q, idx) => {
      let qId = q?.id ? String(q.id).trim() : `q-${idx}`;
      if (!qId || seenIds.has(qId)) {
        qId = `${qId || 'q'}-${idx}`;
      }
      seenIds.add(qId);
      return {
        ...q,
        id: qId,
        question: q?.question || '',
        options: Array.isArray(q?.options) ? q.options : [],
        correctIndex: typeof q?.correctIndex === 'number' ? q.correctIndex : 0,
        explanation: q?.explanation || '',
      };
    });
  }, [questions]);

  const [selectedOptions, setSelectedOptions] = useState<Record<string, number>>({});
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
  const [score, setScore] = useState<number>(0);
  const [passed, setPassed] = useState<boolean>(false);
  const [persistedRecord, setPersistedRecord] = useState<{ score: number; passed: boolean } | null>(null);

  // Load persisted history
  useEffect(() => {
    if (!isBrowser) return;
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed && typeof parsed === 'object' && !Array.isArray(parsed) && parsed[quizId]) {
          setPersistedRecord(parsed[quizId]);
        }
      }
    } catch {}
  }, [isBrowser, quizId]);

  const handleSelectOption = (questionId: string, optionIndex: number) => {
    if (isSubmitted) return;
    setSelectedOptions((prev) => ({
      ...prev,
      [questionId]: optionIndex,
    }));
  };

  const answeredCount = Object.keys(selectedOptions).length;
  const isAllAnswered = safeQuestions.length > 0 && answeredCount === safeQuestions.length;

  const handleSubmit = () => {
    if (!isAllAnswered || safeQuestions.length === 0) return;

    let correctCount = 0;
    safeQuestions.forEach((q) => {
      if (selectedOptions[q.id] === q.correctIndex) {
        correctCount += 1;
      }
    });

    const finalScore = Math.round((correctCount / safeQuestions.length) * 100);
    const isPassed = finalScore >= normalizedThreshold;

    setScore(finalScore);
    setPassed(isPassed);
    setIsSubmitted(true);

    if (isBrowser) {
      try {
        const raw = window.localStorage.getItem(STORAGE_KEY);
        let existing: Record<string, any> = {};
        if (raw) {
          const parsed = JSON.parse(raw);
          if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
            existing = parsed;
          }
        }
        existing[quizId] = {
          score: finalScore,
          passed: isPassed,
          timestamp: new Date().toISOString(),
        };
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify(existing));
        setPersistedRecord(existing[quizId]);
      } catch {}
    }

    sendTelemetry(finalScore, isPassed, correctCount);
  };

  // Render fallback if empty
  if (safeQuestions.length === 0) {
    return (
      <div className={styles.quizCard}>
        <p>No questions configured for this quiz.</p>
      </div>
    );
  }

  // Render question list using safeQuestions
  ...
  {safeQuestions.map((q, qIndex) => {
    const selectedOption = selectedOptions[q.id];
    ...
  })}
```

---

### Remediation Step 4: Fix MDX Curly Braces in Module 5

**Target File**: `ai-book-docs/module5-kinematics-dynamics/5-4-rigid-body-dynamics.mdx`  
**Line**: 163  
**Action**: Replace unescaped `(M^{-1})` with KaTeX inline math `$M^{-1}$`.

#### Exact Line Patch:
```markdown
<<<<
| **Cholesky (M^{-1})** | Naive Forward Dynamics via Matrix Inversion | `O(n^3)` | 180 us | Offline analysis, small kinematic chains |
====
| **Cholesky ($M^{-1}$)** | Naive Forward Dynamics via Matrix Inversion | `O(n^3)` | 180 us | Offline analysis, small kinematic chains |
>>>>
```

---

## 5. Verification Method

Once the implementing agents apply the above patches, run the following commands to independently verify full resolution:

### 1. Backend Hermeticity & E2E Test Suite Pass
```powershell
# Verify single streaming test passes offline
cd backend
uv run pytest -v tests/e2e/test_tier1_backend_coverage.py -k test_ask_sse_streaming_mode

# Verify entire unified E2E suite passes 100% (28/28 tests)
cd ..
python run_e2e_tests.py
```
*Expected*: Exit code 0. 28 passed in ~10s. Zero HTTP calls to `generativelanguage.googleapis.com`.

### 2. Backend Lint Cleanliness
```powershell
cd backend
uv run ruff check .
```
*Expected*: Exit code 0 (`All checks passed!`).

### 3. Frontend Typecheck & Production Build
```powershell
npm run typecheck
npm run build
```
*Expected*: Both exit code 0 with zero diagnostics. Static HTML files generated in `build/`.

### 4. KaTeX MDX Math Rendering Verification
```powershell
node -e "const fs = require('fs'); const line = fs.readFileSync('ai-book-docs/module5-kinematics-dynamics/5-4-rigid-body-dynamics.mdx', 'utf8').split('\n')[162]; console.log('Line 163:', line); console.log('Fixed KaTeX:', line.includes('$M^{-1}$'));"
```
*Expected*: Prints `Fixed KaTeX: true`.

### 5. ChapterProgress Prefix Collision Verification
```powershell
node -e "const prefix='1'; const check = (id) => Boolean(id.match(new RegExp('^module' + prefix + '([^0-9]|$)'))); console.log('module1 match:', check('module1')); console.log('module1-intro match:', check('module1-intro')); console.log('module10-1 collision avoided:', check('module10-1') === false); console.log('module12-1 collision avoided:', check('module12-1') === false);"
```
*Expected*: All conditions return `true`.
