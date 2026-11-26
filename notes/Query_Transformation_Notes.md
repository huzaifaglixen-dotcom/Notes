# Query Transformation — Complete Notes

> **Query Transformation** = User ki original query ko retrieval se **pehle modify/improve/expand** karna, taaki **better/more relevant chunks** retrieve ho sakein.

---

## Table of Contents
1. Why Query Transformation is Needed
2. Query Rewriting
3. HyDE (Hypothetical Document Embeddings)
4. Multi-Query Retrieval
5. Step-Back Prompting
6. Query Decomposition
7. Comparison of All Techniques
8. When to Use Which Technique
9. Common Mistakes
10. Cheat Sheet

---

## 1. Why Query Transformation is Needed

User ki original query hamesha **retrieval ke liye "ideal"** nahi hoti:
- Query bahut **short/vague** ho sakti hai ("fix this")
- Query me **typos/grammar issues** ho sakte hain
- Query **conversational** ho sakti hai lekin documents **formal/technical language** me likhe hain
- Query **complex/multi-part** ho sakti hai jisme multiple sub-questions chhupe hain

> Analogy: Socho aap ek library me librarian se poochte ho "Woh book chahiye jisme scientist wali cheez thi" — librarian ko exact book dhoondhna mushkil hoga. Agar aap query ko **refine/clarify** karke poochte ho ("Marie Curie ki biography chahiye, jo radioactivity pe hai"), librarian **turant sahi book de dega**. Query Transformation yehi refining process automate karta hai.

---

## 2. Query Rewriting

**Simple Meaning:** User ki query ko ek LLM se **behtar, clearer, ya retrieval-friendly** version me rewrite karwana.

### How It Works
```
Original Query: "that error thing from yesterday, how to fix?"
         │
         ▼ (LLM rewrites)
Rewritten Query: "How to fix the [specific error type] that occurred yesterday?"
```

### Common Use Cases
- **Conversational → Standalone:** Chat history ke context ko query me merge karna
```
Chat History: "Tell me about Python decorators" → "How do I use them with classes?"
Rewritten Query: "How do I use Python decorators with classes?"
```
(Yeh especially zaroori hai multi-turn conversations me, jahan follow-up questions pichle context pe depend karte hain)

- **Typo/Grammar Correction:** Spelling mistakes fix karna before embedding
- **Ambiguity Resolution:** Vague terms ko specific karna

### Example Prompt (Conceptual)
```
"Given the conversation history and the latest user question, rewrite the question 
to be a standalone, clear question that can be understood without the conversation history.

History: {chat_history}
Latest Question: {user_question}
Rewritten Standalone Question:"
```

---

## 3. HyDE (Hypothetical Document Embeddings)

**Simple Meaning:** Query ko directly embed karne ke bajaye, pehle LLM se ek **"hypothetical" (imaginary/fake) answer/document** generate karwao us query ke liye, phir **usi hypothetical document ko embed karke search** karo.

### Why This Works (The Insight)
- Queries aksar **short aur question-style** hoti hain ("What causes diabetes?")
- Documents/chunks **longer aur statement-style** hote hain ("Diabetes is caused by insulin resistance...")
- Question-style text aur statement-style text ke embeddings, **thoda "mismatch"** ho sakte hain (kyunki unka structure/style different hai)
- HyDE isko fix karta hai — pehle ek "fake statement-style answer" bana lo, jo **actual documents ke style se zyada match karega**, phir usko embed karke search karo.

### Step-by-Step

```
1. User Query: "What causes diabetes?"
2. LLM generates a hypothetical answer (may be factually imperfect, that's OK):
   "Diabetes is caused by the body's inability to properly regulate blood sugar 
   levels, often due to insulin resistance or insufficient insulin production..."
3. This HYPOTHETICAL document is embedded (not the original query)
4. Vector search is performed using THIS embedding
5. Real, actual relevant documents are retrieved (because their embeddings are 
   "style-similar" to the hypothetical one)
```

### Key Point
> Yeh hypothetical document **khud kabhi user ko nahi dikhaya jata** — yeh sirf ek **"better search query" banane ka intermediate step** hai. Actual answer, retrieved real documents se hi generate hota hai.

### Pros & Cons
- ✅ Short/vague queries ke liye retrieval quality improve karta hai
- ✅ Especially useful jab query aur documents ka "style" bahut different ho
- ❌ Extra LLM call chahiye (cost/latency badhta hai)
- ❌ Agar hypothetical document bahut off-track ban jaye, retrieval bhi galat direction me ja sakta hai

---

## 4. Multi-Query Retrieval

**Simple Meaning:** Ek hi original query se, LLM **multiple alag-alag phrasings/perspectives** generate karta hai, phir **har version se alag se retrieval** karta hai, aur sabke results ko **combine/deduplicate** karke final set banata hai.

### Why This Works
- Ek hi query ko **alag tarike se poochne** se, alag-alag relevant chunks mil sakte hain (jo ek single phrasing se miss ho jate).
- Yeh recall improve karta hai — zyada "angles" se search karne se, chhupe hue relevant chunks bhi mil jate hain.

### Step-by-Step

