from typing import List

from qdrant_client import QdrantClient, models

from app.core.config import settings
from app.core.logging import get_logger
from app.models.models import Document

logger = get_logger(__name__)

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            check_compatibility=False,
        )
        self.collection_name = settings.COLLECTION_NAME

    def create_collection(self):
        try:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
            )
            logger.info(f"Collection '{self.collection_name}' created successfully.")
        except Exception as e:
            logger.error(f"Error creating collection: {e}")

    def save_chunks_to_qdrant(self, embeddings: List[List[float]], documents: List[Document]):
        try:
            points = [
                models.PointStruct(
                    id=i,
                    vector=embedding,
                    payload=doc.dict()
                )
                for i, (embedding, doc) in enumerate(zip(embeddings, documents))
            ]
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
                wait=True
            )
            logger.info(f"Upserted {len(points)} points to collection '{self.collection_name}'.")
        except Exception as e:
            logger.error(f"Error upserting points: {e}")
