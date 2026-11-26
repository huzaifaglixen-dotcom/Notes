# 🔄 Handoff in OpenAI API — Asaan Alfaz Mein Notes

*(Jaise koi dost tumhe samjha raha ho)*

---

## 1. 🧭 Sabse Pehle - Handoff Hai Kya Cheez?

Dekho, jab tum AI Agents banate ho OpenAI ke sath, to kabhi kabhi ek agent akela sab kaam nahi kar sakta. Jaise agar tum ek customer support bot bana rahe ho, to wo bot refund bhi handle kare, billing bhi, technical issues bhi - ye sab ek hi agent se karwana mushkil ho jata hai kyunki har kaam ke liye alag knowledge aur instructions chahiye hoti hain.

To iska solution kya hai? Tum multiple agents banate ho - har agent ka apna specific kaam. Aur **Handoff** wo mechanism hai jisse ek agent doosre agent ko conversation "sonp" deta hai, poori tarah se.

> **Simple definition:** Handoff = ek AI agent ka poori tarah se conversation ka control doosre (zyada specialist) agent ko de dena.

### 🏦 Real-World Example: Bank Wala Scene

Socho tum bank gaye ho. Reception par jo banda baitha hai (ye hua **Agent 1 — Triage Agent**), wo tumhari baat sunta hai:

- Tum bolte ho: *"Mere account mein kuch galat transaction hai, dispute karna hai"*
- Reception wala samajhta hai: *"Arre ye to fraud department ka case hai, mera kaam nahi"*
- Wo tumhe seedha **Fraud Department (Agent 2 — Specialist Agent)** bhej deta hai
- Aur sirf bhejta nahi - **saath mein tumhari file bhi de deta hai** taake tumhe dobara apni problem explain na karni pare

Ab us waqt ke baad tum seedha fraud department wale se baat karoge. **Reception wala beech mein nahi aayega, poori tarah se side ho jayega.**

✅ Yehi Handoff hai - bas AI ki duniya mein. Full transfer, sirf refer nahi kiya.

---

## 2. ⚙️ Ye Kaam Kaise Karta Hai - Step by Step

Chalo dheere dheere samajhte hain, koi mushkil lafz nahi:

### Step 1: Har agent ke pass ek list hoti hai
Jab tum ek agent banate ho, tum usko batate ho ke "agar zarurat pare to tum inn agents ko handoff kar sakte ho". Ye list `handoffs` parameter mein di jati hai.

Jaise Triage Agent (jo sabse pehle user se baat karta hai) ke pass list hogi: Refund Agent, Billing Agent, waghera.

### Step 2: System khud-b-khud in agents ko "function" bana deta hai
Ye sabse interesting part hai. OpenAI ka model sirf **functions/tools call karna** janta hai - usko "agent" ka concept directly nahi pata. To SDK (jo framework hai) chupke se har agent ko ek function ki tarah present kar deta hai LLM ke saamne.

Jaise Refund Agent ban jata hai `transfer_to_refund_agent` naam ka ek function.

### Step 3: Model faisla karta hai
Jab user kuch bolta hai jaise "mujhe refund chahiye", to Triage Agent ka andar wala model (jo dimaag hai) sochta hai:

*"Ye to Refund Agent ka kaam hai"*

Aur wo bilkul aise hi decide karta hai jaise wo koi normal function call kar raha ho, jaise weather check karne wala function.

### Step 4: Yahan asli jadu hota hai - ek Agent object return hota hai
Normal function call mein tumhe data milta hai - jaise number, text, waghera. Lekin handoff mein jo cheez return hoti hai wo hai **poora ka poora doosra Agent** (uska code wala object).

System ye dekh leta hai ke *"arre ye to normal result nahi, ye to ek naya agent hai"* aur samajh jata hai ke ab control switch karna hai.

### Step 5: Runner agent switch kar deta hai
"Runner" wo cheez hai jo pura system chalata hai - poora orchestration. Jaise hi wo dekhta hai ke agent return hua hai, wo turant purane agent ko rok deta hai aur naye agent ko active kar deta hai. **Purana agent ab kuch nahi bolega.**

### Step 6: Poori chat history saath jati hai
Ye bohot important point hai - jo bhi baat cheet ab tak hui thi user aur pehle agent ke beech, wo saari **by default naye agent ko de di jati hai**. Isliye naya agent ko dobara se sawal nahi puchna parta "aap kya keh rahe the pehle". Bilkul waise jaise bank mein file saath chali gayi thi.

