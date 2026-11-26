# 🔄 Handoff in OpenAI API — Study Notes

---

## 1. 🧭 Introduction to Handoff

**Handoff** is a core feature of the **OpenAI Agents SDK** (the production successor to the earlier "Swarm" framework) that enables **Multi-Agent Systems**.

- In simple terms: **Handoff = one AI agent transferring an ongoing conversation to another, more specialized agent.**
- Once the handoff happens, the **new agent takes full control** of the conversation — the first agent steps away completely.
- It's the SDK's mechanism for **agent-to-agent delegation**, used when a task is better handled by a specialist.

### 🏦 Real-World Analogy: The Bank Teller
Imagine you walk into a bank and speak to the **front-desk receptionist (Agent 1 — "Triage Agent")**:
- You say: *"I need help disputing a suspicious transaction."*
- The receptionist realizes this isn't their job — it needs the **Fraud Department (Agent 2 — "Specialist Agent")**.
- The receptionist **doesn't just give you directions** — they **walk you over and hand you off**, along with your file/case history, to the fraud specialist.
- From that point on, **you interact directly with the Fraud Department**. The receptionist is no longer part of the conversation.

✅ That's exactly what Handoff does in code — a **full transfer of ownership + context**, not just a referral.

---

## 2. ⚙️ How It Works (The Technical Flow)

Handoffs are implemented using **function calling** under the hood. Here's the step-by-step flow:

1. **🧩 Handoffs are registered as tools**
   - Every agent has a `handoffs` parameter listing which other agents it can transfer to.
   - The SDK automatically converts each potential handoff into a **callable function/tool** for the LLM — e.g., a handoff to `Refund Agent` becomes a tool named `transfer_to_refund_agent`.

2. **🤔 The LLM decides to hand off**
   - During its reasoning, the current agent's underlying LLM decides the user's request matches a specialist's domain.
   - It "calls" the handoff tool — just like it would call any other function (e.g., `get_weather()`).

3. **📦 The agent "returns" a new Agent object**
   - Instead of returning a normal text/tool response, the function call resolves to **a new Agent object** (the specialist).
   - This is the key mechanical trick: the framework detects that the return value is *another agent*, not just data.

4. **🔁 The Runner switches control**
   - The SDK's orchestration loop (the "Runner") sees this special return type and **switches execution to the new agent**.
   - The original agent's turn ends immediately — no further output from it.

5. **📜 Context & chat history are passed along**
   - By default, the new agent **inherits the entire prior conversation history** — it's "as though the new agent takes over the conversation" from the start.
   - Developers can customize this using an **`input_filter`** — a function that can trim, summarize, or reshape what history gets passed forward.

6. **▶️ The new agent continues the conversation**
   - The specialist agent now responds directly to the user, using its own instructions, tools, and (optionally) its own sub-handoffs.

**Flow Summary:**
```
User Input → Agent A (Triage) → LLM decides to call transfer_to_agent_B()
→ Returns Agent B object → Runner detects handoff → switches active agent
→ Agent B receives full/filtered history → Agent B responds to user
```

---

## 3. 🔍 Deep Dive: Handoff vs. Agent-as-a-Tool

### 📖 Definitions

- **🤝 Handoff**: A **full transfer of control**. One agent completely delegates the conversation to another. The original agent is "done" — the new agent owns everything going forward, including direct interaction with the user.

- **🛠️ Agent-as-a-Tool**: One agent (usually a **manager/orchestrator**) calls another agent **like a function/tool** — e.g., `agent.as_tool(tool_name="refund_expert", ...)`. The sub-agent does its job, **returns a result**, and control comes right back to the manager, who stays in charge and crafts the final response.

### 📊 Comparison Table

| Dimension | 🤝 Handoff | 🛠️ Agent-as-a-Tool |
|---|---|---|
| **Control / Ownership** | Full transfer — new agent owns the conversation entirely | Manager agent retains control throughout; sub-agent is subordinate |
| **Context Window / Memory Load** | New agent inherits the **entire chat history** (or filtered version) — heavier context load carried forward | Sub-agent typically only sees the **specific input/parameters** passed to it — lighter, scoped memory footprint |
| **User Interaction** | **Direct** — user now talks straight to the new agent | **Indirect** — user only ever talks to the manager; sub-agent's output is invisible/internal |
| **Complexity** | Simpler control-flow per agent, but harder to track "who's in charge" across a long session | More complex orchestration logic in the manager, but easier to audit/debug (single thread of control) |

