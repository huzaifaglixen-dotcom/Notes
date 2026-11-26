# Chunking in RAG — Complete Notes

> **Chunking** = Bade documents ko chhote-chhote pieces (chunks) me todna, taaki RAG system unhe efficiently store, search aur retrieve kar sake.
> Yeh RAG pipeline ka **sabse important step** hai — agar chunking galat hui, toh retrieval aur generation dono kharab honge, chahe embedding model kitna bhi accha ho.

---

## Why Chunking is Needed (Simple Reason)

1. **LLMs ki context window limited hoti hai** — pura document ek saath nahi de sakte.
2. **Embedding models** bhi ek limit tak hi text ko accurately represent kar sakte hain — bahut lamba text dene se meaning "dilute" ho jata hai.
3. **Precise Retrieval** — Chote, focused chunks se sirf relevant info milti hai, pura irrelevant document nahi.

> Analogy: Socho ek poori kitab ko dhoondhne ke bajaye, sirf uska relevant paragraph nikal ke doctor/lawyer ko dena — zyada useful hai.

---

## Golden Rule of Chunking

> **"Chunk chhota ho par complete meaning wala ho — na bahut chhota (context lost), na bahut bada (irrelevant info mix ho jaye)."**

---

## Overview Table — All Chunking Types

| Type | Based On | Complexity | Best For |
|---|---|---|---|
| Fixed-Size Chunking | Character/token count | ⭐ Easy | Simple, generic text |
| Recursive Character Chunking | Hierarchical separators (paragraph→sentence→word) | ⭐⭐ Medium | General purpose (most common default) |
| Sentence-Based Chunking | Sentence boundaries | ⭐⭐ Medium | Q&A, precise answers |
| Semantic Chunking | Meaning/similarity of text | ⭐⭐⭐ Advanced | High-accuracy RAG |
| Document-Based/Structural Chunking | Document structure (headings, sections) | ⭐⭐ Medium | Structured docs (manuals, legal, wiki) |
| Sliding Window Chunking | Overlapping fixed windows | ⭐⭐ Medium | Preserving context across boundaries |
| Agentic / LLM-Based Chunking | LLM decides chunk boundaries | ⭐⭐⭐⭐ Advanced | Complex, high-value documents |
| Table/Code-Aware Chunking | Special content type (tables, code) | ⭐⭐⭐ Advanced | Technical docs, code repos |
| Parent-Child Chunking | Two-level chunks (big + small) | ⭐⭐⭐ Advanced | Long structured docs needing context + precision |
| Late Chunking | Embed full doc first, split after | ⭐⭐⭐⭐ Advanced | Docs with heavy pronoun/reference usage, need context-aware embeddings |

---

## 1. Fixed-Size Chunking

**Simple Meaning:** Document ko ek fixed number of characters/tokens me todo — bas seedha count karke split karo.

### How it Works
- Choose a chunk size (e.g., 500 tokens or 1000 characters).
- Cut the text every N tokens/characters, regardless of sentence or paragraph boundaries.

### Example
```
Chunk size = 100 characters

Chunk 1: "The quick brown fox jumps over the lazy dog. Machine learning is a subs..."
Chunk 2: "et of artificial intelligence that focuses on..."
```
(Notice: word "subset" got cut in between — "subs" and "et" split across chunks!)

### Pros
- ✅ Very simple and fast to implement.
- ✅ Predictable chunk sizes (good for embedding models with token limits).

### Cons
- ❌ Can **cut sentences/words in the middle**, breaking meaning.
- ❌ Doesn't respect any natural structure of the document.

### When to Use
- Quick prototypes, simple projects, or when document structure doesn't matter much.

---

## 2. Recursive Character/Text Chunking (Most Common Default)

**Simple Meaning:** Pehle bade separators (paragraph) se todne ki koshish karo, agar chunk phir bhi bada hai, toh chhote separators (sentence, phir word) pe jao.

### How it Works
Hierarchy of separators, tried in order:
```
1. Try splitting by "\n\n" (paragraphs)
2. If still too big → split by "\n" (lines)
3. If still too big → split by ". " (sentences)
4. If still too big → split by " " (words)
```

### Example
- A long paragraph gets split at paragraph breaks first.
- If a single paragraph is still too long, it further breaks it at sentence level.

