# 🤖 Multi-Agent Systems — Complete Notes
### AI Agents | LangGraph | OpenAI Agents SDK | CrewAI | AutoGen

> Ye notes un logon ke liye hain jo Python aur basic AI/LLM concepts jaante hain aur ab **Multi-Agent Systems** (multiple AI agents jo aapas mein collaborate karte hain) samajhna chahte hain.

---

## 📑 Table of Contents

1. [Multi-Agent System Kya Hota Hai?](#1-multi-agent-system-kya-hota-hai)
2. [Single Agent vs Multi-Agent](#2-single-agent-vs-multi-agent)
3. [Core Concepts](#3-core-concepts)
4. [Common Multi-Agent Architectures](#4-common-multi-agent-architectures)
5. [Agent Communication Patterns](#5-agent-communication-patterns)
6. [LangGraph for Multi-Agent Systems](#6-langgraph-for-multi-agent-systems)
7. [OpenAI Agents SDK](#7-openai-agents-sdk)
8. [CrewAI](#8-crewai)
9. [AutoGen (Microsoft)](#9-autogen-microsoft)
10. [Tools & Function Calling](#10-tools--function-calling)
11. [Memory in Multi-Agent Systems](#11-memory-in-multi-agent-systems)
12. [Real-World Example: Full Multi-Agent Workflow](#12-real-world-example-full-multi-agent-workflow)
13. [Common Problems & How to Solve Them](#13-common-problems--how-to-solve-them)
14. [Best Practices](#14-best-practices)
15. [Interview Questions & Answers](#15-interview-questions--answers)
16. [Quick Cheat Sheet](#16-quick-cheat-sheet)
17. [Beginner Mistakes](#17-beginner-mistakes)

---

## 1. Multi-Agent System Kya Hota Hai?

**Simple definition:** Multi-agent system ek aisa setup hai jahan **multiple AI agents** (har ek apna specific role/kaam rakhta hai) aapas mein milkar ek bara task complete karte hain — bilkul jaise ek company mein different departments (sales, support, engineering) mil kar kaam karte hain.

Har **agent** basically ek LLM (jaise GPT-4) hota hai jisko:
- Ek specific **role/goal** diya jata hai
- Kuch **tools** diye jate hain (jaise web search, calculator, database access)
- Kabhi kabhi apni **memory** hoti hai

> 💡 **Analogy:** Socho ek restaurant hai. Ek chef khana banata hai, ek waiter order leta hai, ek manager sab coordinate karta hai. Ye teeno alag "agents" hain jo mil kar restaurant chalate hain — Multi-agent system bhi bilkul isi tarah kaam karta hai, bas AI ke saath.

### Kyun Zaroorat Padi?

| Problem with Single Agent | Multi-Agent Solution |
|---|---|
| Ek hi LLM se sab kaam karwana confusing/complex prompt bana deta hai | Har agent ka apna simple, focused role hota hai |
| Bara task ek shot mein galat ho sakta hai | Task chhote steps mein divide hota hai, har agent apna part sahi karta hai |
| Debugging mushkil hoti hai (pata nahi kaunsa part fail hua) | Har agent independently test/debug ho sakta hai |
| Specialized knowledge ek prompt mein fit nahi hoti | Alag agents alag specialization rakh sakte hain (jaise "Researcher", "Coder", "Reviewer") |

---

## 2. Single Agent vs Multi-Agent

```
SINGLE AGENT:
User -> [ One Big Agent with all tools/knowledge ] -> Response


MULTI-AGENT:
User -> [ Orchestrator Agent ]
              |
      -------------------
      |         |        |
  [Researcher] [Coder] [Reviewer]
      |         |        |
      -------------------
              |
         Final Response
```

| Feature | Single Agent | Multi-Agent |
|---|---|---|
| Complexity | Simple tasks ke liye best | Complex, multi-step tasks ke liye best |
| Speed | Fast (ek hi call) | Slower (multiple calls, coordination) |
| Cost | Kam | Zyada (multiple LLM calls) |
| Reliability | Bara task mein galti ka chance zyada | Har agent focused hone se accuracy zyada |
| Example use case | "2+2 kya hai?" | "Ek company research karo, report likho, aur usko email karo" |

> ⚠️ **Important:** Har task ke liye multi-agent zaroori nahi. Agar simple task hai, single agent hi behtar hai — zyada agents = zyada cost aur zyada complexity.

---

## 3. Core Concepts

### Agent

Ek agent = LLM + Role + Tools + (optional) Memory. Ye decide karta hai ke kya karna hai aur kaise karna hai.

```python
# Conceptual example
agent = {
    "role": "Research Agent",
    "goal": "Find accurate information on the web",
    "tools": ["web_search"],
    "model": "gpt-4"
}
```

### Orchestrator / Supervisor

Ye ek special agent hota hai jo decide karta hai ke **kaunsa agent kab kaam karega**. Ye traffic-controller ki tarah hota hai.

### Tools

Functions jo agent call kar sakta hai — jaise web search, calculator, database query, API call.

### Handoff

Jab ek agent apna kaam complete karke task ko **doosre agent ko pass** kar deta hai.

### State

Shared data jo saare agents ke beech pass hoti hai (jaise conversation history, intermediate results).

### Workflow / Graph

Agents ka execution order — kaun pehle chalega, kis condition par kaunsa agent trigger hoga.

---

## 4. Common Multi-Agent Architectures

### 4.1 Sequential (Pipeline)

Agents ek ke baad ek chalte hain, jaise assembly line.

```
Agent A -> Agent B -> Agent C -> Final Output
```

**Example:** Researcher -> Writer -> Editor (blog post banane ke liye)

### 4.2 Supervisor / Orchestrator Pattern

Ek main agent decide karta hai kaunsa sub-agent call karna hai.

```
                 [ Supervisor ]
                /      |       \
         [Agent 1] [Agent 2] [Agent 3]
```

**Example:** Customer support system jahan supervisor decide karta hai ke query "billing", "technical", ya "general" hai, aur uske hisaab se sahi agent ko route karta hai.

### 4.3 Parallel (Concurrent)

Multiple agents **ek sath** (simultaneously) kaam karte hain, phir results combine hote hain.

```
           [ Task Splitter ]
          /       |         \
   [Agent A]  [Agent B]  [Agent C]
          \       |         /
           [ Combiner/Aggregator ]
```

**Example:** Ek document ko teen agents parallel mein alag alag angles se analyze karte hain (sentiment, summary, keywords).

### 4.4 Hierarchical

Multiple levels ke supervisors, jaise ek company ka org chart.

```
              [ CEO Agent ]
             /              \
   [Manager Agent A]   [Manager Agent B]
       /      \              /      \
 [Worker1] [Worker2]   [Worker3] [Worker4]
```

### 4.5 Collaborative / Debate Pattern

Agents aapas mein "discuss" karte hain, ek doosre ko challenge/review karte hain jab tak best answer na mil jaye.

**Example:** Ek agent code likhta hai, doosra agent us code ko review karta hai aur feedback deta hai, pehla agent improve karta hai — ye loop chalta hai jab tak quality achi na ho.

---

## 5. Agent Communication Patterns

| Pattern | Kaise kaam karta hai |
|---|---|
| **Shared State** | Saare agents ek common "state" (dictionary/object) ko read/write karte hain |
| **Message Passing** | Agents ek doosre ko messages bhejte hain (jaise chat) |
| **Direct Handoff** | Ek agent apna kaam khatam karke seedha doosre agent ko control de deta hai |
| **Blackboard Pattern** | Saare agents ek common "board" par apna kaam likhte hain, doosre uspar build karte hain |

```python
# Shared state example (conceptual)
state = {
    "user_query": "Plan a trip to Paris",
    "research_data": None,
    "itinerary": None,
    "final_response": None
}

# Agent 1 fills research_data
# Agent 2 reads research_data, fills itinerary
# Agent 3 reads itinerary, fills final_response
```

---

## 6. LangGraph for Multi-Agent Systems

LangGraph multi-agent systems banane ke liye sabse popular framework hai — kyunki ye **graph-based** hai (nodes = agents, edges = flow).

### Basic Structure

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    query: str
    research: str
    final_answer: str

def researcher_node(state: AgentState):
    # yahan LLM call hoti hai research karne ke liye
    state["research"] = f"Research findings for: {state['query']}"
    return state

def writer_node(state: AgentState):
    # yahan LLM call hoti hai final answer likhne ke liye
    state["final_answer"] = f"Based on research: {state['research']}"
    return state

# Graph banate hain
graph = StateGraph(AgentState)
graph.add_node("researcher", researcher_node)
graph.add_node("writer", writer_node)

graph.set_entry_point("researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", END)

app = graph.compile()
result = app.invoke({"query": "Python multi-agent systems", "research": "", "final_answer": ""})
print(result["final_answer"])
```

### Conditional Routing (Supervisor Pattern)

```python
def supervisor_node(state: AgentState):
    if "code" in state["query"].lower():
        return "coder"
    else:
        return "researcher"

graph.add_conditional_edges(
    "supervisor",
    supervisor_node,
    {"coder": "coder_node", "researcher": "researcher_node"}
)
```

| Concept | Explanation |
|---|---|
| `StateGraph` | Poore workflow ka blueprint — nodes aur edges define karta hai |
| `add_node()` | Ek agent/function ko graph mein add karta hai |
| `add_edge()` | Do nodes ke beech fixed connection banata hai (A ke baad hamesha B chalega) |
| `add_conditional_edges()` | Condition ke basis par decide karta hai next node kaunsa hoga |
| `set_entry_point()` | Batata hai graph kahan se start hoga |
| `END` | Special node jo workflow ko khatam karta hai |
| `.compile()` | Graph ko executable app mein convert karta hai |
| `.invoke()` | Graph ko run karta hai with initial state |

> 💡 **When to use LangGraph:** Jab aapko complex, branching, ya looping workflows chahiye hon (jaise agent khud decide kare ke usko dobara try karna hai ya nahi).

---

## 7. OpenAI Agents SDK

OpenAI ka apna framework hai multi-agent systems banane ke liye — simpler aur lightweight hai LangGraph ke comparison mein.

```python
from agents import Agent, Runner, handoff

# Individual agents banate hain
billing_agent = Agent(
    name="Billing Agent",
    instructions="You handle billing-related questions only."
)

technical_agent = Agent(
    name="Technical Agent",
    instructions="You handle technical support questions only."
)

# Triage agent jo decide karta hai kis agent ko bhejna hai
triage_agent = Agent(
    name="Triage Agent",
    instructions="Determine if the user's question is about billing or technical issues, and hand off accordingly.",
    handoffs=[billing_agent, technical_agent]
)

result = Runner.run_sync(triage_agent, "My internet is not working")
print(result.final_output)
```

| Concept | Explanation |
|---|---|
| `Agent()` | Ek naya agent banata hai with name, instructions, tools |
| `instructions` | System prompt jaisa hi hai — agent ka role define karta hai |
| `handoffs` | List of agents jinko ye agent control de sakta hai |
| `Runner.run_sync()` | Agent ko synchronously run karta hai |
| `Runner.run()` | Async version, `await` ke saath use hota hai |

### Tools ke sath Agent

```python
from agents import Agent, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

weather_agent = Agent(
    name="Weather Agent",
    instructions="Help users with weather information.",
    tools=[get_weather]
)
```

> 💡 **When to use OpenAI Agents SDK:** Jab simple, clean handoff-based systems chahiye hon aur OpenAI models hi use kar rahe ho.

---

## 8. CrewAI

CrewAI ek framework hai jo agents ko **"Crew"** (team) ki tarah organize karta hai — role-based collaboration ke liye best hai.

```python
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Senior Researcher",
    goal="Find accurate and relevant information",
    backstory="You are an expert researcher with years of experience."
)

writer = Agent(
    role="Content Writer",
    goal="Write engaging content based on research",
    backstory="You are a skilled writer who simplifies complex topics."
)

research_task = Task(
    description="Research the latest trends in AI agents",
    agent=researcher
)

writing_task = Task(
    description="Write a blog post based on the research",
    agent=writer
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task]
)

result = crew.kickoff()
print(result)
```

| Concept | Explanation |
|---|---|
| `Agent(role, goal, backstory)` | Har agent ki personality aur purpose define karta hai |
| `Task` | Ek specific kaam jo kisi agent ko assign hota hai |
| `Crew` | Agents aur tasks ka group jo mil kar kaam karta hai |
| `.kickoff()` | Poori crew ko run karta hai, sequentially ya parallel |

> 💡 **When to use CrewAI:** Jab role-based teams banani hon (jaise "Researcher + Writer + Editor" jaisi setup), aur readable/structured code chahiye ho.

---

## 9. AutoGen (Microsoft)

AutoGen agents ke beech **conversational** collaboration ke liye best hai — agents aapas mein chat karke problem solve karte hain.

```python
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-4"}
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config={"use_docker": False}
)

user_proxy.initiate_chat(
    assistant,
    message="Write Python code to calculate factorial of a number"
)
```

| Concept | Explanation |
|---|---|
| `AssistantAgent` | LLM-powered agent jo tasks solve karta hai |
| `UserProxyAgent` | Human ki jagah kaam karta hai — code execute bhi kar sakta hai |
| `initiate_chat()` | Do agents ke beech conversation start karta hai |

> 💡 **When to use AutoGen:** Jab agents ko aapas mein "discuss" karke, code run karke, ya iterative refinement karke problem solve karna ho (jaise coding assistants).

---

## 10. Tools & Function Calling

Agents ke paas **tools** hone chahiye taake wo sirf text generate na karein, balki actual kaam bhi kar sakein (jaise web search, calculation, database query).

```python
# General pattern (works similarly across frameworks)
def search_web(query: str) -> str:
    """Searches the web and returns results"""
    # actual search logic
    return f"Results for {query}"

def calculate(expression: str) -> float:
    """Evaluates a math expression"""
    return eval(expression)  # NOTE: eval() real projects mein risky hai, safe parser use karo

tools = [search_web, calculate]
```

| Field | Details |
|---|---|
| Purpose | Agent ko real-world actions perform karne ki ability deta hai |
| When to use | Jab agent ko sirf text nahi, balki data fetch/calculate/save karna ho |
| Common Mistakes | Tool ka description clear na likhna — agent confuse ho jata hai kab konsa tool use kare. Bohot zyada tools ek agent ko dena — performance kharab hoti hai |

> ⚠️ **Security Tip:** Kabhi bhi `eval()` ya raw code execution production mein directly use mat karo bina sandboxing ke — security risk hai.

---

## 11. Memory in Multi-Agent Systems

Agents ko kabhi kabhi **memory** chahiye hoti hai — pichli conversations ya facts yaad rakhne ke liye.

| Memory Type | Kya karta hai |
|---|---|
| **Short-term memory** | Current conversation/session ka context (jaise message history) |
| **Long-term memory** | Persistent data jo sessions ke across yaad rahe (jaise vector database mein) |
| **Shared memory** | Saare agents ek common memory access karte hain (state, blackboard) |

```python
# Simple conceptual example
conversation_history = []

def add_to_memory(role, content):
    conversation_history.append({"role": role, "content": content})

add_to_memory("user", "What's the weather in Lahore?")
add_to_memory("assistant", "It's sunny in Lahore.")
```

Real projects mein long-term memory ke liye **vector databases** (jaise Pinecone, Chroma, FAISS) use hote hain jahan embeddings store hoti hain aur semantic search se relevant memories retrieve hoti hain.

---

## 12. Real-World Example: Full Multi-Agent Workflow

Ek complete example — **"Research & Report" system** jo LangGraph jaise pattern follow karta hai:

```python
from typing import TypedDict, List

class AgentState(TypedDict):
    topic: str
    research_notes: List[str]
    draft: str
    final_report: str
    needs_revision: bool

# --- Agent 1: Researcher ---
def researcher_agent(state: AgentState) -> AgentState:
    print("🔍 Researcher is gathering information...")
    state["research_notes"] = [
        "Multi-agent systems improve task accuracy",
        "Popular frameworks: LangGraph, CrewAI, AutoGen"
    ]
    return state

# --- Agent 2: Writer ---
def writer_agent(state: AgentState) -> AgentState:
    print("✍️ Writer is drafting the report...")
    notes = " ".join(state["research_notes"])
    state["draft"] = f"Report on {state['topic']}: {notes}"
    return state

# --- Agent 3: Reviewer ---
def reviewer_agent(state: AgentState) -> AgentState:
    print("🔎 Reviewer is checking the draft...")
    if len(state["draft"]) < 50:
        state["needs_revision"] = True
    else:
        state["needs_revision"] = False
        state["final_report"] = state["draft"]
    return state

# --- Decision function ---
def route_after_review(state: AgentState) -> str:
    return "writer" if state["needs_revision"] else "end"

# --- Building the graph ---
from langgraph.graph import StateGraph, END

graph = StateGraph(AgentState)
graph.add_node("researcher", researcher_agent)
graph.add_node("writer", writer_agent)
graph.add_node("reviewer", reviewer_agent)

graph.set_entry_point("researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", "reviewer")
graph.add_conditional_edges("reviewer", route_after_review, {"writer": "writer", "end": END})

app = graph.compile()

initial_state = {
    "topic": "Multi-Agent AI Systems",
    "research_notes": [],
    "draft": "",
    "final_report": "",
    "needs_revision": False
}

result = app.invoke(initial_state)
print("\n📄 FINAL REPORT:", result["final_report"])
```

**Ye kya sikhata hai:**
- Har agent ka apna **focused kaam** hai (research, write, review)
- **State** saare agents ke beech share hoti hai
- **Conditional routing** hai — agar draft chota hai, wapas writer ke paas jata hai (loop)
- Ye real projects mein "self-correcting" agent pipelines ka basic pattern hai

---

## 13. Common Problems & How to Solve Them

| Problem | Solution |
|---|---|
| Agents infinite loop mein phas jaate hain | Max iteration limit set karo (jaise `max_turns=5`) |
| Agent galat tool choose karta hai | Tool descriptions ko clear aur specific likho |
| Cost bohot zyada ho jati hai (multiple LLM calls) | Chhote/cheaper models use karo simple sub-tasks ke liye (jaise GPT-4 sirf complex reasoning ke liye, GPT-3.5/mini baaki ke liye) |
| Agents ka output inconsistent hota hai | Structured output (Pydantic models, JSON schema) enforce karo |
| Debugging mushkil hoti hai | Logging/tracing tools use karo (LangSmith, AgentOps) taake dekh sako har agent ne kya kiya |
| Agent hallucinate karta hai (galat info deta hai) | Tools use karke real data fetch karwao, sirf LLM ki memory par depend mat karo |
| Race conditions parallel agents mein | Shared state ko carefully manage karo, locks ya proper aggregation logic use karo |

---

## 14. Best Practices

1. **Single Responsibility** — Har agent ka ek hi clear, focused role hona chahiye (jaise "sirf research karo", "sirf code likho")
2. **Clear Instructions** — Agent ke system prompt/instructions specific aur unambiguous hone chahiye
3. **Limit the number of agents** — Zyada agents = zyada complexity aur cost. Jitna kam utna behtar (jab tak kaam ho jaye)
4. **Use structured outputs** — Pydantic models ya JSON schema use karo taake agents ka output predictable ho
5. **Add guardrails** — Max retries, timeouts, aur validation checks add karo
6. **Test each agent individually** — Poore system ko test karne se pehle har agent ko alag test karo
7. **Monitor and log everything** — Production mein tracing tools use karo (LangSmith, Weights & Biases, AgentOps)
8. **Start simple** — Pehle single agent try karo, agar wo insufficient ho tabhi multi-agent mein jao

---

## 15. Interview Questions & Answers

**Q: Multi-agent system kya hai aur single agent se kyun better hai?**
> A: Multi-agent system multiple specialized LLM agents ka collaboration hai jahan har agent ka focused role hota hai. Ye complex tasks ko chhote, manageable parts mein divide karta hai jisse accuracy aur maintainability better hoti hai — lekin cost aur latency zyada hoti hai, isliye simple tasks ke liye single agent hi better hai.

**Q: Orchestrator/Supervisor pattern kya hai?**
> A: Ek central agent jo decide karta hai kaunsa sub-agent kab call hoga, based on incoming request ya current state. Ye "traffic controller" ki tarah kaam karta hai.

**Q: Agent handoff kya hota hai?**
> A: Jab ek agent apna kaam complete karke control (aur relevant context) doosre specialized agent ko pass kar deta hai, taake wo agla step handle kar sake.

**Q: LangGraph mein "state" ka kya role hai?**
> A: State ek shared data structure hai jo saare agents/nodes ke beech pass hoti hai — isme intermediate results, conversation history, aur flags (jaise "needs_revision") store hote hain jo workflow ke decisions control karte hain.

**Q: Multi-agent systems mein sabse bara challenge kya hota hai?**
> A: Coordination aur cost — agents ko sahi order mein chalana, infinite loops se bachna, aur multiple LLM calls ki wajah se cost/latency control karna sabse bare challenges hain.

**Q: Tools/Function calling multi-agent systems mein kyun zaroori hain?**
> A: Bina tools ke agent sirf text generate kar sakta hai — real actions (jaise data fetch karna, calculation karna, database update karna) ke liye tools zaroori hain jo agent ko "actually kaam karne" ki ability dete hain.

---

## 16. Quick Cheat Sheet

```
CORE CONCEPTS
Agent          = LLM + Role + Tools + Memory
Orchestrator   = Decides which agent runs next
Handoff        = One agent passes control to another
State          = Shared data across all agents
Tool           = Function agent can call for real actions

ARCHITECTURES
Sequential      A -> B -> C
Supervisor      Supervisor decides -> routes to A/B/C
Parallel        A + B + C run together -> combine
Hierarchical    Multi-level supervisors
Collaborative   Agents debate/review each other

FRAMEWORKS
LangGraph        graph-based, best for complex/branching workflows
OpenAI Agents SDK  lightweight, handoff-based, OpenAI-native
CrewAI           role-based teams, readable syntax
AutoGen          conversational agents, good for coding tasks

KEY LANGGRAPH FUNCTIONS
StateGraph()            define workflow
add_node()              add an agent
add_edge()              fixed connection
add_conditional_edges() conditional routing
set_entry_point()       starting node
compile() / invoke()    build and run

GOLDEN RULES
1. Start with single agent, upgrade to multi-agent only if needed
2. One agent = one clear job
3. Always set max iteration limits (avoid infinite loops)
4. Use structured outputs (Pydantic/JSON schema)
5. Log/trace everything for debugging
```

---

## 17. Beginner Mistakes

| Mistake | Sahi Tareeqa |
|---|---|
| Har chhote task ke liye multi-agent use karna | Pehle check karo simple single agent/prompt se kaam ho sakta hai ya nahi |
| Max iteration limit set na karna | Hamesha `max_turns` ya `max_iterations` set karo — warna infinite loop/cost explode ho sakta hai |
| Agent ke instructions vague likhna | Specific, clear role define karo (jaise "You ONLY handle billing questions", generic "You are helpful" nahi) |
| Tool descriptions ambiguous likhna | Clear docstrings likho taake agent sahi tool choose kare |
| State ko carelessly overwrite karna | State updates carefully design karo, especially parallel agents mein |
| Production mein bina monitoring ke deploy karna | Tracing/logging tools (LangSmith, AgentOps) use karo taake pata chale agent kya kar raha hai |
| Sab kaam ek hi expensive model se karwana | Simple sub-tasks ke liye chhote/cheaper models use karo, complex reasoning ke liye bara model |
| `eval()` jaisi unsafe cheezein directly production mein use karna | Sandboxed execution ya safe parsing libraries use karo |

---

## 🎯 Final Note

Multi-agent systems bohot powerful hain lekin **complexity aur cost bhi zyada** hoti hai. Hamesha simple se start karo — agar single agent se kaam chal raha hai to multi-agent mat banao. Jab task genuinely complex ho (multiple distinct skills chahiye hon, jaise research + coding + review), tab multi-agent architecture use karo.

**Practice tip:** Ek chhota project banao jaise "Research + Summarize + Email" agent system, LangGraph ya CrewAI use karke — isse concepts practically clear ho jayenge. 🚀
