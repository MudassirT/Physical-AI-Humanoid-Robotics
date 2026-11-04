# Quickstart: RAG Retrieval Verification

**Feature**: `007-verify-rag-retrieval`

This guide provides instructions on how to run the RAG retrieval verification test suite.

## Prerequisites

1.  **Python Environment**: Ensure you have Python 3.13 and `uv` installed, as specified in `backend/.python-version` and `backend/pyproject.toml`.
2.  **Dependencies**: Install the required Python packages.
    ```bash
    cd backend
    uv pip install -r requirements.txt
    ```
3.  **Qdrant Credentials**: The test suite requires access to the Qdrant Cloud database. Ensure the following environment variables are set:
    -   `QDRANT_URL`
    -   `QDRANT_API_KEY`

## Running the Verification Test

The verification test is run using `pytest`.

1.  Navigate to the root of the repository.
2.  Execute the following command:

    ```bash
    pytest backend/tests/retrieval/test_retrieval.py
    ```

## Expected Output

The test runner will execute the predefined set of queries in `test_retrieval.py`.

-   **Console Output**: `pytest` will show the progress of the test run, indicating pass or fail for each assertion.
-   **Log File**: A detailed log file will be generated (e.g., in `backend/logs/retrieval_verification.log`). This log will contain an entry for each query, including the query text, the retrieved chunks, their similarity scores, and their source URLs.

### Example Log Entry

```json
{
  "timestamp": "2025-12-12T14:30:00Z",
  "query_text": "What are the core concepts of ROS 2?",
  "passed": true,
  "retrieved_chunks": [
    {
      "chunk_id": "doc-abc-123",
      "source_url": "ai-book-docs/module1-ros2/1-2-ros2-core-concepts.mdx",
      "score": 0.85,
      "original_text": "ROS 2 core concepts include nodes, topics, services, actions, and parameters..."
    }
  ]
}
```
