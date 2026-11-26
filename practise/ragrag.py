# """
# Production-style educational RAG example (Optimized).
# """

# import os
# import json
# import hashlib
# import chromadb
# from pypdf import PdfReader
# from sentence_transformers import SentenceTransformer
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from google import genai
# from google.genai.errors import APIError # Error handling ke liye

# PDF_PATH = "sample.pdf"
# DB_PATH = "./my_chroma_db"
# COLLECTION_NAME = "pdf_chunks_collection"
# HASH_FILE = "hash.json"

# # Production Best Practice: API Key Environment Variable se uthayein
# # Terminal mein set karein: export GEMINI_API_KEY="your_key" (Linux/Mac) ya set GEMINI_API_KEY="your_key" (Windows)
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "Your_Google_API_Key_Here")  # Default value for testing

# print("Initializing models and clients...")
# model = SentenceTransformer("all-MiniLM-L6-v2")
# gemini = genai.Client(api_key=GEMINI_API_KEY)
# db = chromadb.PersistentClient(path=DB_PATH)
# collection = db.get_or_create_collection(COLLECTION_NAME)

# def calculate_pdf_hash(path):
#     if not os.path.exists(path):
#         raise FileNotFoundError(f"Provided PDF path '{path}' does not exist.")
#     with open(path, "rb") as f:
#         return hashlib.md5(f.read()).hexdigest()

# def load_hashes():
#     if not os.path.exists(HASH_FILE):
#         with open(HASH_FILE, "w") as f:
#             json.dump({}, f, indent=4)
#     with open(HASH_FILE, "r") as f:
#         return json.load(f)

# def save_hashes(h):
#     with open(HASH_FILE, "w") as f:
#         json.dump(h, f, indent=4)

# def read_pdf(path):
#     try:
#         reader = PdfReader(path)
#         pages = []
#         for i, p in enumerate(reader.pages, start=1):
#             t = p.extract_text() or ""
#             pages.append((i, t))
#         return pages
#     except Exception as e:
#         print(f"[-] Error reading PDF: {e}")
#         return []

# def create_chunks(pages):
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50,
#         separators=["\n\n", "\n", " ", ""]
#     )
#     docs, ids, metas = [], [], []
#     c = 0
    
#     # Step 1: Pehle saare chunks aur metadata collect karein
#     for page_no, text in pages:
#         for chunk in splitter.split_text(text):
#             docs.append(chunk)
#             ids.append(f"{os.path.basename(PDF_PATH)}_chunk_{c}")
#             metas.append({"source": PDF_PATH, "page": page_no})
#             c += 1
            
#     # Step 2: BATCH EMBEDDING (Puri list ko ek sath encode karna 10x fast hai)
#     print(f"Generating embeddings for {len(docs)} chunks in a single batch...")
#     embs = model.encode(docs).tolist() if docs else []
    
#     return ids, docs, embs, metas

# def index_pdf():
#     pages = read_pdf(PDF_PATH)
#     if not pages:
#         return
#     ids, docs, embs, metas = create_chunks(pages)
#     if ids:
#         collection.add(ids=ids, documents=docs, embeddings=embs, metadatas=metas)
#         print("[+] Indexing complete!")

# def delete_pdf_chunks():
#     collection.delete(where={"source": PDF_PATH})

# def sync_pdf():
#     try:
#         hashes = load_hashes()
#         current = calculate_pdf_hash(PDF_PATH)
        
#         if PDF_PATH not in hashes:
#             print("[*] New PDF detected -> indexing...")
#             index_pdf()
#         elif hashes[PDF_PATH] != current:
#             print("[*] PDF content changed -> reindexing...")
#             delete_pdf_chunks()
#             index_pdf()
#         else:
#             print("[*] PDF unchanged -> skipping indexing.")
#             return
            
#         hashes[PDF_PATH] = current
#         save_hashes(hashes)
#     except FileNotFoundError as e:
#         print(f"[-] Critical Error: {e}")
#         exit(1)

# def ask(query):
#     qemb = model.encode(query).tolist()
#     res = collection.query(query_embeddings=[qemb], n_results=3)
    
#     if not res["documents"] or not res["documents"][0]:
#         print("\nAnswer: I couldn't find any relevant chunks in the database.")
#         return

#     context = "\n\n".join(res["documents"][0])
    
#     # Professional formatting guidelines added to the prompt
#     prompt = f"""You are a professional assistant. Answer the user's question ONLY using the provided context.
# Use clear bullet points and bold text where appropriate to make the answer highly readable.

# If the answer is not available in the context, reply exactly:
# "I couldn't find that information in the PDF."

# Context:
# {context}

# Question:
# {query}
# """

#     print("\nAnswer: ", end="", flush=True)
#     try:
#         # PRODUCTION LEVEL: Streaming response for instant UI update
#         response_stream = gemini.models.generate_content_stream(
#             model="gemini-2.5-flash",
#             contents=prompt
#         )
#         for chunk in response_stream:
#             print(chunk.text, end="", flush=True)
#         print()
#     except APIError as e:
#         print(f"\n[-] Gemini API Error: {e}")
#     except Exception as e:
#         print(f"\n[-] Unexpected Error: {e}")

#     # Display Sources nicely
#     print("\n" + "-"*40)
#     print("Sources Used:")
#     for m, d in zip(res["metadatas"][0], res["distances"][0]):
#         # Distance jitni kam hogi, chunk utna hi zyada match kar raha hoga
#         print(f"• Page {m['page']} | {m['source']} (Similarity Distance: {d:.4f})")
#     print("-"*40)

# def main():
#     sync_pdf()
#     print("\n" + "="*40)
#     print("        PDF CHATBOT READY (STREAMING)")
#     print("="*40)
#     while True:
#         try:
#             q = input("\nAsk (type 'exit' to quit): ").strip()
#             if not q:
#                 continue
#             if q.lower() == "exit":
#                 print("Good Bye!")
#                 break
#             ask(q)
#         except (KeyboardInterrupt, EOFError):
#             print("\nGood Bye!")
#             break

# if __name__ == "__main__":
#     main()