# BM25 Algorithm — Notes

> BM25 (Best Matching 25) is a **ranking algorithm** used in search engines and RAG retrieval systems to score how relevant a document is to a given query.
> Yeh **keyword-based (sparse) retrieval** algorithm hai — matlab yeh exact word matching pe kaam karta hai (embeddings/meaning wale semantic search se alag).

---

## Simple Meaning

BM25 batata hai: **"Yeh document is query ke liye kitna relevant hai?"**

Isko score karne ke liye teen cheezein dekhta hai:
1. Query ke words document me **kitni baar aaye** (Term Frequency)
2. Woh word **kitna rare/common** hai poore corpus me (Inverse Document Frequency)
3. Document ki **length** — kaheen document sirf lamba hone ki wajah se zyada match toh nahi kar raha (Length Normalization)

---

## Why BM25? (Background)

- Purana simple method tha **TF (Term Frequency)** — jitni baar word aaya utna zyada score. Problem: common words (the, is, a) bhi high score paate the.
- Fir aaya **TF-IDF** — rare words ko zyada importance di gayi.
- **BM25** TF-IDF ka hi improved/smarter version hai — yeh **saturation** (ek limit ke baad word repeat hone ka effect kam karna) aur **document length normalization** bhi handle karta hai.

---

## The Formula

```
                    N
BM25(D, Q) = Σ  IDF(qi) × [ f(qi, D) × (k1 + 1) ] / [ f(qi, D) + k1 × (1 - b + b × |D|/avgdl) ]
                   i=1
```

Yeh dekhne me complex lagta hai, par har part ko todke samjhte hain 👇

---

## Breaking Down Each Part

### 1. IDF(qi) — Inverse Document Frequency

**Simple meaning:** Yeh word kitna **rare/special** hai poore corpus (saare documents) me.

```
IDF(qi) = log( (N - n(qi) + 0.5) / (n(qi) + 0.5) + 1 )
```

- `N` = total number of documents in the corpus
- `n(qi)` = number of documents that contain the term `qi`

**Intuition:**
- Agar word bahut common hai (jaise "the", "is") → **low IDF** (kam importance)
- Agar word rare hai (jaise "photosynthesis") → **high IDF** (zyada importance)

> Rare word mile toh matlab match "special" hai, common word mile toh koi badi baat nahi.

---

### 2. f(qi, D) — Term Frequency in Document

**Simple meaning:** Query ka word `qi`, document `D` me **kitni baar aaya**.

- Jitni baar word repeat hua, utna zyada relevant maana jayega — **but with a limit** (saturation), isiliye neeche `k1` aata hai.

---

### 3. k1 — Term Frequency Saturation Parameter

**Simple meaning:** Yeh control karta hai ki word repeat hone ka effect **kitni jaldi saturate (flatten)** ho jaye.

- Typical value: **k1 = 1.2 to 2.0**
- Agar word 1 baar aaya vs 20 baar aaya — bina saturation ke, 20 baar wale ka score bahut zyada high ho jayega (jo galat hai, kyunki keyword-stuffing possible hai).
- BM25 isko control karta hai — after a point, extra repetitions ka score pe bahut kam effect padta hai.

> Socho: Ek genuine article me keyword 3-4 baar aana natural hai, lekin 50 baar aana spam jaisa lagta hai — BM25 uss "diminishing returns" ko handle karta hai.

---

### 4. b — Length Normalization Parameter

**Simple meaning:** Yeh control karta hai ki document ki **length** kitna effect dalti hai score pe.

- Typical value: **b = 0.75**
- Range: 0 (no length normalization) to 1 (full length normalization)

```
|D|    = length of document D (number of words)
avgdl  = average document length across the whole corpus
```

**Intuition:**
- Bina normalization ke, **lambe documents** naturally zyada word-matches paayenge (bas iss wajah se ki unme zyada text hai) — yeh unfair advantage hai.
- `b` isko balance karta hai — chota document agar relevant hai toh usko bhi fair chance milta hai lambe document ke against.

---

## Putting It All Together — Full Intuition

For each query word:
```
Score = IDF(word) × [ (word repeats in doc) adjusted for saturation and doc length ]
```

Final document score = **sum of scores for all query words**.

---

## Worked Example (Simplified)

**Query:** "cat food"

**Document A:** "The cat loves cat food and cat toys" (word "cat" appears 3 times, document is short)
**Document B:** "A very long article about pets, animals, dogs, cats, and various food items across many pages..." (word "cat" appears once, but document is very long)

| Factor | Document A | Document B |
|---|---|---|
| Term Frequency of "cat" | High (3) | Low (1) |
| Document Length | Short | Very Long |
| Effect | Score is high, and not too long so no penalty | Score is diluted — even though "cat" appeared, document length brings score down |

**Result:** BM25 will likely rank **Document A higher** — it has good keyword frequency without being unnaturally long.

---

## BM25 vs TF-IDF vs Semantic Search (Embeddings)

| Feature | TF-IDF | BM25 | Semantic Search (Embeddings) |
|---|---|---|---|
| Based on | Exact word match | Exact word match (smarter) | Meaning/context (vectors) |
| Handles synonyms? | ❌ No | ❌ No | ✅ Yes |
| Handles saturation (repeated words)? | ❌ No | ✅ Yes (via k1) | N/A |
| Handles document length bias? | ❌ Weak | ✅ Yes (via b) | N/A |
| Good for | Simple keyword search | Robust keyword-based search | Understanding intent/meaning |
| Common use today | Legacy systems | Hybrid RAG search (with vectors) | Modern RAG search |

> **Note:** In modern RAG systems, BM25 is often combined with vector/embedding search — this is called **Hybrid Search**. BM25 catches exact keyword matches (e.g., product codes, names), while embeddings catch semantic/meaning-based matches.

---

## Key Parameters Summary

| Parameter | Meaning | Typical Value |
|---|---|---|
| `k1` | Controls term frequency saturation | 1.2 – 2.0 |
| `b` | Controls document length normalization | 0.75 |
| `N` | Total documents in corpus | Depends on dataset |
| `n(qi)` | Number of docs containing word `qi` | Depends on dataset |
| `avgdl` | Average document length in corpus | Depends on dataset |

---

## Why BM25 Still Matters in RAG (2024-2026 era)

- Even with powerful embedding models, BM25 is still used because:
  - It's **fast** and **cheap** (no GPU needed).
  - It's **great at exact matches** — IDs, names, codes, rare technical terms that embeddings sometimes miss.
  - Combined with vector search in **Hybrid RAG**, it improves overall retrieval accuracy (Hit Rate, Recall, NDCG — the metrics from your previous notes!).

---

## One-Line Memory Trick

> **BM25 = "Kitni baar mila (TF) × Kitna rare hai (IDF) — lekin bahut zyada repeat aur bahut lamba document mat gin"**

- **k1** → "Repeat hone ki himmat kam karo after a point"
- **b** → "Lamba document hone ka fayda mat do"
- **IDF** → "Rare word = zyada importance"
