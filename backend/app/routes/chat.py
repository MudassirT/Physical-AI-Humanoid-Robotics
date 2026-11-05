"""
FastAPI routes for the RAG Agent chat API.

Endpoints:
- POST /ask              — Send a question to the RAG agent.
- GET  /health           — Service health check.
- POST /retrieval-test   — Directly test the Qdrant retrieval pipeline.
"""

from fastapi import APIRouter, HTTPException

from app.core.logging import get_logger

from ..agent.agent_service import AgentService
from ..retriever.retriever_service import RetrieverService
from ..schemas.chat_models import (
    ChatQuery,
    ChatResponse,
    HealthStatus,
    RetrievalTestQuery,
    RetrievalTestResponse,
)

router = APIRouter(tags=["RAG Chat"])
logger = get_logger(__name__)

# Singleton instances — initialised once at import time.
# If your environment variables are missing the server will fail on startup
# with a clear validation error rather than at request time.
agent_service = AgentService()
retriever_service = RetrieverService()


# ---------------------------------------------------------------------------
# POST /ask
# ---------------------------------------------------------------------------

@router.post(
    "/ask",
    response_model=ChatResponse,
    summary="Ask the RAG Agent a question",
    description=(
        "Sends a user query to the RAG agent. The agent retrieves relevant "
        "content from the Qdrant vector database and synthesises a grounded answer."
    ),
)
async def ask(query: ChatQuery) -> ChatResponse:
    """
    Ask the RAG agent a question.

    - **query_text**: The user's natural-language question (non-empty string).

    Returns a JSON body with:
    - **answer_text**: The agent's synthesised, grounded answer.
    - **retrieved_sources**: List of source URLs used to generate the answer.
    """
    logger.info(f"POST /ask — query: '{query.query_text}'")
    try:
        response = agent_service.ask_agent(query.query_text)
        logger.info(
            f"POST /ask — response: '{response.answer_text[:100]}...' | "
            f"sources: {response.retrieved_sources}"
        )
        return response
    except Exception as exc:
        logger.error(f"POST /ask — unhandled error: {exc}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your request. Please try again.",
        )


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

@router.get(
    "/health",
    response_model=HealthStatus,
    summary="Service health check",
    description="Returns the operational status of the RAG Agent API.",
)
async def health() -> HealthStatus:
    """
    Health check endpoint.

    Returns ``{"status": "ok"}`` when the service is running normally.
    """
    logger.info("GET /health — service is healthy.")
    return HealthStatus(status="ok")


# ---------------------------------------------------------------------------
# POST /retrieval-test
# ---------------------------------------------------------------------------

@router.post(
    "/retrieval-test",
    response_model=RetrievalTestResponse,
    summary="Directly test the Qdrant retrieval pipeline",
    description=(
        "Bypasses the agent and calls the retriever directly. "
        "Useful for debugging retrieval quality and Qdrant connectivity."
    ),
)
async def retrieval_test(query: RetrievalTestQuery) -> RetrievalTestResponse:
    """
    Test the retrieval pipeline directly.

    - **query_text**: The query to run against the vector database.

    Returns the raw list of ``ContentChunk`` objects retrieved from Qdrant.
    """
    logger.info(f"POST /retrieval-test — query: '{query.query_text}'")
    try:
        chunks = retriever_service.retrieve_chunks(query_text=query.query_text, top_k=5)
        logger.info(f"POST /retrieval-test — retrieved {len(chunks)} chunks.")
        return RetrievalTestResponse(chunks=chunks)
    except Exception as exc:
        logger.error(f"POST /retrieval-test — unhandled error: {exc}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred during the retrieval test.",
        )
