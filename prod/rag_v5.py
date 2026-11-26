# ==========================================================
# VERSION 5
# Production Style Multi-PDF RAG
# ==========================================================

import os
import json
import hashlib
from pathlib import Path

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai

# ==========================================================
# CONFIGURATION
# ==========================================================

# Folder containing all PDFs
DOCUMENT_FOLDER = "documents"

# ChromaDB storage location
DB_PATH = "./my_chroma_db"

# ChromaDB collection name
COLLECTION_NAME = "pdf_chunks_collection"

# JSON file that stores PDF hashes
HASH_FILE = "hash.json"

# Similarity threshold
THRESHOLD = 0.65

# Gemini API Key
GEMINI_API_KEY = "Your_Google_API_Key_Here"

# ==========================================================
# LOAD AI MODELS
# ==========================================================

print("Loading Embedding Model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding Model Loaded")

# Gemini Client
gemini = genai.Client(
    api_key=GEMINI_API_KEY
)

# ==========================================================
# CHROMADB
# ==========================================================

db = chromadb.PersistentClient(
    path=DB_PATH
)

# NOTE: hnsw:space set to "cosine" because THRESHOLD (0.30) is
# meant to be compared against cosine distance, not the default L2.
collection = db.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

print("ChromaDB Ready")

# ==========================================================
# HASH FUNCTIONS
# ==========================================================

def calculate_pdf_hash(pdf_path):
    """
    Calculate MD5 hash of a PDF.
    Used to detect changes.
    """

    with open(pdf_path, "rb") as file:

        pdf_bytes = file.read()

    return hashlib.md5(
        pdf_bytes
    ).hexdigest()


# ==========================================================
# LOAD HASH FILE
# ==========================================================

def load_hashes():

    # Create hash.json if missing
    if not os.path.exists(HASH_FILE):

        with open(HASH_FILE, "w") as file:

            json.dump({}, file, indent=4)

    with open(HASH_FILE, "r") as file:

        return json.load(file)


# ==========================================================
# SAVE HASH FILE
# ==========================================================

def save_hashes(hashes):

    with open(HASH_FILE, "w") as file:

        json.dump(

            hashes,

            file,

            indent=4

        )

# ==========================================================
# READ PDF
# ==========================================================

def read_pdf(pdf_path):
    """
    Read a PDF page by page.

    Returns:
        [
            (1, page_text),
            (2, page_text),
            ...
        ]
    """

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text is None:
            text = ""

        pages.append(

            (
                page_number,
                text
            )

        )

    return pages


# ==========================================================
# CREATE CHUNKS
# ==========================================================

def create_chunks(pdf_path, pages):
    """
    Convert PDF pages into chunks.

    Returns:

        ids
        documents
        embeddings
        metadatas
    """

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=50,

        separators=[
            "\n\n",
            "\n",
            " ",
            ""
        ]

    )

    ids = []

    documents = []

    embeddings = []

    metadatas = []

    chunk_counter = 0

    # Loop through every page
    for page_number, text in pages:

        # Split current page into chunks
        chunks = splitter.split_text(text)

        # Loop through every chunk
        for chunk in chunks:

            # Store chunk text
            documents.append(chunk)

            # Unique chunk ID
            ids.append(

                f"{pdf_path.stem}_chunk_{chunk_counter}"

            )

            # Create embedding
            embeddings.append(

                embedding_model.encode(chunk).tolist()

            )

            # Metadata
            metadatas.append(

                {

                    "source": pdf_path.name,

                    "page": page_number

                }

            )

            chunk_counter += 1

    return (

        ids,

        documents,

        embeddings,

        metadatas

    )

# ==========================================================
# INDEX PDF
# ==========================================================

def index_pdf(pdf_path):
    """
    Read a PDF and store its chunks
    inside ChromaDB.
    """

    print(f"\nIndexing : {pdf_path.name}")

    # Read PDF
    pages = read_pdf(pdf_path)
    print(f"DEBUG: Extracted text sample from page 1: {pages[0][1][:200]}")

    # Create chunks
    ids, documents, embeddings, metadatas = create_chunks(

        pdf_path,

        pages

    )

    # Skip if PDF produced no chunks (e.g. empty/scanned PDF)
    if len(ids) == 0:

        print(f"No text extracted from {pdf_path.name}, skipping.")

        return

    # Store inside ChromaDB
    collection.add(

        ids=ids,

        documents=documents,

        embeddings=embeddings,

        metadatas=metadatas

    )

    print(f"{pdf_path.name} Indexed Successfully")


# ==========================================================
# DELETE PDF CHUNKS
# ==========================================================

def delete_pdf_chunks(pdf_path_or_name):
    """
    Delete every chunk that belongs
    to one specific PDF.
    """

    pdf_name = (
        pdf_path_or_name.name
        if isinstance(pdf_path_or_name, Path)
        else pdf_path_or_name
    )

    print(f"Removing old chunks : {pdf_name}")

    collection.delete(

        where={

            "source": pdf_name

        }

    )

    print("Old Chunks Deleted")

# ==========================================================
# SYNC SINGLE PDF
# ==========================================================

