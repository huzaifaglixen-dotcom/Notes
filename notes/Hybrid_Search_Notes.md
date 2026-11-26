# Hybrid Search — Complete Notes

> **Hybrid Search** = **Keyword-based search (BM25)** + **Semantic/Vector search (Embeddings)** dono ko **combine** karna, taaki dono ke strengths mil jayein aur weaknesses cancel ho jayein.

---

## Table of Contents
1. Why Hybrid Search is Needed
2. Recap: BM25 vs Vector Search
3. What is Hybrid Search
4. How Hybrid Search Works (Architecture)
5. Score Combination Techniques
6. Reciprocal Rank Fusion (RRF) — Deep Dive
7. Alpha Weighting Method
8. Implementation Approaches
9. Popular Tools/Databases Supporting Hybrid Search
10. When to Use Hybrid Search vs Pure Vector Search
11. Common Mistakes
12. Cheat Sheet

---

## 1. Why Hybrid Search is Needed

Har search method ka apna ek **blind spot** hota hai:

| Method | Strength | Weakness |
|---|---|---|
| **BM25 (Keyword Search)** | Exact matches, names, IDs, technical codes | Synonyms/meaning samajh nahi paata |
| **Vector Search (Semantic)** | Meaning/context samajhta hai, synonyms handle karta hai | Exact keywords/rare terms/codes miss kar sakta hai |

### Example — Problem with Pure Vector Search
```
Query: "Error code XJ-4471"
```
- Vector search yeh soch sakta hai "error code" ka **general meaning** similar hai kisi aur error se, aur galat document retrieve kar de — kyunki "XJ-4471" jaisa **exact/rare identifier** embeddings me utna sharp represent nahi hota.
- BM25 iss case me **perfect** match karega, kyunki yeh exact keyword "XJ-4471" dhoondh raha hai.

### Example — Problem with Pure BM25
```
Query: "How to fix a broken pipe?"
Document: "Repairing a leaking water conduit"
```
- BM25 fail ho sakta hai kyunki koi exact common words nahi hain ("broken" vs "leaking", "pipe" vs "conduit").
- Vector search yeh easily samajh jayega ki dono ka **meaning same** hai.

> **Isiliye Hybrid Search dono combine karta hai** — best of both worlds.

---

## 2. Recap: BM25 vs Vector Search

| Feature | BM25 | Vector Search |
|---|---|---|
| Based on | Exact word/term matching | Meaning/semantic similarity |
| Good at | Rare terms, codes, names, exact phrases | Synonyms, paraphrasing, context |
| Weak at | Synonyms, different phrasing | Exact/rare identifiers, numbers, codes |
| Speed | Very fast | Fast (with ANN indexing) |
| Type | Sparse retrieval | Dense retrieval |

---

## 3. What is Hybrid Search

**Simple Meaning:** Query aane par, **dono methods se alag-alag results nikalo** (BM25 se aur Vector search se), phir un dono ke results ko ek **smart formula** se combine/merge karke ek **final ranked list** banao.

```
Query
  ├──→ BM25 Search  → Result Set A (with scores)
  └──→ Vector Search → Result Set B (with scores)
              │
              ▼
      Combine/Fuse Scores
              │
              ▼
      Final Ranked Results
```

---

## 4. How Hybrid Search Works (Architecture)

### Step-by-Step Flow

1. **Indexing Phase:**
   - Documents ko dono tarike se index kiya jata hai:
     - **Sparse Index** (BM25) — term frequency based
     - **Dense Index** (Vector DB) — embeddings based

2. **Query Phase:**
   - User query ko dono systems ko bheja jata hai:
     - BM25 query → top-K results with keyword-match scores
     - Vector query (embedding banake) → top-K results with similarity scores

3. **Fusion Phase:**
   - Dono result sets ke scores ko **combine** kiya jata hai (neeche techniques dekho).

4. **Final Ranking:**
   - Combined score ke hisaab se results ko **re-rank** karke top results user/LLM ko diye jate hain.

---

## 5. Score Combination Techniques

Problem: BM25 scores aur Vector similarity scores **different scales** pe hote hain (BM25 unbounded ho sakta hai, cosine similarity -1 to 1 range me hota hai) — inko directly add nahi kar sakte. Isliye combine karne ke specific techniques hain:

### 5.1 Simple Weighted Sum (Normalize + Combine)
```
Final Score = (weight1 × normalized_BM25_score) + (weight2 × normalized_vector_score)
```
- Pehle dono scores ko **0-1 range me normalize** karo, phir weighted average nikaalo.

### 5.2 Reciprocal Rank Fusion (RRF) — Most Popular
(Detail neeche section 6 me)

### 5.3 Alpha Weighting (Weaviate Style)
(Detail neeche section 7 me)

---

## 6. Reciprocal Rank Fusion (RRF) — Deep Dive

**Simple Meaning:** RRF **actual scores ignore karta hai**, sirf **rank/position** dekhta hai — kyunki different systems ke scores compare karna mushkil hai, lekin "rank" (1st, 2nd, 3rd...) universal hai.

### Formula
```
RRF_score(document) = Σ [ 1 / (k + rank_in_list_i) ]
```
- `rank_in_list_i` = us document ki position us particular search method (BM25 ya Vector) ke result list me
- `k` = ek constant (usually **60**) — jo bahut low ranks (jaise rank 1) ko bahut zyada dominate hone se rokta hai

