import os

from qdrant_client import QdrantClient

_qdrant_client = None


def get_qdrant_client() -> QdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        qdrant_url = os.getenv("QDRANT_HOST", None)
        qdrant_api_key = os.getenv("QDRANT_API_KEY", None)
        if qdrant_url is None or qdrant_api_key is None:
            raise ValueError("QDRANT_HOST and QDRANT_API_KEY environment variables must be set")
        _qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )
    return _qdrant_client


# Example usage:
# qdrant_client = get_qdrant_client()
# print(qdrant_client.get_collections())
