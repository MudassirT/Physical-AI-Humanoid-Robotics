# Tasks: RAG Data Pipeline

**Input**: Design documents from `specs/006-rag-data-pipeline/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [X] T001 Create `backend` directory for the project.
- [X] T002 Initialize `uv` project in `backend/`.
- [X] T003 Add dependencies to `backend/pyproject.toml`.
- [X] T004 Install dependencies with `uv sync`.
- [X] T005 Create directory structure in `backend/app/`.
- [X] T006 Create `.env` and `.env.example` files in `backend/`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

- [X] T007 [US1] Implement configuration management in `backend/app/core/config.py`.
- [X] T008 [US1] Define data models in `backend/app/models/models.py`.

---

## Phase 3: User Story 1 - Automated Content Ingestion (Priority: P1) 🎯 MVP

**Goal**: Automate the process of crawling a website, extracting content, generating embeddings, and storing them in a vector database.

**Independent Test**: Run the main script and verify that the Qdrant collection is populated with the correct data.

### Implementation for User Story 1

- [ ] T009 [P] [US1] Implement the `Crawler` service in `backend/app/services/crawler.py`.
- [ ] T010 [P] [US1] Implement the `TextProcessor` service in `backend/app/services/text_processor.py`.
- [ ] T011 [P] [US1] Implement the `EmbeddingGenerator` service in `backend/app/services/embedding.py`.
- [ ] T012 [P] [US1] Implement the `VectorStore` service in `backend/app/services/vector_store.py`.
- [ ] T013 [US1] Implement the main pipeline orchestration in `backend/app/main.py`.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [ ] T014 [P] Add logging to all services.
- [ ] T015 [P] Add robust error handling to the pipeline.
- [ ] T016 [P] [US1] Write unit tests for the `Crawler` service in `backend/tests/test_crawler.py`.
- [ ] T017 [P] [US1] Write unit tests for the `TextProcessor` service in `backend/tests/test_text_processor.py`.
- [ ] T018 [P] [US1] Write unit tests for the `EmbeddingGenerator` service in `backend/tests/test_embedding.py`.
- [ ] T019 Update `quickstart.md` with final instructions.
- [ ] T020 Validate the entire pipeline by running the `main.py` script.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Complete.
- **Foundational (Phase 2)**: Complete.
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion.
- **Polish (Phase 4)**: Depends on User Story 1 completion.

### Within Each User Story

- Models are defined before services.
- Services can be implemented in parallel.
- Main pipeline orchestration depends on all services.

### Parallel Opportunities

- The services in Phase 3 (T009-T012) can be implemented in parallel.
- The polish tasks in Phase 4 (T014-T018) can be implemented in parallel.
