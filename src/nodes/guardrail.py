from src.state import AgentState
from src.config import ESCALATE_BELOW

# ── Guardrail node ────────────────────────────────────────────────────────────
def guardrail_node(state: AgentState) -> AgentState:
    """
    Checks if the generated answer is trustworthy.
    Sets escalated=True if confidence is too low or
    model signalled it could not answer.
    """
    confidence = state["confidence"]
    answer     = state["answer"]

    # Check 1: retrieval confidence too low
    if confidence < ESCALATE_BELOW:
        print(f"Guardrail fired: low confidence ({confidence:.2f} < {ESCALATE_BELOW})")
        return {
            **state,
            "escalated": True,
        }

    # Check 2: model signalled insufficient context
    if "INSUFFICIENT_CONTEXT" in answer:
        print("Guardrail fired: model signalled INSUFFICIENT_CONTEXT")
        return {
            **state,
            "escalated": True,
        }

    # Both checks passed
    print(f"Guardrail passed: confidence {confidence:.2f}")
    return {
        **state,
        "escalated": False,
    }


# ── Conditional edge function ─────────────────────────────────────────────────
def check_confidence(state: AgentState) -> str:
    """
    Called by LangGraph conditional edge.
    Returns 'ok' or 'escalate' based on guardrail result.
    """
    if state["escalated"]:
        return "escalate"
    return "ok"