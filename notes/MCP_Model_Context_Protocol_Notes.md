# MCP (Model Context Protocol) — Complete Notes

> **MCP** = Ek **open, standardized protocol** (Anthropic ne introduce kiya) jo LLM applications ko **external tools, data sources, aur systems** se connect karne ka ek **common, universal tareeka** deta hai.

---

## Table of Contents
1. Why MCP was Created (The Problem)
2. What is MCP (Simple Meaning)
3. The "USB-C for AI" Analogy
4. MCP Architecture — Core Components
5. MCP Client vs MCP Server
6. What an MCP Server Can Expose
7. How MCP Communication Works
8. Transport Mechanisms
9. MCP vs Traditional Function/Tool Calling
10. Real-World Examples of MCP Servers
11. Building an MCP Server (Conceptual Overview)
12. Security Considerations
13. MCP in the Broader Agent Ecosystem
14. Common Mistakes
15. Cheat Sheet

---

## 1. Why MCP was Created (The Problem)

Before MCP, agar aapko apna LLM app **10 different tools/services** (Google Drive, Slack, GitHub, database, etc.) se connect karna hota, toh:
- Har service ke liye **alag, custom integration code** likhna padta tha
- Har developer/company apna **khud ka format** use karta tha tool definitions ke liye
- Yeh ek **"N × M" problem** ban jata tha — N applications × M tools = bahut saare custom connections banane padte the

> Analogy (Before MCP): Socho har device (laptop, phone, camera) ka apna **alag charger/cable** ho — koi standard nahi. Bahut messy aur inefficient.

### The Solution: MCP
Ek **standard protocol** jisse **koi bhi MCP-compatible client** (Claude, ya koi bhi LLM app), **kisi bhi MCP-compatible server** (tool/data source) se **same tareeke se** connect ho sake — bina custom integration code likhe.

---

## 2. What is MCP (Simple Meaning)

**MCP (Model Context Protocol)** ek **open standard** hai jo define karta hai ki:
- LLM applications (**clients**) aur external tools/data sources (**servers**) ke beech **communication kaise ho**
- Tools, resources, aur prompts ko **kaise expose/discover** kiya jaye
- Data **kaise securely pass** ki jaye dono ke beech

> Simple words me: MCP ek **"common language/rulebook"** hai jisse AI models aur external systems ek doosre se **baat kar sakte hain**, bina yeh worry kiye ki dusri taraf kaunsa specific software/framework use ho raha hai.

---

## 3. The "USB-C for AI" Analogy

MCP ko often **"USB-C for AI applications"** kaha jata hai:

| USB-C | MCP |
|---|---|
| Ek hi cable/port standard, jisse phone, laptop, camera — sab connect ho sakte hain | Ek hi protocol standard, jisse koi bhi AI app, kisi bhi tool/data source se connect ho sakta hai |
| Manufacturer ko har device ke liye alag port design nahi karna padta | Developer ko har tool ke liye alag integration nahi likhni padti |
| Universal compatibility | Universal compatibility (across different AI apps and tools) |

> Bas ek baar **MCP Server** bana do kisi tool/service ke liye, aur **koi bhi MCP-compatible AI application** (Claude Desktop, Claude Code, ya kisi aur company ka LLM app) usko use kar sakta hai — bina alag se integration likhe.

---

## 4. MCP Architecture — Core Components

```
┌─────────────┐         MCP Protocol          ┌─────────────┐
│  MCP Client │ ◄─────────────────────────────► │  MCP Server │
│ (e.g., Claude│                                 │ (e.g., Slack,│
│   Desktop)   │                                 │  GitHub,     │
│              │                                 │  Database)   │
└─────────────┘                                 └─────────────┘
```

| Component | Role |
|---|---|
| **Host** | The AI application itself (e.g., Claude Desktop, an IDE, a custom agent app) |
| **MCP Client** | Component inside the Host that manages the connection to one MCP Server |
| **MCP Server** | A lightweight program that exposes specific tools/data/capabilities via the MCP standard |

> **Note:** Ek Host (jaise Claude Desktop) ek saath **multiple MCP Servers** se connect ho sakta hai (Slack server, GitHub server, Database server — sab ek saath).

---

## 5. MCP Client vs MCP Server

### MCP Client (Host Side)
- AI application ke andar rehta hai.
- Server se **connection establish** karta hai.
- Server ke **available capabilities discover** karta hai (kaunse tools/resources available hain).
- User/LLM ki taraf se **requests bhejta hai** server ko.

