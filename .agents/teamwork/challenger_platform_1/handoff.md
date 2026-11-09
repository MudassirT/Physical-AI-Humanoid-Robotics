# Handoff Report — Empirical Challenger (Milestone M1 Platform & KaTeX)

**Agent**: `challenger_platform_1`  
**Mission**: Empirically challenge and stress-test the Frontend Platform & KaTeX Upgrades (Milestone M1)  
**Date**: 2026-11-09T19:57:45Z  
**Verdict**: **REJECT** (Pending 5 specific remediations detailed below)

---

## 1. Observation

Direct empirical commands executed and verbatim results observed:

### Observation 1.1: TypeScript Typecheck & Docusaurus Production Build
- Command: `npm run typecheck`  
  Result: Code 0 (clean, no TypeScript diagnostics).
- Command: `npm run build`  
  Result: Code 0 ([SUCCESS] Generated static files in "build", 41 HTML documents built).

### Observation 1.2: KaTeX Syntax Rendering in Build Output
- HTML verification command:
  ```powershell
  node -e "const fs = require('fs'); const path = require('path'); function walk(d){let r=[]; fs.readdirSync(d).forEach(f=>{let p=path.join(d,f); if(fs.statSync(p).isDirectory()) r=r.concat(walk(p)); else r.push(p);}); return r;} const html=walk(path.join('build', 'ai-book')).filter(f=>f.endsWith('.html')); const katexHtml = html.filter(f=>fs.readFileSync(f,'utf8').includes('class=katex')); console.log('HTML with class=katex:', katexHtml.length); katexHtml.forEach(f => console.log('  ', f));"
  ```
  Result:
  `HTML with class=katex: 7`
  - `build\ai-book\module1-ros2\1-2-ros2-core-concepts\index.html`
  - `build\ai-book\module1-ros2\1-8-parameters\index.html`
  - `build\ai-book\module2-digital-twin\2-1-introduction-to-digital-twins\index.html`
  - `build\ai-book\module2-digital-twin\2-4-unity-for-high-fidelity-visuals\index.html`
  - `build\ai-book\module3-ai-robot-brain\3-2-isaac-sim-for-humanoids\index.html`
  - `build\ai-book\module3-ai-robot-brain\3-4-nav2-for-bipedal-movement\index.html`
  - `build\ai-book\module4-vla\4-3-cognitive-planning-with-llms\index.html`
- KaTeX stylesheet link `<link rel=stylesheet href=https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css ...>` is present in `<head>` across all 41 built pages.
- Delimiter scan across all 36 existing MDX documents:
  - Inline math (`$...$`): Present in 10 MDX files.
  - Block math (`$$...$$`): **0 occurrences** across all 36 existing chapters. No chapter currently uses block math syntax.
  - Block math `@mdx-js/mdx` compilation test with `remark-math` and `rehype-katex`: Compiles successfully without JSX syntax conflicts.

### Observation 1.3: Unescaped Curly Braces in MDX Prose / Headings
- AST / Line audit command across all 36 MDX files:
  Line flagged: `ai-book-docs/module5-kinematics-dynamics/5-4-rigid-body-dynamics.mdx:163`:
  ```markdown
  | **Cholesky (M^{-1})** | Naive Forward Dynamics via Matrix Inversion | `O(n^3)` | 180 us | Offline analysis, small kinematic chains |
  ```
- Compiled MDX AST for line 163 via `@mdx-js/mdx`:
  ```javascript
  _jsxs(_components.strong, {
    children: ["Cholesky (M^", -1, ")"]
  })
  ```
  The curly brace `{ -1 }` is swallowed as a JavaScript numeric literal `-1`, rendering broken plain text `Cholesky (M^-1)` rather than LaTeX mathematical superscript `$M^{-1}$` or code ticks `` `M^{-1}` ``.
- Acorn parser test: Unescaped `{ foo: "bar" }` or undeclared `{identifier}` in markdown body triggers `Could not parse expression with acorn` or runtime `ReferenceError`.

### Observation 1.4: ChapterProgress Component Boundary Defect & Prefix Collision
- Component: `src/components/ChapterProgress/ChapterProgress.tsx`
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
  When `chapterId` is `undefined` (e.g. `<ChapterProgress />`), it crashes with uncaught exception:
  `TypeError: Cannot read properties of undefined (reading 'match')`.
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
  Empirical evaluation:
  `'module10'.includes('module1') === true`  
  `'module11'.includes('module1') === true`  
  `'module12'.includes('module1') === true`  
  When a student completes chapters in Module 10, 11, or 12 that contain `module10`, `module11`, or `module12`, Module 1's progress bar falsely increments because `'module10'.includes('module1')` is true.

