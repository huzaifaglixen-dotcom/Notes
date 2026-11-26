from sentence_transformers import SentenceTransformer
import chromadb
from pypdf import PdfReader  # PDF read karne ke liye

# ==========================================
# 1. AI MODEL & CHROMADB SETUP
# ==========================================
model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.EphemeralClient()
collection = chroma_client.create_collection(name="pdf_chunks_collection")
print("1. Model and Database Ready!")

# ==========================================
# 2. PDF READ KARNA AUR TEXT EXTRACT KARNA
# ==========================================
pdf_path = "sample.pdf"  # Apni PDF file ka naam yahan likhein
reader = PdfReader(pdf_path)

full_text = ""
# PDF ke saare pages se text nikaal kar ek jagah jama karein
for page in reader.pages:
    text = page.extract_text()
    if text:  # Agar page khali nahi hai to
        full_text += text + "\n"

print("2. PDF Text Extracted Successfully!")

# ==========================================
# 3. TEXT KO CHUNKS (TUKRON) MEIN TODNA
# ==========================================
# Hum har chunk mein takreeban 500 characters rakhenge
chunk_size = 500
chunks = []

for i in range(0, len(full_text), chunk_size):
    chunk = full_text[i : i + chunk_size]
    chunks.append(chunk)

print(f"3. Text split into {len(chunks)} chunks!")

# ==========================================
# 4. CHUNKS KO CHROMADB MEIN INJECT KARNA
# ==========================================
# Har chunk ke liye ek unique ID chahiye (jaise chunk_0, chunk_1)
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
# Apni PDF ke mutabiq koi bhi sawal yahan likhein
query_text = "What is the patient's name and age?" 

query_embedding = model.encode(query_text).tolist()

# Top 2 sab se milte julte chunks nikalein (n_results=2)
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







# Fixed Size Chunking



# ==========================================================
# STEP 3 : CHARACTER CHUNKING WITH OVERLAP
# ==========================================================

# chunk_size = 500
# chunk_overlap = 100

# chunks = []

# start = 0

# while start < len(full_text):

#     end = start + chunk_size

#     chunk = full_text[start:end]

#     chunks.append(chunk)

#     # Move forward but keep overlap
#     start += chunk_size - chunk_overlap

# print(f"Total Chunks : {len(chunks)}")