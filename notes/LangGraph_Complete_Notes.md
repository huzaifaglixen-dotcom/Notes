# LangGraph — Complete Notes (Every Core Concept)

> LangGraph = Ek framework jo LLM applications ko **graph structure** (nodes + edges) ki tarah design karne deta hai — jisme **state**, **loops**, **conditional branching**, aur **multi-agent coordination** natively support hoti hai.

---

## Table of Contents

1. What is LangGraph (Recap)
2. Core Architecture Overview
3. State
4. Annotations & Reducers
5. Nodes
6. Edges (Normal, Conditional, Entry/Finish)
7. START and END
8. StateGraph — Building the Graph
9. Compiling the Graph
10. Conditional Routing / Router Pattern
11. Cycles & Loops
12. MessagesState & add_messages Reducer
13. Tools & ToolNode
14. Command Object (Combining State Update + Routing)
15. Checkpointers & Memory (Persistence)
16. Human-in-the-Loop (Interrupts)
17. Streaming
18. Subgraphs
19. Multi-Agent Patterns
20. Error Handling & Retries
21. Full Example (Putting It All Together)
22. Cheat Sheet

---

## 1. What is LangGraph (Recap)

**Simple Meaning:** LangGraph ek library hai jisme aap apne LLM application ka **flow ek graph ki tarah** banate ho — jahan har "step" ek **node** hai, aur unke beech connections **edges** hain. Isse complex, stateful, aur non-linear (loops/branches wale) AI agent workflows banana aasan ho jata hai.

> Analogy: Socho ek **flowchart/diagram** jo aap whiteboard pe banate ho — boxes (steps) aur arrows (flow direction). LangGraph usi diagram ko literally **code me convert** karne ka tareeka hai.

---

## 2. Core Architecture Overview

Har LangGraph application in **5 basic building blocks** se milke banta hai:

```
1. State       → Shared data jo poore graph me carry hoti hai
2. Nodes       → Functions jo state ko read/update karte hain (steps)
3. Edges       → Nodes ke beech connections (flow direction)
4. Conditional Edges → Decision points (kaunsa path lena hai)
5. Graph Compilation → Sab kuch jodkar ek executable graph banana
```

Simple Flow:
```
Define State → Define Nodes → Connect with Edges → Compile → Run/Invoke
```

---

## 3. State

**Simple Meaning:** State ek **shared "memory box"** hai jo poore graph ke through carry hoti hai. Har node isko **read** kar sakta hai aur **update** kar sakta hai. Yeh basically ek Python dictionary/object hai jisme aapke workflow ka saara important data store hota hai.

### Defining State

State usually `TypedDict` ya Pydantic model se define hoti hai:

```python
from typing import TypedDict

class MyState(TypedDict):
    question: str
    answer: str
    attempts: int
```

### Key Points
- State **poore graph ka "single source of truth"** hai.
- Har node function ko state (ya uska part) input milta hai, aur wo **updated state ka dict return karta hai**.
- LangGraph automatically state ko **merge** karta hai (based on reducers — neeche detail me).

### Example
```python
def my_node(state: MyState) -> MyState:
    return {"answer": "Generated answer here"}
```

---

## 4. Annotations & Reducers

Yeh concept thoda tricky hai but bahut important hai — isko step by step samjhte hain.

### 4.1 Problem: State Update Kaise Hoti Hai?

Jab multiple nodes state ke **same field** ko update karte hain, LangGraph ko pata hona chahiye ki **naya value purane value ko replace kare** ya **purane ke saath combine/append ho**.

- **Default behavior:** Naya value, purane value ko **overwrite (replace)** kar deta hai.
- Lekin kayi cases me hume chahiye hota hai ki values **append/accumulate** ho (jaise chat messages — purani messages delete nahi honi chahiye, naye add hone chahiye).

Isi problem ko solve karne ke liye **Annotations + Reducers** use hote hain.

### 4.2 Annotation

**Simple Meaning:** `Annotated` ek Python typing feature hai jisse hum state ke kisi field pe **extra metadata** attach kar sakte hain — is case me, "iss field ko update karte waqt kaunsa reducer function use karna hai".

```python
from typing import Annotated
from typing import TypedDict
import operator

class MyState(TypedDict):
    messages: Annotated[list, operator.add]   # reducer = operator.add
    question: str                              # no reducer = default overwrite
```

### 4.3 Reducer

