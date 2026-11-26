from sentence_transformers import SentenceTransformer
import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import hashlib

# ==========================================================
# 1. AI MODEL
# ==========================================================

model = SentenceTransformer("all-MiniLM-L6-v2")

# ==========================================================
# 2. CHROMADB
# ==========================================================

client = chromadb.PersistentClient(path="./my_chroma_db")

collection = client.get_or_create_collection(
    name="pdf_collection"
)

# ==========================================================
# 3. HASH FUNCTION
# ==========================================================

def calculate_pdf_hash(pdf_path):

    # PDF ko binary mode me open karo
    with open(pdf_path, "rb") as file:

        pdf_bytes = file.read()

    # Bytes ka MD5 hash
    hash_object = hashlib.md5(pdf_bytes)

    # Final hash string return karo
    return hash_object.hexdigest()


# ==========================================================
# 4. PDF PATH
# ==========================================================

pdf_path = "sample.pdf"

# Current PDF Hash
current_hash = calculate_pdf_hash(pdf_path)

print("Current PDF Hash:")
print(current_hash)

# Abhi sirf print kar rahe hain.
# Next lesson me JSON se compare karenge.

# ==========================================================
# 5. READ PDF
# ==========================================================

reader = PdfReader(pdf_path)

# ==========================================================
# 6. TEXT SPLITTER
# ==========================================================

text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=500,

    chunk_overlap=50,

    separators=["\n\n", "\n", " ", ""]
)

# ==========================================================
# 7. PAGE-WISE CHUNKING
# ==========================================================

documents = []
embeddings = []
ids = []
metadatas = []

chunk_counter = 0

# enumerate() page number bhi dega
for page_number, page in enumerate(reader.pages):

    text = page.extract_text()

    if not text:
        continue

    # Sirf isi page ke chunks
    chunks = text_splitter.split_text(text)

    for chunk in chunks:

        documents.append(chunk)

        ids.append(f"chunk_{chunk_counter}")

        embeddings.append(model.encode(chunk).tolist())

        # Metadata
        metadatas.append({

            "source": pdf_path,

            "page": page_number + 1

        })

        chunk_counter += 1

print(f"\nTotal Chunks : {len(documents)}")

# ==========================================================
# 8. STORE DATA
# ==========================================================

if collection.count() == 0:

    collection.add(

        ids=ids,

        documents=documents,

        embeddings=embeddings,

        metadatas=metadatas

    )

    print("\nEmbeddings Stored Successfully!")

else:

    print("\nDatabase Already Exists.")
    print("Skipping Embedding Creation.")

# ==========================================================
# 9. CHAT LOOP
# ==========================================================

print("\n==============================")
print("PDF Chat Started")
print("Type exit to quit")
print("==============================")

while True:

    query = input("\nAsk : ")

    if query.lower() == "exit":
        break

    query_embedding = model.encode(query).tolist()

    results = collection.query(

        query_embeddings=[query_embedding],

        n_results=2
    )

    print("\n============= RESULTS =============\n")

    for i in range(len(results["documents"][0])):

        print(f"Result {i+1}")
        print("-" * 40)

        print(results["documents"][0][i])

        print()

        print("Source :", results["metadatas"][0][i]["source"])

        print("Page :", results["metadatas"][0][i]["page"])

        print("Distance :", results["distances"][0][i])

        print("\n")