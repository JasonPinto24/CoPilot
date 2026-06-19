import os
from src.state import AgentState

# ── Gap log file ──────────────────────────────────────────────────────────────
GAP_LOG = "storage/knowledge_gaps.txt"


# ── Escalate node ─────────────────────────────────────────────────────────────
def escalate_node(state: AgentState) -> AgentState:
    """
    Fires when guardrail detects low confidence or insufficient context.
    Returns a structured escalation message.
    Logs the unanswered question to storage/knowledge_gaps.txt.
    """
    query = state["query"]

    # Log the knowledge gap
    os.makedirs("storage", exist_ok=True)
    with open(GAP_LOG, "a", encoding="utf-8") as f:
        f.write(f"{query}\n")

    print(f"Escalating query: {query}")

    escalation_message = (
        "I am not confident enough to answer this question from the "
        "available documents. This query has been forwarded to the "
        "human support queue. A team member will follow up with you shortly.\n\n"
        "If this is urgent please contact the IT helpdesk directly at "
        "helpdesk@northwind.io"
    )

    return {
        **state,
        "answer":    escalation_message,
        "citations": [],
        "escalated": True,
    }