**Simple Meaning:** Reducer ek **function hai jo batata hai ki naya value aur purana value ko kaise combine karna hai** jab state update hoti hai.

| Reducer | Behavior |
|---|---|
| **No reducer (default)** | Naya value, purane ko **replace** kar deta hai |
| **`operator.add`** | Naya value, purane list/string me **append/concatenate** ho jata hai |
| **Custom reducer function** | Aap khud define karo ki merge kaise ho (e.g., dictionary merge, max value rakho, duplicates remove karo, etc.) |

### Example — Custom Reducer

```python
def keep_max(old_value: int, new_value: int) -> int:
    return max(old_value, new_value)

class MyState(TypedDict):
    highest_score: Annotated[int, keep_max]
```

Ab jab bhi koi node `highest_score` update karega, LangGraph **naya aur purana dono value `keep_max` function ko denge**, aur jo return hoga wahi final state banega.

### Why This Matters
- **Bina reducer ke:** Agar 2 nodes ek hi state field update karte hain, toh sirf **last wala update survive** karega (overwrite ho jayega) — data loss ho sakta hai.
- **Reducer ke saath:** Aap control kar sakte ho ki data **accumulate, merge, ya intelligently combine** ho.

> Yeh concept especially important hai **parallel nodes** ke case me (jab multiple nodes ek saath chalte hain aur sabko same state field update karni ho) — reducer batata hai ki conflict kaise resolve hoga.

---

## 5. Nodes

**Simple Meaning:** Node = ek **function/step** jo state ko input leta hai, kuch kaam karta hai (LLM call, tool call, calculation, condition check), aur **updated state ka dictionary return karta hai**.

### Defining a Node

```python
def generate_answer(state: MyState) -> dict:
    response = llm.invoke(state["question"])
    return {"answer": response.content}
```

### Adding Node to Graph
```python
graph.add_node("generate_answer", generate_answer)
```
(First argument = node ka naam/ID, second argument = actual function)

### Key Points
- Node **kuch bhi ho sakta hai** — LLM call, API call, tool execution, data processing, human input wait, etc.
- Node ka naam (string ID) baad me edges define karte waqt use hota hai.
- Ek node **poori state return nahi karta** — sirf jo fields update karni hain, unka dictionary return karta hai (LangGraph baaki state ko as-is rakhta hai).

---

## 6. Edges (Normal, Conditional, Entry/Finish)

**Simple Meaning:** Edge = **connection/arrow** jo batata hai ki ek node ke baad **agla kaunsa node** chalega.

### 6.1 Normal (Direct) Edge

Simple, fixed connection — Node A ke baad hamesha Node B chalega.

```python
graph.add_edge("node_a", "node_b")
```

### 6.2 Conditional Edge (Router)

**Simple Meaning:** Yeh ek **decision point** hai — state ke current values check karke decide kiya jata hai ki **agla kaunsa node** chalega (jaise if/else).

```python
def route_decision(state: MyState) -> str:
    if state["attempts"] > 3:
        return "give_up"
    elif state["answer_is_correct"]:
        return "end"
    else:
        return "retry"

graph.add_conditional_edges(
    "check_answer",           # source node
    route_decision,            # function that decides next node
    {
        "give_up": "fallback_node",
        "end": END,
        "retry": "generate_answer"
    }
)
```

### Key Points
- `route_decision` function **state ko dekhta hai** aur ek **string (key)** return karta hai.
- Yeh string, **mapping dictionary** ke through actual node name se match hoti hai.
- Isi se **loops, branches, aur retries** possible hote hain.

### 6.3 Entry Point & Finish Point
- **Entry Point:** Graph kaunse node se **start** hoga.
- **Finish Point:** Graph kaunse node pe **end** hoga.
(In modern LangGraph, yeh `START` aur `END` special nodes se handle hota hai — neeche section 7 dekho.)

---

## 7. START and END

LangGraph me do special, built-in nodes hote hain:

| Special Node | Meaning |
|---|---|
| **START** | Graph ka **entry point** — yahan se execution shuru hoti hai |
| **END** | Graph ka **exit point** — yahan pahunchne pe execution **stop** ho jati hai |

```python
from langgraph.graph import StateGraph, START, END

graph.add_edge(START, "generate_answer")   # graph shuru hote hi yeh node chalega
graph.add_edge("final_node", END)           # yahan pahunchne pe graph khatam
```

