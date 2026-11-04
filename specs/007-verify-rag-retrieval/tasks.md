# Tasks: RAG Retrieval Pipeline Verification

**Input**: Design documents from `specs/007-verify-rag-retrieval/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Test tasks are included as this feature is a test suite.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- The project structure is defined in `specs/007-verify-rag-retrieval/plan.md`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [ ] T001 Create the directory structure `backend/tests/retrieval/`
- [ ] T002 Create empty Python files: `backend/tests/retrieval/__init__.py`, `backend/tests/retrieval/test_retrieval.py`, `backend/tests/retrieval/qdrant_connector.py`, `backend/tests/retrieval/retrieval_logic.py`, `backend/tests/retrieval/mapping.py`, `backend/tests/retrieval/models.py`
- [ ] T003 [P] Add `qdrant-client` and `pytest` to the project's dependencies in `backend/pyproject.toml`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

- [ ] T004 Implement the Qdrant connection logic in `backend/tests/retrieval/qdrant_connector.py`.
- [ ] T005 Define the data models for queries and retrieval results in `backend/tests/retrieval/models.py`.

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Verify Retrieval Accuracy (Priority: P1) 🎯 MVP

**Goal**: Validate the retrieval pipeline by running a test script that executes predefined queries and verifies the accuracy of the returned content chunks.

**Independent Test**: The entire user story is a test. It can be verified by running `pytest backend/tests/retrieval/test_retrieval.py` and checking the output logs and reports.

### Implementation for User Story 1

- [ ] T006 [US1] In `backend/tests/retrieval/test_retrieval.py`, set up the main test function and a placeholder for the set of 10-20 sample queries.
- [ ] T007 [US1] Implement the core retrieval function in `backend/tests/retrieval/retrieval_logic.py` to query Qdrant using the connector.
- [ ] T008 [US1] Implement the chunk-to-URL mapping logic in `backend/tests/retrieval/mapping.py`.
- [ ] T009 [US1] In `backend/tests/retrieval/test_retrieval.py`, implement the main test assertion logic, using the retrieval and mapping functions to verify results against the expected outcomes.
- [ ] T010 [US1] Add detailed logging to `backend/tests/retrieval/test_retrieval.py` to record the query, returned chunk IDs, similarity scores, and source provenance for each test query.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [ ] T011 [P] Add comprehensive docstrings and comments to all new files in `backend/tests/retrieval/`.
- [ ] T012 Refine the console output and log format of the test run to ensure clarity and readability.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion.
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion.
- **Polish (Phase 4)**: Depends on User Story 1 completion.

### Within Each User Story

- The tasks for User Story 1 should be executed in order, as they depend on each other.

### Parallel Opportunities

- **T003** can be done in parallel with T001 and T002.
- **T011** can be worked on in parallel with other polish tasks.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently by running the pytest script.
5.  Demo the results by showing the test output and logs.
