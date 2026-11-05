---
id: 2
title: Generate Tasks for RAG Retrieval Verification
stage: tasks
date: 2025-12-12
surface: CLI
model: gemini-1.5-pro
feature: 007-verify-rag-retrieval
branch: 007-verify-rag-retrieval
user:
command: /sp.tasks
labels: []
links:
  spec: specs/007-verify-rag-retrieval/spec.md
  plan: specs/007-verify-rag-retrieval/plan.md
  ticket:
  adr:
  pr:
files:
  - specs/007-verify-rag-retrieval/tasks.md
tests:
---

## Prompt

---
description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `.specify.specify/templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - Final Phase: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

Context for task generation: 

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

## Response snapshot

Task generation complete. The   asks.md file has been created at 'specs/007-verify-rag-retrieval/tasks.md'.

Summary:
- Total Tasks: 12
- Tasks for User Story 1: 5
- MVP Scope: Complete Phase 1, 2, and 3.
- Parallel Opportunities: 2 tasks identified.

## Outcome

- ✅ Impact: Successfully generated the `tasks.md` file with a detailed, phased implementation plan.
- 🧪 Tests: No tests were run.
- 📁 Files: Created `specs/007-verify-rag-retrieval/tasks.md`.
- 🔁 Next prompts: /sp.implement
- 🧠 Reflection: The process of generating tasks from the spec and plan documents is well-defined and leads to a clear, actionable checklist for implementation.