### Example

| Document | BM25 Rank | Vector Rank |
|---|---|---|
| Doc A | 1 | 3 |
| Doc B | 2 | 1 |
| Doc C | 3 | 2 |

Using k = 60:
```
RRF(Doc A) = 1/(60+1) + 1/(60+3) = 0.0164 + 0.0159 = 0.0323
RRF(Doc B) = 1/(60+2) + 1/(60+1) = 0.0161 + 0.0164 = 0.0325
RRF(Doc C) = 1/(60+3) + 1/(60+2) = 0.0159 + 0.0161 = 0.0320
```

**Final Ranking:** Doc B > Doc A > Doc C (highest RRF score wins)

### Why RRF is Popular
- ✅ **Score normalization ki zaroorat nahi** — bas ranks use hoti hain, isliye scale-mismatch problem solve ho jati hai.
- ✅ Simple, robust, aur bahut systems (Elasticsearch, Weaviate, LangChain) me built-in support hai.
- ✅ Multiple retrieval methods (sirf 2 nahi, 3-4 bhi) ko easily combine kar sakte ho.

---

## 7. Alpha Weighting Method

**Simple Meaning:** Ek single parameter **alpha (α)** use karke, aap manually decide karte ho ki final score me **kitna weight BM25 ko** aur **kitna weight Vector search ko** dena hai.

```
Final Score = α × (vector_score) + (1 - α) × (BM25_score)
```

| Alpha Value | Behavior |
|---|---|
| α = 1.0 | 100% Vector search (pure semantic) |
| α = 0.0 | 100% BM25 (pure keyword search) |
| α = 0.5 | Equal weight to both |

### When to Adjust Alpha
- Agar aapke queries me **exact terms/codes zyada** important hain (technical docs, legal) → alpha ko **kam** rakho (BM25 ko zyada weight)
- Agar queries **natural language/conversational** hain → alpha ko **zyada** rakho (vector search ko zyada weight)

> Weaviate jaisi vector databases me yeh `alpha` parameter directly configure kiya ja sakta hai query time pe.

---

## 8. Implementation Approaches

### 8.1 Using LangChain (Conceptual)
```python
from langchain.retrievers import EnsembleRetriever

bm25_retriever = BM25Retriever.from_documents(docs)
vector_retriever = vector_store.as_retriever()

hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6]   # 40% BM25, 60% Vector
)

results = hybrid_retriever.invoke("your query here")
```

### 8.2 Using Weaviate (Built-in Hybrid Search)
```python
results = client.query.get("Article", ["title", "content"]) \
    .with_hybrid(query="your query", alpha=0.5) \
    .with_limit(5) \
    .do()
```

---

## 9. Popular Tools/Databases Supporting Hybrid Search

| Tool/DB | Hybrid Search Support |
|---|---|
| **Weaviate** | Native, built-in `alpha` parameter |
| **Elasticsearch/OpenSearch** | Strong support — combines BM25 + kNN vector search |
| **Qdrant** | Supports combining sparse + dense vectors |
| **Pinecone** | Supports sparse-dense hybrid vectors |
| **LangChain (EnsembleRetriever)** | Framework-level combination of any retrievers |

---

## 10. When to Use Hybrid Search vs Pure Vector Search

| Situation | Recommended |
|---|---|
| Queries have technical terms, IDs, codes, names | **Hybrid Search** |
| Purely conversational/natural language queries | Vector Search alone might be enough |
| Legal, medical, technical documentation (precision matters) | **Hybrid Search** (almost always better here) |
| General knowledge Q&A / chatbots | Vector Search alone often sufficient, but Hybrid still improves accuracy |
| Need best possible accuracy, cost/latency not a big concern | **Hybrid Search** (generally recommended default in production RAG) |

> **Industry consensus (as of recent RAG research):** Hybrid Search almost always **outperforms pure vector search alone** in production systems — it's become close to a "best practice default" for serious RAG applications.

---

## 11. Common Mistakes

| Mistake | Problem | Fix |
|---|---|---|
| Directly adding BM25 + Cosine scores without normalization | Scores are on different scales — misleading results | Use RRF or normalize scores before combining |
| Using a fixed alpha for all query types | Some queries need more keyword weight, others more semantic | Consider dynamic alpha tuning or just use RRF (scale-independent) |
| Not testing with real user queries | Assumes hybrid always better without validation | A/B test on your actual data/queries |
| Ignoring computational cost | Running two search systems doubles retrieval cost/latency | Consider caching, parallel execution, or simpler methods if latency-critical |

---

## 12. Cheat Sheet

### One-Line Memory Tricks
- **Hybrid Search** → "Keyword match + Meaning match, dono jodo"
- **RRF** → "Score bhool jao, sirf rank dekho aur combine karo"
- **Alpha Weighting** → "Ek dial se decide karo kitna keyword, kitna semantic"

### Quick Recap Flow
```
Query
  ├─→ BM25 (keyword match)     → Ranked List A
  └─→ Vector Search (semantic) → Ranked List B
         │
         ▼
   Combine using RRF or Alpha Weighting
         │
         ▼
   Final Hybrid Ranked Results → Passed to LLM
```

### Golden Rule
> **"Keywords ke liye BM25 bharosemand hai, meaning ke liye Vector Search — production RAG me dono ko saath use karo, akela mat chhodo."**
