## 2026-11-09T18:31:42Z
You are worker_m3_manipulation (archetype: teamwork_worker).
Your task is to author all 8 chapters for Module 7: Dexterous Manipulation & Hand Design in `ai-book-docs/module7-dexterous-manipulation/`.

Working directory: C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main
State folder: C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\worker_m3_manipulation\
Exclusive Write Ownership: `ai-book-docs/module7-dexterous-manipulation/` ONLY. Do NOT touch any other directory.

Authoritative Reference Documents:
1. `specs/010-master-plan-curriculum-expansion/spec.md` (§ Module 7)
2. `C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\spec_miner_curriculum\handoff.md` (§ Section 4, Module 7)
3. `C:\Users\DELL\Desktop\Spec-Driven-Development-hackathon-main\.agents\teamwork\ORIGINAL_REQUEST.md`
4. Reference chapter style: `ai-book-docs/module1-ros2/1-11-ros2-control.mdx`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Deliverables:
1. Create `ai-book-docs/module7-dexterous-manipulation/_category_.json`:
```json
{
  "label": "Dexterous Manipulation & Hand Design",
  "position": 7
}
```

2. Author all 8 chapters:
- `7-1-introduction-to-dexterous-manipulation.mdx` (Manipulation taxonomy, human hand 21 DOF vs robot hands, kinematic Jacobians)
- `7-2-grasp-theory.mdx` (Contact models, Grasp Matrix G, Form vs Force Closure, Grasp Wrench Space, Ferrari-Canny metric)
- `7-3-robotic-hand-design.mdx` (Underactuated hands, Shadow Hand, tendon routing matrix, Capstan friction, flexure joints)
- `7-4-tactile-sensing.mdx` (GelSight optical tactile, photometric stereo reconstruction, piezoresistive skins, slip detection)
- `7-5-motion-planning-for-manipulation.mdx` (C-space, RRT*, MoveIt 2 C++ client, TAMP PDDLStream, Riemannian Motion Policies)
- `7-6-learning-based-manipulation.mdx` (GraspNet-1B, Contact-GraspNet, ACT bimanual policy on LEROBOT, Bi-DexHands in-hand rotation)
- `7-7-assembly-and-contact-rich-tasks.mdx` (Peg-in-hole jamming/wedging, impedance control, spiral search, Mason hybrid control)
- `7-8-manipulation-benchmarks.mdx` (RoboSuite, ManiSkill3, DROID dataset, BridgeData V2, standardized evaluation protocols)

Per-Chapter Standards:
- Valid YAML Frontmatter (`sidebar_position`: 1 to 8, `title`, `description`)
- Imports at top:
  `import ChapterProgress from '@site/src/components/ChapterProgress';`
  `import QuizEngine from '@site/src/components/QuizEngine';`
- Real-world opening motivation (1-2 paragraphs)
- Full mathematical derivations with LaTeX (`$...$` for inline, `$$...$$` for block)
- Complete Mermaid architecture diagrams
- Complete, runnable Python or C++ code block
- Multi-column comparison tables
- 3–8 seminal research citations with annotations
- Hands-on Lab Project with clear success criteria
- `<ChapterProgress chapterId="7-X-..." moduleId="module7" totalChapters={8} />`
- `<QuizEngine quizId="quiz-7-X" title="..." moduleId="module7" passThreshold={70} questions={[...]} />` (minimum 3 high-quality questions with explanations)
- MDX v3 safety: escape any raw curly braces in markdown prose or use backticks; do not use raw `<` in prose (use `&lt;` or backticks).

Verification:
- Run `npm run build` or verify MDX compilation and write your handoff report to `.agents/teamwork/worker_m3_manipulation/handoff.md`.
- Communicate back when complete via send_message.
