from pydantic import BaseModel
from typing import List, Optional

class Document(BaseModel):
    text: str
    source_url: str
    title: str
    chunk_index: int

class Embedding(BaseModel):
    vector: List[float]
    document: Document
