# API Design & Cost Optimization for LLM Apps — Complete Notes
 
> Yeh notes cover karte hain ki **production-grade LLM applications** kaise design ki jati hain — streaming, rate limiting, caching — aur **cost ko kaise control/optimize** kiya jata hai, jo AI Engineer ka ek daily concern hota hai.
 
---
 
## Table of Contents
1. Why This Matters
2. Streaming Responses
3. Rate Limiting
4. Caching Strategies
5. Prompt Caching (Special Case)
6. Token Usage Optimization
7. Model Selection Strategy (Cost vs Quality)
8. Batching Requests
9. Fallback & Retry Strategies
10. Monitoring Cost in Production
11. Common Mistakes
12. Cheat Sheet
---
 
## 1. Why This Matters
 
LLM APIs **traditional APIs se different** hain kyunki:
- Response **turant nahi** aata (LLM generation me time lagta hai — seconds tak)
- Cost **per-token** based hota hai (traditional APIs usually free ya flat-rate hote hain)
- High traffic me, **rate limits** aur **cost explosion** ka risk zyada hota hai
> Isliye AI Engineer ko sirf "LLM se accha answer kaise le" nahi, balki **"is answer ko efficiently, affordably, aur reliably user tak kaise pahunchayein"** bhi sochna padta hai.
 
---
 
## 2. Streaming Responses
 
**Simple Meaning:** Poore response ka wait karne ke bajaye, LLM ka output **token-by-token (ya chunk-by-chunk)** turant user ko dikhana shuru kar dena — jaise ChatGPT/Claude ki UI me text "type" hote hue dikhta hai.
 
### Why It's Important
- **Perceived Speed:** User ko lagta hai response fast aa raha hai, chahe total generation time same ho.
- **Better UX:** Lambe responses ke liye, poora paragraph ek saath wait karne se better hai ki text gradually aaye.
### How It Works (Conceptual)
```python
# Without streaming — user waits for the ENTIRE response
response = llm.generate(prompt)  # Blocks until fully complete
print(response)
 
# With streaming — tokens arrive incrementally
for chunk in llm.generate_stream(prompt):
    print(chunk, end="", flush=True)  # Display as it arrives
```
 
### When to Use
- ✅ Chatbots, conversational UIs (almost always should stream)
- ✅ Long-form content generation (articles, reports)
- ⚪ Not necessary for backend/programmatic use where you just need the final JSON result
---
 
## 3. Rate Limiting
 
**Simple Meaning:** Ek time period me, **kitni requests** ek user/system LLM API ko bhej sakta hai, uski limit set karna — taaki system overload na ho aur cost control me rahe.
 
### Why It's Needed
- LLM providers (Anthropic, OpenAI) khud bhi rate limits enforce karte hain (requests per minute, tokens per minute).
- Aapke apne application me bhi rate limiting zaroori hai — taaki ek single user/bot poora system resources hijack na kar le, aur costs predictable rahein.
### Common Rate Limiting Strategies
 
| Strategy | How It Works |
|---|---|
| **Fixed Window** | Ek fixed time window (e.g., "100 requests per minute") — window khatam hote hi reset |
| **Sliding Window** | Rolling time window — zyada smooth/fair distribution |
| **Token Bucket** | Har request ek "token" consume karta hai; tokens ek fixed rate se refill hote hain |
| **Per-User Limits** | Har user/API key ka apna alag limit |
| **Priority Queuing** | Important/paid users ko higher priority milti hai during high load |
 
### Handling Rate Limit Errors
```python
import time
 
def call_llm_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return llm.generate(prompt)
        except RateLimitError:
            wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s...
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```
 
> **Exponential Backoff** ek common pattern hai — har retry ke beech wait time double karte jao, taaki API pe pressure na bane.
 
---
 
## 4. Caching Strategies
 
**Simple Meaning:** Agar **same/similar request** pehle bhi aa chuki hai, toh dobara LLM ko call karne ke bajaye, **stored (cached) response** wapas de do — isse cost aur latency dono bachte hain.
 
### Types of Caching
 
