from langchain_ollama import ChatOllama
from src.config import OLLAMA_MODEL, OLLAMA_BASE_URL
from src.state import AgentState
from src.chains import get_retrieval_chain

# ── Ollama client ─────────────────────────────────────────────────────────────
llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.1
)


# ── Summarizer node ───────────────────────────────────────────────────────────
def summarizer_node(state: AgentState) -> AgentState:
    """
    Retrieves relevant content and summarizes it into bullet points.
    Used when user explicitly asks for a summary.
    """
    query = state["query"]

    # Get content using Jason's retrieval chain
    chain = get_retrieval_chain()
    result = chain.invoke({"question": query})

    retrieved_text = result["answer"]
    hits = []

    # Summarize the retrieved content
    summary_prompt = f"""Summarize the following content in exactly 3-5 clear bullet points.
Each bullet point should be one complete sentence.
Be concise and focus on the most important information.

Content to summarize:
{retrieved_text}

Summary (3-5 bullet points):"""

    response = llm.invoke(summary_prompt)
    summary = response.content.strip()

    print(f"Summarizer output: {summary[:100]}...")

    return {
        **state,
        "tool_output": summary,
        "hits":        hits,
        "confidence":  0.5,
    }