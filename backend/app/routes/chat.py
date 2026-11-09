"""
FastAPI routes for the RAG Agent chat API.

Endpoints:
- POST /ask              — Send a question to the RAG agent (supports unary & SSE streaming).
- GET  /health           — Service health check.
- POST /retrieval-test   — Directly test the Qdrant retrieval pipeline.
"""

import json
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

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
agent_service = AgentService()
retriever_service = RetrieverService()


# ---------------------------------------------------------------------------
# POST /ask
# ---------------------------------------------------------------------------

@router.post(
    "/ask",
    response_model=None,
    summary="Ask the RAG Agent a question",
    description=(
        "Sends a user query to the RAG agent. The agent retrieves relevant "
        "content from the Qdrant vector database and synthesises a grounded answer. "
        "Supports real-time token streaming via Server-Sent Events (SSE) when "
        "`stream=true` or `Accept: text/event-stream` is requested."
    ),
)
async def ask(query: ChatQuery, request: Request) -> Any:
    """
    Ask the RAG agent a question.

    - **query_text**: The user's natural-language question (non-empty string).
    - **stream**: If True, returns an SSE stream of tokens and sources.
    - **module_filter**: Optional module identifier to scope retrieval (e.g., 'module1').

    Returns either:
    - Unary `ChatResponse` JSON: { "answer_text": "...", "retrieved_sources": [...] }
    - Server-Sent Events stream (`text/event-stream`)
    """
    logger.info(
        f"POST /ask — query: '{query.query_text}', stream={query.stream}, "
        f"module_filter={query.module_filter}"
    )

    accept_header = request.headers.get("accept", "")
    wants_stream = query.stream is True or "text/event-stream" in accept_header

    if wants_stream:
        def sse_event_generator():
            try:
                for event_type, data in agent_service.ask_agent_stream(
                    user_query=query.query_text,
                    module_filter=query.module_filter,
                ):
                    payload = json.dumps(data)
                    yield f"event: {event_type}\ndata: {payload}\n\n"
            except Exception as exc:
                logger.error(f"POST /ask stream exception: {exc}", exc_info=True)
                err_payload = json.dumps({"error": str(exc)})
                yield f"event: error\ndata: {err_payload}\n\n"

        return StreamingResponse(
            sse_event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    try:
        if query.module_filter:
            response: ChatResponse = agent_service.ask_agent(
                query.query_text,
                module_filter=query.module_filter,
            )
        else:
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
    - **module_filter**: Optional module filter.

    Returns the raw list of ``ContentChunk`` objects retrieved from Qdrant.
    """
    logger.info(f"POST /retrieval-test — query: '{query.query_text}', module: {query.module_filter}")
    try:
        if query.module_filter:
            chunks = retriever_service.retrieve_chunks(
                query_text=query.query_text,
                top_k=5,
                module_filter=query.module_filter,
            )
        else:
            chunks = retriever_service.retrieve_chunks(
                query_text=query.query_text,
                top_k=5,
            )
        logger.info(f"POST /retrieval-test — retrieved {len(chunks)} chunks.")
        return RetrievalTestResponse(chunks=chunks)
    except Exception as exc:
        logger.error(f"POST /retrieval-test — unhandled error: {exc}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred during the retrieval test.",
        )