| Type | How It Works |
|---|---|
| **Exact Match Caching** | Agar exact same prompt/query dobara aaye, cached response return karo |
| **Semantic Caching** | Agar **similar meaning wala** query aaye (exact match nahi, but semantically close), phir bhi cached response use karo |
 
### Example — Exact Match Caching
```python
cache = {}
 
def get_llm_response(prompt):
    if prompt in cache:
        return cache[prompt]  # Return cached, no LLM call needed
    
    response = llm.generate(prompt)
    cache[prompt] = response
    return response
```
 
### Example — Semantic Caching (Conceptual)
```python
def get_llm_response_semantic(prompt):
    prompt_embedding = embed(prompt)
    
    # Search cache for a similar previous query (using vector similarity)
    similar_cached = search_cache_by_similarity(prompt_embedding, threshold=0.95)
    
    if similar_cached:
        return similar_cached.response  # Reuse cached answer
    
    response = llm.generate(prompt)
    save_to_cache(prompt_embedding, response)
    return response
```
 
### When Caching Helps Most
- FAQ-style bots (common repeated questions)
- High-traffic applications with overlapping user queries
- Static/rarely-changing information
### When Caching is Risky
- Personalized responses (different per user — caching could leak wrong info to wrong user)
- Time-sensitive information (weather, stock prices — cached response could be stale/wrong)
---
 
## 5. Prompt Caching (Special Case)
 