Agar developer chahe to isko customize bhi kar sakta hai - matlab pura history na de kar sirf zaroori hissa de, isko `input_filter` kehte hain.

### Step 7: Naya agent ab seedha user se baat karta hai
Ab Refund Agent hi user se baat karega, jaise wo hamesha se hi is conversation mein tha.

### 📋 Poora Flow Ek Nazar Mein:
```
User bolta hai kuch → Triage Agent sunta hai → LLM sochta hai "specialist chahiye"
→ transfer_to_refund_agent() call hota hai → Refund Agent object return hota hai
→ Runner dekhta hai "arre agent hai" → Control switch → Refund Agent ko poori history milti hai
→ Refund Agent ab seedha user se baat karta hai
```

---

## 3. 🔍 Do Concepts Ka Farak - Handoff vs Agent-as-a-Tool

Ye wala part thora zyada dhyan se samjho kyunki log yahan ghalti karte hain, bohot confuse hote hain.

### 📖 Pehle Dono Ki Definition Samjho

**🤝 Handoff:**
Control **poori tarah** doosre agent ko chala jata hai. Jaise reception wale ka example - wo poori tarah se side ho jata hai, ab tum seedha specialist se baat karte ho.

**🛠️ Agent-as-a-Tool:**
Ek manager agent hai jo control apne pass hi rakhta hai, bas doosre agent ko istemal karta hai jaise **ek tool/function ki tarah** - kaam karwata hai, jawab leta hai, aur khud hi final answer deta hai user ko.

### 🏢 Ek Aur Example Samajhne Ke Liye

Socho tumne kisi company ke manager se baat ki. Tumne pucha *"mera contract check karo ke usme koi masla to nahi"*.

- Manager khud contract nahi parhta - wo apne **legal expert** ko bolta hai "zara ye dekho"
- Legal expert check kar ke manager ko jawab batata hai
- Lekin **tumhari manager se hi baat hoti rehti hai**, legal expert tumse seedha kabhi baat nahi karta
- Manager hi tumhe wapis aake batata hai *"haan sab theek hai"* ya *"ye masla hai"*

Yahan control **kabhi transfer nahi hota** - manager hamesha in-charge rehta hai. Ye hai Agent-as-a-Tool.

### 📊 Farak Ek Table Mein

| Cheez | 🤝 Handoff | 🛠️ Agent-as-a-Tool |
|---|---|---|
| **Control kiske pass** | Naye agent ke pass poori tarah chala jata hai | Manager agent hamesha apne pass rakhta hai |
| **Memory / Context Load** | Poori chat history naye agent ko milti hai - thora zyada load | Sub-agent ko sirf wohi specific info milti hai jo zaroori hai - halka load |
| **User se baat kon karta hai** | User seedha naye agent se baat karta hai (Direct) | User hamesha manager se hi baat karta hai (Indirect), sub-agent nazar hi nahi aata |
| **Complexity** | Har agent ka kaam simple hota hai, lekin track karna mushkil hota hai ke "abhi control kiske pass hai" | Manager ka logic thora complex hota hai, lekin sab kuch ek hi jagah se control hota hai - samajhna aasan |

### 💬 Chota Sa Example Dono Ka

**Handoff wala example:**
```
User: "Mera $49 ka charge galat lag raha hai, refund chahiye"
Triage Agent: [andar hi andar Refund Agent ko call karta hai]
Refund Agent: "Ji bataiye, kaunsa transaction hai jo aap dispute karna chahte hain?"
```
👉 Dekho - ab Refund Agent seedha baat kar raha hai, Triage Agent gayab ho gaya poori tarah.

**Agent-as-a-Tool wala example:**
```
User: "Ye contract check karo, koi masla to nahi"
Manager Agent: [andar hi andar Compliance checker ko bolta hai check karne]
   → Compliance checker jawab deta hai: "3 clauses mein masla hai"
Manager Agent: "Maine check kiya, overall theek hai lekin 3 clauses mein 
                thora masla ho sakta hai, batao kya karna hai"
```
👉 Dekho - user ko pata bhi nahi chala ke koi Compliance Agent bhi tha beech mein. Sirf Manager se baat hui.

---

## 4. 🧠 Purane Agent Ka Kya Hota Hai + Back Handoff

### Handoff ke baad purane agent ka kya hota hai?

Bohot logon ka sawal hota hai - "jo pehla agent tha, uska kya hua?"

