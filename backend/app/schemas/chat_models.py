from pydantic import BaseModel, Field
from typing import List, Optional

class ContentChunk(BaseModel):
    """
    Represents a piece of content retrieved from the Qdrant vector database.
    (Copied from specs/007-verify-rag-retrieval/models.py as it's a common entity)
    """
    chunk_id: str = Field(..., description="The unique identifier for the content chunk.")
    source_url: str = Field(..., description="The URL or path of the original document this chunk came from.")
    original_text: str = Field(..., description="The raw text content of the chunk.")
    score: float = Field(..., description="The similarity score returned by the vector search.")


class ChatQuery(BaseModel):
    """
    Represents an incoming user question sent to the /ask endpoint.
    """
    query_text: str = Field(..., min_length=1, description="The natural language text of the user's question.")

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

class RetrievalTestResponse(BaseModel):
    """
    Represents the response from the /retrieval-test endpoint. It returns the raw retrieved chunks.
    """
    chunks: List[ContentChunk] = Field(default_factory=list, description="A list of the raw content chunks retrieved from Qdrant.")
