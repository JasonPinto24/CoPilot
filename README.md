# Enterprise Knowledge Copilot

A RAG + Agentic AI system for large IT services companies. Employees ask questions in plain English and receive cited answers pulled from internal SOPs, runbooks, and past support tickets — powered entirely by open-source models.

---

## Problem Statement

Large IT companies struggle with:
- Scattered documentation across PDFs, wikis, and SOPs
- Duplicate support tickets — the same issue solved repeatedly
- Slow onboarding of new engineers
- Knowledge silos across teams

---

## Solution

An Enterprise Knowledge Copilot that:
- Answers internal employee queries with inline citations
- Retrieves relevant documents from a vector knowledge base
- Detects duplicate support tickets and surfaces past resolutions
- Summarizes long technical documents on request
- Escalates gracefully when not confident enough to answer

---

## Architecture
User Question

↓

LangGraph Agent (Router)

↓

┌─────────────┬──────────────┬─────────────┐

│ doc_search  │ticket_lookup │  summarizer │

└─────────────┴──────────────┴─────────────┘

↓

Qdrant Vector DB (749 chunks)

↓

Cohere Reranker (top-12 → top-4)

↓

Ollama qwen2.5:7b (cited answer)

↓

Guardrail Check → Answer or Escalate

↓

Chainlit UI

---

## Tech Stack

| Layer | Tool |
|---|---|
| LLM | Ollama → qwen2.5:7b (local, free) |
| Embeddings | sentence-transformers bge-small-en-v1.5 (local, free) |
| Vector DB | Qdrant Cloud (free tier) |
| Reranker | Cohere Rerank API (free trial) |
| RAG Chain | LangChain LCEL |
| Agent | LangGraph StateGraph |
| Observability | LangSmith |
| PII Redaction | Microsoft Presidio |
| API | FastAPI |
| UI | Chainlit |
| Eval | Custom LLM-as-Judge + Retrieval metrics |

---

## Dataset

- **Option A** — Public IT docs: Kafka, Kubernetes, Docker, FastAPI, Python (11 files)
- **Option C** — Synthetic Northwind Systems SOPs (20 files) + 200 IT support tickets
- **Total** — 749 chunks indexed in Qdrant

---

## Evaluation Results

### Retrieval Metrics (with Cohere reranking)

| Metric | Without Rerank | With Rerank | Improvement |
|---|---|---|---|
| Precision@4 | 0.587 | 0.630 | +0.043 |
| Recall@4 | 0.761 | 0.761 | +0.000 |
| F1 | 0.649 | 0.676 | +0.027 |
| MRR | 0.786 | 0.783 | -0.004 |

### Answer Quality (LLM-as-Judge via Ollama)

| Metric | Score |
|---|---|
| Avg Faithfulness | 4.5 / 5.0 |
| Avg Answer Relevancy | 3.8 / 5.0 |
| Escalation Accuracy | 3/3 (100%) ||

---

## Setup

### Prerequisites
- Python 3.10 or higher
- Ollama installed and running
- Qdrant Cloud account (free tier)
- Cohere API key (free trial)
- LangSmith account (free tier)

### Installation

```bash
# Clone the repo
git clone https://github.com/JasonPinto24/CoPilot.git
cd CoPilot

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_lg

# Pull Ollama model
ollama pull qwen2.5:7b
```

### Configuration

Copy `.env.example` to `.env` and fill in your keys:
OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_MODEL=qwen2.5:7b

QDRANT_URL=your-qdrant-cluster-url

QDRANT_API_KEY=your-qdrant-api-key

COHERE_API_KEY=your-cohere-api-key

LANGCHAIN_TRACING_V2=true

LANGCHAIN_API_KEY=your-langsmith-api-key

LANGCHAIN_PROJECT=CoPilot

---

## Running the Project

### Step 1 — Build the knowledge base (run once)

```bash
python -m scripts.gen_corpus      # generate synthetic Northwind data
python -m scripts.download_option_a  # download public IT docs
python -m scripts.index           # embed and index all documents
```

### Step 2 — Start the demo

```bash
chainlit run app/ui.py
```

Open http://localhost:8000 in your browser.

---

## Demo Questions

| Question | Feature Demonstrated |
|---|---|
| How do I set up VPN at Northwind? | Basic RAG with citations |
| Summarize the Kubernetes deployment docs | Summarizer node |
| Has anyone seen Kafka consumer lag before? | Ticket lookup — duplicate detection |
| What is Northwind's deployment policy for Singapore? | Escalation — knowledge gap |
| Compare Kafka SOP with related incident tickets | Multi-step agent |

---

## Project Structure
CoPilot/

├── src/

│   ├── config.py          # single source of truth

│   ├── pii.py             # Presidio PII redaction

│   ├── ingest.py          # document loaders

│   ├── chunk.py           # text splitting

│   ├── embed_store.py     # embeddings + Qdrant

│   ├── retrieve.py        # vector search

│   ├── rerank.py          # Cohere reranking

│   ├── chains.py          # LCEL chain

│   ├── state.py           # AgentState

│   └── nodes/             # LangGraph nodes

├── scripts/               # data pipeline scripts

├── eval/                  # evaluation scripts

├── app/

│   ├── api.py             # FastAPI endpoint

│   └── ui.py              # Chainlit UI

└── data/                  # knowledge base documents

---

## Team

- **Jason** — Data pipeline, retrieval, embeddings, evaluation
- **Carolin** — LangGraph agent, API, UI

---

## License

MIT License