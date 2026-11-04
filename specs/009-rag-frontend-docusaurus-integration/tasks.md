# Tasks: RAG Frontend–Backend Integration

**Input**: Design documents from `specs/009-rag-frontend-docusaurus-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the necessary frontend file structure and configure environment variables.

- [ ] T001 Create the directory `src/components/ChatWidget/`.
- [ ] T002 Create empty files: `src/components/ChatWidget/ChatWidget.tsx`, `src/components/ChatWidget/ChatWidget.module.css`, `src/components/ChatWidget/index.ts`.
- [ ] T003 Configure environment variables for API URLs (e.g., in `.env` or `docusaurus.config.js` if it supports `process.env`).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement the basic UI structure for the chat widget.

- [ ] T004 Implement the basic React component structure for `ChatWidget.tsx` with a chat input and an empty message display area.
- [ ] T005 Implement basic CSS styling for `ChatWidget.module.css` to define layout and initial appearance.

**Checkpoint**: Basic chat widget UI is rendered.

---

## Phase 3: User Story 1 - Interact with the Chat Widget (Priority: P1) 🎯 MVP

**Goal**: Enable users to send questions and receive grounded responses through the chat widget.

**Independent Test**: Interact with the chat widget in the Docusaurus frontend, send a question, and verify the agent's response appears.

### Implementation for User Story 1

- [ ] T006 [US1] Implement asynchronous fetch requests in `src/components/ChatWidget/ChatWidget.tsx` to send user queries to the FastAPI `/ask` endpoint.
- [ ] T007 [US1] Implement state management in `src/components/ChatWidget/ChatWidget.tsx` for chat history (list of `ChatMessage` objects), loading states during API calls, and the current user input.
- [ ] T008 [US1] Implement logic to display the agent's responses, including extracted sources if available, in the chat history area (`src/components/ChatWidget/ChatWidget.tsx`).
- [ ] T009 [US1] Add basic network error handling (e.g., `try-catch` for fetch requests) and display user-friendly error messages in `src/components/ChatWidget/ChatWidget.tsx`.
- [ ] T010 [US1] Integrate the `ChatWidget` component into a Docusaurus page (e.g., `src/pages/index.tsx` or a new markdown page) or a common layout for demonstration.

**Checkpoint**: User Story 1 should be fully functional.

---

## Phase 4: User Story 2 - Environment Switching (Priority: P2)

**Goal**: Provide a mechanism to easily switch between development and production API URLs.

**Independent Test**: Verify that changing the environment variable (e.g., `REACT_APP_FASTAPI_BASE_URL`) correctly alters the API endpoint used by the chat widget.

### Implementation for User Story 2

- [ ] T011 [US2] Implement logic in `src/components/ChatWidget/ChatWidget.tsx` to dynamically use the `REACT_APP_FASTAPI_BASE_URL` environment variable for constructing the API endpoint URL.

**Checkpoint**: Environment switching is functional.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Enhance user experience, robustness, and adherence to Docusaurus standards.

- [ ] T012 Ensure responsive design and optimal layout for `ChatWidget.module.css` across various screen sizes.
- [ ] T013 Add input validation to prevent submission of empty queries and sanitize user input in `src/components/ChatWidget/ChatWidget.tsx`.
- [ ] T014 Add comprehensive comments and JSDoc-style documentation to `ChatWidget.tsx`.
- [ ] T015 Perform accessibility checks for the chat widget (e.g., keyboard navigation, ARIA attributes).

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately. All tasks are parallelizable.
-   **Foundational (Phase 2)**: Depends on Phase 1 completion.
-   **User Story 1 (Phase 3)**: Depends on Phase 2 completion.
-   **User Story 2 (Phase 4)**: Depends on Phase 1 completion. Can be implemented in parallel with User Story 1's network integration.
-   **Polish (Phase 5)**: Depends on the UI and functionality being largely complete.

### Within Each User Story

-   Tasks should be executed in a logical flow: setup of UI elements before integration logic.

### Parallel Opportunities

-   All tasks in Phase 1 can be executed in parallel.
-   Phase 2 tasks can be done in parallel.
-   User Story 1 and User Story 2 (specifically T011) can have some parallel aspects if different developers work on them, but T011 directly supports T006.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup.
2.  Complete Phase 2: Foundational.
3.  Complete Phase 3: User Story 1.
4.  **STOP and VALIDATE**: Test User Story 1 independently in the Docusaurus development environment.
5.  Deploy/demo if ready.

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready.
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!).
3.  Add User Story 2 → Test independently → Deploy/Demo.
4.  Each story adds value without breaking previous stories.
