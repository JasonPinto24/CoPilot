import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import CSVLoader
from langchain_core.documents import Document
from src.pii import redact

# ── Folder paths ──────────────────────────────────────────────────────────────
OPTION_A_DIR = "data/raw/option_a"
OPTION_C_DIR = "data/raw/option_c"
TICKETS_FILE = "data/tickets.csv"


# ── Load markdown files ───────────────────────────────────────────────────────
def load_markdown_files(folder: str, dataset: str) -> list:
    """
    Loads all .md files from a folder using plain file reading.
    folder: path to the folder
    dataset: either 'option_a' or 'option_c'
    Returns: list of Document objects
    """
    docs = []
    pattern = os.path.join(folder, "*.md")
    files = glob.glob(pattern)

    print(f"  Found {len(files)} markdown files in {folder}")

    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            content = redact(content)

            doc = Document(
                page_content=content,
                metadata={
                    "source":  os.path.basename(filepath),
                    "page":    1,
                    "type":    "doc",
                    "dataset": dataset,
                }
            )
            docs.append(doc)

        except Exception as e:
            print(f"  Warning: could not load {filepath}: {e}")
            continue

    return docs


# ── Load PDF files ────────────────────────────────────────────────────────────
def load_pdf_files(folder: str, dataset: str) -> list:
    """
    Loads all .pdf files from a folder.
    Each page of the PDF becomes one Document.
    folder: path to the folder
    dataset: either 'option_a' or 'option_c'
    Returns: list of Document objects
    """
    docs = []
    pattern = os.path.join(folder, "*.pdf")
    files = glob.glob(pattern)

    print(f"  Found {len(files)} PDF files in {folder}")

    for filepath in files:
        try:
            loader = PyPDFLoader(filepath)
            loaded = loader.load()

            for doc in loaded:
                doc.page_content = redact(doc.page_content)
                doc.metadata["source"]  = os.path.basename(filepath)
                doc.metadata["type"]    = "doc"
                doc.metadata["dataset"] = dataset

            docs.extend(loaded)

        except Exception as e:
            print(f"  Warning: could not load {filepath}: {e}")
            continue

    return docs


# ── Load tickets CSV ──────────────────────────────────────────────────────────
def load_tickets() -> list:
    """
    Loads data/tickets.csv.
    Each row becomes one Document with type='ticket'.
    Returns: list of Document objects
    """
    docs = []

    if not os.path.exists(TICKETS_FILE):
        print(f"  Warning: {TICKETS_FILE} not found")
        return docs

    try:
        loader = CSVLoader(
            file_path=TICKETS_FILE,
            encoding="utf-8"
        )
        loaded = loader.load()

        print(f"  Found {len(loaded)} tickets in {TICKETS_FILE}")

        for doc in loaded:
            doc.page_content = redact(doc.page_content)
            doc.metadata["source"]  = f"ticket:{doc.metadata.get('row', 0)}"
            doc.metadata["type"]    = "ticket"
            doc.metadata["dataset"] = "option_c"
            doc.metadata["page"]    = 1

            docs.append(doc)

    except Exception as e:
        print(f"  Warning: could not load tickets: {e}")

    return docs


# ── Load everything ───────────────────────────────────────────────────────────
def load_all() -> list:
    """
    Loads all documents from Option A, Option C, and tickets.
    Returns a single flat list of all Document objects.
    """
    all_docs = []

    print("Loading Option A documents...")
    option_a_md  = load_markdown_files(OPTION_A_DIR, "option_a")
    option_a_pdf = load_pdf_files(OPTION_A_DIR, "option_a")
    all_docs.extend(option_a_md)
    all_docs.extend(option_a_pdf)

    print("Loading Option C documents...")
    option_c_md = load_markdown_files(OPTION_C_DIR, "option_c")
    all_docs.extend(option_c_md)

    print("Loading tickets...")
    tickets = load_tickets()
    all_docs.extend(tickets)

    print()
    print(f"Total documents loaded: {len(all_docs)}")
    print(f"  Option A markdown: {len(option_a_md)}")
    print(f"  Option A PDF:      {len(option_a_pdf)}")
    print(f"  Option C markdown: {len(option_c_md)}")
    print(f"  Tickets:           {len(tickets)}")

    return all_docs