import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_ollama import ChatOllama
from src.config import OLLAMA_MODEL, OLLAMA_BASE_URL
from src.graph import app

# ── Ollama judge ──────────────────────────────────────────────────────────────
judge = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.0,
    num_predict=10,
)


def score_faithfulness(context: str, answer: str) -> int:
    """Score how well the answer stays true to the context. 1-5."""
    prompt = f"""Context:
{context[:800]}

Answer:
{answer[:400]}

Score the faithfulness of the answer to the context from 1 to 5.
5 = every claim supported by context
3 = some claims supported
1 = answer ignores context

Reply with ONLY a single digit 1, 2, 3, 4, or 5."""
    response = judge.invoke(prompt)
    try:
        score = int(response.content.strip()[0])
        return min(max(score, 1), 5)
    except:
        return 3


def score_relevancy(question: str, answer: str) -> int:
    """Score how well the answer addresses the question. 1-5."""
    prompt = f"""Question: {question}

Answer: {answer[:400]}

Score how well the answer addresses the question from 1 to 5.
5 = directly and completely answers the question
3 = partially answers
1 = does not address the question

Reply with ONLY a single digit 1, 2, 3, 4, or 5."""
    response = judge.invoke(prompt)
    try:
        score = int(response.content.strip()[0])
        return min(max(score, 1), 5)
    except:
        return 3


def load_qa_set():
    with open("eval/qa_set.json", "r", encoding="utf-8") as f:
        return json.load(f)


def run_eval():
    qa_set = load_qa_set()
    answerable = [q for q in qa_set if q["type"] == "answerable"]
    gap_questions = [q for q in qa_set if q["type"] == "gap"]

    print(f"\n{'='*60}")
    print("LLM-as-Judge Evaluation")
    print(f"{'='*60}\n")

    total_faith = 0
    total_rel   = 0
    escalation_correct = 0

    # Evaluate answerable questions
    for i, item in enumerate(answerable):
        print(f"[{i+1}/{len(answerable)}] {item['question'][:55]}...")

        result = app.invoke({
            "query":       item["question"],
            "messages":    [],
            "tool_output": "",
            "hits":        [],
            "answer":      "",
            "citations":   [],
            "escalated":   False,
            "confidence":  0.0,
        })

        answer  = result["answer"]
        context = result.get("tool_output", "")

        faith = score_faithfulness(context, answer)
        rel   = score_relevancy(item["question"], answer)

        total_faith += faith
        total_rel   += rel

        print(f"  Faithfulness: {faith}/5  Relevancy: {rel}/5")
        print()

    # Evaluate gap questions — should escalate
    print("Testing escalation on gap questions...")
    for item in gap_questions:
        result = app.invoke({
            "query":       item["question"],
            "messages":    [],
            "tool_output": "",
            "hits":        [],
            "answer":      "",
            "citations":   [],
            "escalated":   False,
            "confidence":  0.0,
        })
        if result["escalated"]:
            escalation_correct += 1
            print(f"  ✓ Correctly escalated: {item['question'][:50]}")
        else:
            print(f"  ✗ Should have escalated: {item['question'][:50]}")

    n = len(answerable)
    avg_faith = total_faith / n
    avg_rel   = total_rel / n

    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}")
    print(f"Questions evaluated:   {n}")
    print(f"Avg Faithfulness:      {avg_faith:.1f} / 5.0")
    print(f"Avg Answer Relevancy:  {avg_rel:.1f} / 5.0")
    print(f"Escalation accuracy:   {escalation_correct}/{len(gap_questions)} gap questions correctly escalated")
    print(f"{'='*60}")


if __name__ == "__main__":
    run_eval()