### Observation 1.5: QuizEngine Component Edge Cases & Storage Handling
- Component: `src/components/QuizEngine/QuizEngine.tsx`
- Missing/Null questions prop:
  Lines 34, 150:
  ```typescript
  export function QuizEngine({ ..., questions = [], ... }: QuizProps)
  if (questions.length === 0)
  ```
  If `questions={null as any}` is passed, it crashes with uncaught `TypeError: Cannot read properties of null (reading 'length')`.
- Unselected submission protection:
  Lines 70–71, 108, 280: Submit button is disabled (`disabled={!isAllAnswered}`) and `handleSubmit` aborts if `!isAllAnswered`. Gating works as intended.
- Duplicate Question IDs:
  If a quiz contains questions sharing the same `id`, `selectedOptions[q.id]` collides, so `Object.keys(selectedOptions).length` never reaches `questions.length`. The submit button becomes permanently unclickable.
- Threshold conversion:
  Line 38: `passThreshold <= 1 ? Math.round(passThreshold * 100) : passThreshold`.
  Setting `passThreshold={1}` converts to `100%`.
- LocalStorage error handling:
  Calls to `getItem` and `setItem` in both `ChapterProgress` and `QuizEngine` are wrapped in `try/catch`. When localStorage is disabled or throws `QuotaExceededError`, UI does not crash.
  However, in `QuizEngine.tsx:127`:
  `const existing = raw ? JSON.parse(raw) : {}; existing[quizId] = ...`
  If `raw === '123'`, in strict mode `existing[quizId] = ...` throws `TypeError: Cannot create property on number '123'`, though it is caught by the enclosing `try/catch`.

### Observation 1.6: Dual-Track Test Suite & Linter Gate Failures
- Command: `python run_e2e_tests.py`
  Result: Exit code 1 (FAILED).
  Failure: `tests/e2e/test_tier1_backend_coverage.py::TestTier1BackendCoverage::test_ask_sse_streaming_mode`
  Verbatim stack trace:
  ```text
  google.genai.errors.ClientError: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details...
  ```
  The test executes a live network call to Google Gemini (`gemini-2.5-flash`) without mocking `ask_agent_stream` or `AgentService`, violating the hermetic zero-live-key contract specified in `TEST_INFRA.md` and `ORIGINAL_REQUEST.md`.
- Command: `cd backend; uv run ruff check .`
  Result: Exit code 1 (3 errors found):
  - `tests/test_adversarial_platform_m1.py:10:1: I001 [*] Import block is un-sorted or un-formatted`
  - `tests/test_adversarial_platform_m1.py:18:37: F401 [*] app.agent.agent_service.AgentService imported but unused`
  - `tests/test_adversarial_platform_m1.py:21:37: F401 [*] app.schemas.chat_models.ContentChunk imported but unused`

---

## 2. Logic Chain

1. **Premise 1**: A release candidate for Milestone M1 must satisfy all acceptance criteria in `ORIGINAL_REQUEST.md`: clean documentation build, hermetic tests passing 100%, zero ruff lint errors, and robust interactive components.
2. **Step 2 (Build & KaTeX)**: Based on Observation 1.1 and 1.2, `docusaurus.config.ts` successfully integrates `remark-math@6` and `rehype-katex@7`, generating `<span class=katex>` math elements and linking `katex.min.css`. `npm run build` and `npm run typecheck` succeed with code 0.
3. **Step 3 (MDX Escaping)**: Based on Observation 1.3, `ai-book-docs/module5-kinematics-dynamics/5-4-rigid-body-dynamics.mdx:163` contains unescaped `(M^{-1})`, resulting in MDX evaluating `{-1}` as JavaScript `-1` and generating broken typography `Cholesky (M^-1)` instead of math.
4. **Step 4 (Component Resilience)**: Based on Observation 1.4:
   - `ChapterProgress` crashes when `chapterId` is omitted due to unguarded `.match()` call.
   - `ChapterProgress` suffers from a string prefix collision where `'module10'.includes('module1') === true`, contaminating Module 1's progress calculation when Module 10, 11, or 12 chapters are completed.
