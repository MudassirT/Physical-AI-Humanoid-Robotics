from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ContentChunk(BaseModel):
    """
    Represents a piece of content retrieved from the Qdrant vector database.
    """
    chunk_id: str = Field(..., description="The unique identifier for the content chunk.")
    source_url: str = Field(..., description="The URL or path of the original document this chunk came from.")
    original_text: str = Field(..., description="The raw text content of the chunk.")
    score: float = Field(..., description="The similarity score returned by the vector search.")
    module: Optional[str] = Field(default=None, description="The curriculum module identifier (e.g., 'module1', 'module6').")
    chapter: Optional[str] = Field(default=None, description="The chapter identifier or filename.")
    content_hash: Optional[str] = Field(default=None, description="SHA-256 hash of the content chunk.")


class ChatQuery(BaseModel):
    """
    Represents an incoming user question sent to the /ask endpoint.
    """
    query_text: str = Field(..., min_length=1, description="The natural language text of the user's question.")
    stream: Optional[bool] = Field(default=False, description="Whether to stream the response as Server-Sent Events.")
    module_filter: Optional[str] = Field(default=None, description="Optional module filter for targeted retrieval (e.g., 'module1', 'module6').")


class ChatResponse(BaseModel):
    """
    Represents the agent's response sent back to the user from the /ask endpoint.
    """
    answer_text: str = Field(..., description="The agent's synthesized answer, grounded in the book content.")
    retrieved_sources: List[str] = Field(default_factory=list, description="A list of source URLs/identifiers for the content chunks used to generate the answer.")


class HealthStatus(BaseModel):
    """
    Represents the response from the /health endpoint.
    """
    status: str = Field(..., description="The operational status of the service (e.g., 'ok').")


class RetrievalTestQuery(BaseModel):
    """
    Represents the request for the /retrieval-test endpoint.
    """
    query_text: str = Field(..., min_length=1, description="The query to test against the retriever.")
    module_filter: Optional[str] = Field(default=None, description="Optional module filter for retrieval test.")


class RetrievalTestResponse(BaseModel):
    """
    Represents the response from the /retrieval-test endpoint. It returns the raw retrieved chunks.
    """
    chunks: List[ContentChunk] = Field(default_factory=list, description="A list of the raw content chunks retrieved from Qdrant.")


class AnalyticsEvent(BaseModel):
    """
    Represents a client-side telemetry event sent to the /analytics endpoint.
    """
    event_type: str = Field(..., description="Event type identifier (e.g. 'page_view', 'query', 'quiz_score', 'progress_update').")
    timestamp: Optional[str] = Field(default=None, description="ISO-8601 timestamp string; populated by server if omitted.")
    session_id: Optional[str] = Field(default=None, max_length=128, description="Anonymous session identifier.")
    module_id: Optional[str] = Field(default=None, max_length=64, description="Optional curriculum module identifier.")
    chapter_id: Optional[str] = Field(default=None, max_length=128, description="Optional chapter identifier.")
    data: Dict[str, Any] = Field(default_factory=dict, description="Custom event metadata and payload dictionary.")


class AnalyticsResponse(BaseModel):
    """
    Represents the acknowledgement response from POST /analytics.
    """
    status: str = Field(default="recorded", description="Operation status.")
    event_id: str = Field(..., description="Unique ID assigned to the recorded event.")


class AnalyticsSummary(BaseModel):
    """
    Represents aggregated metrics returned by GET /analytics.
    """
    total_events: int = Field(default=0, description="Total number of events recorded.")
    event_counts: Dict[str, int] = Field(default_factory=dict, description="Counts grouped by event_type.")
    total_queries: int = Field(default=0, description="Total count of query events.")
    popular_modules: Dict[str, int] = Field(default_factory=dict, description="Event counts grouped by module_id.")
    average_quiz_scores: Dict[str, float] = Field(default_factory=dict, description="Average quiz scores grouped by target module/chapter.")
