# Machine Learning Types — Supervised, Unsupervised & Reinforcement Learning

Simple notes on the 3 main ways machines learn from data.

---

## Quick Overview

| Type | Learns From | Goal |
|---|---|---|
| **Supervised Learning** | Labeled data (question + correct answer given) | Predict the correct answer for new data |
| **Unsupervised Learning** | Unlabeled data (no correct answer given) | Find hidden patterns/groups on its own |
| **Reinforcement Learning** | Trial and error (rewards/punishments) | Learn the best action to take in a situation |

---

## 1. Supervised Learning

**Simple definition:** The model learns from data where the **correct answer is already given** (labeled data) — just like a student learning with an answer key.

- You give the model: **Input → Correct Output**
- It learns the pattern, then predicts output for **new, unseen inputs**

### Example
Teaching a model to detect **spam emails**:
- You show it 10,000 emails, each labeled "Spam" or "Not Spam"
- It learns patterns (words like "free money", "click now" = spam)
- Now, when a new email arrives, it predicts: Spam or Not Spam

**Other examples:**
- Predicting house prices (input: size, location → output: price)
- Detecting if a tumor is cancerous or not (input: scan → output: yes/no)
- Recognizing handwritten digits (input: image → output: which number)

> Think of it like: **Studying with an answer key** — you know what "correct" looks like, and you learn to match it.

### Two Main Sub-types
| Sub-type | What it Predicts | Example |
|---|---|---|
| **Classification** | A category/label | Spam or Not Spam |
| **Regression** | A number | House price = $250,000 |

---

## 2. Unsupervised Learning

**Simple definition:** The model learns from data **without any labels or correct answers** — it has to find patterns or groupings **on its own**.

- You give the model: **Input only** (no correct output given)
- It groups similar things together or finds structure by itself

### Example
Imagine giving a model **10,000 customer purchase records** with no labels:
- It will automatically group customers into clusters like:
  - Group A: "Buys baby products" → likely new parents
  - Group B: "Buys gym equipment" → fitness-focused
  - Group C: "Buys electronics only"
- **Nobody told it these categories** — it found the pattern itself

**Other examples:**
- Netflix grouping similar movies together
- Grouping news articles by topic without pre-set categories
- Detecting unusual/fraudulent transactions (things that don't fit any group)

> Think of it like: **Sorting a mixed box of items into groups without being told the categories** — you use similarity to organize them yourself.

### Common Technique
- **Clustering** → grouping similar data points together (e.g., customer segments)

---

## 3. Reinforcement Learning (RL)

**Simple definition:** The model (called an **agent**) learns by **trial and error** — it takes actions, gets **rewards** for good actions and **penalties** for bad ones, and improves over time to maximize rewards.

- No labeled data, no fixed patterns to find
- It **learns by doing**, through feedback (reward/punishment)

### Example
Teaching an AI to **play a video game**:
- It tries random moves at first
- Move helps win points → **Reward** (+1) → "do more of this"
- Move causes it to lose/die → **Penalty** (-1) → "avoid this"
- After thousands of attempts, it learns the best strategy to win

**Other examples:**
- Self-driving cars learning to drive safely (reward: smooth safe driving, penalty: crash)
- Robots learning to walk (reward: staying balanced, penalty: falling)
- AI mastering games like Chess/Go (AlphaGo learned this way)

> Think of it like: **Training a dog with treats** — good behavior gets a treat (reward), bad behavior doesn't, and over time the dog learns what to do.

---

## Side-by-Side Comparison

| Feature | Supervised | Unsupervised | Reinforcement |
|---|---|---|---|
| Data type | Labeled (input + correct answer) | Unlabeled (input only) | No fixed data — learns via actions & feedback |
| Human involvement | High (labels answers) | Low (no labels needed) | Medium (defines rewards/penalties) |
| Goal | Predict correct output | Find hidden patterns/groups | Learn best action/strategy |
| Example | Spam detection | Customer segmentation | Game-playing AI, robots |
| Analogy | Studying with answer key | Sorting items without labels | Training a dog with treats |

---

## Where This Fits

```
Artificial Intelligence (AI)
   └── Machine Learning (ML)
          ├── Supervised Learning
          ├── Unsupervised Learning
          └── Reinforcement Learning
                 └── (Deep Learning can be used inside any of these three,
                      using Neural Networks as the underlying model)
```

---

## One-Line Summary (for quick revision)

- **Supervised Learning** → Learns from labeled data (has an answer key) → predicts outcomes.
- **Unsupervised Learning** → Learns from unlabeled data → finds hidden patterns/groups on its own.
- **Reinforcement Learning** → Learns by trial and error using rewards and penalties → finds the best action/strategy.
