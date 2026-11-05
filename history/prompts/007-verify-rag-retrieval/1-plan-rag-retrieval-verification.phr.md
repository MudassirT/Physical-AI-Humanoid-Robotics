--- 
id: 1
title: Plan RAG Retrieval Verification
stage: plan
date: 2025-12-12
surface: CLI
model: gemini-1.5-pro
feature: 007-verify-rag-retrieval
branch: 007-verify-rag-retrieval
user: 
command: /sp.plan
labels: []
links:
  spec: specs/007-verify-rag-retrieval/spec.md
  ticket: 
  adr: 
  pr: 
files:
  - specs/007-verify-rag-retrieval/plan.md
  - specs/007-verify-rag-retrieval/data-model.md
  - specs/007-verify-rag-retrieval/quickstart.md
tests:
---

## Prompt

---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType gemini`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

---

/sp.plan
- Create an architecture sketch outlining retrieval flow, section structure, and research-while-testing approach.
- Document key decisions: retrieval strategy, chunk mapping, scoring thresholds, and tradeoffs.
- Run retrieval tests using Qdrant: validate relevance, similarity scores, and chunk-to-URL accuracy.
- Apply quality validation checks aligned with acceptance criteria and APA-style documentation rules.
- Organize work in phases: Research → Foundation → Analysis → Synthesis, producing logs + verification results.

## Response snapshot

Planning phase for feature '007-verify-rag-retrieval' is complete. The following artifacts have been generated in 'specs/007-verify-rag-retrieval/':
- plan.md
- data-model.md
- quickstart.md

You can now proceed to the task generation phase with '/sp.tasks'.

## Outcome

- ✅ Impact: Successfully generated all planning artifacts for the feature.
- 🧪 Tests: No tests were run.
- 📁 Files: Created plan.md, data-model.md, and quickstart.md.
- 🔁 Next prompts: /sp.tasks
- 🧠 Reflection: The process was smooth. The constitution file was not directly relevant to the backend task, but it was good to check. The planning phase is now robust.
