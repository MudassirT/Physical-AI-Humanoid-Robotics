# RAG Agent Backend

FastAPI backend for the **Physical AI & Humanoid Robotics** RAG (Retrieval-Augmented Generation) system.

The agent answers questions about the book exclusively from content stored in Qdrant, using OpenAI's `gpt-4o-mini` and Cohere embeddings.

---

## 🏗️ Architecture

```
backend/
├── app/
│   ├── agent/              # OpenAI tool-calling agent
│   │   └── agent_service.py
│   ├── core/               # Config & logging
│   │   ├── config.py       # Pydantic-settings (reads .env)
│   │   └── logging.py
│   ├── models/             # Domain models (Document, Embedding)
│   ├── retriever/          # Qdrant semantic retrieval
│   │   └── retriever_service.py
│   ├── routes/             # FastAPI routes
│   │   └── chat.py         # /ask, /health, /retrieval-test
│   ├── schemas/            # Pydantic request/response schemas
│   │   └── chat_models.py
│   ├── services/           # Data pipeline utilities
│   │   ├── crawler.py
│   │   ├── embedding.py
│   │   ├── text_processor.py
│   │   └── vector_store.py
│   └── main.py             # FastAPI application entry point
├── tests/
│   ├── conftest.py
│   ├── test_routes.py
│   ├── test_agent_service.py
│   ├── test_retriever_service.py
│   ├── test_crawler.py
│   ├── test_embedding.py
│   ├── test_text_processor.py
│   └── retrieval/          # Integration retrieval verification
├── .env.example
└── pyproject.toml
```

---

## ⚡ Quickstart

### 1. Prerequisites

- Python 3.13
- [`uv`](https://docs.astral.sh/uv/) (fast Python package manager)
- Accounts on [Qdrant Cloud](https://qdrant.tech/) and [OpenAI](https://platform.openai.com/)

### 2. Install dependencies

```bash
cd backend
uv pip sync
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and fill in your API keys:
#   COHERE_API_KEY=...
#   QDRANT_API_KEY=...
#   QDRANT_URL=...
#   OPENAI_API_KEY=...
```

### 4. Start the server

```bash
uvicorn app.main:app --reload
```

The API is now available at `http://127.0.0.1:8000`.

---

## 📡 API Endpoints

| Method | Path               | Description                               |
|--------|--------------------|-------------------------------------------|
| POST   | `/ask`             | Send a question to the RAG agent          |
| GET    | `/health`          | Service health check (`{"status":"ok"}`)  |
| POST   | `/retrieval-test`  | Directly test Qdrant retrieval            |
| GET    | `/heartbeat`       | Liveness probe                            |
| GET    | `/docs`            | Interactive OpenAPI documentation         |

### Example — `/ask`

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query_text": "What are ROS 2 nodes?"}'
```

```json
{
  "answer_text": "ROS 2 nodes are the fundamental computing units...",
  "retrieved_sources": ["https://your-site.com/ai-book/1-2-ros2-core-concepts"]
}
```

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v
```

> **Note:** Unit tests use mocks — no API keys or running Qdrant instance required.

---

## 🔧 Configuration Reference

| Variable          | Required | Default            | Description                       |
|-------------------|----------|--------------------|-----------------------------------|
| `COHERE_API_KEY`  | ✅       | —                  | Cohere API key (embeddings)       |
| `QDRANT_API_KEY`  | ✅       | —                  | Qdrant Cloud API key              |
| `QDRANT_URL`      | ✅       | —                  | Qdrant cluster URL                |
| `OPENAI_API_KEY`  | ✅       | —                  | OpenAI API key (GPT-4o-mini)      |
| `COLLECTION_NAME` | ❌       | `ragbot_embedding` | Qdrant collection name            |

---

## 🌐 CORS

CORS is configured to allow all origins (`*`) for the hackathon demo.  
In production, update `allow_origins` in `app/main.py` to your frontend URL.
