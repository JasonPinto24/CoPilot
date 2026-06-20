import sys
import os

# Add project root to path so src imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingest import load_all
from src.chunk import chunk_docs
from src.embed_store import create_collection, upsert_chunks


def main():
    print("=== Enterprise Knowledge Copilot — Index Builder ===")
    print()

    # Step 1: Load all documents
    print("Step 1: Loading documents...")
    docs = load_all()
    print(f"Loaded {len(docs)} documents")
    print()

    # Step 2: Chunk documents
    print("Step 2: Chunking documents...")
    chunks = chunk_docs(docs)
    print(f"Created {len(chunks)} chunks")
    print()

    # Step 3: Create Qdrant collection
    print("Step 3: Creating Qdrant collection...")
    create_collection()
    print()

    # Step 4: Embed and upsert to Qdrant
    print("Step 4: Embedding and uploading to Qdrant...")
    total = upsert_chunks(chunks)
    print()

    print("=== Indexing complete ===")
    print(f"Total chunks in Qdrant: {total}")
    print()
    print("Knowledge base is ready for retrieval.")


if __name__ == "__main__":
    main()