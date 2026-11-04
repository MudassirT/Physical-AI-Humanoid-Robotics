# Data Model: RAG Frontend–Backend Integration

**Source**: `specs/009-rag-frontend-docusaurus-integration/spec.md`

This document outlines the data models relevant to the RAG frontend-backend integration. These represent the structures for messages exchanged within the chat widget and with the FastAPI backend.

## 1. ChatMessage (Frontend State)

Represents a single message displayed in the chat history within the Docusaurus frontend.

-   **Type**: TypeScript Interface/Type
-   **File**: `src/components/ChatWidget/ChatWidget.tsx` (or `src/components/ChatWidget/types.ts`)

| Field       | Type     | Description                                           |
| ----------- | -------- | ----------------------------------------------------- |
| `id`        | string   | Unique identifier for the message (e.g., UUID).      |
| `text`      | string   | The content of the message.                           |
| `sender`    | "user" | "agent" | "system" | Indicates who sent the message.           |
| `timestamp` | Date     | The time when the message was created/received.        |
| `sources`   | string[] | (Optional) List of source URLs if from the agent.     |

## 2. ChatInput (Frontend)

Represents the user's input string before it is sent to the backend.

-   **Type**: string
-   **File**: `src/components/ChatWidget/ChatWidget.tsx`

| Field      | Type   | Description                                          |
| ---------- | ------ | ---------------------------------------------------- |
| `value`    | string | The current text in the user input field.            |

## 3. FastAPIEndpoint (Frontend Configuration)

Represents the configuration for connecting to the FastAPI RAG agent backend.

-   **Type**: string
-   **File**: Docusaurus configuration (e.g., `docusaurus.config.js` or environment variable)

| Field    | Type   | Description                                           |
| -------- | ------ | ----------------------------------------------------- |
| `url`    | string | The base URL of the FastAPI backend (e.g., `http://localhost:8000`). |

## Relationships

-   `ChatInput` is sent to the FastAPI backend, corresponding to the `ChatQuery` model defined in the backend.
-   The FastAPI backend returns a response corresponding to the `ChatResponse` model, which is then used to create `ChatMessage` objects for display in the frontend.