def sync_single_pdf(pdf_path):
    """
    Synchronize one PDF with ChromaDB.

    Cases:

    1. New PDF
            -> Index

    2. Updated PDF
            -> Delete old chunks
            -> Re-index

    3. Unchanged PDF
            -> Skip
    """

    # Load all saved hashes
    hashes = load_hashes()

    # Current PDF hash
    current_hash = calculate_pdf_hash(pdf_path)

    # PDF filename
    pdf_name = pdf_path.name

    # ------------------------------
    # CASE 1 : NEW PDF
    # ------------------------------

    if pdf_name not in hashes:

        print(f"\nNew PDF Found : {pdf_name}")

        index_pdf(pdf_path)

    # ------------------------------
    # CASE 2 : PDF UPDATED
    # ------------------------------

    elif hashes[pdf_name] != current_hash:

        print(f"\nPDF Updated : {pdf_name}")

        delete_pdf_chunks(pdf_path)

        index_pdf(pdf_path)

    # ------------------------------
    # CASE 3 : NO CHANGE
    # ------------------------------

    else:

        print(f"\nNo Changes : {pdf_name}")

        return

    # Update hash
    hashes[pdf_name] = current_hash

    save_hashes(hashes)

# ==========================================================
# SYNC ALL PDFS
# ==========================================================

def sync_all_pdfs():
    """
    Synchronize every PDF inside DOCUMENT_FOLDER with ChromaDB.

    - Indexes new PDFs
    - Re-indexes updated PDFs
    - Skips unchanged PDFs
    - Removes chunks/hashes for PDFs that were deleted from the folder
    """

    pdf_folder = Path(DOCUMENT_FOLDER)

    pdf_files = list(pdf_folder.glob("*.pdf"))

    # ------------------------------------------------------
    # Sync existing PDFs (new / updated / unchanged)
    # ------------------------------------------------------

    if not pdf_files:

        print("\nNo PDFs found in documents folder.")

    else:

        for pdf_path in pdf_files:

            sync_single_pdf(pdf_path)

    # ------------------------------------------------------
    # Remove chunks/hashes for PDFs no longer present
    # ------------------------------------------------------

    hashes = load_hashes()

    current_names = {pdf_path.name for pdf_path in pdf_files}

    removed_names = [name for name in hashes.keys() if name not in current_names]

    for name in removed_names:

        print(f"\nPDF Removed From Folder : {name}")

        delete_pdf_chunks(name)

        del hashes[name]

    if removed_names:

        save_hashes(hashes)

# ==========================================================
# ASK QUESTION
# ==========================================================

def ask(query):
    """
    Search the vector database and generate
    an answer using Gemini.
    """

    # ------------------------------------------
    # Create Query Embedding
    # ------------------------------------------

    query_embedding = embedding_model.encode(

        query

    ).tolist()

    # ------------------------------------------
    # Search ChromaDB
    # ------------------------------------------

    results = collection.query(

        query_embeddings=[query_embedding],

        n_results=5

    )

    # ------------------------------------------
    # Threshold Filtering
    # ------------------------------------------

    context_chunks = []

    source_information = []

    for document, metadata, distance in zip(

        results["documents"][0],

        results["metadatas"][0],

        results["distances"][0]

    ):

        if distance <= THRESHOLD:

            context_chunks.append(

                document

            )

            source_information.append(

                (

                    metadata,

                    distance

                )

            )

    # ------------------------------------------
    # Nothing Found
    # ------------------------------------------

    if len(context_chunks) == 0:

        print("\nI couldn't find that information in the PDF.")

        return

    # ------------------------------------------
    # Build Context
    # ------------------------------------------

    context = "\n\n".join(

        context_chunks

    )

    # ------------------------------------------
    # Prompt
    # ------------------------------------------

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not available in the context,
reply exactly:

"I couldn't find that information in the PDF."

Context:

{context}

Question:

{query}

Answer:
"""

    # ------------------------------------------
    # Gemini
    # ------------------------------------------

    response = gemini.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt

    )

    # ------------------------------------------
    # Display Answer
    # ------------------------------------------

    print("\n" + "=" * 60)

    print("Answer")

    print("=" * 60)

    print(response.text)

    # ------------------------------------------
    # Display Sources
    # ------------------------------------------

    print("\n" + "=" * 60)

    print("Sources")

    print("=" * 60)

    for metadata, distance in source_information:

        print(

            f"Source : {metadata['source']}"

        )

        print(

            f"Page   : {metadata['page']}"

        )

        print(

            f"Distance : {distance:.4f}"

        )

        print("-" * 60)



# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)
    print("        RAG VERSION 5")
    print("     Multi PDF Support")
    print("=" * 60)

    # ------------------------------------------------------
    # Create documents folder if missing
    # ------------------------------------------------------

    os.makedirs(

        DOCUMENT_FOLDER,

        exist_ok=True

    )

    # ------------------------------------------------------
    # Synchronize all PDFs
    # ------------------------------------------------------

    sync_all_pdfs()

    # ------------------------------------------------------
    # Chat Loop
    # ------------------------------------------------------

    while True:

        print()

        query = input(

            "Ask Question (type 'exit' to quit): "

        )

        if query.lower() == "exit":

            print("\nGood Bye!")

            break

        ask(query)


# ==========================================================
# PROGRAM START
# ==========================================================

if __name__ == "__main__":

    main()
    
