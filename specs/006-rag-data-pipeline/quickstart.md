# Quickstart: RAG Data Pipeline

This guide provides the steps to set up and run the RAG data pipeline.

## Prerequisites

- Python 3.11+
- `uv` installed (`pip install uv`)
- A Cohere API key
- A Qdrant Cloud account with an API key and URL

## Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/BBismaarshad/Spec-Driven-Development-hackathon.git
    cd spec-driven-development
    ```

2.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

3.  **Create a virtual environment and install dependencies**:
    ```bash
    uv sync
    ```

4.  **Set up environment variables**:
    -   Create a `.env` file in the `backend` directory.
    -   Add your API keys and Qdrant URL to the `.env` file. See `.env.example` for the required format.

## Running the Tests

To run the unit tests, first install `pytest`:

```bash
uv pip install pytest
```

Then run the tests:

```bash
uv run pytest
```

## Running the Pipeline

To run the data ingestion pipeline, execute the `main.py` script:

```bash
uv run python app/main.py
```

The script will:
1.  Crawl the deployed book website.
2.  Extract, clean, and chunk the text content.
3.  Generate embeddings using the Cohere API.
4.  Create a new collection in Qdrant and upload the embeddings.

## Verification

After the pipeline runs successfully, you can verify the results by:
-   Checking the logs printed to the console.
-   Inspecting the `ragbot_embedding` collection in your Qdrant Cloud dashboard.
