# Research: RAG Data Pipeline

This document outlines the technology choices and best practices for the RAG data pipeline.

## Decisions

- **Language**: Python 3.11+
  - **Rationale**: The Python ecosystem has excellent libraries for web scraping, data processing, and machine learning, making it the ideal choice for this pipeline. `uv` will be used for project and dependency management.
- **Web Crawling**: `requests` and `BeautifulSoup`
  - **Rationale**: `requests` is a simple and robust HTTP library for fetching web pages. `BeautifulSoup` is a powerful and easy-to-use library for parsing HTML and extracting content.
- **Text Cleaning**: `markdownify`
  - **Rationale**: To preserve some of the document structure, we will convert HTML to Markdown before converting to plain text. `markdownify` is a well-maintained library for this purpose.
- **Text Chunking**: `tiktoken`
  - **Rationale**: `tiktoken` is the official tokenizer from OpenAI and is also used by Cohere. Using it ensures that our chunking strategy is aligned with the model's tokenization, which is crucial for effective embeddings.
- **Embeddings**: Cohere's `embed-english-v3.0`
  - **Rationale**: This is a requirement from the feature specification. Cohere's models are state-of-the-art for semantic search and retrieval.
- **Vector Store**: Qdrant Cloud
  - **Rationale**: This is a requirement from the feature specification. Qdrant is a high-performance vector database that is well-suited for RAG applications.

## Alternatives Considered

- **Scrapy**: A more powerful and feature-rich crawling framework.
  - **Reason for rejection**: For this project, `requests` and `BeautifulSoup` are sufficient and simpler to use.
- **LangChain/LlamaIndex**: High-level frameworks for building LLM applications.
  - **Reason for rejection**: While these frameworks are powerful, building the pipeline from scratch provides more control and a better understanding of the underlying components. It also avoids adding a large dependency for a relatively straightforward task.
