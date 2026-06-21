from src.state import AgentState
from src.chains import get_retrieval_chain

# ── Doc search node ───────────────────────────────────────────────────────────
def doc_search_node(state: AgentState) -> AgentState:
    """
    Searches the knowledge base for relevant chunks.
    Calls Jason's get_retrieval_chain() — uses stub until Day 2 sync.
    Stores hits, tool_output, and confidence in AgentState.
    """
    query = state["query"]

    # Call Jason's retrieval chain
    chain = get_retrieval_chain()
    result = chain.invoke({"question": query})

    # Extract answer and source documents
    answer_text = result["answer"]
    source_docs  = result["source_documents"]

    # Format hits list for AgentState
    hits = []
    for doc in source_docs:
        hits.append({
            "text":        doc["page_content"],
            "source":      doc["metadata"].get("source", "unknown"),
            "page":        doc["metadata"].get("page", 1),
            "type":        doc["metadata"].get("type", "doc"),
            "dataset":     doc["metadata"].get("dataset", "unknown"),
            "rerank_score": doc["metadata"].get("rerank_score", 0.5),
        })

    # Confidence is the best rerank score
    confidence = max(
        (h["rerank_score"] for h in hits),
        default=0.0
    )

    print(f"doc_search found {len(hits)} chunks, confidence: {confidence:.2f}")

    return {
        **state,
        "hits":        hits,
        "tool_output": answer_text,
        "confidence":  confidence,
    }