**Simple Meaning:** Modern LLM APIs (including Anthropic's) support **caching parts of your prompt** (especially long, repeated context like system prompts or large documents), so you don't pay full price to reprocess that same content on every request.
 
### How It Works (Conceptual)
```
Request 1: [Long System Prompt + Document Context] + "Question 1"
   → Full context processed, marked for caching
 
Request 2 (same session/context): [SAME Long System Prompt + Document Context] + "Question 2"
   → Cached portion reused at a MUCH lower cost — only "Question 2" is processed fresh
```
 
### Why This Matters
- RAG systems jinme **same large document context** baar-baar use hota hai (multi-turn conversations over the same document), prompt caching **dramatically cost kam kar sakta hai**.
- Especially useful for **agents** that repeatedly send the same tool definitions/system instructions in every turn.
---
 
## 6. Token Usage Optimization
 
**Simple Meaning:** Prompt aur response me **kam tokens use karna**, bina quality kharab kiye — directly cost kam karta hai (kyunki billing per-token hoti hai).
 
### Techniques
 
| Technique | How It Helps |
|---|---|
| **Concise System Prompts** | Unnecessarily lambe instructions avoid karo |
| **Limit Retrieved Context** | Sirf top-K most relevant chunks bhejo (reranking se help milti hai — pichli notes) |
| **Truncate Long Conversations** | Sliding window / summarization memory use karo (pichli Memory notes) |
| **Set max_tokens appropriately** | Response length ko explicitly limit karo jab lamba answer zaroori na ho |
| **Use smaller models for simple tasks** | Har task ke liye sabse bada/expensive model zaroori nahi (next section) |
 
---
 
## 7. Model Selection Strategy (Cost vs Quality)
 
**Simple Meaning:** Har task ke liye **sabse powerful (aur expensive) model** use karna zaroori nahi — task ki complexity ke hisaab se **right-sized model** choose karo.
 
### Example Strategy
```
Simple Classification/Extraction Tasks → Smaller/Cheaper model (e.g., Haiku-tier)
Standard Q&A/Summarization → Mid-tier model (e.g., Sonnet-tier)
Complex Reasoning/Critical Decisions → Larger/Premium model (e.g., Opus-tier)
```
 
### Model Routing (Advanced)
- Ek **router** (chhota classifier ya rule-based logic) decide karta hai ki incoming request ki complexity kya hai, aur uske hisaab se **appropriate model** ko route karta hai.
```
Simple query → Cheap/Fast model
Complex query → Powerful/Expensive model
```
- Yeh significantly cost bacha sakta hai bade scale pe, bina quality compromise kiye critical tasks pe.
---
 
## 8. Batching Requests
 
**Simple Meaning:** Multiple independent requests ko **ek saath (batch me) process** karna, individually ek-ek karke bhejne ke bajaye.
 
### Benefits
- Kuch providers **batch APIs** offer karte hain jo **lower cost per request** dete hain (trade-off: results turant nahi milte, thoda delay ke saath aate hain — asynchronous processing).
- Useful for **non-real-time tasks** — jaise "saari overnight processing karo 10,000 documents ki, result kal subah tak chahiye."
### When to Use Batching
- ✅ Bulk data processing (classification, summarization of many documents)
- ✅ Non-urgent, offline analysis tasks
- ❌ Real-time chatbot responses (user turant jawab chahta hai)
---
 
## 9. Fallback & Retry Strategies
 
**Simple Meaning:** Agar primary LLM call **fail ho jaye** (timeout, rate limit, server error), system ke paas ek **backup plan** hona chahiye.
 
### Common Strategies
 
| Strategy | How It Works |
|---|---|
| **Retry with Backoff** | Thoda wait karke dobara try karo (exponential backoff) |
| **Fallback Model** | Agar primary model (jaise Opus) unavailable ho, ek secondary model (jaise Sonnet) use karo |
| **Fallback Response** | Agar sab kuch fail ho jaye, ek generic "Sorry, try again later" message do (crash hone se better) |
| **Circuit Breaker Pattern** | Agar ek service baar-baar fail ho raha hai, thodi der ke liye usko call karna hi band kar do (system ko overload hone se bachane ke liye), phir dobara try karo |
 
---
 
## 10. Monitoring Cost in Production
 
(Yeh humari pichli **Observability** notes se directly connect hota hai)
 
| What to Track | Why |
|---|---|
| **Cost per request** | Understand unit economics of your application |
| **Cost per user/session** | Identify if certain usage patterns are disproportionately expensive |
| **Token usage trends over time** | Spot unexpected spikes (e.g., a bug causing huge prompts) |
| **Cost by model tier** | See if you're overusing expensive models where cheaper ones would suffice |
 
### Setting Up Alerts
- Alert karo agar daily/monthly cost **expected budget se** significantly zyada ho jaye — taaki bugs (jaise infinite agent loops — pichli Agent notes yaad karo!) jaldi pakde jayein before they cause a huge bill.
---
 
## 11. Common Mistakes
 
| Mistake | Problem | Fix |
|---|---|---|
| Not streaming for user-facing chat apps | Poor perceived performance, users think app is slow | Implement streaming for all conversational interfaces |
| No rate limiting on your own API | Single user/bot could overwhelm system and spike costs | Implement per-user rate limits |
| No caching for repeated/common queries | Paying full LLM cost for identical requests repeatedly | Implement exact-match or semantic caching |
| Always using the most powerful (expensive) model | Overpaying for tasks that a cheaper model could handle | Use model routing based on task complexity |
| No retry/fallback logic | Users see errors when a transient issue occurs | Implement retry with backoff + fallback models/responses |
| Not monitoring cost trends | Bill spikes go unnoticed until the invoice arrives | Set up cost dashboards and alerts (via observability tools) |
 
---
 
## 12. Cheat Sheet
 
### One-Line Memory Tricks
- **Streaming** → "Token-by-token dikhao, poora wait mat karwao"
- **Rate Limiting** → "Ek time me kitni requests allowed hain, control karo"
- **Caching** → "Same/similar sawal dobara pooche toh LLM mat bulao"
- **Prompt Caching** → "Bada, repeated context sasta reprocess karo"
- **Model Routing** → "Chhota kaam, chhota model — bada kaam, bada model"
### Quick Recap Flow
```
Request Comes In
   → [Rate Limit Check]
   → [Cache Check — return if cached]
   → [Model Router — pick right-sized model]
   → [Stream Response to User]
   → [If Error: Retry with Backoff → Fallback if needed]
   → [Log to Observability Tool — track cost/latency]
```
 
### Golden Rule
> **"A great LLM app isn't just about generating good answers — it's about doing so reliably, quickly, and affordably at scale. Streaming, caching, rate limiting, and smart model selection are what separate a prototype from a production system."**