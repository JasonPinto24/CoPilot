from src.embed_store import embed, get_qdrant_client
from src.config import COLLECTION_NAME, TOP_K

# ── Query prefix for bge-small ────────────────────────────────────────────────
QUERY_PREFIX = "Represent this query for retrieval: "


# ── Retrieve top-k chunks from Qdrant ────────────────────────────────────────
def retrieve(query: str, k: int = None) -> list:
    """
    Searches Qdrant for the most relevant chunks for a given query.
    Adds bge-small query prefix before embedding.
    Returns list of k hits with text, metadata, and similarity score.
    """
    k = k or TOP_K

    # Add prefix so bge-small knows this is a question
    query_with_prefix = QUERY_PREFIX + query

    # Embed the query into a vector
    query_vector = embed([query_with_prefix])[0]

    # Connect to Qdrant
    client = get_qdrant_client()

    # Search for top-k most similar vectors
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=k,
        with_payload=True,
    ).points

    # Format results into hits list
    hits = []
    for result in results:
        hits.append({
            "text":        result.payload.get("text", ""),
            "source":      result.payload.get("source", "unknown"),
            "page":        result.payload.get("page", 1),
            "type":        result.payload.get("type", "doc"),
            "dataset":     result.payload.get("dataset", "unknown"),
            "chunk_index": result.payload.get("chunk_index", 0),
            "score":       result.score,
        })

    print(f"Retrieved {len(hits)} chunks for query: '{query[:50]}'")
    return hits