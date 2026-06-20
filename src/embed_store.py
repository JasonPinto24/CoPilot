import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from src.config import (
    QDRANT_URL, QDRANT_API_KEY,
    COLLECTION_NAME, EMBED_MODEL
)

# load embedding model
print("Loading embedding model...")
_embedder = SentenceTransformer(EMBED_MODEL)
print("Embedding model loaded.")

#Qdrant client
def get_qdrant_client() -> QdrantClient:
    """
    Creates and returns a Qdrant cloud client.
    Uses URL and API key from config.
    """
    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )


# ── Embed texts ───────────────────────────────────────────────────────────────
def embed(texts: list) -> list:
    """
    Converts a list of text strings into a list of vectors.
    Each vector is 384 numbers representing the meaning of that text.
    normalize_embeddings=True makes cosine similarity = dot product.
    """
    vectors = _embedder.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return vectors.tolist()