from typing import List

from pydantic import BaseModel


class Document(BaseModel):
    text: str
    source_url: str
    title: str
    chunk_index: int

class Embedding(BaseModel):
    vector: List[float]
    document: Document