5. **Step 5 (Quality Gates)**: Based on Observation 1.6:
   - `python run_e2e_tests.py` fails because `test_ask_sse_streaming_mode` in `test_tier1_backend_coverage.py` makes unmocked live requests to Google Gemini, exhausting quota (HTTP 429).
   - `uv run ruff check .` fails with 3 errors in `test_adversarial_platform_m1.py`.
6. **Conclusion**: While the core Docusaurus KaTeX integration and components are largely functional, the presence of runtime `TypeError` risks in `ChapterProgress`, the progress prefix collision bug, the MDX typography defect, the live API failure in the E2E suite, and the ruff lint errors require a **REJECT** verdict until remediated.

---

## 3. Caveats

- Interactive mouse clicks in real browser DOM were tested via headless SSR/React test harnesses rather than full Chrome Puppeteer/Playwright, as browser binaries are not installed in the workspace.
- The 74 pending chapters for Modules 6–12 are not yet authored (scheduled for M2–M4); the sidebar and navbar graceful fallback to `/ai-book/intro` was verified and works correctly.

---

## 4. Conclusion & Actionable Verdict

### Verdict: **REJECT**

Milestone M1 cannot be approved until the following 5 specific issues are resolved by the implementing agents:

1. **Fix `ChapterProgress.tsx:22` undefined guard**:
   In `src/components/ChapterProgress/ChapterProgress.tsx`, guard `normalizeModuleId`:
   ```typescript
   function normalizeModuleId(chapterId?: string, explicitModuleId?: string): string {
     if (explicitModuleId) return explicitModuleId;
     if (!chapterId) return 'general';
     const match = chapterId.match(/^(\d+)-/);
     if (match) return `module${match[1]}`;
     const prefixMatch = chapterId.match(/^(module\d+)/i);
     if (prefixMatch) return prefixMatch[1].toLowerCase();
     return 'general';
   }
   ```
2. **Fix `ChapterProgress.tsx:117` module prefix collision**:
   Replace string `.includes('module1')` with exact boundary matching so Module 1 does not count Module 10, 11, 12:
   ```typescript
   const moduleCompletedCount = completedChapters.filter((id) => {
     if (modulePrefixNum) {
       return id.startsWith(`${modulePrefixNum}-`) || id.match(new RegExp(`^module${modulePrefixNum}([^0-9]|$)`));
     }
     return id.includes(moduleId);
   }).length;
   ```
3. **Fix MDX typography in `5-4-rigid-body-dynamics.mdx:163`**:
   Change `| **Cholesky (M^{-1})** |` to `| **Cholesky ($M^{-1}$)** |` or `| **Cholesky (`M^{-1}`)** |`.
4. **Fix unmocked Gemini call in `test_tier1_backend_coverage.py:59`**:
   In `backend/tests/e2e/test_tier1_backend_coverage.py`, patch `ask_agent_stream` in `test_ask_sse_streaming_mode` using a mock generator yielding SSE lines so it runs 100% hermetically without live network calls.
5. **Fix ruff lint errors in `backend/tests/test_adversarial_platform_m1.py`**:
   Run `cd backend; uv run ruff check --fix .` or remove unused imports `AgentService` and `ContentChunk` and format import blocks.

---

## 5. Verification Method

To independently verify after fixes are applied:

1. **Verify Docusaurus build & typecheck**:
   ```powershell
   npm run typecheck
   npm run build
   ```
   *Expected*: Both exit code 0 with zero warnings.
2. **Verify MDX Curly Escaping**:
   ```powershell
   node -e "const fs=require('fs'); const lines=fs.readFileSync('ai-book-docs/module5-kinematics-dynamics/5-4-rigid-body-dynamics.mdx','utf8').split('\n'); console.log(lines[162]);"
   ```
   *Expected*: Contains `$M^{-1}$` or `` `M^{-1}` ``.
3. **Verify ChapterProgress Prefix Safety**:
   ```powershell
   node -e "const prefix='1'; const id='module10-1'; const matched = Boolean(id.match(new RegExp('^module' + prefix + '([^0-9]|$)'))); console.log('Collision resolved:', matched === false);"
   ```
   *Expected*: `Collision resolved: true`.
4. **Verify E2E Test Suite**:
   ```powershell
   python run_e2e_tests.py
   ```
   *Expected*: All 28 tests PASSED with 100% pass rate in ~10s.
5. **Verify Backend Linter**:
   ```powershell
   cd backend; uv run ruff check .
   ```
   *Expected*: `All checks passed!`.
