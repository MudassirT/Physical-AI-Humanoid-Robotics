from typing import List, Optional

from pydantic import BaseModel

from app.schemas.chat_models import ContentChunk


class Document(BaseModel):
    text: str
    source_url: str
    title: str
    chunk_index: int
    module: Optional[str] = None
    chapter: Optional[str] = None
    content_hash: Optional[str] = None


class Embedding(BaseModel):
    vector: List[float]
    document: Document


__all__ = ["ContentChunk", "Document", "Embedding"]
