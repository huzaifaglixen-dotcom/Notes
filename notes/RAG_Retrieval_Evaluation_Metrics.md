# RAG Evaluation — Retrieval Metrics Notes

> Focus: How to evaluate the **Retrieval part** of RAG (Retrieval-Augmented Generation)
> These metrics tell us — did the system fetch the **right chunks**, in the **right order**, without missing important ones?

---

## Quick Overview Table

| Metric | Question it Answers | Focus |
|---|---|---|
| Hit Rate | Was the correct chunk retrieved at all? | Presence |
| MRR | At what position was the first correct chunk found? | Ranking (early hit) |
| Precision | Out of retrieved chunks, how many are relevant? | Quality of retrieved set |
| Recall | Out of all relevant chunks, how many were retrieved? | Completeness |
| NDCG | Are highly relevant chunks ranked higher than less relevant ones? | Ranking quality (graded) |

---

## 1. Hit Rate

**Simple meaning:** Chunk sahi retrieve hua ya nahi — bas yes/no check.

**Definition:** For a given query, did **at least one** relevant/correct chunk appear anywhere in the top-K retrieved results?

### Formula
```
Hit Rate = (Number of queries where at least 1 relevant chunk was retrieved) / (Total number of queries)
```

### Example
- You ask 10 questions.
- For 8 of them, the correct chunk appeared somewhere in top-5 results.
- Hit Rate = 8/10 = **0.8 (80%)**

### Key Points
- It does **not care about position** — even if the correct chunk is at rank 5, it still counts as a "hit".
- It does **not care how many** relevant chunks were retrieved — just "at least one".
- Good for a **quick, simple check**: "Is retrieval even working?"
- Weakness: Doesn't tell you about ranking quality or completeness.

---

## 2. Mean Reciprocal Rank (MRR)

**Simple meaning:** Position of the current right retrieved chunk — kitni jaldi sahi chunk mila.

**Definition:** Measures **how early** the first correct/relevant chunk appears in the retrieved list.

### Formula
```
Reciprocal Rank (per query) = 1 / (rank position of first relevant chunk)

MRR = (Sum of Reciprocal Ranks for all queries) / (Total number of queries)
```

### Example

| Query | Rank of first correct chunk | Reciprocal Rank |
|---|---|---|
| Q1 | 1st position | 1/1 = 1.0 |
| Q2 | 3rd position | 1/3 = 0.33 |
| Q3 | Not found | 0 |

```
MRR = (1.0 + 0.33 + 0) / 3 = 0.44
```

### Key Points
- **Higher MRR = correct chunks are found earlier** (closer to rank 1).
- Only considers the **first relevant result** — ignores if more relevant chunks exist later.
- Great for cases where **only one correct answer/chunk matters** (e.g., FAQ bot, single-fact lookup).
- Range: 0 to 1 (1 = always found at rank 1).

---

## 3. Precision

**Simple meaning:** Retrieved chunks me se kitne useful the — "Retrieved → Useful" ka ratio.

**Definition:** Out of all the chunks retrieved, what fraction are actually relevant?

### Formula
```
Precision = (Number of Relevant Chunks Retrieved) / (Total Number of Chunks Retrieved)
```

### Example
- System retrieves **top 5 chunks**.
- Out of these, **3 are actually relevant**, 2 are irrelevant/noise.
```
Precision = 3/5 = 0.6 (60%)
```

### Key Points
- High precision = **less noise/junk** in retrieved results.
- Doesn't care if you **missed** other relevant chunks elsewhere (that's Recall's job).
- Often measured as **Precision@K** (e.g., Precision@5, Precision@10) — precision considering only top-K results.
- Tradeoff: Retrieving very few chunks can boost precision but hurt recall.

---

## 4. Recall

**Simple meaning:** Jo useful tha (total relevant chunks), usme se kitne retrieve hue — "Useful → Retrieved" ka ratio.

**Definition:** Out of all the truly relevant chunks that exist, how many did the system actually retrieve?

### Formula
```
Recall = (Number of Relevant Chunks Retrieved) / (Total Number of Relevant Chunks that Exist)
```

