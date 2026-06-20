from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from src.config import OLLAMA_MODEL, OLLAMA_BASE_URL
from src.retrieve import retrieve
from src.rerank import rerank

# ── Ollama LLM ────────────────────────────────────────────────────────────────
_llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.1,
)

# ── Citation prompt ───────────────────────────────────────────────────────────
_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an enterprise knowledge assistant for Northwind Systems.
Answer the question using ONLY the numbered context provided.
Cite every claim inline using [1], [2], [3] matching the context numbers.
If the context does not contain enough information, output exactly: INSUFFICIENT_CONTEXT
Never invent facts, URLs, or ticket numbers."""),
    ("human", """Context:
{context}

Question: {question}

Answer with inline citations:"""),
])

# ── Output parser ─────────────────────────────────────────────────────────────
_parser = StrOutputParser()


# ── Helper: retrieve and rerank ───────────────────────────────────────────────
def _retrieve_and_rerank(inputs: dict) -> dict:
    """
    Step 1 of the chain.
    Takes the question, retrieves top-12 from Qdrant,
    reranks to top-4 with Cohere, builds numbered context.
    """
    question = inputs["question"]

    # Retrieve top-12 from Qdrant
    hits = retrieve(question)

    # Rerank to top-4 with Cohere
    hits = rerank(question, hits)

    # Build numbered context string
    context_blocks = []
    for i, hit in enumerate(hits, 1):
        block = f"[{i}] (source: {hit['source']}, page {hit['page']})\n{hit['text']}"
        context_blocks.append(block)

    context = "\n\n".join(context_blocks)

    return {
        "question": question,
        "context":  context,
        "hits":     hits,
    }


# ── Helper: attach sources to final output ────────────────────────────────────
def _attach_sources(inputs: dict) -> dict:
    """
    Final step of the chain.
    Packages the answer string and source documents
    into the contract format Carolin expects.
    """
    answer = inputs["answer"]
    hits   = inputs["hits"]

    source_docs = []
    for hit in hits:
        source_docs.append({
            "page_content": hit["text"],
            "metadata": {
                "source":       hit["source"],
                "page":         hit["page"],
                "type":         hit["type"],
                "dataset":      hit["dataset"],
                "rerank_score": hit.get("rerank_score", 0.0),
            }
        })

    return {
        "answer":           answer,
        "source_documents": source_docs,
    }


# ── Build the LCEL chain ──────────────────────────────────────────────────────
def get_retrieval_chain():
    """
    Builds and returns the full LCEL retrieval chain.
    Carolin calls: chain.invoke({"question": query})
    Returns: {"answer": str, "source_documents": list}

    Chain flow:
    retrieve_and_rerank → prompt → LLM → parser → attach_sources
    """
    # Step 1: retrieve and rerank
    step1 = RunnableLambda(_retrieve_and_rerank)

    # Step 2-4: prompt → LLM → parse to string
    # We need to pass both the answer AND the hits to the final step
    # So we use RunnablePassthrough to carry hits alongside the chain
    step2_to_4 = (
        RunnablePassthrough.assign(
            answer=(
                (lambda x: {"question": x["question"], "context": x["context"]})
                | _prompt
                | _llm
                | _parser
            )
        )
    )

    # Step 5: package into contract format
    step5 = RunnableLambda(_attach_sources)

    # Compose full chain
    chain = step1 | step2_to_4 | step5

    return chain