from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.

    Required variables:
    - COHERE_API_KEY: API key for Cohere embedding service.
    - QDRANT_API_KEY: API key for Qdrant vector database.
    - QDRANT_URL: URL of the Qdrant instance.
    - OPENAI_API_KEY: API key for OpenAI LLM service.

    Optional variables:
    - COLLECTION_NAME: Qdrant collection name (default: 'ragbot_embedding').
    """

    model_config = ConfigDict(env_file=".env")

    COHERE_API_KEY: str
    QDRANT_API_KEY: str
    QDRANT_URL: str
    OPENAI_API_KEY: str
    COLLECTION_NAME: str = "ragbot_embedding"


settings = Settings()
