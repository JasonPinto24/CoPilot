import os
from dotenv import load_dotenv

load_dotenv()

# ── Ollama (local LLM) ────────────────────────────────────────────────────────
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

# ── Embeddings (local, free) ──────────────────────────────────────────────────
EMBED_MODEL = "BAAI/bge-small-en-v1.5"

# ── Qdrant ────────────────────────────────────────────────────────────────────
QDRANT_URL      = os.getenv("QDRANT_URL")
QDRANT_API_KEY  = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "enterprise_docs"

# ── Cohere ────────────────────────────────────────────────────────────────────
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# ── LangSmith ─────────────────────────────────────────────────────────────────
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "CoPilot")

# ── Chunking ──────────────────────────────────────────────────────────────────
CHUNK_SIZE    = 800
CHUNK_OVERLAP = 120

# ── Retrieval ─────────────────────────────────────────────────────────────────
TOP_K          = 12
TOP_N          = 4
ESCALATE_BELOW = 0.25