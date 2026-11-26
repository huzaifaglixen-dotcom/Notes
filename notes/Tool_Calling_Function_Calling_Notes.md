# Tool Calling / Function Calling — Complete Notes

> **Tool Calling (Function Calling)** = Woh mechanism jisse ek LLM **external functions/APIs/tools** ko call kar sakta hai — jaise search karna, calculator use karna, database query karna, ya koi bhi custom function chalana — apne training data ki limitation ke bahar jaake.

---

## Table of Contents
1. Why Tool Calling is Needed
2. What is Tool/Function Calling (Simple Meaning)
3. How Tool Calling Works — Step-by-Step
4. Anatomy of a Tool Definition
5. The Full Request-Response Cycle
6. Parallel Tool Calls
7. Structured Output vs Tool Calling
8. Common Tools Used in Practice
9. Error Handling in Tool Calls
10. Multi-Step Tool Use (Chaining Tools)
11. Best Practices for Designing Tools
12. Common Mistakes
13. Cheat Sheet

---

## 1. Why Tool Calling is Needed

LLMs apne aap **kuch cheezein nahi kar sakte**:
- ❌ Real-time data nahi jaante (aaj ka weather, latest stock price)
- ❌ Precise math calculations me galti kar sakte hain (large numbers)
- ❌ Apne training data ke baad ki koi info nahi jaante (knowledge cutoff)
- ❌ Actual actions perform nahi kar sakte (email bhejna, database update karna)

**Tool Calling isko solve karta hai** — LLM ko ek "bridge" deta hai external world se connect hone ke liye.

> Analogy: LLM ek bahut smart insaan hai jisko **saari knowledge yaad hai** (jo usne padha tha), lekin uske paas **na phone hai, na calculator, na internet** — agar usse aaj ka weather poochoge, wo nahi bata payega, lekin agar aap usko ek "phone" (tool) de do jisse wo weather app check kar sake, toh wo turant bata dega.

---

## 2. What is Tool/Function Calling (Simple Meaning)

Developer LLM ko **available tools ki list** deta hai (har tool ka naam, kya karta hai, aur kaunse inputs chahiye). Jab LLM ko lagta hai ki koi tool use karna zaroori hai, wo:
1. **Khud text generate nahi karta** answer ke roop me
2. Balki ek **structured request** return karta hai: "Please call `tool_name` with these `parameters`"
3. Developer (code) us tool ko **actually execute** karta hai
4. Result wapas LLM ko diya jata hai
5. LLM us result ko use karke **final answer** generate karta hai

> **Important:** LLM khud tool ko run nahi karta — LLM sirf bolta hai "yeh tool, yeh parameters ke saath call karo". Actual execution **aapka code/system** karta hai.

---

## 3. How Tool Calling Works — Step-by-Step

```
1. Developer defines tools (name, description, input schema)
2. Developer sends: [User Query] + [Available Tools List] → LLM
3. LLM decides: "Do I need a tool, or can I answer directly?"
   
   IF tool needed:
      LLM returns: { tool_name: "get_weather", parameters: {"city": "Tokyo"} }
      → Developer's code executes get_weather("Tokyo")
      → Result: "18°C, Rainy"
      → This result is sent BACK to the LLM
      → LLM generates final answer using this result
   
   IF no tool needed:
      LLM directly generates the final text answer
```

---

## 4. Anatomy of a Tool Definition

Har tool ko LLM ko is tarah define karke diya jata hai (JSON Schema jaisa format):

```json
{
  "name": "get_weather",
  "description": "Get the current weather for a specific city",
  "input_schema": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "The name of the city, e.g. Tokyo"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "description": "Temperature unit"
      }
    },
    "required": ["city"]
  }
}
```

### Key Parts
| Part | Purpose |
|---|---|
| **name** | Tool ka unique identifier |
| **description** | LLM isko padh ke decide karta hai ki yeh tool kab use karna hai — **bahut important hai clear likhna** |
| **input_schema** | Tool ko kaunse parameters chahiye, unke types, aur kaunse required hain |

> **Golden Tip:** Tool ki `description` jitni clear aur specific hogi, LLM utna sahi decide kar payega ki **kab** aur **kaise** use karna hai. Vague description = galat/unnecessary tool calls.

---

## 5. The Full Request-Response Cycle

```
[Turn 1]
User: "What's the weather in Tokyo?"
           │
           ▼
LLM receives: User message + Tool definitions
           │
           ▼
LLM Response: "I need to call get_weather tool"
   → tool_use block: { name: "get_weather", input: {"city": "Tokyo"} }

[Developer's Code]
   → Executes: get_weather("Tokyo")
   → Returns: {"temp": "18°C", "condition": "Rainy"}

[Turn 2]
Developer sends back to LLM: 
   Previous conversation + Tool Result: {"temp": "18°C", "condition": "Rainy"}
           │
           ▼
LLM Final Response: "It's currently 18°C and rainy in Tokyo. You might want to bring an umbrella!"
```

> Notice: Yeh **do LLM calls** lagti hain — ek jo decide karta hai tool chahiye, doosri jo tool result use karke final answer banata hai.

---

## 6. Parallel Tool Calls