- Uska turn **turant khatam** ho jata hai - ab wo kuch process nahi karta
- Wo delete nahi hota, bas "background" mein chala jata hai - jaise wo **mic chor deta hai**
- Uska code (instructions, tools) wesa hi maujood rehta hai - bas active nahi hai abhi
- Poori conversation history (handoff se pehle wali) **preserve rehti hai** aur naye agent ko chali jati hai (jab tak `input_filter` na lagaya ho)

### 🔙 Back Handoff Kya Hai?

Agar zarurat pare to purana agent dobara bulaya ja sakta hai - iske liye **Back Handoff** ka concept hai.

**Back Handoff** ka matlab hai - specialist agent (jaise Refund Agent) apna kaam khatam karne ke baad **wapis Triage Agent ko control de deta hai**. Bilkul wahi mechanism jo forward handoff mein tha - bas ulta:

- Refund Agent ka LLM sochta hai "mera kaam ho gaya, ab wapis bhej do"
- Wo `transfer_to_triage_agent` jaisa function call karta hai
- Original Agent (Triage) ka object return hota hai
- Runner phir se control switch kar deta hai - wapis Triage Agent ke pass

**Practical use:** Billing Agent ne refund solve kar diya, ab agar user ka koi aur (unrelated) sawal ho to Billing Agent usse wapis Triage Agent ke pass bhej deta hai - bilkul jaise bank mein specialist tumhe wapis reception bhej deta hai.

⚠️ **Zaroori baat:** Ye automatic nahi hota. Agar tum chahte ho ke Refund Agent wapis Triage Agent ko bhej sake, to tumhe Refund Agent ke `handoffs` list mein **Triage Agent ko explicitly daalna parega**. Warna wo wapis nahi ja sakta - dono taraf ka rasta khud-b-khud nahi khulta.

---

## 5. 💻 Code Ka Blueprint - Bilkul Simple

Chalo ab code dekhte hain, Python style mein (OpenAI Agents SDK / Swarm jaisa):

```python
from agents import Agent, Runner

# 🧑‍💼 Refund wala specialist
refund_agent = Agent(
    name="Refund Agent",
    instructions="Tum refund requests handle karte ho, dosti se baat karo",
)

# 🧑‍💼 Billing wala specialist
billing_agent = Agent(
    name="Billing Agent",
    instructions="Tum billing disputes handle karte ho",
)

# 🧑‍💻 Triage - jo sabse pehle user se milta hai
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "Tum sabse pehle user ki baat sunte ho. "
        "Agar refund chahiye to Refund Agent ko bhej do. "
        "Agar billing ka masla hai to Billing Agent ko bhej do."
    ),
    handoffs=[refund_agent, billing_agent],  # 👈 ye list hai possible handoffs ki
)

# ▶️ Conversation run karo
result = Runner.run_sync(
    triage_agent,
    "Mujhse double charge ho gaya, refund chahiye"
)

print(result.final_output)
```

### 🔑 Yahan Ho Kya Raha Hai - Line by Line Samjho

1. `triage_agent` ko user ka message milta hai
2. Uska LLM sochta hai: *"ye to Refund Agent ka case hai"* → andar hi andar `transfer_to_refund_agent` call karta hai
3. SDK is call ko resolve karta hai **`refund_agent` object mein** (koi text nahi, poora agent object)
4. `Runner` dekh leta hai ke Agent return hua hai → **active agent switch kar deta hai**
5. `refund_agent` ko poori chat history milti hai aur ab wo hi final jawab banata hai user ke liye

### 🔙 Back Handoff Add Karna Ho To:

```python
refund_agent = Agent(
    name="Refund Agent",
    instructions="Refund handle karo, agar refund ka masla nahi to Triage ko wapis bhej do",
    handoffs=[triage_agent],  # 👈 ye line wapis jane ka rasta khol deti hai
)
```

Bas itni si baat hai - is line ke bina Refund Agent kabhi wapis Triage Agent ko nahi bhej sakta.

---

## 📌 Quick Recap - Sab Ek Nazar Mein

| Concept | Ek Line Mein Samjho |
|---|---|
| **Handoff** | Poora control specialist agent ko chala jata hai - bilkul jaise bank tumhe doosre department bhej deta hai |
| **Mechanism** | Function/tool call ke zariye hota hai; Agent object return hone se switch trigger hota hai |
| **Context** | Poori chat history default mein pass hoti hai (customize kar sakte ho `input_filter` se) |
| **Agent-as-Tool** | Manager hamesha in-charge rehta hai; sub-agent bas data deta hai, user se seedha baat nahi karta |
| **Back Handoff** | Same mechanism ulta - lekin explicitly `handoffs` list mein dono taraf add karna zaroori hai |
