import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient


def get_qdrant_client():
    """
    Initializes and returns a Qdrant client using credentials from environment variables.

    Loads environment variables from a .env file if present.

    Returns:
        QdrantClient: An instance of the Qdrant client.
    
    Raises:
        ValueError: If QDRANT_URL or QDRANT_API_KEY environment variables are not set.
    """
    load_dotenv()  # Load environment variables from .env file

    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in environment variables.")

    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
    )
    return client

if __name__ == '__main__':
    # Example usage and connection test
    try:
        qdrant_client = get_qdrant_client()
        print("Successfully connected to Qdrant.")
        # You can add a simple operation here to further test the connection,
        # for example, listing collections.
        collections = qdrant_client.get_collections()
        print("Available collections:", collections)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
