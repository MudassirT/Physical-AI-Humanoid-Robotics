# Data Model: RAG Data Pipeline

This document defines the data structures used in the RAG data pipeline.

## Entities

### Content Chunk

Represents a piece of text extracted from the source documents.

-   **`text`**: `string`
    -   The actual text content of the chunk (300-500 tokens).
-   **`source_url`**: `string`
    -   The URL of the page from which the text was extracted.
-   **`title`**: `string`
    -   The title of the source page.
-   **`chunk_index`**: `integer`
    -   The index of the chunk within the page.

### Embedding Vector

Represents the numerical embedding of a `Content Chunk`.

-   **`vector`**: `array[float]`
    -   The high-dimensional vector representing the semantic meaning of the text. The dimension is determined by the Cohere model (1024 for `embed-english-v3.0`).
-   **`document`**: `Content Chunk`
    -   The `Content Chunk` that the vector represents. This is stored as the payload in Qdrant.

## Relationships

-   A `Content Chunk` has one and only one `Embedding Vector`.
-   An `Embedding Vector` corresponds to exactly one `Content Chunk`.

## State Transitions

-   A `Content Chunk` is created during the text processing phase.
-   An `Embedding Vector` is created during the embedding generation phase.
-   Both are stored in the Qdrant vector store and are considered immutable after creation. If the source content changes, the pipeline is re-run to generate new chunks and embeddings.