> Har graph ka kam se kam ek path **START se END tak** hona chahiye, warna graph "stuck" reh sakta hai.

---

## 8. StateGraph — Building the Graph

`StateGraph` LangGraph ka main class hai jisse hum poora graph banate hain.

```python
from langgraph.graph import StateGraph

# Step 1: Define state schema
class MyState(TypedDict):
    question: str
    answer: str

# Step 2: Create graph object with that state schema
graph = StateGraph(MyState)

# Step 3: Add nodes
graph.add_node("generate", generate_answer)
graph.add_node("check", check_quality)

# Step 4: Add edges
graph.add_edge(START, "generate")
graph.add_edge("generate", "check")
graph.add_conditional_edges("check", route_decision, {"retry": "generate", "end": END})
```

---

## 9. Compiling the Graph

Graph define karne ke baad, usko **compile** karna padta hai — tabhi wo run karne layak (executable) banta hai.

```python
app = graph.compile()

# Ab isko invoke/run kar sakte ho:
result = app.invoke({"question": "What is LangGraph?"})
```

### Key Points
- `compile()` graph ki **validation** bhi karta hai (e.g., koi disconnected/unreachable node toh nahi hai).
- Compile karte waqt hi aap **checkpointer** (memory/persistence) bhi attach kar sakte ho (section 15 me dekho).

---

## 10. Conditional Routing / Router Pattern (Deep Dive)

Yeh pattern **decision-making agents** banane ke liye core hai.

### Simple Router Example
```python
def router(state: MyState) -> str:
    if "weather" in state["question"].lower():
        return "weather_tool"
    elif "math" in state["question"].lower():
        return "calculator_tool"
    else:
        return "general_llm"

graph.add_conditional_edges("classify_question", router, {
    "weather_tool": "call_weather_api",
    "calculator_tool": "call_calculator",
    "general_llm": "call_llm"
})
```

### Real-World Use Cases
- **Agent deciding which tool to use** (search, calculator, database query, etc.)
- **Quality check loops** (agar answer galat hai, retry karo)
- **Multi-agent handoff** (kaunsa specialized agent iss query ko handle karega)

---

## 11. Cycles & Loops

**Simple Meaning:** LangGraph me ek node se **wapas pichle node** pe ja sakte ho — isse "retry until correct" jaisi logic naturally ban jati hai.

```python
graph.add_edge("generate_answer", "check_quality")
graph.add_conditional_edges("check_quality", 
    lambda state: "retry" if not state["is_good"] else "done",
    {"retry": "generate_answer", "done": END}
)
```

### Important: Avoid Infinite Loops
- Hamesha ek **counter/limit** rakho state me (e.g., `attempts`), taaki agar model baar-baar galat answer de, toh ek limit ke baad **force stop/fallback** ho jaye.
- LangGraph me built-in **recursion limit** bhi hota hai jo infinite loops se app ko crash hone se bachata hai.

---

## 12. MessagesState & add_messages Reducer

Chatbot/conversation-based apps ke liye LangGraph ek **pre-built state schema** deta hai: `MessagesState`.

```python
from langgraph.graph import MessagesState

class MyState(MessagesState):
    extra_field: str
```

- `MessagesState` already ek `messages` field deta hai jisme reducer **`add_messages`** attached hota hai.
- `add_messages` reducer automatically **naye messages ko purani conversation history me append** karta hai (aur duplicate/same-ID messages ko intelligently update bhi kar sakta hai).

```python
{
    "messages": Annotated[list[AnyMessage], add_messages]
}
```

> Yeh chatbot jaisi apps me bahut common hai — har node LLM/human ka naya message "add" karta hai, purani history overwrite nahi hoti.

---

## 13. Tools & ToolNode

**Simple Meaning:** Tools = external functions (search, calculator, API calls) jo LLM "call" kar sakta hai. `ToolNode` ek **pre-built node** hai jo tool-calling ko automatically handle karta hai.

```python
from langgraph.prebuilt import ToolNode

tools = [search_tool, calculator_tool]
tool_node = ToolNode(tools)

graph.add_node("tools", tool_node)
```

### Typical Agent + Tools Pattern (ReAct Style)
```
LLM Node (decides: answer directly OR call a tool)
   │
   ▼ (conditional edge: "tool_call" or "end")
Tool Node (executes the tool, returns result)
   │
   ▼ (edge back to LLM node)
LLM Node (uses tool result to continue reasoning)
```

