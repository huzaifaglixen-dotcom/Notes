from sentence_transformers import SentenceTransformer
import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================================
# 1. AI MODEL & CHROMADB SETUP
# ==========================================================

# Embedding Model Load
model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent Database (Data program close hone ke baad bhi save rahega)
chroma_client = chromadb.PersistentClient(path="./my_chroma_db")

# Collection agar pehle se hai to use open karega,
# warna nayi collection create karega.
collection = chroma_client.get_or_create_collection(
    name="pdf_chunks_collection"
)

print("1. Model and Database Ready!")

# ==========================================================
# 2. READ PDF
# ==========================================================

pdf_path = "sample.pdf"

reader = PdfReader(pdf_path)

full_text = ""

# PDF ke tamam pages ka text ek string mein store karna
for page in reader.pages:

    text = page.extract_text()

    if text:
        full_text += text + "\n"

print("2. PDF Text Extracted Successfully!")

# ==========================================================
# 3. SMART CHUNKING
# ==========================================================

text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=500,

    chunk_overlap=50,

    separators=["\n\n", "\n", " ", ""]

)

chunks = text_splitter.split_text(full_text)

print(f"3. Total Chunks Created : {len(chunks)}")

# ==========================================================
# 4. STORE DATA IN CHROMADB
# ==========================================================

# Agar database khaali hai tabhi embeddings banao
if collection.count() == 0:

    print("\nDatabase is Empty.")
    print("Creating Embeddings...\n")

    ids = []

    for i in range(len(chunks)):
        ids.append(f"chunk_{i}")

    embeddings = model.encode(chunks).tolist()

    collection.add(

        ids=ids,

        documents=chunks,

        embeddings=embeddings

    )

    print("Embeddings Stored Successfully!")

else:

    print("\nDatabase Already Exists.")
    print("Skipping Embedding Creation.")


# ==========================================================
# 5. CHAT LOOP
# ==========================================================

print("\n========== PDF CHAT ==========")
print("Type 'exit' to close the chatbot.\n")

while True:

    # User se question lo
    query_text = input("Enter your question : ")

    # Agar user exit likhe to program band
    if query_text.lower() == "exit":
        print("\nGoodbye 👋")
        break

    # Query ki embedding banao
    query_embedding = model.encode(query_text).tolist()

    # ChromaDB mein semantic search
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    # ==========================================================
    # 6. DISPLAY RESULTS
    # ==========================================================

    print("\n====================================")
    print("User Question :")
    print(query_text)
    print("====================================")

    print("\nBest Match 1\n")
    print(results["documents"][0][0])

    print("\nDistance Score :")
    print(results["distances"][0][0])

    print("\n------------------------------------")

    print("\nBest Match 2\n")
    print(results["documents"][0][1])

    print("\nDistance Score :")
    print(results["distances"][0][1])

    print("\n====================================\n")