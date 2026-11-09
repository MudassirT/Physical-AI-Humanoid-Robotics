"""
Hermetic test doubles for retrieval verification tests.

Provides deterministic in-memory vector embedding and search capabilities
without requiring live network connectivity or external Cohere/Qdrant credentials.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any

import numpy as np

STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but",
    "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from",
    "further", "had", "has", "have", "having", "he", "her", "here", "hers", "him", "his", "how",
    "i", "if", "in", "into", "is", "it", "its", "just", "me", "more", "most", "my", "no", "nor",
    "not", "now", "of", "off", "on", "once", "only", "or", "other", "our", "out", "over", "own",
    "same", "she", "should", "so", "some", "such", "than", "that", "the", "their", "them", "then",
    "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why",
    "with", "would", "you", "your"
}


def deterministic_embed(text: str, dim: int = 1024) -> list[float]:
    """Generates a deterministic 1024-dimensional normalized vector from text."""
    v = np.zeros(dim, dtype=np.float32)
    words = re.findall(r"\b[a-zA-Z0-9_\-]+\b", text.lower())
    for w in words:
        if w in STOP_WORDS or len(w) < 2:
            continue
        idx = int(hashlib.sha256(w.encode("utf-8")).hexdigest(), 16) % dim
        v[idx] += 1.0
    norm = float(np.linalg.norm(v))
    if norm > 0:
        v = v / norm
    else:
        v.fill(1.0 / np.sqrt(dim))
    return v.tolist()


class MockEmbeddingGenerator:
    """Hermetic double for app.services.embedding.EmbeddingGenerator."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.embedding_dimension = 1024

    def generate_embeddings(
        self,
        texts: list[str],
        input_type: str = "search_query",
    ) -> list[list[float]]:
        """Return deterministic vectors without network requests."""
        return [deterministic_embed(t, dim=self.embedding_dimension) for t in texts]


class MockScoredPoint:
    """Represents a scored vector search result from Qdrant."""

    def __init__(self, point_id: str, score: float, payload: dict[str, Any]) -> None:
        self.id = point_id
        self.score = score
        self.payload = payload


class MockQueryResult:
    """Result object mimicking Qdrant query_points return value."""

    def __init__(self, points: list[MockScoredPoint]) -> None:
        self.points = points


DEFAULT_CORPUS: list[dict[str, Any]] = [
    {
        "id": "chunk-102",
        "source_url": "ai-book-docs/module1-ros2/1-2-ros2-core-concepts.mdx",
        "title": "Core Concepts & Communication Primitives",
        "text": "ROS 2 core concepts include nodes, topics, services, actions, and the computational graph topology. Nodes are the primary computational units communicating over DDS middleware.",
        "module": "module1",
        "chapter": "1-2-ros2-core-concepts",
    },
    {
        "id": "chunk-103",
        "source_url": "ai-book-docs/module1-ros2/1-3-ros2-workspace.mdx",
        "title": "ROS 2 Workspace Configuration",
        "text": "Creating a ROS 2 workspace involves configuring dev_ws/src, running colcon build, underlay sourcing, and workspace package management.",
        "module": "module1",
        "chapter": "1-3-ros2-workspace",
    },
    {
        "id": "chunk-201",
        "source_url": "ai-book-docs/module2-digital-twin/2-1-introduction-to-digital-twins.mdx",
        "title": "Introduction to Digital Twins",
        "text": "A digital twin is a high-fidelity virtual representation and simulation of a physical robotics system operating synchronously in Gazebo and Isaac Sim.",
        "module": "module2",
        "chapter": "2-1-introduction-to-digital-twins",
    },
    {
        "id": "chunk-309",
        "source_url": "ai-book-docs/module3-ai-robot-brain/3-9-multi-sensor-fusion.mdx",
        "title": "Multi-Sensor Fusion & NIS",
        "text": "Multi-sensor fusion combines IMU accelerometer and gyroscope data with visual odometry using an Extended Kalman Filter, verified via Normalized Innovation Squared.",
        "module": "module3",
        "chapter": "3-9-multi-sensor-fusion",
    },
    {
        "id": "chunk-602",
        "source_url": "ai-book-docs/module6-bipedal-locomotion/6-2-zero-moment-point.mdx",
        "title": "Zero-Moment Point (ZMP)",
        "text": "The Zero-Moment Point (ZMP) criterion ensures dynamic stability during bipedal locomotion, specifying the ground contact reference for center-of-pressure trajectory planning.",
        "module": "module6",
        "chapter": "6-2-zero-moment-point",
    },
]


class MockQdrantClient:
    """Hermetic double for qdrant_client.QdrantClient."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.points_store: list[dict[str, Any]] = []
        for doc in DEFAULT_CORPUS:
            item = dict(doc)
            content = f"{item['title']} {item['text']}"
            item["vector"] = np.array(deterministic_embed(content), dtype=np.float32)
            self.points_store.append(item)

    def query_points(
        self,
        collection_name: str,
        query: list[float] | None = None,
        query_filter: Any = None,
        limit: int = 5,
        with_payload: bool = True,
        **kwargs: Any,
    ) -> MockQueryResult:
        """Execute vector search across indexed documents."""
        if query is None:
            return MockQueryResult([])

        qv = np.array(query, dtype=np.float32)
        candidates = self.points_store

        # Apply module filter if present
        if query_filter and hasattr(query_filter, "must"):
            filtered: list[dict[str, Any]] = []
            for item in candidates:
                match = True
                for condition in query_filter.must:
                    key = getattr(condition, "key", None)
                    match_val = getattr(getattr(condition, "match", None), "value", None)
                    if key and match_val is not None:
                        if item.get(key) != match_val:
                            match = False
                            break
                if match:
                    filtered.append(item)
            candidates = filtered

        scored: list[MockScoredPoint] = []
        for item in candidates:
            dv = item["vector"]
            cos_sim = float(np.dot(qv, dv))
            calibrated_score = float(np.clip(cos_sim * 1.35, 0.0, 0.98))
            payload = {
                "source_url": item["source_url"],
                "text": item["text"],
                "title": item["title"],
                "module": item.get("module"),
                "chapter": item.get("chapter"),
            }
            scored.append(MockScoredPoint(item["id"], calibrated_score, payload))

        scored.sort(key=lambda p: p.score, reverse=True)
        return MockQueryResult(scored[:limit])


def get_mock_qdrant_client(*args: Any, **kwargs: Any) -> MockQdrantClient:
    """Factory function returning a hermetic MockQdrantClient."""
    return MockQdrantClient()