- Yeh pattern **ReAct (Reasoning + Acting)** ka LangGraph implementation hai.

---

## 14. Command Object (Combining State Update + Routing)

**Simple Meaning:** `Command` ek special object hai jisse ek node **ek hi jagah pe** — state update bhi kar sakta hai **aur** agla node bhi decide kar sakta hai (normally yeh do alag cheezein hoti hain: state update node ke return se, routing conditional edge se).

```python
from langgraph.types import Command

def my_node(state: MyState) -> Command:
    return Command(
        update={"answer": "some value"},
        goto="next_node"
    )
```

- ✅ Useful jab routing logic **node ke andar hi** decide honi ho (state update ke saath-saath).
- Especially **multi-agent systems** me useful — ek agent apna kaam karke, agla kaunsa agent chalega yeh bhi decide kar deta hai, ek hi jagah pe.

---

## 15. Checkpointers & Memory (Persistence)

**Simple Meaning:** Checkpointer LangGraph ko batata hai ki **state ko kahan save karna hai**, taaki:
- Conversation/workflow **beech me pause** ho sake aur baad me **resume** ho sake.
- Multiple separate conversations (threads) ka state **alag-alag track** ho sake.

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# Run with a specific thread ID (conversation identity)
config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke({"question": "Hi!"}, config=config)
```

### Types of Checkpointers
| Type | Use Case |
|---|---|
| **MemorySaver** | In-memory, testing/development ke liye (server restart pe data chala jata hai) |
| **SqliteSaver** | Local file-based persistence |
| **PostgresSaver** | Production-grade, database-backed persistence |

### Why This Matters
- Bina checkpointer ke, har `invoke()` call **fresh state se shuru** hoti hai (purani conversation yaad nahi rehti).
- Checkpointer ke saath, same `thread_id` use karke **conversation continue** ki ja sakti hai — jaise ek chatbot jo purani baatein yaad rakhta hai.

---

## 16. Human-in-the-Loop (Interrupts)

**Simple Meaning:** Kabhi-kabhi workflow ko **beech me rokna** padta hai — human se approval/input lene ke liye — phir wahi se aage continue karna hota hai.

```python
app = graph.compile(checkpointer=checkpointer, interrupt_before=["sensitive_action_node"])

# Graph "sensitive_action_node" se pehle ruk jayega
result = app.invoke({"question": "..."}, config=config)

# Human review karke, manually resume karta hai:
result = app.invoke(None, config=config)   # None = "continue from where it stopped"
```

### Use Cases
- Financial transactions ko approve karwana before executing.
- Sensitive actions (email send, database delete) pe human confirmation lena.
- Content moderation — human review before publishing.

---

## 17. Streaming

**Simple Meaning:** Poora result ek saath aane ka wait karne ke bajaye, LangGraph **step-by-step (node-by-node) updates stream** kar sakta hai — jaise real-time progress dikhana.

```python
for step in app.stream({"question": "..."}, config=config):
    print(step)   # har node ke complete hote hi output print hota hai
```

- ✅ Useful for showing **live progress** in UI (e.g., "Searching... Generating... Done").

---

## 18. Subgraphs

**Simple Meaning:** Ek bade graph ke andar, **ek chhota independent graph** bhi embed kiya ja sakta hai — jaise ek function ke andar doosra function call karna.

- Complex systems ko **modular** banane ke liye useful — har subgraph apna khud ka state/logic handle karta hai, lekin bade graph ka part bhi ban sakta hai.
- Example: Ek "Research Agent" subgraph, jo khud ke andar multiple steps (search → summarize → verify) rakhta hai, use ek bade "Customer Support Graph" ke ek node ki tarah use kiya ja sakta hai.

---

## 19. Multi-Agent Patterns

LangGraph multi-agent systems banane ke liye popular hai. Common patterns:

| Pattern | Kya Hota Hai |
|---|---|
| **Supervisor Pattern** | Ek "supervisor" agent decide karta hai ki kaunsa specialized agent (worker) query ko handle karega |
| **Network Pattern** | Multiple agents ek doosre ko directly call kar sakte hain (peer-to-peer jaisa) |
| **Hierarchical Pattern** | Supervisors ke multiple layers — top-level supervisor, jo sub-supervisors ko manage karta hai, jo aage workers ko manage karte hain |
| **Sequential/Pipeline Pattern** | Agents ek fixed order me kaam karte hain (Agent A → Agent B → Agent C) |

### Example — Supervisor Pattern (Conceptual)
```
                 ┌─────────────┐
                 │ Supervisor  │
                 └──────┬──────┘
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
  ┌──────────┐    ┌──────────┐     ┌──────────┐
  │Researcher│    │  Coder   │     │  Writer  │
  └──────────┘    └──────────┘     └──────────┘
