import cohere
from src.config import COHERE_API_KEY, TOP_N

# ── Cohere client ─────────────────────────────────────────────────────────────
_cohere = cohere.Client(COHERE_API_KEY)


# ── Rerank hits ───────────────────────────────────────────────────────────────
def rerank(query: str, hits: list, top_n: int = None) -> list:
    """
    Takes top-12 hits from Qdrant and reranks them using Cohere.
    Cohere reads query and each chunk together for more accurate scoring.
    Returns top_n hits sorted by rerank score descending.
    """
    top_n = top_n or TOP_N

    if not hits:
        return hits

    # Extract texts for Cohere
    documents = [hit["text"] for hit in hits]

    # Call Cohere rerank API
    response = _cohere.rerank(
        query=query,
        documents=documents,
        top_n=top_n,
        model="rerank-english-v3.0",
    )

    # Build reranked hits list
    reranked = []
    for item in response.results:
        original_hit = hits[item.index]
        reranked.append({
            **original_hit,
            "rerank_score": item.relevance_score,
        })

    print(f"Reranked {len(hits)} → top {len(reranked)} hits")
    print(f"Best rerank score: {reranked[0]['rerank_score']:.3f}")

    return reranked