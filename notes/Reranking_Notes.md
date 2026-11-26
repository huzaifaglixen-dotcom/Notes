# Reranking — Complete Notes

> **Reranking** = Retrieval ke **baad** ka ek extra step, jisme initially retrieve kiye gaye chunks ko **ek zyada powerful (lekin slower) model** se dobara score/order kiya jata hai, taaki **sabse relevant chunks top pe** aa jayein.

---

## Table of Contents
1. Why Reranking is Needed
2. Two-Stage Retrieval Pipeline (Concept)
3. Bi-Encoders vs Cross-Encoders
4. How Reranking Works (Step-by-Step)
5. Popular Rerankers
6. Implementation Example
7. Reranking Metrics Impact
8. Cost/Latency Tradeoffs
9. When to Use Reranking
10. Common Mistakes
11. Cheat Sheet

---

## 1. Why Reranking is Needed

Vector search / hybrid search **fast** hote hain, lekin unki similarity calculation thodi **"approximate/rough"** hoti hai — kyunki wo speed ke liye optimize kiye gaye hote hain (millions of documents me se milliseconds me search karna hai).

**Problem:** Top-K retrieval (jaise top-20 chunks) me se, **hamesha sabse relevant chunk #1 position pe nahi hota** — kabhi wo #5 ya #10 pe hota hai, aur kam relevant chunk upar aa jata hai.

**Solution:** Reranking — ek **zyada accurate lekin slower model** use karo, sirf un **thoda thoda chunks (jaise top-20)** pe — taaki unhe **precisely dobara order** kiya ja sake.

> Analogy: Socho ek **job interview process**:
> - **Stage 1 (Retrieval):** Resume screening — jaldi se 1000 applications me se 20 shortlist karna (rough filter, fast)
> - **Stage 2 (Reranking):** In-depth interview — un 20 shortlisted logon ko **detail se evaluate** karke best 3 choose karna (slow, precise)

---

## 2. Two-Stage Retrieval Pipeline (Concept)

```
Stage 1: Initial Retrieval (Fast, Approximate)
   Vector Search / Hybrid Search / BM25
   → Millions of documents → Top 20-50 candidates
              │
              ▼
Stage 2: Reranking (Slow, Precise)
   Cross-Encoder / Rerank Model
   → Top 20-50 candidates → Re-scored → Top 3-5 final results
              │
              ▼
   Final Results → Passed to LLM for Generation
```

> **Key Idea:** Reranking **replace nahi karta** initial retrieval ko — yeh usko **refine/improve** karta hai. Pehle bahut sare documents me se fast filter karo, phir un chhote se set ko accurately re-order karo.

---

## 3. Bi-Encoders vs Cross-Encoders

Yeh concept samajhna reranking ke liye sabse zaroori hai.

### 3.1 Bi-Encoder (Jo Normal Vector Search Use Karta Hai)

**Simple Meaning:** Query aur Document **alag-alag, independently** embed kiye jate hain. Phir unke embeddings ke beech similarity (cosine, etc.) calculate ki jati hai.

```
Query    → Embedding Model → Vector A
Document → Embedding Model → Vector B

Similarity = cosine(Vector A, Vector B)
```

- ✅ **Fast** — documents ke embeddings pehle se precompute karke store kiye ja sakte hain.
- ❌ Query aur document **ek doosre ko "dekhe" bina** independently process hote hain — isliye subtle relevance nuances miss ho sakte hain.

### 3.2 Cross-Encoder (Jo Reranking Use Karta Hai)

**Simple Meaning:** Query aur Document ko **saath me, ek hi input ki tarah** model ko diya jata hai — model dono ko **ek saath dekhkar** ek direct relevance score deta hai.

```
Input: [Query + Document] together → Cross-Encoder Model → Relevance Score (0 to 1)
```

- ✅ **Bahut zyada accurate** — kyunki model query aur document ke beech ka **actual interaction/relationship** deep level pe samajhta hai.
- ❌ **Slow** — har query-document pair ke liye alag se model run karna padta hai (precompute/cache nahi kar sakte, kyunki query har baar naya hota hai).

### Side-by-Side Comparison

| Feature | Bi-Encoder | Cross-Encoder |
|---|---|---|
| Processing | Query & Document alag-alag | Query & Document saath me |
| Speed | ✅ Very Fast | ❌ Slow |
| Accuracy | Good, but approximate | ✅ Much more accurate |
| Scalability | ✅ Millions of docs easily | ❌ Only feasible on small candidate sets |
| Use Case | Initial/Stage-1 Retrieval | Stage-2 Reranking |

> Isiliye pipeline **dono ko combine** karta hai — Bi-Encoder se fast initial filter, Cross-Encoder se precise final reranking.

---

## 4. How Reranking Works (Step-by-Step)

1. User query aati hai.
2. **Stage 1:** Vector/Hybrid search se top-20 (ya top-50) candidate chunks retrieve kiye jate hain (Bi-Encoder based, fast).
3. **Stage 2:** Har candidate chunk ko query ke saath **pair** banakar Cross-Encoder/Rerank model ko diya jata hai.
4. Rerank model har pair ko ek **relevance score** deta hai.
5. Chunks ko is **naye score** ke hisaab se **re-sort** kiya jata hai.
6. Top 3-5 (final) chunks LLM ko generation ke liye diye jate hain.

### Example

**Query:** "What are the side effects of ibuprofen?"

**Initial Retrieval (Vector Search) — Top 5, unordered by true relevance:**
```
1. General info about pain relievers (medium relevance)
2. Ibuprofen dosage instructions (medium relevance)
3. Ibuprofen side effects and warnings (HIGH relevance) ← should be #1!
4. History of NSAIDs (low relevance)
5. Ibuprofen vs Acetaminophen comparison (medium relevance)
```

