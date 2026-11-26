from sentence_transformers import SentenceTransformer
import chromadb

# ======================================================
# STEP 1 : Load Embedding Model
# ======================================================

model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model Loaded Successfully!\n")


# ======================================================
# STEP 2 : Create ChromaDB Client
# ======================================================

client = chromadb.Client()

collection = client.create_collection(
    name="documents"
)


# ======================================================
# STEP 3 : Documents
# ======================================================

documents = [
    "Flutter is a mobile framework developed by Google.",
    "Python is widely used for Artificial Intelligence and Machine Learning.",
    "Docker helps developers package applications into containers."
]

ids = [
    "doc1",
    "doc2",
    "doc3"
]


# ======================================================
# STEP 4 : Create Embeddings
# ======================================================

# embeddings = model.encode(documents).tolist()

embeddings = []

for doc in documents:

    embedding = model.encode(doc)

    embeddings.append(
        embedding.tolist()
    )


# ======================================================
# STEP 5 : Store in ChromaDB
# ======================================================

collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings
)

print("Documents Stored Successfully!\n")


# ======================================================
# STEP 6 : User Query
# ======================================================

query = "How can I build Android applications?"

query_embedding = model.encode(query)


# ======================================================
# STEP 7 : Search
# ======================================================

results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=2
)


# ======================================================
# STEP 8 : Print Results
# ======================================================

print("=" * 50)
print("SEARCH RESULTS")
print("=" * 50)

print(results)

print("=" * 50)