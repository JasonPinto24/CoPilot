from langchain_ollama import ChatOllama
from src.config import OLLAMA_MODEL, OLLAMA_BASE_URL
from src.state import AgentState

# ── Ollama client ─────────────────────────────────────────────────────────────
llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.0
)

# ── Classification prompt ─────────────────────────────────────────────────────
ROUTER_PROMPT = """You are a query classifier for an enterprise IT knowledge system.

Classify the user query into exactly one of these three categories:

doc_search - Use this when:
  - User asks how to do something (how do I, how to, what is the procedure)
  - User asks about configuration, setup, or troubleshooting steps
  - User wants to know about a technology or process
  - Examples: "how do I set up VPN", "what is Kafka consumer lag", "how to debug pods"

ticket_lookup - Use this when:
  - User asks if anyone has seen an issue before
  - User describes a problem and wants to know if it was solved before
  - User mentions "has anyone", "did anyone", "seen this before", "same issue"
  - Examples: "has anyone seen this Kafka error", "did anyone fix this VPN issue"

summarizer - Use this when:
  - User explicitly asks for a summary
  - User says "summarize", "give me a brief overview", "tldr"
  - Examples: "summarize the Kubernetes docs", "give me a summary of the deployment guide"

Reply with ONLY one word: doc_search, ticket_lookup, or summarizer
No explanation. No punctuation. Just the one word.

User query: {query}"""


# ── Router node ───────────────────────────────────────────────────────────────
def router_node(state: AgentState) -> AgentState:
    query = state["query"]

    prompt = ROUTER_PROMPT.format(query=query)
    response = llm.invoke(prompt)

    # Clean the response - take only first word, lowercase
    decision = response.content.strip().lower().split()[0]

    # Validate - if unexpected output default to doc_search
    valid = ["doc_search", "ticket_lookup", "summarizer"]
    if decision not in valid:
        decision = "doc_search"

    print(f"Router decision: {decision}")
    return state


# ── Route decision function (used by LangGraph conditional edge) ───────────────
def route_decision(state: AgentState) -> str:
    query = state["query"]

    prompt = ROUTER_PROMPT.format(query=query)
    response = llm.invoke(prompt)

    decision = response.content.strip().lower().split()[0]

    valid = ["doc_search", "ticket_lookup", "summarizer"]
    if decision not in valid:
        decision = "doc_search"
    return decision