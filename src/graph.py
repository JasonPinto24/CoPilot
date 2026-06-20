from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes.router import router_node, route_decision
from src.nodes.doc_search import doc_search_node
from src.nodes.ticket_lookup import ticket_lookup_node
from src.nodes.summarizer import summarizer_node
from src.nodes.generate import generate_node
from src.nodes.guardrail import guardrail_node, check_confidence
from src.nodes.escalate import escalate_node


# ── Build the graph ───────────────────────────────────────────────────────────
def build_graph():
    """
    Wires all 7 nodes into a LangGraph StateGraph.
    Returns compiled app ready to invoke.
    """
    graph = StateGraph(AgentState)

    # ── Add all nodes ─────────────────────────────────────────────────────────
    graph.add_node("router",        router_node)
    graph.add_node("doc_search",    doc_search_node)
    graph.add_node("ticket_lookup", ticket_lookup_node)
    graph.add_node("summarizer",    summarizer_node)
    graph.add_node("generate",      generate_node)
    graph.add_node("guardrail",     guardrail_node)
    graph.add_node("escalate",      escalate_node)

    # ── Entry point ───────────────────────────────────────────────────────────
    graph.set_entry_point("router")

    # ── Conditional edges from router ─────────────────────────────────────────
    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "doc_search":    "doc_search",
            "ticket_lookup": "ticket_lookup",
            "summarizer":    "summarizer",
            "escalate":      "escalate",
        }
    )

    # ── Normal edges — all tool nodes feed into generate ──────────────────────
    graph.add_edge("doc_search",    "generate")
    graph.add_edge("ticket_lookup", "generate")
    graph.add_edge("summarizer",    "generate")

    # ── Generate feeds guardrail ──────────────────────────────────────────────
    graph.add_edge("generate", "guardrail")

    # ── Conditional edges from guardrail ──────────────────────────────────────
    graph.add_conditional_edges(
        "guardrail",
        check_confidence,
        {
            "ok":       END,
            "escalate": "escalate",
        }
    )

    # ── Escalate always goes to END ───────────────────────────────────────────
    graph.add_edge("escalate", END)

    # ── Compile and return ────────────────────────────────────────────────────
    return graph.compile()


# ── Create the app ────────────────────────────────────────────────────────────
app = build_graph()