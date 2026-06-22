from qdrant_client.models import Filter, FieldCondition, MatchValue
from src.state import AgentState
from src.embed_store import embed, get_qdrant_client
from src.config import COLLECTION_NAME, TOP_K, ESCALATE_BELOW

# ── Ticket lookup node ────────────────────────────────────────────────────────
def ticket_lookup_node(state: AgentState) -> AgentState:
    """
    Searches ONLY support tickets in Qdrant using metadata filter.
    Used for duplicate ticket detection.
    Filters by type='ticket' so SOPs are never searched here.
    """
    query = state["query"]

    # Add query prefix for bge-small
    query_with_prefix = "Represent this query for retrieval: " + query

    # Embed the query
    query_vector = embed([query_with_prefix])[0]

    # Connect to Qdrant
    client = get_qdrant_client()

    # Search ONLY tickets using metadata filter
    results = client.query_points(
    collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=TOP_K,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="type",
                    match=MatchValue(value="ticket")
                )
            ]
        ),
        with_payload=True,
    ).points
    # Format hits
    hits = []
    for result in results:
        hits.append({
            "text":         result.payload.get("text", ""),
            "source":       result.payload.get("source", "unknown"),
            "page":         result.payload.get("page", 1),
            "type":         result.payload.get("type", "ticket"),
            "dataset":      result.payload.get("dataset", "option_c"),
            "rerank_score": result.score,
        })

    # Build tool output from ticket hits
    if hits:
        tool_output = "\n\n".join([
            f"Ticket {h['source']}:\n{h['text'][:300]}"
            for h in hits[:4]
        ])
    else:
        tool_output = "No similar tickets found in the knowledge base."

    confidence = max(
        (h["rerank_score"] for h in hits),
        default=0.0
    )

    print(f"ticket_lookup found {len(hits)} tickets, confidence: {confidence:.2f}")

    return {
        **state,
        "hits":        hits,
        "tool_output": tool_output,
        "confidence":  confidence,
    }