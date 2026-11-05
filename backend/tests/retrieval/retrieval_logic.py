from app.services.embedding import EmbeddingGenerator

from .models import ContentChunk
from .qdrant_connector import get_qdrant_client


def retrieve_chunks(query_text: str, top_k: int = 5) -> list[ContentChunk]:
    """
    Retrieves the most relevant content chunks for a given query.

    Args:
        query_text: The text of the query.
        top_k: The number of top results to retrieve.

    Returns:
        A list of ContentChunk objects.
    """
    qdrant_client = get_qdrant_client()

    # Get the embedding for the query text.
    embedding_generator = EmbeddingGenerator()
    embeddings = embedding_generator.generate_embeddings([query_text], input_type="search_query")
    if not embeddings:
        return []
    query_embedding = embeddings[0]

    # Search for the most similar vectors in Qdrant
    collection_name = "ai-book-chunks"

    search_result = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=top_k,
        with_payload=True,
    )

    retrieved_chunks: list[ContentChunk] = []
    points = getattr(search_result, "points", search_result)
    for hit in points:
        payload = hit.payload
        if payload:
            chunk = ContentChunk(
                chunk_id=str(hit.id),
                source_url=payload.get("source_url", ""),
                original_text=payload.get("text", ""),
                score=hit.score,
            )
            retrieved_chunks.append(chunk)

    return retrieved_chunks

if __name__ == '__main__':
    # Example usage
    test_query = "What are ROS 2 nodes?"
    try:
        chunks = retrieve_chunks(test_query)
        if chunks:
            print(f"Found {len(chunks)} chunks for query: '{test_query}'")
            for i, chunk in enumerate(chunks):
                print(f"  {i+1}. Score: {chunk.score:.4f}, Source: {chunk.source_url}")
                # print(f"     Text: {chunk.original_text[:100]}...")
        else:
            print(f"No chunks found for query: '{test_query}'")
    except Exception as e:
        print(f"An error occurred: {e}")