**After Reranking (Cross-Encoder re-scores each):**
```
1. Ibuprofen side effects and warnings (HIGH relevance) ✅ now correctly #1
2. Ibuprofen vs Acetaminophen comparison
3. Ibuprofen dosage instructions
4. General info about pain relievers
5. History of NSAIDs
```

> Reranking ne sabse relevant chunk ko **top pe** move kar diya — jo pehle #3 pe tha.

---

## 5. Popular Rerankers

| Reranker | Provider | Notes |
|---|---|---|
| **Cohere Rerank (rerank-3)** | Cohere | Very popular, API-based, easy to integrate, strong performance |
| **Voyage Rerank** | Voyage AI | High quality, works well with Claude-based RAG apps |
| **BGE Reranker** | BAAI (open-source) | Free, self-hostable |
| **ms-marco Cross-Encoders (sentence-transformers)** | Open-source | Lightweight, good for self-hosted setups |
| **Jina Reranker** | Jina AI | Supports long documents, multilingual |

---

## 6. Implementation Example (Conceptual — Cohere Rerank)

```python
import cohere

co = cohere.Client("API_KEY")

candidates = [
    "Ibuprofen dosage instructions...",
    "Ibuprofen side effects and warnings...",
    "History of NSAIDs...",
    # ... more retrieved chunks
]

response = co.rerank(
    query="What are the side effects of ibuprofen?",
    documents=candidates,
    top_n=3,
    model="rerank-english-v3.0"
)

for result in response.results:
    print(result.index, result.relevance_score)
```

---

## 7. Reranking Metrics Impact

Reranking directly improves the retrieval metrics aapne pehle seekhe the:

| Metric | Reranking ka Impact |
|---|---|
| **Precision@K** | ✅ Improves — kyunki top positions me ab zyada relevant chunks hain |
| **NDCG** | ✅ Significantly improves — kyunki ranking order ab true relevance ke zyada close hai |
| **MRR** | ✅ Improves — sabse relevant chunk aksar #1 rank pe aa jata hai reranking ke baad |
| **Recall** | ⚪ No change — reranking sirf **order** badalta hai, initial retrieval already jo chunks laaya tha, usi set me se choose karta hai. Agar relevant chunk stage-1 me hi miss ho gaya, reranking usko wapas nahi la sakta. |

> **Important:** Reranking **Recall improve nahi karta** — agar Stage-1 retrieval ne relevant chunk ko bilkul miss kar diya (top-20 me bhi nahi laya), toh reranking uska kuch nahi kar sakta. Isliye Stage-1 (initial retrieval) ko bhi accha rakhna zaroori hai.

---

## 8. Cost/Latency Tradeoffs

| Aspect | Without Reranking | With Reranking |
|---|---|---|
| Latency | Fast (single vector search) | Thoda slower (extra API/model call) |
| Cost | Lower | Higher (extra compute/API cost per query) |
| Accuracy | Good | Better |

> **Practical Tip:** Reranking sirf **top-K candidates** (jaise 20-50) pe hoti hai, poore database pe nahi — isliye extra latency **manageable** hoti hai (usually 100-300ms extra), jo accuracy improvement ke liye worth hota hai production systems me.

---

## 9. When to Use Reranking

| Situation | Recommended? |
|---|---|
| High-stakes accuracy needed (legal, medical, finance) | ✅ Definitely use reranking |
| Simple FAQ bot with small document set | ⚪ Optional — initial retrieval might already be good enough |
| Large-scale production RAG system | ✅ Almost always recommended |
| Extremely latency-sensitive application (real-time, <100ms) | ⚠️ Consider carefully — reranking adds latency |
| Budget-constrained project | ⚠️ Weigh cost vs accuracy improvement |

---

## 10. Common Mistakes

| Mistake | Problem | Fix |
|---|---|---|
| Reranking too many candidates (e.g., 500) | Very slow, defeats the purpose | Keep candidate set small (top 20-50) before reranking |
| Expecting reranking to fix bad initial retrieval | Reranking can't recover chunks that were never retrieved | Ensure Stage-1 retrieval (embeddings/hybrid search) is solid first |
| Not measuring before/after impact | Don't know if reranking actually helped | A/B test with metrics like NDCG/Precision before deploying |
| Using reranking on every single query regardless of need | Unnecessary cost/latency for simple queries | Consider conditional reranking (only for complex/ambiguous queries) |

---

## 11. Cheat Sheet

### One-Line Memory Tricks
- **Reranking** → "Pehle jaldi filter karo, phir dhyan se dobara order karo"
- **Bi-Encoder** → "Query aur Doc alag-alag dekhta hai — fast"
- **Cross-Encoder** → "Query aur Doc saath me dekhta hai — accurate but slow"
- **Reranking improves** → Precision, NDCG, MRR
- **Reranking does NOT improve** → Recall (can't fix what Stage-1 missed)

### Quick Recap Flow
```
Query
  │
  ▼
Stage 1: Fast Retrieval (Bi-Encoder / Vector or Hybrid Search)
  → Top 20-50 candidates
  │
  ▼
Stage 2: Reranking (Cross-Encoder — Cohere/Voyage/BGE Rerank)
  → Precisely re-scored and re-ordered
  │
  ▼
Top 3-5 Final Chunks → Sent to LLM for Answer Generation
```

### Golden Rule
> **"Retrieval finds the candidates fast; Reranking finds the truth precisely — use both together for best RAG accuracy."**
