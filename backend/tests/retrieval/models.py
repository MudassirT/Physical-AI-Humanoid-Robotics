from typing import List

from pydantic import BaseModel, Field


class ContentChunk(BaseModel):
    """
    Represents a piece of content retrieved from the Qdrant vector database.
    """
    chunk_id: str = Field(..., description="The unique identifier for the content chunk.")
    source_url: str = Field(..., description="The URL or path of the original document this chunk came from.")
    original_text: str = Field(..., description="The raw text content of the chunk.")
    score: float = Field(..., description="The similarity score returned by the vector search.")

class Query(BaseModel):
    """
    Represents a single test query to be executed against the vector database.
    """
    query_text: str = Field(..., description="The natural language text of the question to be asked.")
    expected_id: str = Field(..., description="An identifier for the expected source document/chunk.")

class RetrievalLog(BaseModel):
    """
    Represents the logged output for a single verification query.
    """
    timestamp: str = Field(..., description="The time the query was executed.")
    query_text: str = Field(..., description="The text of the query that was run.")
    passed: bool = Field(..., description="Whether the retrieval was considered a success or not.")
    retrieved_chunks: List[ContentChunk] = Field(..., description="A list of the content chunks returned by the query.")