### MCP Server (Tool/Data Side)
- Ek specific service (jaise GitHub, Slack, ek database, ya koi custom internal tool) ko **MCP-compatible bana deta hai**.
- **Expose karta hai:**
  - **Tools** (functions LLM call kar sake, jaise "create_issue", "send_message")
  - **Resources** (data jo LLM read kar sake, jaise files, database records)
  - **Prompts** (pre-defined prompt templates jo server suggest kar sakta hai)

---

## 6. What an MCP Server Can Expose

| Capability | Simple Meaning | Example |
|---|---|---|
| **Tools** | Actions/functions that can be called (with side effects) | `create_github_issue(title, body)`, `send_slack_message(channel, text)` |
| **Resources** | Read-only data that can be fetched/referenced | A file's content, a database record, a webpage |
| **Prompts** | Reusable prompt templates the server suggests for common tasks | "Summarize this GitHub PR" template |

> Yeh teeno concepts humne pehle "Tool Calling" notes me dekhe the (tools), lekin MCP isko ek **standardized, discoverable format** me package karta hai, jisse **koi bhi client** inhe automatically samajh aur use kar sake.

---

## 7. How MCP Communication Works

```
1. Client connects to Server (via stdio, HTTP, etc. — see Transport section)
2. Client asks Server: "What capabilities do you have?" (discovery/handshake)
3. Server responds: "I have these tools: [list], these resources: [list]"
4. LLM (via Client) decides it needs to use a specific tool
5. Client sends request to Server: "Call tool X with these parameters"
6. Server executes the action (e.g., actually creates a GitHub issue)
7. Server sends result back to Client
8. Client passes result to LLM → LLM generates final response
```

> Yeh flow bilkul **Tool Calling** jaisa hi hai (jo humne pichli notes me dekha), bas MCP isko **standardized protocol level** pe define karta hai, taaki yeh flow **kisi bhi tool aur kisi bhi AI app** ke beech consistently kaam kare.

---

## 8. Transport Mechanisms

MCP client aur server **kaise communicate** karte hain, iske liye alag transport options hain:

| Transport | Use Case |
|---|---|
| **stdio (Standard Input/Output)** | Local tools/servers jo same machine pe chal rahe hain (e.g., local file system access) |
| **HTTP/SSE (Server-Sent Events)** | Remote servers — jab tool/service kisi doosre server pe hosted ho (e.g., cloud-based service) |

> **stdio** typically local development/desktop use ke liye use hota hai (fast, simple), **HTTP-based** transport remote/cloud services ke liye zaroori hai.

---

## 9. MCP vs Traditional Function/Tool Calling

| Feature | Traditional Function Calling | MCP |
|---|---|---|
| **Standardization** | Har app/framework apna format define karta hai | Universal, open standard — sabke liye same |
| **Reusability** | Ek app ke liye likha gaya tool, doosre app me directly use nahi ho sakta | Ek MCP Server, kisi bhi MCP-compatible client ke saath use ho sakta hai |
| **Discovery** | Developer ko manually tools define/register karne padte hain har app me | Client automatically server se "available capabilities" discover kar leta hai |
| **Scope** | Sirf tools (functions) | Tools + Resources + Prompts — broader scope |
| **Ecosystem** | Fragmented — har company/framework apna approach | Growing shared ecosystem — community MCP servers ban rahe hain jo koi bhi use kar sakta hai |

> **Simple takeaway:** Function/Tool calling ek **concept** hai (LLM tools call kar sakta hai). MCP ek **standardized way** hai us concept ko implement karne ka, taaki reusability aur interoperability mile.

---

## 10. Real-World Examples of MCP Servers

| MCP Server | What It Enables |
|---|---|
| **GitHub MCP Server** | LLM ko GitHub issues, PRs, repos ke saath interact karne deta hai |
| **Slack MCP Server** | Messages read/send karna, channels manage karna |
| **Google Drive MCP Server** | Files search/read karna |
| **Database MCP Server (e.g., PostgreSQL)** | SQL queries run karna, schema explore karna |
| **Filesystem MCP Server** | Local files read/write karna |
| **Browser/Web MCP Server** | Web pages browse karna, actions perform karna (clicks, form fills) |

