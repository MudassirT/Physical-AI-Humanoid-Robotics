from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import get_logger
from app.routes import analytics, chat

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Log a startup message so operators know the server is ready."""
    logger.info("RAG Agent API starting up — version 0.1.0")
    logger.info("Endpoints: POST /ask  |  GET /health  |  POST /retrieval-test")
    yield
    # Shutdown logic (if any) goes here


app = FastAPI(
    title="RAG Agent API",
    description=(
        "API for interacting with the Physical AI & Humanoid Robotics RAG Agent. "
        "Answers are grounded exclusively in the book content stored in Qdrant."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS — allow the Docusaurus frontend (and local dev) to call the API.
# In production, replace ["*"] with the exact frontend origin(s).
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # e.g. ["https://your-docusaurus-site.example.com"]
    allow_credentials=False,       # Must be False when allow_origins=["*"]
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Accept"],
)

app.include_router(chat.router)
app.include_router(analytics.router)


@app.get("/heartbeat", summary="Liveness probe")
async def heartbeat():
    """
    Returns a simple liveness signal.

    This is separate from /health so that load-balancers can distinguish
    'server is alive' from 'service is fully operational'.
    """
    return {"status": "alive"}


# ---------------------------------------------------------------------------
# Note: The RAG data-pipeline logic (crawling, embedding, vector storage)
# lives in backend/app/services/ and should be run as a one-off command,
# NOT as part of this API server.  Example:
#   cd backend && uv run python -m app.services.vector_store
# ---------------------------------------------------------------------------
