from sentence_transformers import SentenceTransformer
import chromadb
from pypdf import PdfReader  # PDF read karne ke liye
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Naya Splitter

# ==========================================
# 1. AI MODEL & CHROMADB SETUP
# ==========================================
model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.EphemeralClient()     # Ye RAM use karta hai. Program band. Database gayab.
collection = chroma_client.create_collection(name="pdf_chunks_collection")
print("1. Model and Database Ready!")

# ==========================================
# 2. PDF READ KARNA AUR TEXT EXTRACT KARNA
# ==========================================
pdf_path = "sample.pdf"  # Apni PDF file ka naam yahan likhein
reader = PdfReader(pdf_path)

full_text = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        full_text += text + "\n"

print("2. PDF Text Extracted Successfully!")

# ==========================================
# 3. TEXT KO SMART CHUNKS MEIN TODNA (SMART STRATEGY)
# ==========================================
# Humne splitter ko initialize kiya aur bataya ke chunks kaise banane hain
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # Har chunk zyadatar 500 characters ka hoga
    chunk_overlap=50,     # 50 characters pichle chunk se repeat honge (taaki context na toote)
    separators=["\n\n", "\n", " ", ""] # Pehle double line break check karega, phir line break, phir space
)

# Isne automatic hamare lambay paragraph ko smart chunks ki list mein badal diya
chunks = text_splitter.split_text(full_text)

print(f"3. Text smartly split into {len(chunks)} chunks!")

# ==========================================
# 4. CHUNKS KO CHROMADB MEIN INJECT KARNA
# ==========================================
ids = [f"chunk_{i}" for i in range(len(chunks))]

# Saare chunks ki embeddings ek sath nikalein
embeddings = model.encode(chunks).tolist()

# Database mein save karein
collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=ids
)
print("4. All chunks successfully injected into ChromaDB!")

print("\n--- SYSTEM READY: ASK ANY QUESTION ABOUT THE PDF ---")

# ==========================================
# 5. TEST QUERY (PDF SE SAWAL POOCHNA)
# ==========================================
query_text = input("Enter your question about the PDF: ")

query_embedding = model.encode(query_text).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

# Result print karein
print(f"\nYour Query: '{query_text}'")
print("\n--- Best Match 1 ---")
print(results['documents'][0][0])
print("Distance Score:", results['distances'][0][0])

print("\n--- Best Match 2 ---")
print(results['documents'][0][1])
print("Distance Score:", results['distances'][0][1])





# client = chromadb.PersistentClient(
#     path="./chroma_db"
# )