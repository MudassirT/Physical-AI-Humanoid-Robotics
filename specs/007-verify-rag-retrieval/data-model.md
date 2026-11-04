# Data Model: RAG Retrieval Verification

**Source**: `specs/007-verify-rag-retrieval/spec.md`

This document outlines the data entities relevant to the RAG retrieval verification feature. As this is a test suite, these are not persistent database models but rather in-memory data structures used during the script's execution.

## 1. Query

Represents a single test query to be executed against the vector database.

-   **Type**: `Class` (in-memory)
-   **File**: `backend/tests/retrieval/models.py`

| Field         | Type   | Description                                           |
| ------------- | ------ | ----------------------------------------------------- |
| `query_text`  | string | The natural language text of the question to be asked. |
| `expected_id` | string | An identifier for the expected source document/chunk. |

## 2. Content Chunk

Represents a piece of content retrieved from the Qdrant vector database.

-   **Type**: `Class` (in-memory, maps to Qdrant payload)
-   **File**: `backend/tests/retrieval/models.py`

| Field           | Type   | Description                                                    |
| --------------- | ------ | -------------------------------------------------------------- |
| `chunk_id`      | string | The unique identifier for the content chunk.                   |
| `source_url`    | string | The URL or path of the original document this chunk came from. |
| `original_text` | string | The raw text content of the chunk.                             |
| `score`         | float  | The similarity score returned by the vector search.            |

## 3. Retrieval Log

Represents the logged output for a single verification query. This is for reporting and debugging.

-   **Type**: `Log Entry` (structured log output)
-   **File**: N/A (written to a log file)

| Field               | Type          | Description                                           |
| ------------------- | ------------- | ----------------------------------------------------- |
| `timestamp`         | datetime      | The time the query was executed.                      |
| `query_text`        | string        | The text of the query that was run.                   |
| `retrieved_chunks`  | list[ContentChunk] | A list of the content chunks returned by the query.   |
| `passed`            | boolean       | Whether the retrieval was considered a success or not. |

## Relationships

-   A `Query` is executed and results in one `Retrieval Log`.
-   A `Retrieval Log` contains one or more `Content Chunk` objects.
