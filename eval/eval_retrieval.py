import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.retrieve import retrieve
from src.rerank import rerank

# ── Load gold test set ────────────────────────────────────────────────────────
def load_qa_set():
    with open("eval/qa_set.json", "r", encoding="utf-8") as f:
        return json.load(f)


# ── Metrics ───────────────────────────────────────────────────────────────────
def precision_at_k(retrieved_sources, relevant_sources, k=4):
    """Of the top-k retrieved, what fraction were relevant?"""
    if not relevant_sources:
        return 0.0
    top_k = retrieved_sources[:k]
    relevant_set = set(relevant_sources)
    hits = sum(1 for s in top_k if any(r in s for r in relevant_set))
    return hits / max(len(top_k), 1)


def recall_at_k(retrieved_sources, relevant_sources, k=4):
    """Of all relevant sources, what fraction did we retrieve?"""
    if not relevant_sources:
        return 0.0
    top_k = retrieved_sources[:k]
    relevant_set = set(relevant_sources)
    hits = sum(1 for r in relevant_set if any(r in s for s in top_k))
    return hits / max(len(relevant_set), 1)


def f1_score(precision, recall):
    """Harmonic mean of precision and recall."""
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def mrr(retrieved_sources, relevant_sources):
    """Mean Reciprocal Rank — where does the first relevant result appear?"""
    if not relevant_sources:
        return 0.0
    relevant_set = set(relevant_sources)
    for i, source in enumerate(retrieved_sources, 1):
        if any(r in source for r in relevant_set):
            return 1.0 / i
    return 0.0


# ── Run evaluation ────────────────────────────────────────────────────────────
def evaluate(use_rerank=True):
    qa_set = load_qa_set()

    # Only evaluate answerable and ticket questions
    eval_questions = [q for q in qa_set if q["type"] != "gap"]

    total_precision = 0.0
    total_recall    = 0.0
    total_f1        = 0.0
    total_mrr       = 0.0

    print(f"\n{'='*60}")
    print(f"Retrieval Evaluation — rerank={'ON' if use_rerank else 'OFF'}")
    print(f"{'='*60}\n")

    for i, item in enumerate(eval_questions):
        question         = item["question"]
        relevant_sources = item["relevant_sources"]

        # Retrieve
        hits = retrieve(question)

        # Optionally rerank
        if use_rerank:
            hits = rerank(question, hits)

        # Get retrieved source names
        retrieved_sources = [h["source"] for h in hits]

        # Calculate metrics
        p         = precision_at_k(retrieved_sources, relevant_sources)
        r         = recall_at_k(retrieved_sources, relevant_sources)
        f1        = f1_score(p, r)
        mrr_score = mrr(retrieved_sources, relevant_sources)

        total_precision += p
        total_recall    += r
        total_f1        += f1
        total_mrr       += mrr_score

        print(f"Q{i+1}: {question[:50]}...")
        print(f"  Retrieved: {retrieved_sources}")
        print(f"  Expected:  {relevant_sources}")
        print(f"  P@4={p:.2f}  R@4={r:.2f}  F1={f1:.2f}  MRR={mrr_score:.2f}")
        print()

    n       = len(eval_questions)
    avg_p   = total_precision / n
    avg_r   = total_recall / n
    avg_f1  = total_f1 / n
    avg_mrr = total_mrr / n

    print(f"{'='*60}")
    print(f"RESULTS — {n} questions evaluated")
    print(f"{'='*60}")
    print(f"Avg Precision@4: {avg_p:.3f}")
    print(f"Avg Recall@4:    {avg_r:.3f}")
    print(f"Avg F1:          {avg_f1:.3f}")
    print(f"Avg MRR:         {avg_mrr:.3f}")
    print(f"{'='*60}\n")

    return {
        "precision": avg_p,
        "recall":    avg_r,
        "f1":        avg_f1,
        "mrr":       avg_mrr,
    }


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Running WITHOUT reranking...")
    results_no_rerank = evaluate(use_rerank=False)

    print("Running WITH reranking...")
    results_with_rerank = evaluate(use_rerank=True)

    print("\n" + "="*60)
    print("COMPARISON — Impact of Cohere Reranking")
    print("="*60)
    print(f"{'Metric':<20} {'Without':>12} {'With':>12} {'Improvement':>12}")
    print("-"*60)
    for metric in ["precision", "recall", "f1", "mrr"]:
        before = results_no_rerank[metric]
        after  = results_with_rerank[metric]
        diff   = after - before
        print(f"{metric:<20} {before:>12.3f} {after:>12.3f} {diff:>+12.3f}")
    print("="*60)