> Aapne pichle conversations me dekha hoga ki Claude jaisi applications me "connectors"/"MCP Apps" available hote hain — yeh sab dar-asal MCP Servers hi hain jo different services (Google Drive, Asana, etc.) ko Claude se connect karte hain.

---

## 11. Building an MCP Server (Conceptual Overview)

Ek basic MCP Server banane ka simplified flow (Python SDK jaisa):

```python
from mcp.server import Server

server = Server("my-custom-tool-server")

@server.tool()
def get_customer_info(customer_id: str) -> dict:
    """Fetch customer information from our database."""
    # Your actual logic here
    return {"name": "...", "email": "..."}

@server.resource("customers://{customer_id}")
def get_customer_resource(customer_id: str) -> str:
    """Expose customer data as a readable resource."""
    return fetch_customer_data(customer_id)

server.run()
```

> Iske baad, **koi bhi MCP client** (Claude Desktop, ya koi custom agent app) is server se connect hokar `get_customer_info` tool ko discover aur call kar sakta hai — bina developer ko us client ke liye alag se kuch likhna pade.

---

## 12. Security Considerations

MCP servers **real actions** perform kar sakte hain (files delete karna, messages bhejna, database modify karna) — isliye security bahut important hai:

| Consideration | Why It Matters |
|---|---|
| **Authentication** | Server ko verify karna chahiye ki request legitimate client se aa rahi hai |
| **Authorization/Permissions** | User ko explicitly approve karna chahiye sensitive actions (jaise "delete file") — human-in-the-loop |
| **Least Privilege** | MCP Server ko sirf utni hi capability deni chahiye jitni zaroori hai, sab kuch expose mat karo |
| **Input Validation** | Server ko har incoming request/parameter ko validate karna chahiye (LLM galat/malicious input bhi bhej sakta hai) |
| **Untrusted Content** | Agar MCP resource untrusted source (jaise ek public webpage) se data laata hai, uske andar **hidden/malicious instructions** ho sakti hain (prompt injection risk) — isko carefully handle karna chahiye |

---

## 13. MCP in the Broader Agent Ecosystem

MCP ka role samajhne ke liye, yeh dekho ki yeh humari pichli notes ke saath kaise fit hota hai:

```
┌─────────────────────────────────────────────────────┐
│                    AI AGENT                          │
│  (Reasoning, Planning, ReAct loop — pichli notes)     │
└───────────────────────┬───────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Tool Calling       │  (Concept: LLM decides
              │   (Concept)          │   what tool to call)
              └──────────┬───────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   MCP (Protocol)     │  (Standardized way to
              │                      │   actually connect & call)
              └──────────┬───────────┘
                         │
           ┌─────────────┼─────────────┐
           ▼             ▼             ▼
     GitHub Server  Slack Server  DB Server
```

> MCP, Agent aur Tool Calling ko **replace nahi karta** — yeh unke **implementation ko standardize** karta hai, taaki ecosystem-wide reusability mile.

---

## 14. Common Mistakes

| Mistake | Problem | Fix |
|---|---|---|
| Exposing too many capabilities in one MCP server | LLM confuse ho sakta hai, security risk badhta hai | Keep servers focused — one server per clear domain/service |
| No authentication/authorization checks | Anyone could potentially trigger sensitive actions | Always implement proper auth before exposing tools |
| Trusting all resource content blindly | Malicious content (e.g., from a webpage) could contain prompt injections | Treat external resource content as untrusted data, not instructions |
| Not testing with real client behavior | Server might not handle edge cases the client sends | Test thoroughly with actual MCP clients before deploying |
| Building custom integration instead of MCP when reusability matters | Wastes effort recreating what MCP already standardizes | Use MCP when building tools meant to work across multiple AI applications |

---

## 15. Cheat Sheet

### One-Line Memory Tricks
- **MCP** → "USB-C for AI — ek standard jisse AI apps aur tools connect hote hain"
- **MCP Client** → "AI application ki taraf se connection manage karta hai"
- **MCP Server** → "Tool/data source ko expose karta hai standardized tareeke se"
- **Tools, Resources, Prompts** → "Actions, Data, aur Templates jo server deta hai"

### Quick Recap Flow
```
AI App (Host) → MCP Client → [Standard Protocol] → MCP Server → Actual Tool/Service
                                                            │
                                                            ▼
                                                    Result flows back
```

### Golden Rule
> **"MCP doesn't invent tool calling — it standardizes it, so any AI app can talk to any tool/service without custom, one-off integration code."**
