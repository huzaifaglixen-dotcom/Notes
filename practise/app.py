
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Model Loaded")

embedding = model.encode("Flutter is a mobile framework.")
embedding1 = model.encode("Flutter helps build Android applications.")

score = util.cos_sim(embedding, embedding1)
print("Cosine Similarity Score: ", score)
print("Cosine Similarity Score: ", score.item())   # item lgane se tensor ka word ht gya score me se 




# print("Embedding: ",embedding)
# print("Type of embedding: ", type(embedding))
# print("Shape of embedding: ", embedding.shape)
# print("Length of embedding: ", len(embedding))
