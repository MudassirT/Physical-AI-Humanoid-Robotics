# Data Model: RAG Agent API

**Source**: `specs/008-rag-agent-openai-fastapi/spec.md`

This document outlines the data models for the RAG Agent's FastAPI backend. These models will be implemented as Pydantic schemas in `backend/app/schemas/chat_models.py`.

## 1. ChatQuery (Request)

Represents an incoming user question sent to the `/ask` endpoint.

-   **Type**: Pydantic BaseModel
-   **File**: `backend/app/schemas/chat_models.py`

| Field         | Type   | Description                            | Validation |
| ------------- | ------ | -------------------------------------- | ---------- |
| `query_text`  | string | The natural language text of the user's question. | Required, non-empty |

## 2. ChatResponse (Response)

Represents the agent's response sent back to the user from the `/ask` endpoint.

-   **Type**: Pydantic BaseModel
-   **File**: `backend/app/schemas/chat_models.py`

| Field              | Type             | Description                                                   |
| ------------------ | ---------------- | ------------------------------------------------------------- |
| `answer_text`      | string           | The agent's synthesized answer, grounded in the book content. |
| `retrieved_sources`| list[string]     | A list of source URLs/identifiers for the content chunks used to generate the answer. |

## 3. HealthStatus (Response)

Represents the response from the `/health` endpoint.

-   **Type**: Pydantic BaseModel
-   **File**: `backend/app/schemas/chat_models.py`

| Field    | Type   | Description                             |
| -------- | ------ | --------------------------------------- |
| `status` | string | The operational status of the service (e.g., "ok"). |

## 4. RetrievalTestQuery (Request)

Represents the request for the `/retrieval-test` endpoint.

-   **Type**: Pydantic BaseModel
-   **File**: `backend/app/schemas/chat_models.py`

| Field         | Type   | Description                            |
| ------------- | ------ | -------------------------------------- |
| `query_text`  | string | The query to test against the retriever. |

## 5. RetrievalTestResponse (Response)

Represents the response from the `/retrieval-test` endpoint. It returns the raw retrieved chunks.

-   **Type**: Pydantic BaseModel
-   **File**: `backend/app/schemas/chat_models.py`

| Field    | Type             | Description                             |
| -------- | ---------------- | --------------------------------------- |
| `chunks` | list[ContentChunk] | A list of the raw content chunks retrieved from Qdrant. |

*(Note: `ContentChunk` would be another Pydantic model with fields like `chunk_id`, `source_url`, `original_text`, and `score`.)*