```
Supervisor decide karta hai query dekh ke ki kaunsa agent (Researcher/Coder/Writer) call karna hai — phir uska output wapas supervisor ko milta hai, jo next decision leta hai.

---

## 20. Error Handling & Retries

- Nodes ke andar normal Python **try/except** use kar sakte ho.
- Conditional edges se **retry logic** bana sakte ho (agar node fail ho ya bad output de, toh wapas usi node pe route karo).
- **Recursion limit** set kar sakte ho taaki infinite retries na ho:
```python
app.invoke(input, config={"recursion_limit": 25})
```

---

## 21. Full Example (Putting It All Together)

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import operator

# 1. Define State with a reducer
class AgentState(TypedDict):
    question: str
    attempts: Annotated[int, operator.add]
    answer: str
    is_correct: bool

# 2. Define Nodes
def generate_answer(state: AgentState) -> dict:
    answer = llm.invoke(state["question"])
    return {"answer": answer, "attempts": 1}

def check_answer(state: AgentState) -> dict:
    correct = verify(state["answer"])
    return {"is_correct": correct}

# 3. Define Router (Conditional Edge Logic)
def route(state: AgentState) -> str:
    if state["is_correct"]:
        return "end"
    elif state["attempts"] >= 3:
        return "give_up"
    else:
        return "retry"

# 4. Build the Graph
graph = StateGraph(AgentState)
graph.add_node("generate", generate_answer)
graph.add_node("check", check_answer)
graph.add_node("fallback", lambda state: {"answer": "Sorry, couldn't solve it."})

graph.add_edge(START, "generate")
graph.add_edge("generate", "check")
graph.add_conditional_edges("check", route, {
    "retry": "generate",
    "give_up": "fallback",
    "end": END
})
graph.add_edge("fallback", END)

# 5. Compile with Memory
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# 6. Run
config = {"configurable": {"thread_id": "session-1"}}
result = app.invoke({"question": "What is 25 * 4?", "attempts": 0}, config=config)
print(result)
```

**Iss example me kya-kya use hua:**
- ✅ State (with reducer on `attempts`)
- ✅ Nodes (`generate`, `check`, `fallback`)
- ✅ Normal edges (START→generate, generate→check, fallback→END)
- ✅ Conditional edge/router (`route` function)
- ✅ Loop (check→generate agar retry chahiye)
- ✅ Checkpointer (memory/persistence)

---

## 22. Cheat Sheet

| Concept | One-Line Meaning |
|---|---|
| **State** | Shared data box jo poore graph me carry hoti hai |
| **Node** | Ek function/step jo state read/update karta hai |
| **Edge** | Fixed connection — Node A ke baad hamesha Node B |
| **Conditional Edge (Router)** | Decision point — state dekh ke agla node choose karo |
| **START/END** | Graph ka entry aur exit point |
| **Annotation** | State field pe metadata (jaise reducer) attach karna |
| **Reducer** | Batata hai naya aur purana value kaise merge/combine ho |
| **StateGraph** | Main class jisse graph banate hain |
| **compile()** | Graph ko run-karne-layak banata hai |
| **Cycle/Loop** | Node se wapas pichle node pe jana (retry logic) |
| **MessagesState** | Pre-built state for chat apps (with `add_messages` reducer) |
| **ToolNode** | Pre-built node jo tools ko execute karta hai |
| **Command** | State update + routing ek saath, ek node ke andar |
| **Checkpointer** | State ko save/persist karta hai (memory across runs) |
| **Interrupt** | Graph ko beech me rokna (human approval ke liye) |
| **Streaming** | Step-by-step live output dikhana |
| **Subgraph** | Ek graph ke andar doosra chhota graph embed karna |
| **Multi-Agent Pattern** | Multiple agents ka coordination (supervisor, network, hierarchical) |

### Golden One-Liner
> **"State carry hoti hai, Nodes kaam karte hain, Edges decide karte hain agla kya hoga, Reducers decide karte hain data kaise combine hoga."**
