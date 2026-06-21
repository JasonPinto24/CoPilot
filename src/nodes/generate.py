from langchain_ollama import ChatOllama
from src.config import OLLAMA_MODEL, OLLAMA_BASE_URL
from src.state import AgentState

# ── Ollama client ─────────────────────────────────────────────────────────────
llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.1
)

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an enterprise knowledge assistant for Northwind Systems.

Answer the question using ONLY the numbered context provided below.
Cite every claim inline using [1], [2], [3] corresponding to the context numbers.

Rules:
- ONLY use information from the context
- Cite every sentence with the correct [number]
- If the context does not contain enough information to answer, output exactly: INSUFFICIENT_CONTEXT
- Never invent facts, URLs, or ticket numbers
- Keep the answer clear and concise"""

# ── Build numbered context from hits ─────────────────────────────────────────
def build_context(hits: list) -> str:
    """
    Formats retrieved chunks into a numbered context string for the LLM.
    Example output:
    [1] (source: kafka.md, page 2)
    chunk text here...

    [2] (source: vpn-setup.md, page 1)
    chunk text here...
    """
    if not hits:
        return "No context available."

    blocks = []
    for i, hit in enumerate(hits, 1):
        source = hit.get("source", "unknown")
        page   = hit.get("page", 1)
        text   = hit.get("text", "")
        blocks.append(f"[{i}] (source: {source}, page {page})\n{text}")

    return "\n\n".join(blocks)


# ── Build citations list for the UI ──────────────────────────────────────────
def build_citations(hits: list) -> list:
    """
    Creates a citations list mapping numbers to source files.
    Used by the Chainlit UI to show the source panel.
    """
    citations = []
    for i, hit in enumerate(hits, 1):
        citations.append({
            "n":      i,
            "source": hit.get("source", "unknown"),
            "page":   hit.get("page", 1),
            "type":   hit.get("type", "doc"),
        })
    return citations


# ── Generate node ─────────────────────────────────────────────────────────────
def generate_node(state: AgentState) -> AgentState:
    """
    Generates a cited answer from retrieved context using Ollama.
    Reads: query, hits, tool_output from AgentState
    Writes: answer, citations to AgentState
    """
    query       = state["query"]
    hits        = state["hits"]
    tool_output = state["tool_output"]

    # Build context from hits if available otherwise use tool_output
    if hits:
        context = build_context(hits)
    else:
        context = tool_output if tool_output else "No context available."

    # Build the full user message
    user_message = f"""Context:
{context}

Question: {query}

Answer (cite every claim with [1][2] etc):"""

    # Call Ollama
    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": user_message},
    ])

    answer     = response.content.strip()
    citations  = build_citations(hits)

    print(f"Generated answer: {answer[:100]}...")

    return {
        **state,
        "answer":    answer,
        "citations": citations,
    }