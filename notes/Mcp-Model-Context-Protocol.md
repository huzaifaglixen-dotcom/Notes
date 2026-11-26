# MCP (Model Context Protocol) — From Scratch to Advanced

Simple notes on MCP — the "USB-C for AI" that lets AI models connect to real tools and data.

---

## 1. The Problem Before MCP

AI models like Claude/GPT are great at **thinking and generating text**, but by themselves they are **stuck inside a chat box** — they can't:
- Check your actual Gmail
- Look at your Google Drive files
- Check today's real weather
- Update a Notion page
- Query your company's database

To connect an AI to each of these tools, developers had to build a **custom, one-off integration** for every single tool, for every single AI model.

### The Old Way (Messy)
```
ChatGPT ↔ custom code ↔ Gmail
ChatGPT ↔ custom code ↔ Notion
Claude  ↔ custom code ↔ Gmail       (built again, separately!)
Claude  ↔ custom code ↔ Notion      (built again, separately!)
```

Every AI needed its **own separate connector** for every tool — lots of duplicate work, hard to maintain.

---

## 2. What is MCP?

**Simple definition:** MCP (**Model Context Protocol**) is an **open standard** (created by Anthropic) that defines **one common way** for AI models to connect to external tools, apps, and data sources — instead of everyone building custom, one-off connections.

> **Simple analogy: USB-C.** Before USB-C, every device had a different charging port/cable. USB-C became **one universal standard** — now any USB-C device works with any USB-C cable/charger. MCP does the same thing for connecting AI to tools — **build one MCP connector for Gmail, and ANY MCP-compatible AI (Claude, or others) can use it.**

### The New Way (Clean, with MCP)
```
Gmail  → MCP Server ─┐
Notion → MCP Server ─┼──→ MCP (standard connection) ──→ Any AI model (Claude, etc.)
Slack  → MCP Server ─┘
```
Build the connector **once**, and it works with **any AI that supports MCP** — no need to rebuild it for every model.

---

## 3. Core Building Blocks of MCP

| Term | Simple Meaning |
|---|---|
| **MCP Server** | A small program that connects to a specific tool/data source (e.g., Gmail, GitHub, a database) and exposes it in a standard way |
| **MCP Client** | The AI application (like Claude) that connects to MCP servers to use their tools |
| **Tools** | Specific actions the server offers (e.g., "send_email," "search_files," "create_task") |
| **Resources** | Data the server can provide to the model (e.g., a document, a database record) |
| **Prompts** | Pre-written prompt templates the server can offer for common tasks |

### Example
Think of an **MCP Server for Gmail**:
- **Tools it exposes:** `send_email`, `search_inbox`, `read_email`
- **Resources it exposes:** the actual email content/threads
- Claude (the **MCP client**) can now call these tools directly — e.g., "search my inbox for invoices from last month" — because the Gmail MCP server understands and handles that request.

---

## 4. How MCP Works (Step-by-Step, Simplified)

| Step | What Happens |
|---|---|
| 1. **Connection** | The AI app (client) connects to an MCP server (e.g., a Gmail MCP server) |
| 2. **Discovery** | The client asks the server: "What tools/resources do you offer?" |
| 3. **Request** | Based on the user's request ("check my unread emails"), the AI decides to call a specific tool (`search_inbox`) |
| 4. **Execution** | The MCP server actually performs the action (searches Gmail) and returns real data |
| 5. **Response** | The AI takes that real data and uses it to generate a helpful answer for the user |

### Example (Full Flow)
You ask Claude: *"Do I have any unread emails from my boss today?"*

1. Claude (client) connects to the **Gmail MCP server**
2. Claude sees the server offers a `search_inbox` tool
3. Claude calls `search_inbox` with filters (unread, sender = boss, today)
4. The Gmail MCP server actually searches your real inbox and returns results
5. Claude reads the results and replies: *"Yes, you have 2 unread emails from [boss] today..."*

> Without MCP, Claude would have **no way to actually check your real inbox** — it would just generate a generic, made-up-sounding response (potential hallucination!). This is exactly the same "look-up-then-answer" idea you learned in **RAG** — MCP is one of the ways an AI actually performs the "look-up" part on real, live tools instead of documents.

---

## 5. Why MCP Matters (Key Benefits)

| Benefit | Explanation |
|---|---|
| **One standard, many tools** | Build a connector once — works across any MCP-supporting AI |
| **Faster development** | No need to rebuild custom integrations for every AI model separately |
| **Real, live actions** | AI can perform actual actions (send emails, book meetings) — not just talk about them |
| **Reduces hallucination** | AI can pull real, current data instead of guessing |
| **Growing ecosystem** | Since it's an open standard, many companies build MCP servers for their own products |

---

## 6. Where MCP Fits with What You've Already Learned

```
RAG            → AI looks up documents/knowledge before answering (read-only, mostly)
MCP            → AI connects to real tools & live data sources in a standardized way
AI Agents      → Use tools (via MCP or similar) to perform tasks
Agentic AI     → Uses MULTIPLE tools/MCP servers together, planning multi-step actions independently
```

**In short:** MCP is often the **"plumbing"** that makes AI Agents and Agentic AI actually able to **do things** in the real world — checking your calendar, sending a message, running a search — instead of just generating text about it.

---

## 7. Real-World Examples of MCP in Use

| MCP Server Example | What It Lets the AI Do |
|---|---|
| **Google Drive MCP** | Search/read your files and documents |
| **GitHub MCP** | Check issues, pull requests, repositories |
| **Slack MCP** | Read/send messages in specific channels |
| **Database MCP** | Query and retrieve records from a company database |
| **Calendar MCP** | Check availability, create/update events |
| **Web Search / Browser MCP** | Search the internet and browse pages live |

---

## 8. Key Terms (Quick Glossary — Full List)

| Term | Simple Meaning |
|---|---|
| **MCP** | Model Context Protocol — a universal standard connecting AI models to tools/data |
| **MCP Server** | Program exposing a specific tool/data source in the MCP standard format |
| **MCP Client** | The AI app (e.g., Claude) that uses MCP servers |
| **Tool** | A specific action an MCP server offers (e.g., send_email) |
| **Resource** | Data an MCP server can provide to the AI |
| **Connector** | Common term for an MCP server built for a specific app/service |
| **Open Standard** | A publicly available specification anyone can build with/for — not owned by one company |

---

## One-Line Summary (for quick revision)

- **MCP** → A universal standard ("USB-C for AI") that lets AI models connect to real tools/data in one consistent way.
- **Before MCP** → Every AI needed a separate, custom-built connector for every tool (messy, repeated work).
- **With MCP** → Build a connector once → works with any MCP-supporting AI.
- **Why it matters** → Lets AI perform **real actions** (not just talk), reduces hallucination by using live data, and powers modern AI Agents/Agentic AI systems.
