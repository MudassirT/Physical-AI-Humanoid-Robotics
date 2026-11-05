from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.

    Required variables:
    - COHERE_API_KEY: API key for Cohere embedding service.
    - QDRANT_API_KEY: API key for Qdrant vector database.
    - QDRANT_URL: URL of the Qdrant instance.
    - GEMINI_API_KEY: API key for Google Gemini LLM service.

    Optional variables:
    - COLLECTION_NAME: Qdrant collection name (default: 'ragbot_embedding').
    """

    model_config = ConfigDict(env_file=".env", extra="ignore")

    COHERE_API_KEY: str
    QDRANT_API_KEY: str
    QDRANT_URL: str
    GEMINI_API_KEY: str
    COLLECTION_NAME: str = "ragbot_embedding"


settings = Settings()