**Simple Meaning:** Kabhi-kabhi ek hi query ke liye **multiple tools ek saath** call karne ki zaroorat hoti hai — modern LLMs isko ek hi turn me handle kar sakte hain.

```
User: "What's the weather in Tokyo and New York?"

LLM Response (Parallel Tool Calls):
   → get_weather(city="Tokyo")
   → get_weather(city="New York")

Both executed simultaneously → Results returned together → LLM combines into one final answer
```

- ✅ Zyada **efficient** — sequential calls ki jagah ek saath execute hote hain, latency kam hoti hai.

---

## 7. Structured Output vs Tool Calling

Yeh do concepts thode similar lagte hain, lekin purpose alag hai:

| Feature | Structured Output | Tool Calling |
|---|---|---|
| **Purpose** | LLM ka final answer ek fixed format (JSON) me chahiye | LLM ko external action/data chahiye task complete karne ke liye |
| **Execution** | Kuch execute nahi hota, sirf format enforce hota hai | Actual function/API call hoti hai |
| **Example** | "Extract name and email as JSON" | "Get today's weather" |

> Kabhi-kabhi dono combine bhi hote hain — tool ka result bhi structured JSON format me expect kiya ja sakta hai.

---

## 8. Common Tools Used in Practice

| Tool Category | Examples |
|---|---|
| **Search** | Web search, internal document search (RAG retrieval bhi ek "tool" hi hai conceptually) |
| **Calculation** | Calculator, code execution (Python sandbox) |
| **Data Retrieval** | Database queries, API calls (weather, stock prices) |
| **Actions** | Send email, create calendar event, update a record |
| **File Operations** | Read/write files, generate documents |

---

## 9. Error Handling in Tool Calls

Real-world me tools **fail bhi ho sakte hain** — network error, invalid input, API down, etc. Isko handle karna zaroori hai.

```python
try:
    result = execute_tool(tool_name, parameters)
except Exception as e:
    result = f"Error: Tool failed with message: {str(e)}"

# Result (success or error) LLM ko wapas bhej do
# LLM ko decide karne do ki error ke case me kya karna hai (retry, fallback, ya user ko batana)
```

### Best Practice
- **Errors ko bhi LLM ko wapas bhejo** (chhupao mat) — LLM khud decide kar sakta hai ki retry karna hai, alternate approach lena hai, ya user ko politely batana hai ki "yeh info abhi available nahi hai".

---

## 10. Multi-Step Tool Use (Chaining Tools)

Complex tasks me, ek tool ka result **doosre tool ka input** ban sakta hai — yeh multiple rounds me chalta hai (yehi ReAct loop hai jo pichli notes me dekha tha).

### Example
```
User: "Convert the current temperature in Tokyo from Celsius to Fahrenheit"

Round 1: Call get_weather(city="Tokyo") → Result: 18°C
Round 2: Call convert_temperature(value=18, from="celsius", to="fahrenheit") → Result: 64.4°F
Final Answer: "It's currently 64.4°F in Tokyo."
```

---

## 11. Best Practices for Designing Tools

| Practice | Why |
|---|---|
| **Clear, specific descriptions** | LLM sahi decide kar payega kab use karna hai |
| **Minimal, focused tools** | Ek tool = ek clear job (don't make one giant tool that does everything) |
| **Good parameter naming** | `city` not `c`, `date_range` not `dr` — clarity matters |
| **Return clean, structured results** | LLM ke liye process karna aasan ho (JSON format better than messy text) |
| **Limit number of tools per request** | Bahut zyada tools dene se LLM confuse ho sakta hai kaunsa choose kare |
| **Include examples in descriptions (if ambiguous)** | Especially for tools jisme similar-sounding purpose ho |

---

## 12. Common Mistakes

| Mistake | Problem | Fix |
|---|---|---|
| Vague tool descriptions | LLM galat tool choose karta hai ya zaroorat na hone par bhi call karta hai | Clear, specific description likho with examples if needed |
| Too many tools at once | LLM confuse ho jata hai, wrong tool select karta hai | Group/limit tools relevant to the current context |
| Not validating tool inputs | LLM invalid parameters de sakta hai (e.g., wrong date format) | Validate inputs before executing, return clear error if invalid |
| Ignoring tool call errors | System crashes ya silently fails | Always handle exceptions, return error info back to LLM |
| Not testing edge cases | Tool fails on unexpected inputs in production | Test with various realistic and edge-case inputs before deploying |

---

## 13. Cheat Sheet

### One-Line Memory Tricks
- **Tool Calling** → "LLM decide karta hai kya call karna hai, code actually karta hai"
- **Tool Definition** → "Naam + Description + Input Schema"
- **Parallel Tool Calls** → "Ek saath multiple tools call karna, time bachana"
- **Multi-Step Tool Use** → "Ek tool ka result, doosre tool ka input banta hai"

### Quick Recap Flow
```
User Query → LLM (with tool definitions)
   → LLM decides: "Call tool X with params Y"
   → Code executes tool X
   → Result sent back to LLM
   → LLM generates final natural language answer
```

### Golden Rule
> **"LLM proposes which tool to call and with what — your code actually executes it. LLM is the brain, your code is the hands."**