### 💬 Scenario 1 — Handoff (Direct, Full Transfer)
```
User: "I want to dispute a charge on my account."
Triage Agent: [internally calls transfer_to_billing_agent()]
Billing Agent: "Hi, I can see your recent transactions. Which charge would you like to dispute?"
User: "The $49.99 charge from March 3rd."
```
➡️ Notice: the user is now **talking directly to the Billing Agent**. The Triage Agent is completely out of the picture.

### 💬 Scenario 2 — Agent-as-a-Tool (Indirect, Manager Stays in Control)
```
User: "Can you summarize this contract and check if it's compliant?"
Manager Agent: [internally calls compliance_checker_tool(contract_text)]
   → Compliance Agent (as tool) returns: "3 clauses may violate GDPR."
Manager Agent: "I reviewed the contract — it looks solid overall, but 3 clauses 
                may raise GDPR compliance concerns. Want me to flag them?"
```
➡️ Notice: the user **never sees or talks to** the Compliance Agent directly — the Manager Agent absorbs the result and replies on its behalf.

---

## 4. 🧠 Context & State Management

### What happens to Agent 1 after a handoff?
- **Its turn ends immediately** — it does not process any further input from the user.
- It **loses "the mic"**: it no longer has direct access to the live conversation unless control is explicitly handed back.
- However, it is **not deleted or destroyed** — it's simply not active. Its definition (instructions, tools) still exists in code and can be re-invoked later.
- The conversation **history up to the handoff point** is preserved and passed to Agent 2 by default (full transparency), unless an `input_filter` trims it.

### 🔙 "Back Handoff" (Reverse Transfer)
- A **Back Handoff** occurs when the second (specialist) agent determines the conversation should return to the original agent (or a third agent) — e.g., after resolving its specialized task.
- Mechanically, it works **identically to a forward handoff**:
  - Agent 2's LLM calls a handoff tool (e.g., `transfer_to_triage_agent`).
  - It returns the **original Agent object** (or another agent).
  - The Runner switches control back.
- **Practical use case**: A Billing Agent resolves a refund, then hands back to the Triage Agent in case the user has an unrelated question — mimicking how a bank specialist might send you back to the receptionist.
- ⚠️ Key point: For a back handoff to be possible, **Agent 2 must have Agent 1 listed in its own `handoffs` parameter** — handoff pathways are not automatically bidirectional; they must be explicitly configured in both directions.

---

## 5. 💻 Conceptual Code Blueprint

A minimal, Swarm/Agents-SDK-style example showing how one agent "returns" another agent to perform a handoff:

```python
from agents import Agent, Runner

# 🧑‍💼 Specialist Agent: Refunds
refund_agent = Agent(
    name="Refund Agent",
    instructions="You handle refund requests. Be empathetic and efficient.",
)

# 🧑‍💼 Specialist Agent: Billing
billing_agent = Agent(
    name="Billing Agent",
    instructions="You handle billing disputes and invoice questions.",
)

# 🧑‍💻 Triage Agent: The "front desk" — decides where to route the user
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are the first point of contact. "
        "If the user wants a refund, hand off to the Refund Agent. "
        "If the user has a billing dispute, hand off to the Billing Agent."
    ),
    handoffs=[refund_agent, billing_agent],  # 👈 registers possible handoff targets
)

# ▶️ Running the conversation
result = Runner.run_sync(
    triage_agent,
    "I was double-charged for my last order, I need a refund."
)

print(result.final_output)
```

### 🔑 What's happening conceptually:
1. `triage_agent` is invoked with the user's message.
2. Its LLM reasons: *"This matches the Refund Agent's job"* → internally "calls" `transfer_to_refund_agent`.
3. The SDK resolves this call to **the `refund_agent` object itself** (not a string, not plain data).
4. `Runner` detects an `Agent` was returned → **switches the active agent** to `refund_agent`.
5. `refund_agent` receives the full conversation history and generates the final reply — becoming the one "talking" to the user from here on.

### 🔙 Adding a Back Handoff:
```python
refund_agent = Agent(
    name="Refund Agent",
    instructions="Handle refunds. If the issue isn't a refund, hand back to Triage Agent.",
    handoffs=[triage_agent],  # 👈 enables reverse transfer
)
```

---

## 📌 Quick Recap Cheat-Sheet

| Concept | One-Line Takeaway |
|---|---|
| Handoff | Full control transfer to a specialist agent — like a bank routing you to another department |
| Mechanism | Implemented via function/tool calling; returning an `Agent` object triggers the switch |
| Context | Entire chat history passed by default (customizable via `input_filter`) |
| Agent-as-Tool | Orchestrator stays in charge; sub-agent just returns data, no direct user contact |
| Back Handoff | Same mechanism in reverse — must be explicitly configured on the specialist agent |
