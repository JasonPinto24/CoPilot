from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

# ── Create splitter once at module level ──────────────────────────────────────
_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " ", ""],
)


# ── Chunk all documents ───────────────────────────────────────────────────────
def chunk_docs(docs: list) -> list:
    """
    Splits all Documents into smaller chunks.
    Each chunk inherits the parent document's metadata.
    Adds chunk_index to track position within parent document.
    Returns: flat list of all chunk Documents
    """
    all_chunks = []

    for doc in docs:
        # Split this document into chunks
        chunks = _splitter.split_documents([doc])

        # Add chunk_index to each chunk's metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = i

        all_chunks.extend(chunks)

    print(f"Chunking complete: {len(docs)} documents → {len(all_chunks)} chunks")
    return all_chunks