### Example
- Suppose there are **6 relevant chunks** in total (ground truth) for a query.
- System retrieves **3 of them** correctly.
```
Recall = 3/6 = 0.5 (50%)
```

### Key Points
- High recall = **system doesn't miss** important information.
- Doesn't care about junk/noise mixed in (that's Precision's job).
- Often measured as **Recall@K**.
- Tradeoff: Retrieving more chunks (higher K) usually increases recall but can lower precision.

### Precision vs Recall — Simple Analogy
> Imagine fishing in a pond with 10 fish (relevant) and 20 rocks (irrelevant).
> - **Precision** = out of everything you caught, how many were fish?
> - **Recall** = out of all 10 fish in the pond, how many did you actually catch?

---

## 5. Normalized Discounted Cumulative Gain (NDCG)

**Simple meaning:** Sirf yeh nahi ki relevant chunk mila ya nahi — balki **kitna relevant** tha, aur **kaha rank pe** tha, dono important hain.

Unlike Hit Rate/Precision/Recall (which are usually binary: relevant or not), NDCG works with **graded relevance** — e.g., a chunk can be "highly relevant" (score 3), "somewhat relevant" (score 2), "slightly relevant" (score 1), or "not relevant" (score 0).

### Step-by-Step Concept

**Step 1: Cumulative Gain (CG)**
```
CG = Sum of relevance scores of retrieved chunks (no position discount)
```

**Step 2: Discounted Cumulative Gain (DCG)**
Chunks ranked lower get "discounted" — because a user is less likely to scroll down and see them.
```
DCG = Σ ( relevance_score_i / log2(i + 1) )   for i = 1 to K
```
(i = rank position of the chunk)

**Step 3: Ideal DCG (IDCG)**
This is the **best possible DCG** — if chunks were sorted in perfect order (most relevant first).

**Step 4: Normalized DCG (NDCG)**
```
NDCG = DCG / IDCG
```

### Example

Suppose relevance scores (0–3) of retrieved chunks in the order they appear:

| Rank | Chunk | Relevance Score |
|---|---|---|
| 1 | A | 3 |
| 2 | B | 0 |
| 3 | C | 2 |

```
DCG = 3/log2(2) + 0/log2(3) + 2/log2(4)
    = 3/1 + 0/1.58 + 2/2
    = 3 + 0 + 1
    = 4.0
```

Now, Ideal order would be: 3, 2, 0 (highest relevance first)
```
IDCG = 3/log2(2) + 2/log2(3) + 0/log2(4)
     = 3 + 1.26 + 0
     = 4.26
```

```
NDCG = DCG / IDCG = 4.0 / 4.26 ≈ 0.94
```

### Key Points
- **Range: 0 to 1** (1 = perfect ranking, most relevant chunks are at the top).
- Best metric when **relevance is not just yes/no but has levels/grades**.
- Rewards systems that put **highly relevant chunks at the top**, penalizes if they're buried lower.
- Commonly reported as **NDCG@K** (e.g., NDCG@5, NDCG@10).

---

## Summary Cheat Sheet

| Metric | Binary or Graded? | Cares about Order? | Cares about Completeness? | Best Used When |
|---|---|---|---|---|
| **Hit Rate** | Binary | ❌ No | ❌ No | Quick sanity check |
| **MRR** | Binary | ✅ Yes (first hit only) | ❌ No | Single correct-answer tasks |
| **Precision** | Binary | ❌ No | ❌ No | Checking noise/junk in results |
| **Recall** | Binary | ❌ No | ✅ Yes | Checking if anything important is missed |
| **NDCG** | Graded | ✅ Yes (full ranking) | Partially | Best overall ranking quality metric |

---

## One-Line Memory Trick

- **Hit Rate** → "Mila ya nahi?"
- **MRR** → "Kitni jaldi mila?"
- **Precision** → "Jo mila, usme kitna sahi tha?"
- **Recall** → "Jo sahi tha, usme kitna mila?"
- **NDCG** → "Sahi cheez sahi jagah (top) pe thi ya nahi?"