### Pros
- ✅ Respects natural document structure much better than fixed-size.
- ✅ Balances chunk size with meaning preservation.
- ✅ Most popular default method (used in LangChain's `RecursiveCharacterTextSplitter`).

### Cons
- ❌ Still can occasionally split mid-thought if paragraphs/sentences are very long.

### When to Use
- **Default choice** for most RAG projects — general-purpose documents (articles, blogs, reports).

---

## 3. Sentence-Based Chunking

**Simple Meaning:** Document ko sentence boundaries pe hi todo — ek chunk me poore sentences honge, kabhi bhi sentence beech me nahi katega.

### How it Works
- Use NLP libraries (like `nltk`, `spaCy`) to detect sentence boundaries.
- Group a certain number of sentences together (e.g., 3-5 sentences per chunk) or until a token limit is reached.

### Example
```
Chunk 1: "AI is transforming industries. Machine learning models are becoming more efficient. Companies are investing heavily in AI research."

Chunk 2: "However, ethical concerns remain. Data privacy is a major issue. Regulators are working on new AI laws."
```

### Pros
- ✅ Preserves complete thoughts/sentences.
- ✅ Good for precise Q&A — answer usually lies within 1-2 complete sentences.

### Cons
- ❌ Sentence length varies a lot, so chunk sizes become inconsistent.
- ❌ May lose paragraph-level context (relation between sentences across chunks).

### When to Use
- Q&A systems where **precise, short answers** matter (e.g., FAQ bots, fact retrieval).

---

## 4. Semantic Chunking

**Simple Meaning:** Chunk banate waqt sirf character count nahi, balki **meaning/topic ka similarity** dekha jata hai. Jab tak text ka topic same hai, wahi chunk continue hota hai; jaise hi topic change hota hai, naya chunk shuru hota hai.

### How it Works
1. Break text into sentences.
2. Generate embeddings for each sentence.
3. Compare similarity between consecutive sentences.
4. Agar similarity **drop** ho jaye (matlab topic change ho gaya) → naya chunk start karo.

### Example
```
"Machine learning is a subset of AI. It uses algorithms to learn patterns from data."
   ↑ (similar topic — same chunk)

"Meanwhile, the stock market saw a major crash today due to inflation concerns."
   ↑ (different topic — similarity drops — NEW chunk starts here)
```

### Pros
- ✅ Chunks are **topically coherent** — highest quality for retrieval accuracy.
- ✅ Reduces irrelevant info mixing into a single chunk.

### Cons
- ❌ Computationally expensive (needs embeddings just to create chunks).
- ❌ Slower to process large documents.

### When to Use
- **High-accuracy production RAG systems**, especially when documents cover multiple topics (e.g., research papers, mixed-topic articles).

---

## 5. Document-Based / Structural Chunking

**Simple Meaning:** Document ki **natural structure** (headings, sections, bullet points, markdown headers) ke hisaab se chunk karo.

### How it Works
- Use existing structure markers: `# Heading`, `## Subheading`, HTML tags (`<h1>`, `<p>`), or PDF section breaks.
- Each section/heading becomes its own chunk (or group of related sub-sections).

### Example
```
Document:
# Chapter 1: Introduction to AI
  (content...)
# Chapter 2: Machine Learning Basics
  (content...)

→ Chunk 1 = Chapter 1 content
→ Chunk 2 = Chapter 2 content
```

### Pros
- ✅ Naturally aligns with how humans organize information.
- ✅ Great metadata can be attached (e.g., "this chunk belongs to Chapter 2").

### Cons
- ❌ Only works well if the document **already has clear structure**. Unstructured text (like plain paragraphs) won't benefit.
- ❌ Section sizes can vary hugely (one heading might have 2 lines, another 5 pages).

### When to Use
- Structured documents: **manuals, legal contracts, Wikipedia-style articles, technical documentation, textbooks**.

---

## 6. Sliding Window Chunking (Overlapping Chunks)

**Simple Meaning:** Chunks banate waqt thoda **overlap** rakho, taaki boundary pe important context lost na ho.

### How it Works
- Instead of Chunk 1 ending exactly where Chunk 2 starts, let them **overlap** by some tokens/characters.

### Example
```
Chunk size = 100 tokens, Overlap = 20 tokens

Chunk 1: tokens 1-100
Chunk 2: tokens 81-180   (overlap of 20 tokens: 81-100 repeated)
Chunk 3: tokens 161-260
```

### Pros
- ✅ Reduces risk of losing context at chunk boundaries.
- ✅ Improves retrieval when key info sits right at a chunk edge.

### Cons
- ❌ Increases total storage (duplicate/overlapping content).
- ❌ Slightly more compute needed during embedding/indexing.

### When to Use
- Combined with **any other chunking method above** (fixed-size, recursive, sentence-based) — overlap is usually an **add-on strategy**, not standalone. Very commonly used in practice (typical overlap: 10-20% of chunk size).

---

## 7. Agentic / LLM-Based Chunking

**Simple Meaning:** Ek LLM khud padhta hai document ko aur decide karta hai ki chunk boundaries kahan honi chahiye — jaise ek insaan manually document ko sections me divide karega.

### How it Works
1. Feed the document (or parts of it) to an LLM.
2. Prompt it: "Split this text into meaningful, self-contained chunks that preserve context."
3. LLM returns proposed chunk boundaries or directly returns the chunks.

### Example
Prompt to LLM: *"Divide the following article into logical chunks, each covering one complete idea."*
→ LLM intelligently decides where one idea ends and another begins (better than simple similarity-based semantic chunking).

### Pros
- ✅ Highest quality — understands **context, meaning, and even document intent**.
- ✅ Can handle complex/messy documents where structure isn't obvious.

### Cons
- ❌ **Expensive** (LLM API calls for chunking itself).
- ❌ **Slow** — not practical for very large document sets.
- ❌ Adds another layer of potential error (LLM might chunk inconsistently).

### When to Use
- **High-value, complex documents** where accuracy matters more than cost/speed (e.g., legal contracts, medical records, critical research).

---

## 8. Table / Code-Aware Chunking (Special Content Chunking)

**Simple Meaning:** Tables, code blocks, ya structured data ko normal text ki tarah mat todo — inko apna special treatment do taaki structure na tootay.

### How it Works
- Detect special content types (Markdown tables, code blocks, JSON, CSV data).
- Keep them **intact as a single chunk** (don't split a table row in half or break a function mid-way).
- Optionally attach a text description/summary alongside for better retrieval.

### Example
```
❌ Bad: Splitting a table mid-row
| Name | Age
| John | -- (chunk cut here) --
25

✅ Good: Whole table kept as one chunk
| Name | Age |
| John | 25  |
| Mary | 30  |
```

### Pros
- ✅ Preserves structure and correctness of technical/tabular content.
- ✅ Prevents broken code/tables from confusing the LLM during generation.

### Cons
- ❌ Requires content-type detection logic (more engineering effort).
- ❌ Large tables/code files may still need internal splitting logic (row groups, function-level splits).

### When to Use
- Documents with **code snippets, tables, JSON/CSV data** — e.g., technical documentation, API docs, code repositories, financial reports.

---

## 9. Parent-Child Chunking (Small-to-Big Retrieval)

**Simple Meaning:** Document ko **do levels** pe chunk karo — ek **bada chunk (Parent)** aur uske andar chhote chunks (Children). Retrieval **child-level** pe hoti hai (precise match ke liye), lekin LLM ko answer generate karne ke liye **parent-level** (bada context) diya jata hai.

### Problem it Solves

- **Chhote chunks** → Retrieval accurate hoti hai (precise match), par LLM ko context kam milta hai.
- **Bade chunks** → Context zyada milta hai, par retrieval me irrelevant info mix ho jati hai (precision girti hai).

Parent-Child dono ka best of both worlds deta hai.

### How it Works

1. Document ko pehle **bade Parent chunks** me todo (e.g., 2000 tokens — poora section/paragraph group).
2. Har Parent ko aage **chhote Child chunks** me todo (e.g., 200-400 tokens — sentence ya small paragraph level).
3. Sirf **Child chunks embed aur index** kiye jate hain (vector DB me) — saath me unka parent ID/reference store hota hai.
4. Query aane par:
   - **Child chunk match hota hai** (kyunki woh precise/focused hai, embedding search sharp result deta hai)
   - Retrieval ke baad, system uske corresponding **Parent chunk** ko fetch karta hai (child→parent mapping se)
   - LLM ko final answer generate karne ke liye **Parent (bada context)** diya jata hai, na ki sirf woh chhota child

### Example

```
Parent Chunk (Section: "Machine Learning Basics")
├── Child 1: "ML is a subset of AI that learns from data."
├── Child 2: "Common algorithms include linear regression, decision trees..."
└── Child 3: "ML models improve performance through training on datasets."
```

Query: *"What algorithms are used in ML?"*
- Retrieval matches **Child 2** (best semantic match — sharp, focused text)
- Lekin LLM ko diya jata hai **poora Parent chunk** (poori "Machine Learning Basics" section) — taaki answer me broader context bhi ho, sirf ek isolated line na ho.

### Pros
- ✅ Precise retrieval (child-level) + Rich context (parent-level)
- ✅ Reduces "context loss" problem of small chunking
- ✅ Better answer quality without sacrificing search accuracy

### Cons
- ❌ Thoda zyada engineering complexity (do levels maintain karne padte hain — child→parent mapping)
- ❌ Storage/indexing thoda zyada (parent + child dono store karne padte hain)

### When to Use
- Jab documents **lambe aur structured** hon (manuals, wikis, research papers)
- Jab chhote chunks se retrieval toh accurate hoti hai, lekin LLM ka answer **incomplete/context-less** lagta hai

> Also known as **"Small-to-Big Retrieval"** — same concept, different name (used interchangeably in LlamaIndex/LangChain docs).

---

## 10. Late Chunking

**Simple Meaning:** Normal chunking me hum pehle document ko **todte** hain, phir har chunk ko **alag-alag embed** karte hain — is se har chunk ko sirf apna hi text pata hota hai, baaki document ka context miss ho jata hai. **Late Chunking me order ulta hai** — pehle poora document embed hota hai, chunking sabse **aakhri (late)** step me hoti hai.

### Problem it Solves

Normal chunking me pronouns/references ka context lost ho jata hai. Example:
```
"Berlin is the capital of Germany. It has a population of about 3.7 million."
```
Agar yeh do chunks me split ho jaye, toh doosre chunk ("It has a population...") ko embed karte waqt model ko pata hi nahi chalta ki **"It" = Berlin**. Iska embedding generic ban jata hai, aur query *"Berlin's population?"* is chunk ko utna acche se match nahi kar payegi.

### How it Works

1. **Poore document ko embed karo** — ek **long-context embedding model** use karke jo lambi text ek saath process kar sake.
2. Model **har token/word ke liye ek embedding** banata hai — yeh embeddings poore document ka context "dekh" ke bante hain (attention mechanism pura document cover karta hai, isliye "It" ka matlab "Berlin" model ko pata chal jata hai).
3. **Uske baad** (isiliye naam "late") in token-level embeddings ko chunk boundaries ke hisaab se **group/pool** karke chunk-level embeddings banaye jaate hain.

> Matlab — chunking sabse aakhri step hai, embedding ke baad. Normal approach me chunking pehle hoti hai, embedding baad me — Late Chunking isko reverse kar deta hai.

### Normal Chunking vs Late Chunking

| | Normal Chunking | Late Chunking |
|---|---|---|
| Order | Split → phir Embed (har chunk alag se) | Embed (poora doc) → phir Split |
| Context | Har chunk ko sirf apna text pata hai | Har chunk ko **poore document ka context** pata hai |
| Pronoun/reference problem | ❌ Solve nahi hota | ✅ Solve hota hai |

### Example

```
Document: "Berlin is the capital of Germany. It has a population of about 3.7 million."
```

**Normal Chunking:**
```
Chunk 1: "Berlin is the capital of Germany."
Chunk 2: "It has a population of about 3.7 million."
```
Chunk 2 ka embedding "generic city population" jaisa banega — "It" ka reference miss ho jata hai.

**Late Chunking:**
- Pura paragraph pehle embed hota hai — model ko pata chal jata hai ki "It" = Berlin (kyunki poora context saath me process hua)
- Fir jab Chunk 2 ka embedding token-embeddings se "pool" kiya jata hai, usme already "Berlin" ka context baked-in hota hai
- Ab query *"Berlin's population"* Chunk 2 ko sahi se match karega

### Pros
- ✅ Pronoun/reference resolution better hota hai (jaise "it", "he", "this", "the company" jaise words ka matlab pata rehta hai)
- ✅ Chunk embeddings zyada "context-aware" hote hain bina overlap/parent-child jaisi extra engineering ke
- ✅ Chunking flexible rehti hai — baad me chunk boundaries change bhi kar sakte ho bina dobara pura embed kiye

### Cons
- ❌ Long-context embedding model chahiye (jo pura document ek saath process kar sake — token limit issue ho sakta hai bahut bade docs ke liye)
- ❌ Har embedding model isko support nahi karta — specific implementation chahiye hoti hai
- ❌ Thoda naya/advanced concept hai — sab frameworks me directly built-in nahi milta

### When to Use
- Jab documents me **pronouns/references** bahut zyada ho (jaise "it", "this", "the above method") jo doosre paragraphs ko refer karte hain
- Jab **high retrieval accuracy** chahiye aur long-context embedding model available ho (e.g., Jina AI ne yeh technique popularize ki hai)

---

## How to Choose the Right Chunking Strategy (Decision Guide)

| Your Situation | Recommended Chunking |
|---|---|
| Just starting out / prototype | Fixed-Size or Recursive Chunking |
| General-purpose documents (blogs, articles, reports) | Recursive Character Chunking |
| Need precise short answers (FAQ/Q&A bot) | Sentence-Based Chunking |
| Document covers multiple topics/mixed content | Semantic Chunking |
| Well-structured docs (manuals, wikis, textbooks) | Document-Based/Structural Chunking |
| Important info often sits at chunk boundaries | Sliding Window (add overlap to any method) |
| High-stakes, complex documents, budget allows | Agentic/LLM-Based Chunking |
| Docs contain tables/code | Table/Code-Aware Chunking |
| Long docs where small chunks lose context for LLM | Parent-Child Chunking |

> **In practice:** Most production RAG systems combine multiple strategies — e.g., **Structural Chunking** (split by sections) + **Recursive Chunking** (within each section) + **Sliding Window overlap** (for boundary safety).

---

## Important Parameters to Tune (Regardless of Method)

| Parameter | Meaning | Typical Value |
|---|---|---|
| **Chunk Size** | How big each chunk is (tokens/characters) | 200–1000 tokens (varies by use case) |
| **Chunk Overlap** | How much consecutive chunks overlap | 10–20% of chunk size |
| **Separator Priority** | Order of splitting rules (paragraph > sentence > word) | Depends on method |

> **Tip:** Chunk size choice depends on your embedding model's context limit AND your LLM's context window. Smaller chunks = more precise retrieval but may lose broader context. Bigger chunks = more context but risk of irrelevant info mixing in (hurts Precision).

---

## How Chunking Connects to Evaluation (Link to Previous Notes)

Bad chunking directly hurts your retrieval metrics:
- **Poor chunking → Low Precision** (irrelevant text bundled in with relevant text)
- **Poor chunking → Low Recall** (important info split across chunks, none of them fully "relevant")
- **Poor chunking → Low NDCG** (even if relevant chunk retrieved, its content is incomplete/messy)

> Isiliye chunking ko RAG pipeline ka **foundation step** mana jata hai — agar yeh galat hui, toh BM25, embeddings, reranking — sab kuch iske upar hi struggle karega.

---

## One-Line Memory Trick

- **Fixed-Size** → "Bas ginti karke kaato"
- **Recursive** → "Pehle bada tod, phir chhota — jab tak fit na ho"
- **Sentence-Based** → "Sentence adhoora mat chhodo"
- **Semantic** → "Topic badle toh chunk badlo"
- **Structural** → "Document ki apni structure follow karo"
- **Sliding Window** → "Thoda overlap rakho, context na tootay"
- **Agentic** → "LLM khud decide kare kahan todna hai"
- **Table/Code-Aware** → "Tables/code ko mat todo, poora rakho"
- **Parent-Child** → "Match chhote se, jawab bade se do"
- **Late-Chunking** → "Pehle Embedding bnao, fir chunks me toro"