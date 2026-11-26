from sentence_transformers import SentenceTransformer
import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai

# ==========================================================
# 1. LOAD EMBEDDING MODEL
# ==========================================================

# Ye model text ko vector (embedding) mein convert karega.
model = SentenceTransformer("all-MiniLM-L6-v2")

# ==========================================================
# 2. GEMINI CLIENT
# ==========================================================

# Gemini se baat karne ke liye client create kar rahe hain.
client = genai.Client(
    api_key="Your_Google_API_Key_Here"   
)

# ==========================================================
# 3. CHROMADB SETUP
# ==========================================================

# PersistentClient ka matlab:
# Database program band hone ke baad bhi save rahega.
chroma_client = chromadb.PersistentClient(path="./my_chroma_db")

# Agar collection pehle se hai to usi ko use karega.
# Agar nahi hai to nayi collection create karega.
collection = chroma_client.get_or_create_collection(
    name="pdf_chunks_collection"
)

print("Model, Gemini & ChromaDB Ready!")

# ==========================================================
# 4. READ PDF
# ==========================================================

pdf_path = "sample.pdf"

reader = PdfReader(pdf_path)

full_text = ""

# PDF ke tamam pages ka text ek string mein collect karna.
for page in reader.pages:

    text = page.extract_text()

    if text:
        full_text += text + "\n"

print("PDF Text Extracted Successfully!")

# ==========================================================
# 5. SMART CHUNKING
# ==========================================================

# RecursiveCharacterTextSplitter paragraph aur sentences
# ko possible extent tak preserve karta hai.
text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=500,

    chunk_overlap=50,

    separators=[
        "\n\n",
        "\n",
        " ",
        ""
    ]
)

chunks = text_splitter.split_text(full_text)

print(f"Total Chunks Created : {len(chunks)}")

# ==========================================================
# 6. STORE EMBEDDINGS IN CHROMADB (ONLY FIRST TIME)
# ==========================================================

# Agar database empty hai tabhi embeddings banengi.
if collection.count() == 0:

    print("\nDatabase Empty")
    print("Creating Embeddings...\n")
    
        # ids = [f"chunk_{i}" for i in range(len(chunks))] 

    ids = []

    # Har chunk ki unique ID
    for i in range(len(chunks)):
        ids.append(f"chunk_{i}")

    # Saare chunks ki embeddings ek hi baar create karna
    embeddings = model.encode(chunks).tolist()

    # ChromaDB mein save karna
    collection.add(

        ids=ids,

        documents=chunks,

        embeddings=embeddings

    )

    print("Embeddings Stored Successfully!")

else:

    print("\nDatabase Already Exists")
    print("Skipping Embedding Creation")

# ==========================================================
# 7. CHAT LOOP
# ==========================================================

print("\n===============================")
print("      PDF CHATBOT READY")
print("===============================\n")

while True:

    # User se question lena
    query_text = input("Ask Question (type 'exit' to quit): ")

    # Program band karna
    if query_text.lower() == "exit":
        print("\nGood Bye!")
        break

    # ======================================================
    # QUERY EMBEDDING
    # ======================================================

    # User question ko embedding mein convert karna
    query_embedding = model.encode(query_text).tolist()

    # ======================================================
    # SEMANTIC SEARCH
    # ======================================================

    # ChromaDB se top 2 similar chunks retrieve karna
    results = collection.query(

        query_embeddings=[query_embedding],

        n_results=2

    )

    # ======================================================
    # CONTEXT BUILDING
    # ======================================================

    # Retrieved chunks ek list ki form mein aate hain.
    #
    # Example:
    #
    # [
    #   "Chunk 1",
    #   "Chunk 2"
    # ]
    #
    # join() in dono chunks ko ek single string bana deta hai.

    context = "\n\n".join(results["documents"][0])

    # ======================================================
    # PROMPT ENGINEERING
    # ======================================================

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not available in the context,
reply exactly:

"I couldn't find that information in the PDF."

Context:

{context}

Question:

{query_text}

Answer:
"""

    # ======================================================
    # GEMINI GENERATES FINAL ANSWER
    # ======================================================

    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt

    )

    # ======================================================
    # DISPLAY ANSWER
    # ======================================================

    print("\n===================================")
    print("Gemini Answer")
    print("===================================\n")

    print(response.text)

    print("\n===================================\n")