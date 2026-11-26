# ==========================================================
# rag_v4.py
# PART 1 / 3
# ==========================================================

"""
Production Style RAG

Features
--------
✔ Read PDF
✔ Smart Chunking
✔ SentenceTransformer Embeddings
✔ ChromaDB Persistent
✔ Metadata
✔ MD5 Hash
✔ hash.json
✔ Auto Re-index
✔ Threshold Filtering
✔ Gemini
"""

import os
import json
import hashlib

import chromadb

from pypdf import PdfReader

from sentence_transformers import SentenceTransformer

from langchain_text_splitters import RecursiveCharacterTextSplitter

from google import genai

# ==========================================================
# CONFIGURATION
# ==========================================================

PDF_PATH = "sample.pdf"

DB_PATH = "./my_chroma_db"

COLLECTION_NAME = "pdf_chunks_collection"

HASH_FILE = "hash.json"

THRESHOLD = 0.30

GEMINI_API_KEY = "YOUR_API_KEY"

# ==========================================================
# LOAD MODEL
# ==========================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ==========================================================
# GEMINI
# ==========================================================

gemini = genai.Client(
    api_key=GEMINI_API_KEY
)

# ==========================================================
# CHROMADB
# ==========================================================

db = chromadb.PersistentClient(
    path=DB_PATH
)

collection = db.get_or_create_collection(
    COLLECTION_NAME
)

# ==========================================================
# HASH FUNCTION
# ==========================================================

def calculate_pdf_hash(pdf_path):

    with open(pdf_path, "rb") as file:

        pdf_bytes = file.read()

    hash_object = hashlib.md5(pdf_bytes)

    return hash_object.hexdigest()

# ==========================================================
# LOAD HASH.JSON
# ==========================================================

def load_hashes():

    if not os.path.exists(HASH_FILE):

        with open(HASH_FILE, "w") as file:

            json.dump({}, file, indent=4)

    with open(HASH_FILE, "r") as file:

        return json.load(file)

# ==========================================================
# SAVE HASH.JSON
# ==========================================================

def save_hashes(hashes):

    with open(HASH_FILE, "w") as file:

        json.dump(hashes, file, indent=4)

# ==========================================================
# READ PDF
# ==========================================================

def read_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text is None:
            text = ""

        pages.append(
            (page_number, text)
        )

    return pages

# ==========================================================
# CHUNKING
# ==========================================================

def create_chunks(pages):

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

    for page_number, text in pages:

        chunks = splitter.split_text(text)

        for chunk in chunks:

            ids.append(

                f"{os.path.basename(PDF_PATH)}_chunk_{chunk_counter}"

            )

            documents.append(chunk)

            embeddings.append(

                model.encode(chunk).tolist()

            )

            metadatas.append(

                {
                    "source": os.path.basename(PDF_PATH),

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
# PART 2 / 3
# ==========================================================

# ==========================================================
# INDEX PDF
# ==========================================================

def index_pdf():

    print("\nReading PDF...")

    pages = read_pdf(PDF_PATH)

    print("Creating Chunks...")

    ids, documents, embeddings, metadatas = create_chunks(pages)

    print(f"Total Chunks : {len(documents)}")

    print("Storing Embeddings...\n")

    collection.add(

        ids=ids,

        documents=documents,

        embeddings=embeddings,

        metadatas=metadatas

    )

    print("Indexing Completed Successfully!")

# ==========================================================
# DELETE OLD CHUNKS
# ==========================================================

def delete_pdf_chunks():

    print("Deleting Old Chunks...")

    collection.delete(

        where={

            "source": os.path.basename(PDF_PATH)

        }

    )

# ==========================================================
# SYNC PDF
# ==========================================================

def sync_pdf():

    hashes = load_hashes()

    current_hash = calculate_pdf_hash(PDF_PATH)

    # ---------------------------------------------
    # NEW PDF
    # ---------------------------------------------

    if PDF_PATH not in hashes:

        print("\nNew PDF Detected")

        index_pdf()

        hashes[PDF_PATH] = current_hash

        save_hashes(hashes)

        return

    # ---------------------------------------------
    # PDF UPDATED
    # ---------------------------------------------

    if hashes[PDF_PATH] != current_hash:

        print("\nPDF Updated")

        delete_pdf_chunks()

        index_pdf()

        hashes[PDF_PATH] = current_hash

        save_hashes(hashes)

        return

    # ---------------------------------------------
    # NO CHANGE
    # ---------------------------------------------

    print("\nPDF Unchanged")

    print("Skipping Re-indexing")

# ==========================================================
# ASK QUESTION
# ==========================================================

def ask(query):

    # ---------------------------------------------
    # Query Embedding
    # ---------------------------------------------

    query_embedding = model.encode(query).tolist()

    # ---------------------------------------------
    # Semantic Search
    # ---------------------------------------------

    results = collection.query(

        query_embeddings=[query_embedding],

        n_results=3

    )

    # ---------------------------------------------
    # Threshold Filtering
    # ---------------------------------------------

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

    # ---------------------------------------------
    # Nothing Found
    # ---------------------------------------------

    if len(context_chunks) == 0:

        print("\nI couldn't find that information in the PDF.")

        return

    # ---------------------------------------------
    # Build Context
    # ---------------------------------------------

    context = "\n\n".join(

        context_chunks

    )

    # ==========================================================
    # PROMPT
    # ==========================================================

    prompt = f"""

You are a helpful AI assistant.

Answer ONLY using the given context.

If answer is not available,

reply exactly:

"I couldn't find that information in the PDF."

Context:

{context}

Question:

{query}

Answer:

"""
# ==========================================================
# PART 3 / 3
# ==========================================================

    # ==========================================================
    # GEMINI
    # ==========================================================

    response = gemini.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt

    )

    # ==========================================================
    # DISPLAY ANSWER
    # ==========================================================

    print("\n" + "=" * 60)
    print("Answer")
    print("=" * 60)

    print(response.text)

    # ==========================================================
    # DISPLAY SOURCES
    # ==========================================================

    print("\n" + "=" * 60)
    print("Sources")
    print("=" * 60)

    for metadata, distance in source_information:

        print(

            f"Page : {metadata['page']} | "

            f"Source : {metadata['source']} | "

            f"Distance : {distance:.4f}"

        )

# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)
    print("         RAG VERSION 4")
    print("=" * 60)

    # ---------------------------------------------
    # Check PDF Status
    # ---------------------------------------------

    sync_pdf()

    # ---------------------------------------------
    # Chat Loop
    # ---------------------------------------------

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