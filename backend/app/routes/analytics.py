"""
FastAPI routes for Telemetry & Analytics.

Endpoints:
- POST /analytics — Ingest telemetry events (page_view, query, quiz_score, progress_update).
- GET  /analytics — Summarise recorded telemetry events with aggregate metrics.
"""

import json
import os
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.core.logging import get_logger
from app.schemas.chat_models import (
    AnalyticsEvent,
    AnalyticsResponse,
    AnalyticsSummary,
)

router = APIRouter(prefix="/analytics", tags=["Telemetry & Analytics"])
logger = get_logger(__name__)

# Backend logs directory and JSONL file path
DEFAULT_LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
ANALYTICS_LOG_PATH = Path(os.getenv("ANALYTICS_LOG_PATH", str(DEFAULT_LOG_DIR / "analytics.jsonl")))

_file_lock = threading.Lock()


def get_analytics_file_path() -> Path:
    """Returns the current path for the analytics log file."""
    return Path(os.getenv("ANALYTICS_LOG_PATH", str(DEFAULT_LOG_DIR / "analytics.jsonl")))


# ---------------------------------------------------------------------------
# POST /analytics
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=AnalyticsResponse,
    summary="Record a client telemetry event",
    description=(
        "Accepts a telemetry event (e.g. page_view, query, quiz_score, progress_update), "
        "validates its payload, and appends the single-line JSON record to the analytics log."
    ),
)
async def record_event(event: AnalyticsEvent) -> AnalyticsResponse:
    """
    Record an incoming client telemetry event.

    - **event_type**: Event category ('page_view', 'query', 'quiz_score', 'progress_update', etc.).
    - **timestamp**: ISO-8601 string (auto-generated if omitted).
    - **session_id**: Optional anonymous session identifier.
    - **module_id**: Optional module identifier.
    - **chapter_id**: Optional chapter identifier.
    - **data**: Custom metadata key-value dictionary.
    """
    logger.info(f"POST /analytics — event_type: '{event.event_type}', module: '{event.module_id}'")

    event_id = str(uuid.uuid4())
    if not event.timestamp:
        event.timestamp = datetime.now(timezone.utc).isoformat()

    record = event.model_dump()
    record["event_id"] = event_id

    file_path = get_analytics_file_path()
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(record) + "\n"
        with _file_lock:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(line)

        return AnalyticsResponse(status="recorded", event_id=event_id)
    except Exception as exc:
        logger.error(f"POST /analytics failed to record event — {exc}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to record analytics event.",
        )


# ---------------------------------------------------------------------------
# GET /analytics
# ---------------------------------------------------------------------------

@router.get(
    "",
    response_model=AnalyticsSummary,
    summary="Get aggregated analytics metrics",
    description=(
        "Reads the analytics JSONL log and computes aggregate metrics including "
        "total events, event counts by type, total queries, popular modules, and "
        "average quiz scores."
    ),
)
async def get_analytics_summary() -> AnalyticsSummary:
    """
    Retrieve aggregated analytics summary.
    """
    file_path = get_analytics_file_path()

    if not file_path.exists():
        logger.info("GET /analytics — log file does not exist yet; returning empty summary.")
        return AnalyticsSummary()

    total_events = 0
    event_counts: dict[str, int] = {}
    total_queries = 0
    popular_modules: dict[str, int] = {}
    quiz_scores_map: dict[str, list[float]] = {}

    try:
        with _file_lock:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        logger.warning(f"Corrupted line skipped in analytics log: {line[:50]}")
                        continue

                    total_events += 1
                    etype = record.get("event_type", "unknown")
                    event_counts[etype] = event_counts.get(etype, 0) + 1

                    if etype == "query":
                        total_queries += 1

                    mid = record.get("module_id")
                    if mid:
                        popular_modules[mid] = popular_modules.get(mid, 0) + 1

                    if etype == "quiz_score":
                        target = record.get("chapter_id") or mid or "general"
                        data = record.get("data") or {}
                        score = data.get("score")
                        if isinstance(score, (int, float)):
                            quiz_scores_map.setdefault(target, []).append(float(score))

        average_quiz_scores: dict[str, float] = {
            target: round(sum(scores) / len(scores), 2)
            for target, scores in quiz_scores_map.items()
            if scores
        }

        return AnalyticsSummary(
            total_events=total_events,
            event_counts=event_counts,
            total_queries=total_queries,
            popular_modules=popular_modules,
            average_quiz_scores=average_quiz_scores,
        )
    except Exception as exc:
        logger.error(f"GET /analytics failed to compute summary — {exc}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate analytics summary.",
        )
