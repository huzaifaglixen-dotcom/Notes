# Cosine Similarity — Complete Guide

> Yeh file Cosine Similarity ko A se Z tak explain karti hai — concept, formula, manual calculation, Python code (from scratch, NumPy, sklearn), real AI use-cases, aur Euclidean distance se comparison.

---

## Table of Contents

1. [Concept kya hai?](#1-concept-kya-hai)
2. [Formula](#2-formula)
3. [Manual Example (step by step)](#3-manual-example-step-by-step)
4. [Python Code — From Scratch](#4-python-code--from-scratch)
5. [Python Code — NumPy ke sath](#5-python-code--numpy-ke-sath)
6. [Python Code — sklearn ke sath](#6-python-code--sklearn-ke-sath)
7. [Multiple Vectors ke beech Similarity (Batch)](#7-multiple-vectors-ke-beech-similarity-batch)
8. [Text/Embeddings ke sath Real Use-case](#8-textembeddings-ke-sath-real-use-case)
9. [AI Engineering mein Use-cases](#9-ai-engineering-mein-use-cases)
10. [Cosine Similarity vs Euclidean Distance](#10-cosine-similarity-vs-euclidean-distance)
11. [Cosine Distance](#11-cosine-distance)
12. [Quick Summary](#12-quick-summary)

---

## 1. Concept kya hai?

Cosine similarity do vectors ke beech ka **angle** measure karti hai — yeh unki **length/magnitude** ko ignore karti hai aur sirf yeh dekhti hai ke vectors **kis direction** mein point kar rahe hain.

| Angle | Similarity Value | Matlab |
|---|---|---|
| 0° (same direction) | **1** | Bilkul similar |
| 90° (perpendicular) | **0** | Bilkul unrelated |
| 180° (opposite direction) | **-1** | Bilkul opposite |

**Simple analogy:** do log ek hi direction mein chal rahe hain (chahe unki speed alag ho) — unki "walking direction" similar hai. Cosine similarity yehi cheez measure karti hai.

---

## 2. Formula

$$\text{cosine similarity} = \cos(\theta) = \frac{A \cdot B}{\|A\| \times \|B\|}$$

Jahan:

- **A · B** → dono vectors ka **dot product** (har corresponding element ko multiply kar ke sum karna)
- **‖A‖** aur **‖B‖** → har vector ki **magnitude / length** (Euclidean norm), formula: $\sqrt{\sum x_i^2}$

---

## 3. Manual Example (step by step)

```
A = [1, 2, 3]
B = [4, 5, 6]

Step 1: Dot Product
A · B = (1×4) + (2×5) + (3×6)
      = 4 + 10 + 18
      = 32

Step 2: Magnitude of A
|A| = sqrt(1² + 2² + 3²) = sqrt(14) ≈ 3.742

Step 3: Magnitude of B
|B| = sqrt(4² + 5² + 6²) = sqrt(77) ≈ 8.775

Step 4: Cosine Similarity
= 32 / (3.742 × 8.775)
≈ 0.9746
```

**Result:** 0.9746 → dono vectors ki direction bohat close hai (1 ke qareeb), matlab yeh highly similar hain.

---

## 4. Python Code — From Scratch

Bina kisi library ke, sirf `math` module se.

```python
import math

def cosine_similarity_manual(A, B):
    dot_product = sum(a * b for a, b in zip(A, B))
    magnitude_A = math.sqrt(sum(a**2 for a in A))
    magnitude_B = math.sqrt(sum(b**2 for b in B))
    return dot_product / (magnitude_A * magnitude_B)

A = [1, 2, 3]
B = [4, 5, 6]

print(cosine_similarity_manual(A, B))
# Output: 0.9746318461970762
```

---

## 5. Python Code — NumPy ke sath

Faster aur cleaner tareeqa — real projects mein yeh zyada use hota hai.

```python
import numpy as np

def cosine_similarity(A, B):
    dot_product = np.dot(A, B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)
    return dot_product / (norm_A * norm_B)

A = np.array([1, 2, 3])
B = np.array([4, 5, 6])

print(cosine_similarity(A, B))
# Output: 0.9746318461970762
```

---

## 6. Python Code — sklearn ke sath

Production aur ML pipelines mein yeh sabse common tareeqa hai.

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

A = np.array([[1, 2, 3]])
B = np.array([[4, 5, 6]])

similarity = cosine_similarity(A, B)
print(similarity)
# Output: [[0.9746]]
```

> **Note:** sklearn ka function hamesha **2D array** leta hai (list of vectors), isliye single vector ko bhi `[[...]]` shape mein dena zaroori hai.

---

## 7. Multiple Vectors ke beech Similarity (Batch)

Jab ek se zyada vectors ko aapas mein compare karna ho (jaise sab documents ko sab documents ke sath).

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

vectors = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

similarity_matrix = cosine_similarity(vectors)
print(similarity_matrix)
```

Yeh ek **matrix** return karega, jahan `matrix[i][j]` batata hai ke vector `i` aur vector `j` kitne similar hain.

---

## 8. Text/Embeddings ke sath Real Use-case

NLP mein text ko pehle numbers (vectors) mein convert karte hain, phir unki similarity nikalte hain.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

docs = ["I love machine learning", "I love deep learning"]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(docs)

similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
print(similarity)
```

Yehi concept modern AI mein **embeddings** (OpenAI, BERT, Word2Vec) ke sath bhi use hota hai — sirf text ki jagah high-dimensional embedding vectors hote hain.

---

## 9. AI Engineering mein Use-cases

| Use-case | Kaise use hoti hai |
|---|---|
| **Semantic Search / RAG** | Query embedding vs document embeddings compare kar ke sabse relevant results nikalna |
| **Recommendation Systems** | User preferences vs product vectors compare karna |
| **NLP / Embeddings** | Word2Vec, BERT, OpenAI embeddings ke beech "meaning" similarity check karna |
| **Face Recognition** | Face embeddings compare kar ke match dhoondna |
| **Plagiarism Detection** | Documents ki similarity check karna |
| **Vector Databases** | Pinecone, FAISS, Chroma jaise tools andar cosine similarity hi use karte hain nearest-neighbor search ke liye |

---

## 10. Cosine Similarity vs Euclidean Distance

| Feature | Cosine Similarity | Euclidean Distance |
|---|---|---|
| Kya measure karti hai | Direction / angle | Actual straight-line distance |
| Magnitude ka asar | Ignore karti hai | Magnitude matter karti hai |
| Best for | Text, embeddings (high-dimensional data) | Numeric / spatial data |
| Range | -1 se 1 tak | 0 se ∞ tak |

**Rule of thumb:** High-dimensional data (jaise 768 ya 1536-dimension text embeddings) mein cosine similarity zyada reliable hoti hai, kyunke sirf **direction** matter karti hai, length nahi.

---

## 11. Cosine Distance

Agar similarity ki jagah **distance** chahiye ho (jaise clustering algorithms mein zaroorat parti hai):

```python
cosine_distance = 1 - cosine_similarity
```

Jitni similarity zyada, distance utni kam — aur ulta.

---

## 12. Quick Summary

- Cosine Similarity = vectors ke beech **angle** ka measure, magnitude ignore karta hai.
- Formula: **dot product ÷ (magnitude of A × magnitude of B)**
- Range: **-1 to 1** (1 = identical direction, 0 = unrelated, -1 = opposite)
- Python mein `numpy` ya `sklearn.metrics.pairwise.cosine_similarity` se easily calculate hoti hai.
- AI mein sabse zyada use: **semantic search, embeddings comparison, recommendation systems, RAG pipelines**.

---

*Yeh guide interviews, projects, aur AI concepts revise karne ke liye ek quick reference hai.*
