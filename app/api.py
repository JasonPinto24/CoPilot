from fastapi import FastAPI
from pydantic import BaseModel
from src.graph import app as graph_app

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Enterprise Knowledge Copilot",
    description="RAG + LangGraph agent for internal IT knowledge",
    version="1.0.0"
)

# ── Request model ─────────────────────────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str


# ── Response model ────────────────────────────────────────────────────────────
class QuestionResponse(BaseModel):
    answer:    str
    citations: list
    escalated: bool


# ── POST /ask endpoint ────────────────────────────────────────────────────────
@app.post("/ask", response_model=QuestionResponse)
async def ask(request: QuestionRequest):
    """
    Receives a question and returns a cited answer.
    Runs the full LangGraph agent pipeline.
    """
    initial_state = {
        "query":       request.question,
        "messages":    [],
        "tool_output": "",
        "hits":        [],
        "answer":      "",
        "citations":   [],
        "escalated":   False,
        "confidence":  0.0,
    }

    result = graph_app.invoke(initial_state)

    return QuestionResponse(
        answer=result["answer"],
        citations=result["citations"],
        escalated=result["escalated"],
    )


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "service": "Enterprise Knowledge Copilot"}