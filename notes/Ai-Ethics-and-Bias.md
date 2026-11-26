# AI Ethics & Bias

Simple notes on why AI can behave unfairly or harmfully, and the key ethical concerns around it.

---

## 1. What is AI Bias?

**Simple definition:** AI Bias happens when an AI system gives **unfair or skewed results** for certain groups of people — usually because the **data it learned from was biased**, not because the AI is "intentionally" being unfair.

> Remember: AI learns from data. **If the data has bias, the AI will learn that bias too.** "Garbage in, garbage out."

### Example
A company builds an AI to **shortlist job resumes** by training it on 10 years of past hiring data.
- If the company mostly hired men in the past (even if unintentionally), the AI **learns that pattern**
- It starts **favoring male candidates** and rejecting equally qualified female candidates
- This actually happened — **Amazon scrapped an AI hiring tool** in 2018 for exactly this reason

**Other real examples:**
- Facial recognition systems being **less accurate for darker-skinned faces** (trained mostly on lighter-skinned faces)
- Loan approval AI **rejecting minority applicants more often**, because historical loan data reflected past discrimination
- Voice assistants understanding certain **accents better than others**

---

## 2. Where Does Bias Come From?

| Source | Explanation | Example |
|---|---|---|
| **Biased Training Data** | Data reflects real-world historical inequalities | Hiring data with fewer women in tech roles |
| **Unbalanced Data** | Some groups are underrepresented in the dataset | Facial recognition trained mostly on one skin tone |
| **Human Bias in Labeling** | Humans labeling data bring their own biases | Labeling certain speech as "aggressive" based on accent/dialect |
| **Design Choices** | Developers unintentionally build assumptions into the system | An app assuming everyone has a smartphone/internet |

---

## 3. Key Ethical Concerns in AI

### a) **Bias & Fairness**
AI should treat all groups of people fairly — covered above.

### b) **Privacy**
AI models are often trained on huge amounts of data — sometimes including personal or sensitive information without proper consent.

**Example:** An AI trained on social media posts might accidentally memorize and reveal someone's private details.

### c) **Transparency (Explainability)**
Many AI models are a **"black box"** — even the developers don't fully know *why* it gave a specific answer.

**Example:** A bank's AI rejects your loan application, but no one — not even the bank — can clearly explain **why** the AI decided that.

### d) **Accountability**
If an AI makes a harmful mistake, **who is responsible** — the company, the developer, or the AI itself?

**Example:** A self-driving car causes an accident. Is it the car manufacturer's fault, the software developer's fault, or the AI's "fault"?

### e) **Misinformation & Deepfakes**
AI can generate **very convincing fake text, images, audio, or video** — which can be used to spread false information or impersonate real people.

**Example:** A fake AI-generated video of a political leader saying something they never actually said.

### f) **Job Displacement**
AI automating tasks can **replace human jobs**, raising concerns about employment and economic impact.

**Example:** AI writing tools reducing the need for certain content-writing jobs.

---

## 4. How Companies Try to Reduce Bias & Improve Ethics

| Method | What It Does |
|---|---|
| **Diverse Training Data** | Include data representing many groups, backgrounds, accents, skin tones, etc. |
| **Bias Testing/Auditing** | Regularly test the AI's outputs across different groups to catch unfair patterns |
| **Human Review** | Keep humans in the loop for important decisions (hiring, loans, medical) instead of fully automating them |
| **Transparency Reports** | Companies publishing how their models are trained and tested |
| **Guardrails/Safety Training** | Fine-tuning models (like RLHF) to refuse harmful requests and reduce toxic/biased outputs |

---

## 5. Simple Analogy

Think of AI like a **student who only studied from one textbook written by one biased author**:

- If that textbook mostly talked about one group of people, ignored others, or had unfair stereotypes...
- The student (AI) will **repeat those same biases and gaps** when answering questions — not because the student is "evil," but because that's **all it was taught**.

The fix: **give the student better, more diverse, and fact-checked textbooks** (better training data) — and **teach them to question and double-check their assumptions** (bias auditing + human review).

---

## 6. Key Terms (Quick Glossary)

| Term | Simple Meaning |
|---|---|
| **Bias** | Unfair favoritism or discrimination in AI outputs |
| **Fairness** | Ensuring AI treats all groups equitably |
| **Black Box Model** | An AI system whose internal decision-making isn't easily explainable |
| **Explainability/Interpretability** | Being able to understand *why* an AI made a certain decision |
| **Deepfake** | AI-generated fake image/video/audio that looks/sounds real |
| **Guardrails** | Built-in rules/training that stop an AI from generating harmful or biased content |
| **Human-in-the-loop** | Keeping a human involved in reviewing/approving AI decisions, especially for important matters |

---

## One-Line Summary (for quick revision)

- **AI Bias** → Unfair outputs caused by biased or unbalanced training data ("garbage in, garbage out").
- **Ethics concerns** → Bias/fairness, privacy, transparency, accountability, misinformation, job impact.
- **Fix approach** → Diverse data + bias testing + human review + transparency + safety fine-tuning.
- **Analogy** → AI is like a student who only learned from one biased textbook — better textbooks (data) = better student (AI).
