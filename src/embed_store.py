from qdrant_client import QdrantClient
from src.config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME

# ── Temporary stub — Jason replaces this at Day 2 sync ───────────────────────

def get_qdrant_client() -> QdrantClient:
    """Returns a Qdrant cloud client."""
    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )

def embed(texts: list) -> list:
    """
    STUB — Jason fills this in at Day 2 sync.
    Returns fake vectors for development.
    """
    return [[0.1] * 384 for _ in texts]