```
Original Query: "How do I improve team productivity?"

LLM generates variations:
1. "What are effective strategies to boost team performance?"
2. "How can managers increase employee efficiency?"
3. "Ways to make a team work more productively"

For each variation → Run vector search → Get results
Combine all results → Remove duplicates → Final retrieved set
```

### Pros & Cons
- ✅ Recall improve hota hai (multiple angles se search)
- ✅ Ambiguous queries ke liye robust
- ❌ Multiple retrieval calls chahiye (zyada latency/cost)
- ❌ Zyada results ko combine/dedupe karna extra complexity hai

---

## 5. Step-Back Prompting

**Simple Meaning:** Specific/detailed query se pehle, ek **"zoomed-out", more general/abstract question** poochna — taaki broader context mil sake jo specific answer ko better support kare.

### Example
```
Original Query: "What was the temperature at which water boiled in the experiment 
conducted on July 15th at Stanford Lab?"

Step-Back Question: "What are the general principles of water's boiling point 
and factors that affect it (altitude, pressure)?"

Both queries are used for retrieval:
- Step-back query gets general/foundational context
- Original query gets specific details

Both retrieved contexts are combined for the final answer generation.
```

### Why This Works
- Complex/specific questions often **need broader context** to be answered correctly.
- Retrieving only hyper-specific chunks might miss **foundational information** needed to properly interpret them.

---

## 6. Query Decomposition

**Simple Meaning:** Ek **complex, multi-part query** ko chhote, **independent sub-questions** me todna, har ek ko alag se retrieve/answer karna, phir results ko combine karna.

### Example
```
Original Query: "Compare the revenue growth of Company A and Company B over the 
last 3 years, and explain which factors contributed to the difference."

Decomposed Sub-Questions:
1. "What was Company A's revenue growth over the last 3 years?"
2. "What was Company B's revenue growth over the last 3 years?"
3. "What factors influenced Company A's revenue growth?"
4. "What factors influenced Company B's revenue growth?"

Each sub-question → retrieved separately → all context combined → final comprehensive answer
```

### Why This Works
- Complex queries me **multiple distinct information needs** hote hain — ek single retrieval call sabko cover nahi kar payegi achhe se.
- Sub-questions ko alag-alag retrieve karne se, **har part ke liye targeted, relevant chunks** milte hain.

---

## 7. Comparison of All Techniques

| Technique | Core Idea | Best For |
|---|---|---|
| **Query Rewriting** | Query ko clearer/standalone banana | Conversational/vague/typo-filled queries |
| **HyDE** | Fake answer banake usse search karna | Short queries, query-document style mismatch |
| **Multi-Query Retrieval** | Multiple phrasings se search karna | Improving recall, ambiguous queries |
| **Step-Back Prompting** | General question bhi poochna specific ke saath | Complex queries needing foundational context |
| **Query Decomposition** | Complex query ko sub-questions me todna | Multi-part, comparison-type queries |

---

## 8. When to Use Which Technique

| Situation | Recommended Technique |
|---|---|
| Multi-turn chatbot (follow-up questions) | Query Rewriting (standalone question conversion) |
| Very short/vague user queries | HyDE |
| Need to maximize recall, ambiguous phrasing | Multi-Query Retrieval |
| Complex questions needing broader context | Step-Back Prompting |
| Multi-part/comparison questions | Query Decomposition |
| Simple, clear, well-formed queries | None needed — direct retrieval is fine! |

> **Important:** Query Transformation **extra LLM calls** add karta hai (latency + cost). Simple, clear queries ke liye yeh overkill ho sakta hai — inhe **selectively** use karo, sirf jab genuinely retrieval quality improve ho.

---

## 9. Common Mistakes

| Mistake | Problem | Fix |
|---|---|---|
| Applying query transformation to every single query | Unnecessary latency/cost for simple queries | Use conditionally — detect when query is vague/complex first |
| Not testing if transformation actually helps | Assuming it improves results without validation | A/B test with retrieval metrics (Recall, NDCG) before/after |
| Using HyDE for very factual/specific queries | Hypothetical document might introduce inaccuracies that mislead retrieval | Use HyDE mainly for conceptual/broad queries, not precise fact lookups |
| Not deduplicating Multi-Query results | Redundant chunks passed to LLM, wasting context space | Always deduplicate combined results before passing to generation |
| Ignoring conversational context in multi-turn chats | Follow-up questions retrieved poorly without rewriting | Always rewrite to standalone question using chat history |

---

## 10. Cheat Sheet

### One-Line Memory Tricks
- **Query Rewriting** → "Vague/conversational query ko clear banao"
- **HyDE** → "Pehle fake answer likho, phir usse search karo"
- **Multi-Query** → "Ek query, kayi phrasings, sab se search karo"
- **Step-Back** → "General question bhi poocho specific ke saath"
- **Query Decomposition** → "Bade sawal ko chhote sawalon me todo"

### Quick Recap Flow
```
User Query
   │
   ▼
[Optional: Transform the query — Rewrite / HyDE / Multi-Query / Step-Back / Decompose]
   │
   ▼
Retrieval (using transformed query/queries)
   │
   ▼
Better, more relevant chunks retrieved → Passed to LLM
```

### Golden Rule
> **"The user's raw query isn't always the best search query — transforming it intelligently before retrieval often makes the difference between mediocre and great RAG results."**
