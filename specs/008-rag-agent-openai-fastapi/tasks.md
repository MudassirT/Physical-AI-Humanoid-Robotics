# Tasks: RAG Agent with OpenAI and FastAPI

**Input**: Design documents from `specs/008-rag-agent-openai-fastapi/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the directory structure and initial files for the new RAG agent feature.

- [ ] T001 [P] Create the directory `backend/app/agent/`.
- [ ] T002 [P] Create the directory `backend/app/retriever/`.
- [ ] T003 [P] Create the directory `backend/app/routes/`.
- [ ] T004 [P] Create the directory `backend/app/schemas/`.
- [ ] T005 [P] Create the file `backend/app/agent/__init__.py`.
- [ ] T006 [P] Create the file `backend/app/agent/agent_service.py`.
- [ ] T007 [P] Create the file `backend/app/retriever/__init__.py`.
- [ ] T008 [P] Create the file `backend/app/retriever/retriever_service.py`.
- [ ] T009 [P] Create the file `backend/app/routes/__init__.py`.
- [ ] T010 [P] Create the file `backend/app/routes/chat.py`.
- [ ] T011 [P] Create the file `backend/app/schemas/__init__.py`.
- [ ] T012 [P] Create the file `backend/app/schemas/chat_models.py`.
- [ ] T013 [P] Add `openai` to the dependencies in `backend/pyproject.toml`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement the data models required for the API.

- [ ] T014 Implement the Pydantic schemas (`ChatQuery`, `ChatResponse`, `HealthStatus`, `RetrievalTestQuery`, `RetrievalTestResponse`) in `backend/app/schemas/chat_models.py`.

**Checkpoint**: Foundation ready.

---

## Phase 3: User Story 1 - Chat with the RAG Agent (Priority: P1) 🎯 MVP

**Goal**: Implement the core functionality of the RAG agent and expose it via the `/ask` endpoint.

**Independent Test**: Send a POST request to the `/ask` endpoint and verify the response is grounded in the book content.

### Implementation for User Story 1

- [ ] T015 [US1] Implement the Qdrant retrieval logic in `backend/app/retriever/retriever_service.py`. This will be similar to the logic in `specs/007-verify-rag-retrieval`.
- [ ] T016 [US1] Implement the OpenAI Agent logic in `backend/app/agent/agent_service.py`. This service will initialize the agent and include the custom retrieval function which calls the `retriever_service`.
- [ ] T017 [US1] Implement the `/ask` route in `backend/app/routes/chat.py`. This route will use the `agent_service` to get a response.
- [ ] T018 [US1] Mount the new chat routes in the main FastAPI application in `backend/app/main.py`.

**Checkpoint**: User Story 1 should be functional.

---

## Phase 4: User Story 2 - Health and Retrieval Check (Priority: P2)

**Goal**: Implement endpoints for monitoring and debugging the service.

**Independent Test**: Send GET requests to `/health` and POST requests to `/retrieval-test` to verify their responses.

### Implementation for User Story 2

- [ ] T019 [US2] Implement the `/health` endpoint in `backend/app/routes/chat.py`.
- [ ] T020 [US2] Implement the `/retrieval-test` endpoint in `backend/app/routes/chat.py`, which will directly call the `retriever_service`.

**Checkpoint**: User Story 2 should be functional.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Add logging and error handling to improve robustness.

- [ ] T021 Add structured logging to `backend/app/routes/chat.py` for all incoming requests and responses.
- [ ] T022 Implement exception handling in the API routes to catch errors from the agent or retriever and return appropriate HTTP error responses.
- [ ] T023 Add comprehensive docstrings to all new functions and classes.

---

## Dependencies & Execution Order

- **Setup (Phase 1)**: Can start immediately. All tasks are parallelizable.
- **Foundational (Phase 2)**: Depends on Phase 1 completion.
- **User Story 1 (Phase 3)**: Depends on Phase 2 completion.
- **User Story 2 (Phase 4)**: Depends on Phase 2 completion. Can be implemented in parallel with User Story 1.
- **Polish (Phase 5)**: Can be done after the user stories are complete.
