# Quickstart: RAG Agent Backend

**Feature**: `008-rag-agent-openai-fastapi`

This guide provides instructions on how to run the RAG Agent's FastAPI backend server.

## Prerequisites

1.  **Python Environment**: Ensure you have Python 3.13 and `uv` installed.
2.  **Dependencies**: Install the required Python packages, including `fastapi`, `uvicorn`, `openai`, and `qdrant-client`.
    ```bash
    cd backend
    uv pip sync
    ```
3.  **Environment Variables**: The application requires several environment variables to be set. Create a `.env` file in the `backend` directory with the following keys:
    -   `QDRANT_URL`: The URL of your Qdrant instance.
    -   `QDRANT_API_KEY`: The API key for your Qdrant instance.
    -   `OPENAI_API_KEY`: Your OpenAI API key.

## Running the Server

1.  Navigate to the `backend` directory.
2.  Run the FastAPI server using `uvicorn`:

    ```bash
    uvicorn app.main:app --reload
    ```
    
    The server will start, typically on `http://127.0.0.1:8000`.

## Interacting with the API

You can interact with the API using tools like `curl`, Postman, or the automatically generated FastAPI documentation.

### API Documentation

Once the server is running, navigate to `http://127.0.0.1:8000/docs` in your browser to view the interactive OpenAPI documentation.

### Example: Asking a Question

Send a POST request to the `/ask` endpoint:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/ask' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d 
'{
  "query_text": "What are the core concepts of ROS 2?"
}'
```

### Example: Checking Health

Send a GET request to the `/health` endpoint:

```bash
curl 'http://127.0.0.1:8000/health'
```

