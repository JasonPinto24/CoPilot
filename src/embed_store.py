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
# ── Create Qdrant collection ──────────────────────────────────────────────────
def create_collection():
    """
    Creates the enterprise_docs collection in Qdrant.
    Skips if collection already exists.
    Vector size: 384 (bge-small output)
    Distance: Cosine (standard for text embeddings)
    """
    client = get_qdrant_client()

    # Check if collection already exists
    existing = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME in existing:
        print(f"Collection '{COLLECTION_NAME}' already exists — skipping creation")
        return

    # Create fresh collection
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE,
        )
    )
    print(f"Collection '{COLLECTION_NAME}' created successfully")


# ── Upsert chunks to Qdrant ───────────────────────────────────────────────────
def upsert_chunks(chunks: list) -> int:
    """
    Embeds all chunks and uploads them to Qdrant in batches of 100.
    Each chunk becomes one point with vector + payload.
    Returns total number of chunks uploaded.
    """
    client = get_qdrant_client()
    batch_size = 100
    total = 0

    print(f"Uploading {len(chunks)} chunks to Qdrant in batches of {batch_size}...")

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]

        # Extract texts for embedding
        texts = [chunk.page_content for chunk in batch]

        # Embed this batch
        vectors = embed(texts)

        # Build Qdrant points
        points = []
        for j, (chunk, vector) in enumerate(zip(batch, vectors)):
            point = PointStruct(
                id=i + j,
                vector=vector,
                payload={
                    "text":        chunk.page_content,
                    "source":      chunk.metadata.get("source", "unknown"),
                    "page":        chunk.metadata.get("page", 1),
                    "type":        chunk.metadata.get("type", "doc"),
                    "dataset":     chunk.metadata.get("dataset", "unknown"),
                    "chunk_index": chunk.metadata.get("chunk_index", 0),
                }
            )
            points.append(point)

        # Upload batch to Qdrant
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )

        total += len(batch)
        print(f"  Uploaded {total}/{len(chunks)} chunks")

    print(f"Done. {total} chunks stored in Qdrant collection '{COLLECTION_NAME}'")
    return total