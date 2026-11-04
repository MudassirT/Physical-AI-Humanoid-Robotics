# Physical AI & Humanoid Robotics — RAG Book System

A full-stack **Retrieval-Augmented Generation (RAG)** system built for the *Physical AI & Humanoid Robotics* book.

Users can browse the interactive Docusaurus book website and ask questions through the chat widget. The FastAPI backend retrieves relevant passages from the book's vector database and generates grounded answers using OpenAI.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│  Docusaurus Frontend (TypeScript + React)           │
│  - Book content (MDX pages)                         │
│  - ChatWidget → POST /ask → FastAPI backend         │
└─────────────────────┬───────────────────────────────┘
                      │ HTTP (fetch)
┌─────────────────────▼───────────────────────────────┐
│  FastAPI Backend (Python 3.13)                      │
│  - POST /ask    → RAG Agent (OpenAI gpt-4o-mini)   │
│  - GET  /health → Service health                    │
│  - POST /retrieval-test → Qdrant direct query       │
└──────────┬──────────────────────────────────────────┘
           │  Cohere embeddings + Qdrant vector search
┌──────────▼──────────────────────────────────────────┐
│  Qdrant Cloud (Vector Database)                     │
│  Collection: ragbot_embedding (1024-dim cosine)     │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

| Tool | Version |
|------|---------|
| Node.js | ≥ 20 |
| Python | 3.13 |
| uv | latest |

### 1. Frontend (Docusaurus)

```bash
npm install
npm start          # Starts dev server at http://localhost:3000
```

### 2. Backend (FastAPI)

```bash
cd backend
cp .env.example .env   # Fill in API keys
uv pip sync
uvicorn app.main:app --reload
# API at http://127.0.0.1:8000
# Docs at http://127.0.0.1:8000/docs
```

### 3. Configure Frontend → Backend connection

By default the chat widget connects to `http://127.0.0.1:8000`.

To point to a different backend, set the environment variable before building:

```bash
REACT_APP_FASTAPI_BASE_URL=https://your-api.example.com npm start
```

---

## 📁 Project Structure

```
.
├── ai-book-docs/          # Docusaurus MDX book content (10+ modules)
├── backend/               # FastAPI + Python RAG backend
│   ├── app/
│   │   ├── agent/         # OpenAI tool-calling agent
│   │   ├── retriever/     # Qdrant semantic retrieval
│   │   ├── routes/        # API endpoints
│   │   ├── schemas/       # Pydantic models
│   │   ├── services/      # Data pipeline (crawler, embedder)
│   │   └── main.py
│   └── tests/
├── src/
│   ├── components/
│   │   └── ChatWidget/    # React chat interface
│   └── pages/
├── specs/                 # Spec-Driven Development specs
└── docusaurus.config.ts
```

---

## 🧪 Running Tests

```bash
# Backend unit tests (mocked — no API keys needed)
cd backend
pytest tests/ -v

# Frontend TypeScript check
npm run typecheck
```

---

## 📚 Specs

| Spec | Description |
|------|-------------|
| `specs/006-rag-data-pipeline/` | Web crawler + embedding pipeline |
| `specs/007-verify-rag-retrieval/` | Retrieval accuracy verification |
| `specs/008-rag-agent-openai-fastapi/` | FastAPI RAG agent backend |
| `specs/009-rag-frontend-docusaurus-integration/` | Chat widget integration |
