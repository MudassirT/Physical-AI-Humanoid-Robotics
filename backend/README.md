# Physical AI & Humanoid Robotics — RAG Agent Backend

FastAPI backend and autonomous Retrieval-Augmented Generation (RAG) agent powering the **Physical AI & Humanoid Robotics** interactive curriculum.

The service integrates **Google Gemini 2.5 Flash** for tool-calling reasoning, **Cohere `embed-english-v3.0`** for high-fidelity semantic embeddings, and **Qdrant Cloud** for vector similarity search.

---

## 🏗️ Architecture & Component Topology

```
backend/
├── app/
│   ├── agent/              # Google Gemini 2.5 Flash tool-calling agent
│   │   └── agent_service.py
│   ├── core/               # Configuration & Logging
│   │   ├── config.py       # Pydantic Settings (.env management)
│   │   └── logging.py      # Structured JSON/Console Logger
│   ├── models/             # Core domain models (Document, Embedding)
│   ├── retriever/          # Qdrant semantic search & point extraction
│   │   └── retriever_service.py
│   ├── routes/             # REST API endpoints
│   │   └── chat.py         # /ask, /heartbeat, /retrieval-test
│   ├── schemas/            # Pydantic request/response validation
│   │   └── chat_models.py
│   ├── services/           # Data pipeline services
│   │   ├── crawler.py      # MDX documentation crawler
│   │   ├── embedding.py    # Cohere API client with retry & backoff
│   │   ├── text_processor.py # Semantic chunking & overlap
│   │   └── vector_store.py # Qdrant Cloud client & collection manager
│   └── main.py             # FastAPI entry point & CORS configuration
├── tests/                  # Pytest unit & integration suite
├── ingest_docs.py          # Vector database ingestion script
├── Dockerfile              # Multi-stage production container
├── pyproject.toml          # Python package & dependency specifications
└── .env.example            # Environment variable template
```

---

## ⚡ Quickstart

### 1. Prerequisites
- Python 3.13+
- [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip`
- Accounts on [Qdrant Cloud](https://qdrant.tech/), [Cohere](https://cohere.com/), and [Google AI Studio](https://aistudio.google.com/)

### 2. Environment Configuration
Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

| Key | Description |
| :--- | :--- |
| `GEMINI_API_KEY` | Google AI Studio API key (powers `gemini-2.5-flash`) |
| `COHERE_API_KEY` | Cohere API key (generates `embed-english-v3.0` embeddings) |
| `QDRANT_URL` | Qdrant Cloud cluster endpoint |
| `QDRANT_API_KEY` | Qdrant Cloud read/write API key |
| `COLLECTION_NAME`| Target Qdrant collection (default: `ragbot_embedding`) |

### 3. Local Installation & Run
```bash
# Setup virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies in editable mode
uv pip install -e .

# Start development server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Interactive API documentation will be available at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📚 Ingestion Pipeline

To chunk and embed the entire 26-chapter curriculum into Qdrant Cloud:

```bash
python ingest_docs.py
```

This reads all `.mdx` files from `../ai-book-docs/`, splits them into semantic chunks with 50-word overlap, generates Cohere embeddings, and upserts them to the `ragbot_embedding` collection.

---

## 🧪 Testing

Run the automated test suite:

```bash
pytest
```

Run code formatting and linting:

```bash
ruff check .
```

---

## 📡 API Reference

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/heartbeat` | `GET` | Health check endpoint returning `{"status": "alive"}` |
| `/ask` | `POST` | Primary RAG agent query endpoint. Accepts query and returns answer with citations |
| `/retrieval-test` | `POST` | Raw semantic search verification against Qdrant without LLM synthesis |
