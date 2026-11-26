# 🐍 Python Complete Notes for Beginners (3–6 Months Experience)
### Backend | AI | Automation | Real-World Projects ke liye

> Ye notes un logon ke liye hain jo Python thora bohot jaante hain (3-6 months experience) aur ab real-world projects (FastAPI, Django, AI, LangChain) mein jump karna chahte hain.

---

## 📑 Table of Contents

1. [Strings](#1-strings)
2. [Lists](#2-lists)
3. [Dictionaries](#3-dictionaries)
4. [Sets](#4-sets)
5. [Tuples](#5-tuples)
6. [Built-in Functions](#6-built-in-functions)
7. [Loops](#7-loops)
8. [Conditions](#8-conditions)
9. [Functions](#9-functions)
10. [Classes (OOP)](#10-classes-oop)
11. [Exceptions](#11-exceptions)
12. [File Handling](#12-file-handling)
13. [Modules](#13-modules)
14. [Async Python](#14-async-python)
15. [Useful Operators](#15-useful-operators)
16. [Common Real-World Methods](#16-common-real-world-methods)
17. [Python You'll See Every Day in Real Projects](#17-python-youll-see-every-day-in-real-projects)
    - [FastAPI](#171-fastapi)
    - [Django](#172-django)
    - [Flask](#173-flask)
    - [AI Projects](#174-ai-projects)
    - [LangChain](#175-langchain)
    - [LangGraph](#176-langgraph)
    - [OpenAI Agents SDK](#177-openai-agents-sdk)
    - [File Handling in Projects](#178-file-handling-in-projects)
    - [APIs (requests library)](#179-apis-requests-library)
    - [JSON](#1710-json)
    - [Databases](#1711-databases)
18. [One-Page Quick Revision Cheat Sheet](#18-one-page-quick-revision-cheat-sheet)
19. [Top 50 Most-Used Python Functions in Real Projects](#19-top-50-most-used-python-functions-in-real-projects)
20. [Top 50 Most-Used String/List/Dictionary Methods](#20-top-50-most-used-stringlistdictionary-methods)
21. [Interview Tips for Each Important Function](#21-interview-tips-for-each-important-function)
22. [Memory Tricks (Yaad Rakhne Ke Tarike)](#22-memory-tricks-yaad-rakhne-ke-tarike)
23. [Beginner Mistakes and How to Avoid Them](#23-beginner-mistakes-and-how-to-avoid-them)
24. [Bonus: Extra Topics You Should Also Know](#24-bonus-extra-topics-you-should-also-know)

---

## How to Read This Table Format

Har function/method is table format mein explain hoga:

| Field | Matlab |
|---|---|
| **Purpose** | Ye kya karta hai (simple English/Urdu mein) |
| **Syntax** | General likhne ka tareeqa |
| **Example** | Real code |
| **Output** | Code chalane se kya milega |
| **When to use** | Kab use karna hai |
| **Common Mistakes** | Beginners jo galti karte hain |

---

## 1. Strings

Strings text data hoti hai jaise `"Hello World"`. Python mein strings **immutable** hoti hain (ek baar ban gayi to change nahi ho sakti, naya string banta hai).

### `strip()`

| Field | Details |
|---|---|
| Purpose | String ke shuru aur akhir se extra spaces (ya specified characters) hata deta hai |
| Syntax | `string.strip(chars=None)` |
| Example | `"  hello  ".strip()` |
| Output | `'hello'` |
| When to use | User input clean karne ke liye, ya file se aaye data ke extra whitespace hatane ke liye |
| Common Mistakes | Beginners sochte hain ye string ke beech ke spaces bhi hata deta hai — nahi, sirf **shuru aur akhir** ke |

```python
text = "   Hello World   "
print(text.strip())        # 'Hello World'
print("xxHelloxx".strip("x"))  # 'Hello'
```

### `lstrip()`

| Field | Details |
|---|---|
| Purpose | Sirf **left side** (shuru) se spaces/characters hatata hai |
| Syntax | `string.lstrip(chars=None)` |
| Example | `"  hello".lstrip()` |
| Output | `'hello'` |
| When to use | Jab sirf left side clean karna ho |
| Common Mistakes | `rstrip()` se confuse ho jaate hain (l = left, r = right) |

```python
print("   Hello".lstrip())  # 'Hello'
```

### `rstrip()`

| Field | Details |
|---|---|
| Purpose | Sirf **right side** (akhir) se spaces/characters hatata hai |
| Syntax | `string.rstrip(chars=None)` |
| Example | `"hello   ".rstrip()` |
| Output | `'hello'` |
| When to use | File lines ke akhir se newline `\n` hatane ke liye common hai |
| Common Mistakes | `lstrip()` ke saath mix up |

```python
line = "Hello World\n"
print(line.rstrip())  # 'Hello World'
```

### `split()`

| Field | Details |
|---|---|
| Purpose | String ko break karke **list** bana deta hai, kisi separator ke basis par |
| Syntax | `string.split(separator=None, maxsplit=-1)` |
| Example | `"a,b,c".split(",")` |
| Output | `['a', 'b', 'c']` |
| When to use | CSV data parse karne, sentence ko words mein todne ke liye |
| Common Mistakes | Bina argument diye `.split()` space se split karta hai — log bhool jaate hain default comma nahi hai |

```python
sentence = "Python is fun"
print(sentence.split())          # ['Python', 'is', 'fun']
print("a,b,c".split(","))        # ['a', 'b', 'c']
print("a,b,c".split(",", 1))     # ['a', 'b,c']  -> maxsplit=1
```

### `join()`

| Field | Details |
|---|---|
| Purpose | List of strings ko ek single string bana deta hai (opposite of split) |
| Syntax | `separator.join(iterable)` |
| Example | `",".join(["a","b","c"])` |
| Output | `'a,b,c'` |
| When to use | List ko CSV ya sentence banane ke liye |
| Common Mistakes | `join()` string par call hota hai, list par nahi — beginners `list.join()` likhne ki koshish karte hain jo galat hai |

```python
words = ["Python", "is", "fun"]
print(" ".join(words))   # 'Python is fun'
```

### `replace()`

| Field | Details |
|---|---|
| Purpose | String ke andar ek text ko doosre text se replace karta hai |
| Syntax | `string.replace(old, new, count=-1)` |
| Example | `"I like cats".replace("cats", "dogs")` |
| Output | `'I like dogs'` |
| When to use | Text cleaning, censoring, data formatting |
| Common Mistakes | Original string change nahi hoti (immutable) — naya assign karna zaroori hai |

```python
s = "I like cats"
new_s = s.replace("cats", "dogs")
print(new_s)  # 'I like dogs'
print(s)      # 'I like cats' (original same rehta hai)
```

### `find()`

| Field | Details |
|---|---|
| Purpose | Substring ki position (index) return karta hai, nahi milne par `-1` |
| Syntax | `string.find(substring)` |
| Example | `"hello world".find("world")` |
| Output | `6` |
| When to use | Jab pata karna ho ke koi word maujood hai ya nahi, bina error ke |
| Common Mistakes | `index()` se confuse karte hain — `find()` error nahi deta, `-1` deta hai |

```python
print("hello world".find("world"))  # 6
print("hello world".find("xyz"))    # -1
```

### `index()`

| Field | Details |
|---|---|
| Purpose | Substring ki position return karta hai, nahi milne par **error** deta hai |
| Syntax | `string.index(substring)` |
| Example | `"hello".index("l")` |
| Output | `2` |
| When to use | Jab confirm ho ke substring maujood hai |
| Common Mistakes | Agar substring na mile to `ValueError` crash ho jata hai — `find()` use karna safer hai jab uncertain ho |

```python
print("hello".index("l"))  # 2
# "hello".index("z")  -> ValueError: substring not found
```

### `startswith()`

| Field | Details |
|---|---|
| Purpose | Check karta hai string kisi particular text se **start** hoti hai ya nahi |
| Syntax | `string.startswith(prefix)` |
| Example | `"hello.py".startswith("hello")` |
| Output | `True` |
| When to use | File extensions check karna, URL prefix check karna (jaise `"https://"`) |
| Common Mistakes | Case-sensitive hota hai — `"Hello".startswith("hello")` False hoga |

```python
filename = "report.pdf"
print(filename.startswith("report"))  # True
url = "https://example.com"
print(url.startswith("https://"))     # True
```

### `endswith()`

| Field | Details |
|---|---|
| Purpose | Check karta hai string kisi text par **end** hoti hai ya nahi |
| Syntax | `string.endswith(suffix)` |
| Example | `"photo.png".endswith(".png")` |
| Output | `True` |
| When to use | File type check karna (images, PDFs, etc.) |
| Common Mistakes | Tuple bhi de sakte hain: `endswith((".png", ".jpg"))` — beginners ye feature miss karte hain |

```python
files = ["a.png", "b.txt", "c.jpg"]
for f in files:
    if f.endswith((".png", ".jpg")):
        print(f, "is an image")
```

### `lower()`

| Field | Details |
|---|---|
| Purpose | Poori string ko **lowercase** mein convert karta hai |
| Syntax | `string.lower()` |
| Example | `"HELLO".lower()` |
| Output | `'hello'` |
| When to use | Case-insensitive comparison ke liye (jaise email match karna) |
| Common Mistakes | Original string change nahi hoti |

```python
print("HELLO World".lower())  # 'hello world'
```

### `upper()`

| Field | Details |
|---|---|
| Purpose | Poori string ko **uppercase** mein convert karta hai |
| Syntax | `string.upper()` |
| Example | `"hello".upper()` |
| Output | `'HELLO'` |
| When to use | Headings, alerts, ya standardized codes (jaise country codes) |
| Common Mistakes | Numbers/symbols par koi effect nahi hota |

```python
print("hello123".upper())  # 'HELLO123'
```

### `title()`

| Field | Details |
|---|---|
| Purpose | Har word ka pehla letter capital kar deta hai |
| Syntax | `string.title()` |
| Example | `"hello world".title()` |
| Output | `'Hello World'` |
| When to use | Names, headings display karne ke liye |
| Common Mistakes | Apostrophes ke saath ajeeb result deta hai: `"it's".title()` -> `"It'S"` |

```python
print("hello world".title())  # 'Hello World'
```

### `capitalize()`

| Field | Details |
|---|---|
| Purpose | Sirf **pehle letter** ko capital karta hai, baaki sab lowercase |
| Syntax | `string.capitalize()` |
| Example | `"hello WORLD".capitalize()` |
| Output | `'Hello world'` |
| When to use | Sentences ko properly format karne ke liye |
| Common Mistakes | `title()` se confuse hote hain — `capitalize()` sirf ek word capitalize karta hai (sentence ka pehla) |

```python
print("hello WORLD".capitalize())  # 'Hello world'
```

### `casefold()`

| Field | Details |
|---|---|
| Purpose | `lower()` jaisa hi hai lekin zyada aggressive — special/unicode characters ke liye better |
| Syntax | `string.casefold()` |
| Example | `"ß".casefold()` |
| Output | `'ss'` |
| When to use | International text comparison ke liye (German jaisi languages) |
| Common Mistakes | Beginners `lower()` hi use karte rehte hain, casefold ke baare mein pata nahi hota |

```python
print("Straße".casefold())  # 'strasse'
print("Straße".lower())     # 'straße'  (different!)
```

### `swapcase()`

| Field | Details |
|---|---|
| Purpose | Upper ko lower aur lower ko upper kar deta hai |
| Syntax | `string.swapcase()` |
| Example | `"Hello World".swapcase()` |
| Output | `'hELLO wORLD'` |
| When to use | Kam use hota hai real projects mein, kabhi kabhi fun/text transformation ke liye |
| Common Mistakes | Real-world use rare hai — interview mein trick question ke liye pucha ja sakta hai |

```python
print("Hello World".swapcase())  # 'hELLO wORLD'
```

### `count()`

| Field | Details |
|---|---|
| Purpose | String mein koi substring kitni baar aata hai, wo ginta hai |
| Syntax | `string.count(substring)` |
| Example | `"banana".count("a")` |
| Output | `3` |
| When to use | Word frequency check karne ke liye |
| Common Mistakes | Overlapping matches nahi ginta (jaise `"aaaa".count("aa")` -> `2`, not 3) |

```python
print("banana".count("a"))  # 3
print("aaaa".count("aa"))   # 2 (overlap count nahi hota)
```

### `format()`

| Field | Details |
|---|---|
| Purpose | String ke andar values insert karta hai (placeholders `{}` use karke) |
| Syntax | `"text {}".format(value)` |
| Example | `"My name is {}".format("Ali")` |
| Output | `'My name is Ali'` |
| When to use | Dynamic strings banane ke liye (f-strings se pehle ye common tha) |
| Common Mistakes | Index numbers galat order mein dena: `"{1} {0}".format("a","b")` -> `'b a'` |

```python
print("My name is {} and I am {} years old".format("Ali", 25))
print("{0} + {1} = {2}".format(2, 3, 5))
```

### f-strings (Formatted String Literals)

| Field | Details |
|---|---|
| Purpose | String ke andar directly variables/expressions daalne ka modern tareeqa |
| Syntax | `f"text {variable}"` |
| Example | `f"My name is {name}"` |
| Output | `'My name is Ali'` |
| When to use | **Hamesha** — ye sabse fast aur readable tareeqa hai (Python 3.6+) |
| Common Mistakes | `f` prefix lagana bhool jaate hain, phir `{name}` literally print hota hai |

```python
name = "Ali"
age = 25
print(f"My name is {name} and I am {age} years old")
print(f"Next year I will be {age + 1}")   # expressions bhi chal sakti hain
price = 49.999
print(f"Price: {price:.2f}")   # formatting: 'Price: 50.00'
```

> 💡 **Tip:** Real-world projects mein hamesha f-strings use karo — `.format()` aur `%` wala purana style avoid karo jab tak legacy code na ho.

---

## 2. Lists

Lists ordered aur **mutable** (changeable) collections hain. `[]` se banti hain.

### `append()`

| Field | Details |
|---|---|
| Purpose | List ke **akhir mein** ek item add karta hai |
| Syntax | `list.append(item)` |
| Example | `my_list.append(5)` |
| Output | List mein 5 add ho jata hai akhir mein |
| When to use | Loop mein data collect karte waqt |
| Common Mistakes | `append()` return kuch nahi karta (`None`) — `my_list = my_list.append(5)` likhne se list `None` ban jayegi! |

```python
fruits = ["apple", "banana"]
fruits.append("mango")
print(fruits)  # ['apple', 'banana', 'mango']
```

### `extend()`

| Field | Details |
|---|---|
| Purpose | Ek list mein doosri list (ya iterable) ke saare items add karta hai |
| Syntax | `list.extend(iterable)` |
| Example | `list1.extend(list2)` |
| Output | `list1` mein `list2` ke saare elements add ho jaate hain |
| When to use | Do lists merge karne ke liye |
| Common Mistakes | `append()` use kar dete hain jisse poori list ek single item ban jati hai: `[1,2].append([3,4])` -> `[1,2,[3,4]]` (galat agar merge chahiye) |

```python
a = [1, 2]
b = [3, 4]
a.extend(b)
print(a)  # [1, 2, 3, 4]

# Difference from append:
x = [1, 2]
x.append([3, 4])
print(x)  # [1, 2, [3, 4]]  <- nested list
```

### `insert()`

| Field | Details |
|---|---|
| Purpose | Specific position par item add karta hai |
| Syntax | `list.insert(index, item)` |
| Example | `list.insert(1, "new")` |
| Output | Index 1 par "new" insert ho jata hai |
| When to use | Jab item ko specific jagah par daalna ho, akhir mein nahi |
| Common Mistakes | Index out of range hone par error nahi aata — Python automatically end ya start mein daal deta hai |

```python
fruits = ["apple", "mango"]
fruits.insert(1, "banana")
print(fruits)  # ['apple', 'banana', 'mango']
```

### `remove()`

| Field | Details |
|---|---|
| Purpose | List se **value** ke basis par pehla matching item hata deta hai |
| Syntax | `list.remove(value)` |
| Example | `fruits.remove("banana")` |
| Output | "banana" list se hat jata hai |
| When to use | Jab value pata ho lekin index na pata ho |
| Common Mistakes | Agar value list mein nahi hai to `ValueError` aata hai |

```python
fruits = ["apple", "banana", "mango"]
fruits.remove("banana")
print(fruits)  # ['apple', 'mango']
```

### `pop()`

| Field | Details |
|---|---|
| Purpose | Index ke basis par item hata kar wo **return** bhi karta hai |
| Syntax | `list.pop(index=-1)` |
| Example | `fruits.pop(0)` |
| Output | Pehla item return hoga aur list se hat jayega |
| When to use | Jab item nikaalna ho aur uski value bhi chahiye ho (jaise stack/queue implementation) |
| Common Mistakes | Bina index diye `pop()` **last** item nikaalta hai, first nahi |

```python
fruits = ["apple", "banana", "mango"]
last = fruits.pop()
print(last)     # 'mango'
print(fruits)   # ['apple', 'banana']
```

### `clear()`

| Field | Details |
|---|---|
| Purpose | List ke saare elements hata deta hai (empty list bana deta hai) |
| Syntax | `list.clear()` |
| Example | `fruits.clear()` |
| Output | `[]` |
| When to use | List ko reset karne ke liye bina naya object banaye |
| Common Mistakes | `fruits = []` alag hai (naya object banata hai), `clear()` same object ko empty karta hai — memory reference wale scenarios mein farq padta hai |

```python
fruits = ["apple", "banana"]
fruits.clear()
print(fruits)  # []
```

### `copy()`

| Field | Details |
|---|---|
| Purpose | List ki **shallow copy** banata hai |
| Syntax | `list.copy()` |
| Example | `new_list = old_list.copy()` |
| Output | New independent list (top-level) |
| When to use | Jab original list ko safe rakhna ho, changes copy mein karni hon |
| Common Mistakes | `new_list = old_list` copy NAHI karta — dono same object ko point karte hain! Ye sabse common beginner mistake hai |

```python
a = [1, 2, 3]
b = a.copy()
b.append(4)
print(a)  # [1, 2, 3]      <- original safe
print(b)  # [1, 2, 3, 4]

# WRONG WAY:
c = a
c.append(99)
print(a)  # [1, 2, 3, 99]  <- 'a' bhi change ho gaya!
```

### `reverse()`

| Field | Details |
|---|---|
| Purpose | List ke elements ka order **ulta** kar deta hai (in-place) |
| Syntax | `list.reverse()` |
| Example | `nums.reverse()` |
| Output | List reverse order mein ho jati hai |
| When to use | Order palatne ke liye |
| Common Mistakes | Kuch return nahi karta — `nums = nums.reverse()` se `None` mil jayega |

```python
nums = [1, 2, 3]
nums.reverse()
print(nums)  # [3, 2, 1]
```

### `sort()`

| Field | Details |
|---|---|
| Purpose | List ko in-place sort (order mein arrange) karta hai |
| Syntax | `list.sort(key=None, reverse=False)` |
| Example | `nums.sort()` |
| Output | Ascending order mein sorted list |
| When to use | Data ko order mein dikhane ke liye (numbers, names, etc.) |
| Common Mistakes | `sort()` original list ko change karta hai aur `None` return karta hai. Agar naya sorted result chahiye bina original change kiye, to `sorted()` function use karo |

```python
nums = [3, 1, 4, 1, 5]
nums.sort()
print(nums)  # [1, 1, 3, 4, 5]

nums.sort(reverse=True)
print(nums)  # [5, 4, 3, 1, 1]

# Sorting with key
words = ["banana", "kiwi", "apple"]
words.sort(key=len)
print(words)  # ['kiwi', 'apple', 'banana']
```

### `index()` (for lists)

| Field | Details |
|---|---|
| Purpose | Value ki pehli occurrence ka index return karta hai |
| Syntax | `list.index(value)` |
| Example | `fruits.index("banana")` |
| Output | Index number |
| When to use | Jab position pata karni ho |
| Common Mistakes | Value na milne par `ValueError` aata hai |

```python
fruits = ["apple", "banana", "mango"]
print(fruits.index("banana"))  # 1
```

### `count()` (for lists)

| Field | Details |
|---|---|
| Purpose | List mein koi value kitni baar hai, wo ginta hai |
| Syntax | `list.count(value)` |
| Example | `[1,2,2,3].count(2)` |
| Output | `2` |
| When to use | Duplicate items count karne ke liye |
| Common Mistakes | Nested lists ke andar count nahi karta, sirf top-level |

```python
nums = [1, 2, 2, 3, 2]
print(nums.count(2))  # 3
```

### Slicing

| Field | Details |
|---|---|
| Purpose | List (ya string) ka ek **part/portion** nikaalta hai |
| Syntax | `list[start:stop:step]` |
| Example | `nums[1:4]` |
| Output | Index 1 se 3 tak ke elements |
| When to use | Data ka subset nikaalne ke liye, list palatne ke liye (`[::-1]`) |
| Common Mistakes | `stop` index **exclude** hota hai — beginners sochte hain include hoga |

```python
nums = [10, 20, 30, 40, 50]
print(nums[1:4])    # [20, 30, 40]
print(nums[:3])     # [10, 20, 30]
print(nums[2:])     # [30, 40, 50]
print(nums[::-1])   # [50, 40, 30, 20, 10]  (reverse trick)
print(nums[::2])    # [10, 30, 50]  (every 2nd element)
```

### List Comprehensions

| Field | Details |
|---|---|
| Purpose | Ek line mein naya list banane ka short aur fast tareeqa |
| Syntax | `[expression for item in iterable if condition]` |
| Example | `[x*2 for x in range(5)]` |
| Output | `[0, 2, 4, 6, 8]` |
| When to use | Jab loop se list banani ho — cleaner aur faster hai normal for-loop se |
| Common Mistakes | Zyada complex logic ko comprehension mein daal dena — readability kharab ho jati hai. Simple cases ke liye hi use karo |

```python
squares = [x**2 for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]

# With condition
evens = [x for x in range(10) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8]

# Real-world example: cleaning data
names = ["  ali", "SARA  ", "zain"]
cleaned = [n.strip().title() for n in names]
print(cleaned)  # ['Ali', 'Sara', 'Zain']
```


---

## 3. Dictionaries

Dictionaries `key: value` pairs store karti hain. `{}` se banti hain. Fast lookup ke liye best hain.

### `get()`

| Field | Details |
|---|---|
| Purpose | Key ki value nikaalta hai, agar key na ho to error ki jagah default value deta hai |
| Syntax | `dict.get(key, default=None)` |
| Example | `person.get("age", 0)` |
| Output | Agar "age" key hai to uski value, warna `0` |
| When to use | **Hamesha** jab pakka na ho ke key exist karti hai — crash se bachata hai |
| Common Mistakes | `dict["key"]` use karna jab key exist na ho -> `KeyError` crash |

```python
person = {"name": "Ali", "age": 25}
print(person.get("age"))          # 25
print(person.get("city"))         # None
print(person.get("city", "N/A"))  # 'N/A'
```

### `keys()`

| Field | Details |
|---|---|
| Purpose | Dictionary ki saari **keys** return karta hai |
| Syntax | `dict.keys()` |
| Example | `person.keys()` |
| Output | `dict_keys(['name', 'age'])` |
| When to use | Loop mein keys check karne ke liye |
| Common Mistakes | Direct list treat karte hain — actually list nahi, `dict_keys` object hai |

```python
person = {"name": "Ali", "age": 25}
print(list(person.keys()))  # ['name', 'age']
for k in person.keys():
    print(k)
```

### `values()`

| Field | Details |
|---|---|
| Purpose | Dictionary ki saari **values** return karta hai |
| Syntax | `dict.values()` |
| Example | `person.values()` |
| Output | `dict_values(['Ali', 25])` |
| When to use | Sirf values chahiye hon, keys nahi |
| Common Mistakes | Purane code mein order guaranteed nahi tha (Python 3.7+ mein insertion order fix hai) |

```python
print(list(person.values()))  # ['Ali', 25]
```

### `items()`

| Field | Details |
|---|---|
| Purpose | Key-value pairs ek saath (tuples ki form mein) return karta hai |
| Syntax | `dict.items()` |
| Example | `for k, v in person.items():` |
| Output | Har pair `(key, value)` |
| When to use | Loop mein key aur value dono chahiye hon |
| Common Mistakes | `for k, v in person:` likhna (bina `.items()`) — error aata hai |

```python
for key, value in person.items():
    print(f"{key}: {value}")
# name: Ali
# age: 25
```

### `update()`

| Field | Details |
|---|---|
| Purpose | Dictionary mein naye key-value pairs add ya existing ko update karta hai |
| Syntax | `dict.update(other_dict)` |
| Example | `person.update({"age": 26, "city": "Lahore"})` |
| Output | "age" update ho jayega, "city" naya add ho jayega |
| When to use | Multiple values ek saath update/add karne ke liye |
| Common Mistakes | Existing keys ko silently overwrite kar deta hai — data loss ka risk |

```python
person = {"name": "Ali", "age": 25}
person.update({"age": 26, "city": "Lahore"})
print(person)  # {'name': 'Ali', 'age': 26, 'city': 'Lahore'}
```

### `pop()` (for dict)

| Field | Details |
|---|---|
| Purpose | Key ke basis par item hata kar uski value return karta hai |
| Syntax | `dict.pop(key, default)` |
| Example | `person.pop("age")` |
| Output | Age ki value, aur dict se "age" remove ho jata hai |
| When to use | Key nikaal kar use karna ho, phir dict se hatana ho |
| Common Mistakes | Default value na do aur key na mile to `KeyError` aayega |

```python
person = {"name": "Ali", "age": 25}
age = person.pop("age")
print(age)     # 25
print(person)  # {'name': 'Ali'}
print(person.pop("city", "Not Found"))  # 'Not Found'
```

### `popitem()`

| Field | Details |
|---|---|
| Purpose | **Last inserted** key-value pair ko remove karke return karta hai |
| Syntax | `dict.popitem()` |
| Example | `person.popitem()` |
| Output | `('age', 25)` type tuple |
| When to use | Stack-jaisa behavior chahiye ho (LIFO) |
| Common Mistakes | Empty dictionary par call karne se `KeyError` aata hai |

```python
person = {"name": "Ali", "age": 25}
print(person.popitem())  # ('age', 25)
```

### `setdefault()`

| Field | Details |
|---|---|
| Purpose | Key exist karti hai to uski value return karta hai, warna naya key-value set karta hai |
| Syntax | `dict.setdefault(key, default)` |
| Example | `person.setdefault("city", "Unknown")` |
| Output | Agar "city" nahi hai to add ho jati hai with value "Unknown" |
| When to use | Counting/grouping logic mein bohot useful |
| Common Mistakes | `get()` se confuse hote hain — `setdefault()` dictionary ko modify **bhi** karta hai |

```python
word_count = {}
words = ["a", "b", "a", "c", "b", "a"]
for w in words:
    word_count.setdefault(w, 0)
    word_count[w] += 1
print(word_count)  # {'a': 3, 'b': 2, 'c': 1}
```

### `clear()` (for dict)

| Field | Details |
|---|---|
| Purpose | Dictionary ke saare items hata deta hai |
| Syntax | `dict.clear()` |
| Example | `person.clear()` |
| Output | `{}` |
| When to use | Dictionary reset karne ke liye |
| Common Mistakes | Same object empty hota hai, naya nahi banta |

```python
person = {"name": "Ali"}
person.clear()
print(person)  # {}
```

### `copy()` (for dict)

| Field | Details |
|---|---|
| Purpose | Dictionary ki shallow copy banata hai |
| Syntax | `dict.copy()` |
| Example | `new_dict = old_dict.copy()` |
| Output | Independent copy (top-level) |
| When to use | Original dictionary ko safe rakhte hue changes karni hon |
| Common Mistakes | `new_dict = old_dict` reference banata hai, copy nahi |

```python
a = {"x": 1}
b = a.copy()
b["x"] = 99
print(a)  # {'x': 1}
print(b)  # {'x': 99}
```

---

## 4. Sets

Sets **unique** aur **unordered** collections hain. Duplicate values automatically remove ho jaati hain.

### `add()`

| Field | Details |
|---|---|
| Purpose | Set mein ek naya element add karta hai |
| Syntax | `set.add(element)` |
| Example | `my_set.add(5)` |
| Output | 5 set mein add ho jata hai (agar pehle se nahi hai) |
| When to use | Unique items collect karne ke liye |
| Common Mistakes | Element pehle se hai to silently ignore ho jata hai, error nahi aata |

```python
s = {1, 2, 3}
s.add(4)
print(s)  # {1, 2, 3, 4}
```

### `remove()`

| Field | Details |
|---|---|
| Purpose | Set se element hata deta hai |
| Syntax | `set.remove(element)` |
| Example | `s.remove(2)` |
| Output | 2 set se hat jata hai |
| When to use | Jab pakka pata ho element maujood hai |
| Common Mistakes | Element na hone par `KeyError` aata hai |

```python
s = {1, 2, 3}
s.remove(2)
print(s)  # {1, 3}
```

### `discard()`

| Field | Details |
|---|---|
| Purpose | `remove()` jaisa hi hai lekin element na milne par error nahi deta |
| Syntax | `set.discard(element)` |
| Example | `s.discard(10)` |
| Output | Kuch nahi hota, silently skip |
| When to use | Safe removal ke liye jab unsure ho |
| Common Mistakes | Beginners `remove()` use karte reh jaate hain aur crash face karte hain |

```python
s = {1, 2, 3}
s.discard(10)  # no error
print(s)  # {1, 2, 3}
```

### `union()`

| Field | Details |
|---|---|
| Purpose | Do sets ke saare unique elements combine karta hai |
| Syntax | `set1.union(set2)` or `set1 \| set2` |
| Example | `{1,2}.union({2,3})` |
| Output | `{1, 2, 3}` |
| When to use | Do groups merge karne ke liye bina duplicates ke |
| Common Mistakes | Original sets change nahi hote, naya set return hota hai |

```python
a = {1, 2, 3}
b = {3, 4, 5}
print(a.union(b))  # {1, 2, 3, 4, 5}
```

### `intersection()`

| Field | Details |
|---|---|
| Purpose | Dono sets mein common elements return karta hai |
| Syntax | `set1.intersection(set2)` or `set1 & set2` |
| Example | `{1,2,3}.intersection({2,3,4})` |
| Output | `{2, 3}` |
| When to use | Common items find karne ke liye (jaise mutual friends) |
| Common Mistakes | `&` ko `and` samajh lena — alag cheezein hain |

```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a.intersection(b))  # {2, 3}
```

### `difference()`

| Field | Details |
|---|---|
| Purpose | Ek set mein hain lekin doosre mein nahi, wo elements return karta hai |
| Syntax | `set1.difference(set2)` or `set1 - set2` |
| Example | `{1,2,3}.difference({2,3})` |
| Output | `{1}` |
| When to use | Ek group mein kya extra hai doosre ke comparison mein |
| Common Mistakes | Order matter karta hai: `a - b` != `b - a` |

```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a.difference(b))  # {1}
```

---

## 5. Tuples

Tuples **immutable** ordered collections hain. Ek baar ban gayi to change nahi ho sakti.

### `count()` (for tuple)

| Field | Details |
|---|---|
| Purpose | Tuple mein value kitni baar aati hai |
| Syntax | `tuple.count(value)` |
| Example | `(1,2,2,3).count(2)` |
| Output | `2` |
| When to use | Fixed data mein frequency check karne ke liye |
| Common Mistakes | List ke `count()` jaisa hi lagta hai — bas tuple modify nahi ho sakti |

```python
t = (1, 2, 2, 3, 2)
print(t.count(2))  # 3
```

### `index()` (for tuple)

| Field | Details |
|---|---|
| Purpose | Value ki pehli position return karta hai |
| Syntax | `tuple.index(value)` |
| Example | `(10,20,30).index(20)` |
| Output | `1` |
| When to use | Position pata karni ho |
| Common Mistakes | Value na milne par `ValueError` |

```python
t = (10, 20, 30)
print(t.index(20))  # 1
```

> 💡 **Tuple vs List:** Tuple **immutable** hai (fast/safe, jab data change nahi hona chahiye — jaise coordinates `(x, y)`), List **mutable** hai (jab data change hoga).

---

## 6. Built-in Functions

Ye woh functions hain jo Python mein directly available hain, bina import kiye.

### `len()`

| Field | Details |
|---|---|
| Purpose | Kisi bhi collection (string, list, dict, etc.) ki **length** (size) batata hai |
| Syntax | `len(object)` |
| Example | `len([1,2,3])` |
| Output | `3` |
| When to use | Har jagah — validation, loops, conditions |
| Common Mistakes | `None` par call karne se error aata hai |

```python
print(len("hello"))       # 5
print(len([1, 2, 3]))     # 3
print(len({"a": 1, "b": 2}))  # 2
```

### `type()`

| Field | Details |
|---|---|
| Purpose | Kisi variable ka **data type** batata hai |
| Syntax | `type(object)` |
| Example | `type(5)` |
| Output | `<class 'int'>` |
| When to use | Debugging ke liye, ya type check karne ke liye |
| Common Mistakes | `type()` ko comparison mein use karna: `if type(x) == int` — behtar hai `isinstance()` use karo (inheritance handle karta hai) |

```python
print(type(5))        # <class 'int'>
print(type("hi"))      # <class 'str'>
print(type([1,2]))     # <class 'list'>
```

### `isinstance()`

| Field | Details |
|---|---|
| Purpose | Check karta hai object kisi particular type ka hai ya nahi |
| Syntax | `isinstance(object, type)` |
| Example | `isinstance(5, int)` |
| Output | `True` |
| When to use | Type checking ke liye — `type() ==` se better hai |
| Common Mistakes | Tuple of types bhi de sakte ho: `isinstance(x, (int, float))` — beginners iska pata nahi hota |

```python
print(isinstance(5, int))          # True
print(isinstance(5, (int, float))) # True
print(isinstance("hi", str))       # True
```

### `print()`

| Field | Details |
|---|---|
| Purpose | Output screen par dikhata hai |
| Syntax | `print(*values, sep=' ', end='\n')` |
| Example | `print("Hello", "World", sep="-")` |
| Output | `Hello-World` |
| When to use | Debugging, output display karne ke liye |
| Common Mistakes | `sep` aur `end` parameters ke baare mein pata nahi hota beginners ko |

```python
print("Hello", "World")             # Hello World
print("Hello", "World", sep="-")    # Hello-World
print("Loading", end="...")          # Loading... (no newline)
```

### `input()`

| Field | Details |
|---|---|
| Purpose | User se **keyboard input** leta hai |
| Syntax | `input(prompt)` |
| Example | `name = input("Enter name: ")` |
| Output | Jo user type kare wo string ban jata hai |
| When to use | Console-based programs mein user se data lene ke liye |
| Common Mistakes | `input()` hamesha **string** return karta hai — numbers ke liye `int(input())` karna padta hai |

```python
age = input("Enter your age: ")
print(type(age))         # <class 'str'> (even if user typed 25)
age = int(input("Enter your age: "))
print(type(age))         # <class 'int'>
```

### `range()`

| Field | Details |
|---|---|
| Purpose | Numbers ki ek sequence generate karta hai (loops ke liye) |
| Syntax | `range(start, stop, step)` |
| Example | `range(0, 10, 2)` |
| Output | `0, 2, 4, 6, 8` |
| When to use | For loops mein kitni baar repeat karna hai, ye decide karne ke liye |
| Common Mistakes | `stop` value **exclude** hoti hai — `range(5)` 0 se 4 tak jayega, 5 tak nahi |

```python
for i in range(5):
    print(i)  # 0 1 2 3 4

for i in range(2, 10, 2):
    print(i)  # 2 4 6 8
```

### `enumerate()`

| Field | Details |
|---|---|
| Purpose | Loop mein item ke saath uska **index** bhi deta hai |
| Syntax | `enumerate(iterable, start=0)` |
| Example | `for i, val in enumerate(["a","b"]):` |
| Output | `0 a` <br> `1 b` |
| When to use | Jab loop mein index bhi chahiye ho — manual counter (`i = 0; i += 1`) ki zaroorat khatam kar deta hai |
| Common Mistakes | `for i in enumerate(list):` likhna aur phir `i` ko value samajhna — actually `i` tuple hota hai `(index, value)` |

```python
fruits = ["apple", "banana", "mango"]
for index, fruit in enumerate(fruits):
    print(index, fruit)
# 0 apple
# 1 banana
# 2 mango

for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)  # 1 apple, 2 banana, 3 mango
```

### `zip()`

| Field | Details |
|---|---|
| Purpose | Do (ya zyada) lists ko **parallel** combine karta hai |
| Syntax | `zip(iterable1, iterable2, ...)` |
| Example | `zip([1,2],["a","b"])` |
| Output | `(1,'a'), (2,'b')` |
| When to use | Do related lists ko ek saath loop karne ke liye |
| Common Mistakes | Agar lists ki length different ho to shortest list ke hisaab se stop ho jata hai — extra items silently drop ho jaate hain |

```python
names = ["Ali", "Sara"]
ages = [25, 22]
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")
# Ali is 25 years old
# Sara is 22 years old

# converting to dict
print(dict(zip(names, ages)))  # {'Ali': 25, 'Sara': 22}
```

### `map()`

| Field | Details |
|---|---|
| Purpose | Har item par ek function apply karta hai aur naya iterable return karta hai |
| Syntax | `map(function, iterable)` |
| Example | `map(str.upper, ["a","b"])` |
| Output | `['A', 'B']` (list() se convert karne ke baad) |
| When to use | Poori list par ek transformation apply karni ho, bina explicit loop likhe |
| Common Mistakes | `map()` khud print nahi hota — `list()` se convert karna padta hai kyunki ye ek "lazy" map object return karta hai |

```python
nums = [1, 2, 3]
squared = list(map(lambda x: x**2, nums))
print(squared)  # [1, 4, 9]
```

### `filter()`

| Field | Details |
|---|---|
| Purpose | Condition ke basis par items ko **filter** karta hai |
| Syntax | `filter(function, iterable)` |
| Example | `filter(lambda x: x>2, [1,2,3,4])` |
| Output | `[3, 4]` (list() se convert karne ke baad) |
| When to use | List se sirf wo items chahiye jo condition satisfy karte hain |
| Common Mistakes | `map()` ki tarah ye bhi lazy hai — `list()` mein wrap karna zaroori hai |

```python
nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)  # [2, 4, 6]
```

### `sorted()`

| Field | Details |
|---|---|
| Purpose | Naya **sorted** list return karta hai, original change nahi hota |
| Syntax | `sorted(iterable, key=None, reverse=False)` |
| Example | `sorted([3,1,2])` |
| Output | `[1, 2, 3]` |
| When to use | Jab original data safe rakhna ho, sirf sorted copy chahiye ho |
| Common Mistakes | `list.sort()` se confuse hote hain — `sort()` list ka method hai (in-place), `sorted()` ek function hai (naya object return karta hai, kisi bhi iterable par kaam karta hai) |

```python
nums = [3, 1, 4, 1, 5]
print(sorted(nums))            # [1, 1, 3, 4, 5]
print(nums)                    # [3, 1, 4, 1, 5]  (unchanged!)
print(sorted(nums, reverse=True))  # [5, 4, 3, 1, 1]

people = [{"name": "Ali", "age": 25}, {"name": "Sara", "age": 22}]
print(sorted(people, key=lambda p: p["age"]))
```

### `sum()`

| Field | Details |
|---|---|
| Purpose | Numbers ki list ka **total** deta hai |
| Syntax | `sum(iterable, start=0)` |
| Example | `sum([1,2,3])` |
| Output | `6` |
| When to use | Total calculate karne ke liye (bill total, scores, etc.) |
| Common Mistakes | Strings ke sath use karne ki koshish karna -> error (`sum(["a","b"])` kaam nahi karega) |

```python
print(sum([1, 2, 3, 4]))  # 10
print(sum([1, 2, 3], 10))  # 16 (start=10)
```

### `min()`

| Field | Details |
|---|---|
| Purpose | Sabse **choti** value return karta hai |
| Syntax | `min(iterable)` |
| Example | `min([3,1,2])` |
| Output | `1` |
| When to use | Smallest value dhoondne ke liye |
| Common Mistakes | Empty list par call karne se error aata hai |

```python
print(min([3, 1, 4, 1, 5]))  # 1
print(min("banana"))          # 'a'
```

### `max()`

| Field | Details |
|---|---|
| Purpose | Sabse **badi** value return karta hai |
| Syntax | `max(iterable)` |
| Example | `max([3,1,2])` |
| Output | `3` |
| When to use | Largest value dhoondne ke liye |
| Common Mistakes | Different types mix karne se error aata hai (`max([1, "a"])` fail hoga) |

```python
print(max([3, 1, 4, 1, 5]))  # 5
```

### `any()`

| Field | Details |
|---|---|
| Purpose | Check karta hai kya iterable mein **koi bhi** ek value True hai |
| Syntax | `any(iterable)` |
| Example | `any([False, False, True])` |
| Output | `True` |
| When to use | Jab check karna ho ke condition kam se kam ek jagah satisfy hoti hai |
| Common Mistakes | Empty iterable par `False` return karta hai — beginners `True` expect karte hain |

```python
nums = [0, 0, 3, 0]
print(any(nums))  # True (kyunki 3 non-zero hai)
print(any([x > 10 for x in [1, 2, 3]]))  # False
```

### `all()`

| Field | Details |
|---|---|
| Purpose | Check karta hai kya iterable ke **saare** values True hain |
| Syntax | `all(iterable)` |
| Example | `all([True, True, True])` |
| Output | `True` |
| When to use | Jab check karna ho ke saari conditions satisfy hoti hain |
| Common Mistakes | Empty iterable par `True` return karta hai (opposite of `any()`) — confusing lag sakta hai |

```python
print(all([True, True, False]))  # False
print(all([x > 0 for x in [1, 2, 3]]))  # True
```

### `abs()`

| Field | Details |
|---|---|
| Purpose | Kisi number ki **absolute** (positive) value deta hai |
| Syntax | `abs(number)` |
| Example | `abs(-5)` |
| Output | `5` |
| When to use | Negative differences ko positive banane ke liye |
| Common Mistakes | Strings par use karne ki koshish karna -> error |

```python
print(abs(-5))    # 5
print(abs(5))     # 5
print(abs(-3.14)) # 3.14
```

### `round()`

| Field | Details |
|---|---|
| Purpose | Number ko given decimal places tak **round** karta hai |
| Syntax | `round(number, digits=0)` |
| Example | `round(3.14159, 2)` |
| Output | `3.14` |
| When to use | Money, percentages, ya kisi bhi precision-controlled output ke liye |
| Common Mistakes | Python "banker's rounding" use karta hai: `round(2.5)` -> `2` (not 3!) — ye surprise deta hai beginners ko |

```python
print(round(3.14159, 2))  # 3.14
print(round(2.5))          # 2  (banker's rounding!)
print(round(3.5))          # 4
```

### `open()`

| Field | Details |
|---|---|
| Purpose | File ko **open** karta hai (read/write ke liye) |
| Syntax | `open(filename, mode)` |
| Example | `open("data.txt", "r")` |
| Output | File object return hota hai |
| When to use | File se data read/write karne ke liye |
| Common Mistakes | File ko close karna bhool jaana — `with open()` use karo taake automatically close ho jaye |

```python
with open("data.txt", "r") as f:
    content = f.read()
print(content)
```

### `id()`

| Field | Details |
|---|---|
| Purpose | Object ka unique **memory address** (identity) deta hai |
| Syntax | `id(object)` |
| Example | `id(x)` |
| Output | Ek unique integer number |
| When to use | Debugging ke liye, ya check karna ke do variables **same object** hain ya alag |
| Common Mistakes | Real-world projects mein rarely use hota hai — mostly learning/debugging ke liye |

```python
a = [1, 2, 3]
b = a
print(id(a) == id(b))  # True (same object)
c = a.copy()
print(id(a) == id(c))  # False (different object)
```

### `dir()`

| Field | Details |
|---|---|
| Purpose | Object ke saare available attributes/methods list karta hai |
| Syntax | `dir(object)` |
| Example | `dir([])` |
| Output | List methods jaise `['append', 'clear', ...]` |
| When to use | Explore karne ke liye ke koi object kya kya kar sakta hai |
| Common Mistakes | Bohot saare "dunder" methods (`__init__` etc.) bhi show karta hai jo confusing lag sakte hain |

```python
print(dir([]))  # shows all list methods
```

### `help()`

| Field | Details |
|---|---|
| Purpose | Kisi function/module ki **documentation** dikhata hai |
| Syntax | `help(object)` |
| Example | `help(str.upper)` |
| Output | Documentation text |
| When to use | Jab kisi function ke baare mein detail chahiye ho, bina internet ke |
| Common Mistakes | Interactive terminal mein best kaam karta hai; scripts mein use karna common nahi hai |

```python
help(str.upper)
```

### `vars()`

| Field | Details |
|---|---|
| Purpose | Object ke `__dict__` (attributes) ko dictionary form mein deta hai |
| Syntax | `vars(object)` |
| Example | `vars(my_object)` |
| Output | `{'name': 'Ali', 'age': 25}` type dictionary |
| When to use | Class instances ke attributes debug karne ke liye |
| Common Mistakes | Sab objects ke saath kaam nahi karta (jaise built-in types ke saath error de sakta hai) |

```python
class Person:
    def __init__(self, name):
        self.name = name

p = Person("Ali")
print(vars(p))  # {'name': 'Ali'}
```

### `repr()`

| Field | Details |
|---|---|
| Purpose | Object ki **developer-friendly** string representation deta hai |
| Syntax | `repr(object)` |
| Example | `repr("hello")` |
| Output | `"'hello'"` (quotes ke saath) |
| When to use | Debugging ke liye, jab exact data type/format dekhna ho |
| Common Mistakes | `str()` se confuse hote hain — `str()` user-friendly hota hai, `repr()` debug-friendly |

```python
print(str("hello"))   # hello
print(repr("hello"))  # 'hello'
```

### `str()`, `int()`, `float()`, `bool()` (Type Conversion)

| Field | Details |
|---|---|
| Purpose | Data ko doosre type mein convert karte hain |
| Syntax | `str(x)`, `int(x)`, `float(x)`, `bool(x)` |
| Example | `int("25")` |
| Output | `25` (as integer) |
| When to use | User input, file data, ya API response ko sahi type mein convert karne ke liye |
| Common Mistakes | `int("25.5")` fail hoga — pehle `float()` phir `int()` karna padega. `bool("False")` -> `True` hai! (kyunki non-empty string hamesha truthy hoti hai) |

```python
print(int("25"))       # 25
print(str(25))          # '25'
print(float("3.14"))    # 3.14
print(bool(""))          # False
print(bool("False"))     # True  <- tricky!
print(bool(0))           # False
print(bool(1))           # True
```

### `list()`, `tuple()`, `set()`, `dict()` (Collection Conversion)

| Field | Details |
|---|---|
| Purpose | Kisi iterable ko given collection type mein convert karte hain |
| Syntax | `list(x)`, `tuple(x)`, `set(x)`, `dict(x)` |
| Example | `list("abc")` |
| Output | `['a', 'b', 'c']` |
| When to use | Data structure conversion ke liye (jaise duplicates hatane ke liye `set()`) |
| Common Mistakes | `dict()` ko random list se banane ki koshish karna — dict banane ke liye pairs (tuples) chahiye |

```python
print(list("abc"))              # ['a', 'b', 'c']
print(tuple([1, 2, 3]))          # (1, 2, 3)
print(set([1, 1, 2, 2, 3]))      # {1, 2, 3}  <- duplicates removed
print(dict([("a", 1), ("b", 2)]))  # {'a': 1, 'b': 2}
```

---

## 7. Loops

### `for`

| Field | Details |
|---|---|
| Purpose | Kisi iterable (list, string, range, etc.) ke har item par repeat karta hai |
| Syntax | `for item in iterable:` |
| Example | `for i in range(3): print(i)` |
| Output | `0 1 2` |
| When to use | Jab pata ho kitni baar ya kis cheez par loop chalana hai |
| Common Mistakes | Colon `:` bhoolna, ya indentation galat karna |

```python
for fruit in ["apple", "banana"]:
    print(fruit)
```

### `while`

| Field | Details |
|---|---|
| Purpose | Jab tak condition **True** hai, tab tak repeat karta hai |
| Syntax | `while condition:` |
| Example | `while x < 5:` |
| Output | Condition false hone tak chalta rehta hai |
| When to use | Jab pata na ho kitni baar loop chalega, sirf condition pata ho |
| Common Mistakes | **Infinite loop** — counter update karna bhool jaana |

```python
x = 0
while x < 5:
    print(x)
    x += 1  # yeh na likhein to infinite loop ban jayega
```

### `break`

| Field | Details |
|---|---|
| Purpose | Loop ko **turant** rok deta hai |
| Syntax | `break` |
| Example | `if x == 5: break` |
| Output | Loop wahin exit ho jata hai |
| When to use | Jab koi condition mile aur loop continue karne ki zaroorat na ho |
| Common Mistakes | Nested loops mein `break` sirf **innermost** loop ko rokta hai, outer loop chalta rehta hai |

```python
for i in range(10):
    if i == 5:
        break
    print(i)  # 0 1 2 3 4
```

### `continue`

| Field | Details |
|---|---|
| Purpose | Current iteration skip karke agli iteration par chala jata hai |
| Syntax | `continue` |
| Example | `if x % 2 == 0: continue` |
| Output | Us particular value ko skip karke aage badh jata hai |
| When to use | Kisi specific case ko skip karna ho lekin loop continue rakhna ho |
| Common Mistakes | `break` se confuse hote hain — `continue` loop rokta nahi, sirf ek iteration skip karta hai |

```python
for i in range(5):
    if i == 2:
        continue
    print(i)  # 0 1 3 4  (2 skip ho gaya)
```

### `pass`

| Field | Details |
|---|---|
| Purpose | Kuch bhi nahi karta — sirf **placeholder** hota hai |
| Syntax | `pass` |
| Example | `if x: pass` |
| Output | Koi output nahi, code sirf syntactically valid rehta hai |
| When to use | Jab function/class/loop ka structure likhna ho lekin logic baad mein likhna ho |
| Common Mistakes | `pass` aur `continue` ko confuse karna — `pass` kuch nahi karta, bas syntax error se bachata hai |

```python
def my_function():
    pass  # TODO: implement later

for i in range(5):
    if i == 2:
        pass  # nothing happens, loop continues normally
    print(i)
```

---

## 8. Conditions

### `if` / `elif` / `else`

| Field | Details |
|---|---|
| Purpose | Condition ke basis par decision lena |
| Syntax | `if condition: ... elif condition2: ... else: ...` |
| Example | `if age >= 18: print("Adult")` |
| Output | Condition ke hisaab se output |
| When to use | Har jagah jahan decision-making chahiye |
| Common Mistakes | `=` (assignment) aur `==` (comparison) mix karna. `elif` ki jagah `else if` likhna (Python mein sirf `elif` valid hai) |

```python
age = 20
if age < 13:
    print("Child")
elif age < 18:
    print("Teenager")
else:
    print("Adult")
```

---

## 9. Functions

### `def`

| Field | Details |
|---|---|
| Purpose | Naya function define karta hai |
| Syntax | `def function_name(parameters):` |
| Example | `def greet(name): print(f"Hello {name}")` |
| Output | Function call hone par output |
| When to use | Reusable code blocks banane ke liye |
| Common Mistakes | Colon bhoolna, indentation galat karna |

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Ali")  # Hello, Ali!
```

### `return`

| Field | Details |
|---|---|
| Purpose | Function se **value wapas** bhejta hai |
| Syntax | `return value` |
| Example | `return x + y` |
| Output | Function call karne wali jagah par value milti hai |
| When to use | Jab function ka result use karna ho |
| Common Mistakes | `return` ke baad ka code kabhi nahi chalta (function turant exit ho jata hai). `print()` aur `return` confuse karna — `print()` sirf dikhata hai, `return` value deta hai use karne ke liye |

```python
def add(a, b):
    return a + b

result = add(2, 3)
print(result)  # 5
```

### `*args`

| Field | Details |
|---|---|
| Purpose | Function ko **koi bhi number** of positional arguments accept karne deta hai |
| Syntax | `def func(*args):` |
| Example | `def total(*args): return sum(args)` |
| Output | `args` ek tuple ban jata hai saare arguments ka |
| When to use | Jab pata na ho kitne arguments aayenge |
| Common Mistakes | `args` ko list samajh lena — actually ye **tuple** hai |

```python
def total(*args):
    return sum(args)

print(total(1, 2, 3))       # 6
print(total(1, 2, 3, 4, 5)) # 15
```

### `**kwargs`

| Field | Details |
|---|---|
| Purpose | Function ko **koi bhi number** of keyword arguments accept karne deta hai |
| Syntax | `def func(**kwargs):` |
| Example | `def info(**kwargs): print(kwargs)` |
| Output | `kwargs` ek dictionary ban jata hai |
| When to use | Jab named arguments ki flexible number chahiye ho (jaise config options) |
| Common Mistakes | Order guaranteed nahi tha purane Python mein, lekin 3.7+ mein insertion order preserve hoti hai |

```python
def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

show_info(name="Ali", age=25, city="Lahore")
# name: Ali
# age: 25
# city: Lahore
```

### `lambda`

| Field | Details |
|---|---|
| Purpose | **Anonymous** (bina naam ki) chhoti function banata hai, ek line mein |
| Syntax | `lambda arguments: expression` |
| Example | `lambda x: x * 2` |
| Output | Function object jo call hone par result deta hai |
| When to use | Chhote, one-time-use functions ke liye (jaise `sort()`, `map()`, `filter()` ke saath) |
| Common Mistakes | Complex logic lambda mein daalne ki koshish karna — lambda sirf **single expression** support karta hai, statements (if/for blocks) nahi |

```python
square = lambda x: x ** 2
print(square(5))  # 25

# Common use with sort
people = [{"name": "Ali", "age": 25}, {"name": "Sara", "age": 22}]
people.sort(key=lambda p: p["age"])
print(people)
```

---

## 10. Classes (OOP)

### `class`

| Field | Details |
|---|---|
| Purpose | Naya **blueprint** (class) define karta hai objects banane ke liye |
| Syntax | `class ClassName:` |
| Example | `class Car:` |
| Output | Class definition, objects banane ke liye ready |
| When to use | Jab related data aur functions ko ek unit mein rakhna ho (OOP) |
| Common Mistakes | Class name convention `PascalCase` hota hai (jaise `MyClass`), lowercase use karna style guideline violate karta hai |

```python
class Car:
    def __init__(self, brand):
        self.brand = brand

    def show(self):
        print(f"This car is a {self.brand}")

my_car = Car("Toyota")
my_car.show()  # This car is a Toyota
```

### `__init__`

| Field | Details |
|---|---|
| Purpose | Class ka **constructor** — object banate waqt automatically call hota hai |
| Syntax | `def __init__(self, params):` |
| Example | `def __init__(self, name): self.name = name` |
| Output | Object ban jata hai apni initial values ke saath |
| When to use | Object create hote hi jo initial setup chahiye (jaise attributes set karna) |
| Common Mistakes | `self` parameter likhna bhool jaana |

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Ali", 25)
print(p.name)  # Ali
```

### `self`

| Field | Details |
|---|---|
| Purpose | Current object (instance) ko refer karta hai class ke andar |
| Syntax | Har method ka pehla parameter |
| Example | `def greet(self): print(self.name)` |
| Output | Object ke apne attributes access ho jaate hain |
| When to use | Har instance method mein zaroori hai |
| Common Mistakes | `self` likhna bhool jaana class methods mein — error aayega |

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        print(f"{self.name} says Woof!")

d = Dog("Rex")
d.bark()  # Rex says Woof!
```

### Inheritance

| Field | Details |
|---|---|
| Purpose | Ek class doosri class ki properties/methods **inherit** (le) sakti hai |
| Syntax | `class Child(Parent):` |
| Example | `class Dog(Animal):` |
| Output | Child class parent ke saare methods use kar sakti hai |
| When to use | Jab code reuse karna ho aur "is-a" relationship ho (Dog is an Animal) |
| Common Mistakes | Parent ka `__init__` call karna bhool jaana (super() use karke) |

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound")

class Dog(Animal):
    def speak(self):
        print(f"{self.name} barks")

d = Dog("Rex")
d.speak()  # Rex barks
```

### `super()`

| Field | Details |
|---|---|
| Purpose | Parent class ke methods/constructor ko call karta hai |
| Syntax | `super().__init__(args)` |
| Example | `super().__init__(name)` |
| Output | Parent ka `__init__` bhi run ho jata hai |
| When to use | Jab child class parent ka logic reuse karna chahe, plus apna extra logic add kare |
| Common Mistakes | `super()` use na karke parent ka `__init__` overwrite kar dena bina call kiye |

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # parent's __init__ call
        self.breed = breed

d = Dog("Rex", "Labrador")
print(d.name, d.breed)  # Rex Labrador
```

---

## 11. Exceptions

### `try` / `except` / `finally`

| Field | Details |
|---|---|
| Purpose | Errors ko **handle** karta hai bina program crash kiye |
| Syntax | `try: ... except Error: ... finally: ...` |
| Example | `try: 1/0 except ZeroDivisionError: print("Error")` |
| Output | Error catch ho jata hai, program crash nahi hota |
| When to use | Jahan error aane ka chance ho (file operations, API calls, user input, division) |
| Common Mistakes | Bina specific exception type diye bare `except:` likhna — ye sab errors silently hide kar deta hai jo debugging mushkil bana deta hai |

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
finally:
    print("This always runs")

# Better practice: specific exceptions
try:
    num = int(input("Enter a number: "))
except ValueError:
    print("That's not a valid number!")
except Exception as e:
    print(f"Something went wrong: {e}")
finally:
    print("Done trying")
```

### `raise`

| Field | Details |
|---|---|
| Purpose | Khud se ek exception **generate/throw** karta hai |
| Syntax | `raise ExceptionType("message")` |
| Example | `raise ValueError("Invalid input")` |
| Output | Program us jagah exception raise kar deta hai |
| When to use | Jab custom validation fail ho aur caller ko batana ho |
| Common Mistakes | Generic `Exception` raise karna jab specific type (jaise `ValueError`, `TypeError`) zyada meaningful hota |

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    return age

try:
    set_age(-5)
except ValueError as e:
    print(e)  # Age cannot be negative
```

---

## 12. File Handling

### `with open()`

| Field | Details |
|---|---|
| Purpose | File ko safely open karta hai aur kaam khatam hone par **automatically close** kar deta hai |
| Syntax | `with open(filename, mode) as f:` |
| Example | `with open("data.txt", "r") as f:` |
| Output | File object `f` milta hai use karne ke liye |
| When to use | **Hamesha** file open karte waqt — `open()` akela use karke `close()` bhoolne se bacha jata hai |
| Common Mistakes | `with` use na karke sirf `f = open(...)` likhna aur `f.close()` bhool jaana — file locked reh sakti hai |

```python
with open("data.txt", "r") as f:
    content = f.read()
print(content)
# file yahan automatically close ho chuki hoti hai
```

### `read()`

| Field | Details |
|---|---|
| Purpose | Poori file ka content ek **single string** mein padhta hai |
| Syntax | `file.read(size=-1)` |
| Example | `f.read()` |
| Output | Poora file content as string |
| When to use | Choti files ke liye jab poora content ek sath chahiye ho |
| Common Mistakes | Badi files par `read()` use karna — memory bhar sakti hai. Bari files ke liye line-by-line read karo |

```python
with open("data.txt", "r") as f:
    text = f.read()
print(text)
```

### `readline()`

| Field | Details |
|---|---|
| Purpose | File se sirf **ek line** padhta hai |
| Syntax | `file.readline()` |
| Example | `f.readline()` |
| Output | Ek line as string (with `\n`) |
| When to use | Jab line-by-line control chahiye ho |
| Common Mistakes | Bar bar call karna zaroori hai agli lines ke liye — loop mein use karna common hai |

```python
with open("data.txt", "r") as f:
    first_line = f.readline()
    print(first_line)
```

### `readlines()`

| Field | Details |
|---|---|
| Purpose | Poori file ko **list of lines** mein padhta hai |
| Syntax | `file.readlines()` |
| Example | `f.readlines()` |
| Output | `['line1\n', 'line2\n', ...]` |
| When to use | Jab har line ko separately process karna ho |
| Common Mistakes | Har line ke saath `\n` bhi aata hai — beginners bhool jaate hain `.strip()` karna |

```python
with open("data.txt", "r") as f:
    lines = f.readlines()
for line in lines:
    print(line.strip())
```

### `write()`

| Field | Details |
|---|---|
| Purpose | File mein ek **string** likhta hai |
| Syntax | `file.write(text)` |
| Example | `f.write("Hello\n")` |
| Output | File mein text add ho jata hai |
| When to use | File mein data save karne ke liye |
| Common Mistakes | Mode `"w"` use karna file ko **overwrite** kar deta hai — agar add karna ho to `"a"` (append) mode use karo |

```python
with open("output.txt", "w") as f:
    f.write("Hello World\n")

# Appending instead of overwriting
with open("output.txt", "a") as f:
    f.write("Another line\n")
```

### `writelines()`

| Field | Details |
|---|---|
| Purpose | Multiple lines (list of strings) file mein ek sath likhta hai |
| Syntax | `file.writelines(list_of_strings)` |
| Example | `f.writelines(["a\n", "b\n"])` |
| Output | File mein saari lines add ho jaati hain |
| When to use | Jab list of strings ko efficiently file mein daalna ho |
| Common Mistakes | Ye automatically `\n` add nahi karta — khud add karna padta hai har string ke akhir mein |

```python
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("output.txt", "w") as f:
    f.writelines(lines)
```

**File Modes Quick Reference:**

| Mode | Matlab |
|---|---|
| `"r"` | Read (default) |
| `"w"` | Write (overwrite karta hai) |
| `"a"` | Append (end mein add karta hai) |
| `"r+"` | Read + Write |
| `"rb"` / `"wb"` | Binary mode (images, PDFs ke liye) |

---

## 13. Modules

### `import`

| Field | Details |
|---|---|
| Purpose | Doosri file/library ka code use karne ke liye |
| Syntax | `import module_name` |
| Example | `import math` |
| Output | Module ke functions available ho jaate hain |
| When to use | Jab external libraries (jaise `os`, `math`, `requests`) use karni hon |
| Common Mistakes | Module install na hone par `ModuleNotFoundError` — `pip install module_name` karna padta hai pehle |

```python
import math
print(math.sqrt(16))  # 4.0
```

### `from ... import ...`

| Field | Details |
|---|---|
| Purpose | Poore module ki bajaye sirf **specific cheez** import karta hai |
| Syntax | `from module import name` |
| Example | `from math import sqrt` |
| Output | Ab `sqrt()` direct use kar sakte ho bina `math.` likhe |
| When to use | Jab poori library nahi, sirf ek function/class chahiye |
| Common Mistakes | Bohot saare imports ek saath karna aur naming conflicts create karna |

```python
from math import sqrt, pi
print(sqrt(16))  # 4.0
print(pi)          # 3.14159...
```

### `as`

| Field | Details |
|---|---|
| Purpose | Import kiye gaye module/function ko ek **alias** (nickname) deta hai |
| Syntax | `import module as alias` |
| Example | `import pandas as pd` |
| Output | Ab `pd` se poora `pandas` module access hota hai |
| When to use | Lambe naam wale modules ke liye shorthand banane ke liye (common convention) |
| Common Mistakes | Bohot ajeeb/confusing alias choose karna jo koi aur samajh na paye |

```python
import numpy as np
import pandas as pd

arr = np.array([1, 2, 3])
```

---

## 14. Async Python

### `async` / `await`

| Field | Details |
|---|---|
| Purpose | **Asynchronous** code likhne ke liye — ek kaam ka wait karte hue doosra kaam bhi ho sakta hai |
| Syntax | `async def func(): ... await something` |
| Example | `async def get_data(): result = await fetch()` |
| Output | Function bina block kiye chalta hai |
| When to use | APIs, database calls, ya kisi bhi "waiting" operation mein — jaise FastAPI endpoints, web scraping, multiple API calls parallel mein |
| Common Mistakes | `async def` function ko bina `await` ya event loop ke normal function ki tarah call karna — result milta hai ek "coroutine object", actual value nahi |

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(2)  # simulate waiting (jaise API call)
    return "Data received"

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())
```

> 💡 **Real-world use:** FastAPI mein `async def` endpoints likhe jaate hain taake server ek request ka wait kartay hue doosri requests bhi handle kar sake.

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/data")
async def get_data():
    # yahan koi async database call ya API call ho sakti hai
    return {"message": "Hello"}
```

---

## 15. Useful Operators

### `in`

| Field | Details |
|---|---|
| Purpose | Check karta hai koi value kisi collection mein **maujood** hai ya nahi |
| Syntax | `value in collection` |
| Example | `"a" in [1, "a", 2]` |
| Output | `True` |
| When to use | Membership check ke liye — lists, strings, dicts (keys check karta hai), sets |
| Common Mistakes | Dictionary mein `in` sirf **keys** check karta hai, values nahi |

```python
print(3 in [1, 2, 3])         # True
print("a" in "banana")         # True
d = {"name": "Ali"}
print("name" in d)              # True (checks keys)
print("Ali" in d)                # False (Ali is a value, not key)
```

### `not in`

| Field | Details |
|---|---|
| Purpose | Check karta hai value collection mein **maujood nahi** hai |
| Syntax | `value not in collection` |
| Example | `5 not in [1,2,3]` |
| Output | `True` |
| When to use | Jab confirm karna ho ke koi cheez missing hai |
| Common Mistakes | `not (x in y)` aur `x not in y` same result dete hain, lekin `not in` zyada readable hai |

```python
print(5 not in [1, 2, 3])  # True
```

### `is`

| Field | Details |
|---|---|
| Purpose | Check karta hai do variables **same object** hain (memory mein) |
| Syntax | `a is b` |
| Example | `x is None` |
| Output | `True`/`False` |
| When to use | `None` check karne ke liye hamesha `is` use karo, `==` nahi |
| Common Mistakes | `is` ko `==` ki jagah values compare karne ke liye use karna — `is` identity check karta hai, value equality nahi |

```python
x = None
print(x is None)   # True (correct way)

a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)  # True  (same values)
print(a is b)  # False (different objects in memory)
```

### `is not`

| Field | Details |
|---|---|
| Purpose | Check karta hai do variables **alag object** hain |
| Syntax | `a is not b` |
| Example | `x is not None` |
| Output | `True`/`False` |
| When to use | `None` check ke opposite case ke liye |
| Common Mistakes | `!= ` se confuse hote hain — `is not` identity, `!=` value inequality check karta hai |

```python
x = 5
if x is not None:
    print("x has a value")
```

---

## 16. Common Real-World Methods

Ye methods aksar real projects, APIs aur libraries mein baar baar dikhte hain.

| Method | Kahan milta hai | Kya karta hai |
|---|---|---|
| `.strip()` | Text cleaning | Extra spaces hatata hai |
| `.json()` | `requests` library (API responses) | API response ko Python dict mein convert karta hai |
| `.text` | `requests` library | Response ka raw text (string) deta hai |
| `.items()` | Dictionaries | Key-value pairs loop karne ke liye |
| `.get()` | Dictionaries, APIs, Django ORM | Safe value fetch karta hai |
| `.copy()` | Lists, Dicts | Shallow copy banata hai |
| `.update()` | Dictionaries | Values update/add karta hai |
| `.append()` | Lists | Naya item add karta hai |
| `.sort()` | Lists | List ko order mein arrange karta hai |
| `.reverse()` | Lists | Order ulta karta hai |

### `.json()` aur `.text` (requests library se)

```python
import requests

response = requests.get("https://api.example.com/users")

print(response.text)   # raw string response
print(response.json()) # parsed as Python dict/list
```

| Field | Details |
|---|---|
| Purpose | `.json()` API response ko Python object (dict/list) mein convert karta hai, `.text` raw string deta hai |
| When to use | `.json()` jab response JSON format mein ho (aksar hota hai), `.text` jab HTML/plain text chahiye |
| Common Mistakes | `.json()` call karna jab response actually JSON na ho — `JSONDecodeError` aayega |

---

## 17. Python You'll See Every Day in Real Projects

### 17.1 FastAPI

FastAPI mein aksar ye patterns dikhte hain:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.get("/")
def home():
    return {"message": "Welcome"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, "name": "Ali"}

@app.post("/users")
async def create_user(user: User):
    return {"message": f"User {user.name} created"}
```

- `@app.get()`, `@app.post()` — **decorators** jo route define karte hain
- `BaseModel` — Pydantic se data validation ke liye
- `async def` — non-blocking endpoints ke liye
- `HTTPException` — proper error response bhejne ke liye

### 17.2 Django

```python
from django.db import models
from django.shortcuts import render, get_object_or_404

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product.html", {"product": product})
```

- `models.Model` — database table define karne ke liye
- `get_object_or_404()` — object na milne par automatically 404 error deta hai
- `render()` — HTML template ko response ke saath bhejta hai

### 17.3 Flask

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello World"})

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.json
    return jsonify({"received": data})

if __name__ == "__main__":
    app.run(debug=True)
```

- `jsonify()` — Python dict ko JSON response mein convert karta hai
- `request.json` — incoming request ka JSON body
- `app.run(debug=True)` — development server chalata hai (auto-reload ke saath)

### 17.4 AI Projects

```python
import numpy as np

data = np.array([1, 2, 3, 4, 5])
print(data.mean())    # average
print(data.std())     # standard deviation

# Common pattern: preprocessing
normalized = (data - data.min()) / (data.max() - data.min())
print(normalized)
```

- `numpy` — numerical operations ke liye
- `.mean()`, `.std()` — statistics calculate karne ke liye
- Data normalization/scaling AI projects mein bohot common hai

### 17.5 LangChain

```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write a short summary about {topic}"
)

chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(topic="Python programming")
print(result)
```

- `PromptTemplate` — dynamic prompts banane ke liye
- `LLMChain` — prompt + model ko combine karta hai ek "chain" mein
- `.run()` — chain execute karta hai aur result deta hai

### 17.6 LangGraph

```python
from langgraph.graph import StateGraph, END

def node_a(state):
    state["count"] += 1
    return state

def should_continue(state):
    return "continue" if state["count"] < 3 else "end"

graph = StateGraph(dict)
graph.add_node("a", node_a)
graph.set_entry_point("a")
graph.add_conditional_edges("a", should_continue, {"continue": "a", "end": END})

app = graph.compile()
result = app.invoke({"count": 0})
print(result)  # {'count': 3}
```

- `StateGraph` — AI agent ke steps (nodes) ka flow define karta hai
- `add_conditional_edges()` — condition ke basis par next step decide karta hai
- Ye agent workflows banane ke liye use hota hai (loops, decisions)

### 17.7 OpenAI Agents SDK

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What is Python?"}
    ]
)

print(response.choices[0].message.content)
```

- `client.chat.completions.create()` — model ko call karne ka main function
- `messages` — conversation history ka list
- `response.choices[0].message.content` — actual reply text yahan milta hai

### 17.8 File Handling in Projects

```python
import os

# Check if file exists before reading
if os.path.exists("config.json"):
    with open("config.json", "r") as f:
        data = f.read()

# Working with paths
folder = "uploads"
filename = "report.pdf"
full_path = os.path.join(folder, filename)
print(full_path)  # uploads/report.pdf
```

### 17.9 APIs (requests library)

```python
import requests

response = requests.get("https://api.example.com/data", params={"page": 1})

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")

# POST request
payload = {"name": "Ali", "email": "ali@example.com"}
response = requests.post("https://api.example.com/users", json=payload)
```

- `response.status_code` — HTTP status check karne ke liye (200 = success)
- `params` — URL query parameters bhejne ke liye
- `json=payload` — request body ko JSON format mein bhejta hai automatically

### 17.10 JSON

```python
import json

# Python dict -> JSON string
data = {"name": "Ali", "age": 25}
json_string = json.dumps(data)
print(json_string)  # '{"name": "Ali", "age": 25}'

# JSON string -> Python dict
parsed = json.loads(json_string)
print(parsed["name"])  # Ali

# Read/write JSON files
with open("data.json", "w") as f:
    json.dump(data, f)

with open("data.json", "r") as f:
    loaded = json.load(f)
```

| Function | Kya karta hai |
|---|---|
| `json.dumps()` | Python object -> JSON **string** |
| `json.loads()` | JSON string -> Python **object** |
| `json.dump()` | Python object -> JSON **file** |
| `json.load()` | JSON file -> Python **object** |

> 💡 **Memory trick:** "s" wale functions (`dumps`, `loads`) **strings** ke saath kaam karte hain. Bina "s" wale (`dump`, `load`) **files** ke saath.

### 17.11 Databases

```python
import sqlite3

# Connect to database
conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
""")

# Insert data
cursor.execute("INSERT INTO users (name) VALUES (?)", ("Ali",))
conn.commit()

# Read data
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print(rows)

conn.close()
```

- `cursor.execute()` — SQL query run karta hai
- `conn.commit()` — changes ko permanently save karta hai (isko bhoolna common mistake hai!)
- `cursor.fetchall()` — saare results ek list mein deta hai
- `?` placeholders use karo direct string formatting ki bajaye — ye **SQL injection** se bachata hai

```python
# ORM example (SQLAlchemy style, jaise Django/FastAPI mein use hota hai)
from sqlalchemy.orm import Session

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
```

---

## 18. One-Page Quick Revision Cheat Sheet

```
STRINGS          strip() lstrip() rstrip() split() join() replace()
                 find() index() startswith() endswith() lower() upper()
                 title() capitalize() count() f"{var}"

LISTS            append() extend() insert() remove() pop() clear()
                 copy() reverse() sort() index() count() list[a:b]
                 [x for x in items]  <- comprehension

DICTS            get() keys() values() items() update() pop()
                 popitem() setdefault() clear() copy()

SETS             add() remove() discard() union() intersection()
                 difference()  |  &  -

TUPLES           count() index()   <- immutable, cannot change

BUILT-INS        len() type() isinstance() print() input() range()
                 enumerate() zip() map() filter() sorted() sum()
                 min() max() any() all() abs() round() open()

LOOPS/COND       for while break continue pass if elif else

FUNCTIONS        def return *args **kwargs lambda

CLASSES          class __init__ self super() inheritance

ERRORS           try except finally raise

FILES            with open() read() readline() readlines()
                 write() writelines()

MODULES          import  from x import y  import x as y

ASYNC            async def ... await ...

OPERATORS        in  not in  is  is not

JSON             json.dumps() json.loads() json.dump() json.load()

APIs             requests.get() requests.post() .json() .status_code
```

**Golden Rules to Remember:**
1. `sort()` changes original list, `sorted()` makes a new one
2. `copy()` list/dict, mat direct `=` use karo agar independent copy chahiye
3. `dict.get()` safe hai, `dict["key"]` risky hai
4. `is` identity check, `==` value check
5. `async def` ke andar `await` zaroori hai actual result ke liye
6. File open karne ke liye hamesha `with open()` use karo

---

## 19. Top 50 Most-Used Python Functions in Real Projects

| # | Function | # | Function |
|---|---|---|---|
| 1 | `print()` | 26 | `map()` |
| 2 | `len()` | 27 | `filter()` |
| 3 | `range()` | 28 | `sorted()` |
| 4 | `type()` | 29 | `zip()` |
| 5 | `isinstance()` | 30 | `open()` |
| 6 | `int()` | 31 | `input()` |
| 7 | `str()` | 32 | `float()` |
| 8 | `list()` | 33 | `dict()` |
| 9 | `set()` | 34 | `tuple()` |
| 10 | `sum()` | 35 | `min()` |
| 11 | `max()` | 36 | `abs()` |
| 12 | `round()` | 37 | `any()` |
| 13 | `all()` | 38 | `enumerate()` |
| 14 | `id()` | 39 | `dir()` |
| 15 | `help()` | 40 | `vars()` |
| 16 | `repr()` | 41 | `bool()` |
| 17 | `super()` | 42 | `isinstance()` |
| 18 | `requests.get()` | 43 | `requests.post()` |
| 19 | `json.dumps()` | 44 | `json.loads()` |
| 20 | `os.path.join()` | 45 | `os.path.exists()` |
| 21 | `datetime.now()` | 46 | `time.sleep()` |
| 22 | `asyncio.run()` | 47 | `re.match()` |
| 23 | `re.search()` | 48 | `logging.info()` |
| 24 | `Path()` (pathlib) | 49 | `argparse.ArgumentParser()` |
| 25 | `functools.reduce()` | 50 | `itertools.chain()` |

---

## 20. Top 50 Most-Used String/List/Dictionary Methods

| # | Method | Type |
|---|---|---|
| 1 | `.strip()` | String |
| 2 | `.split()` | String |
| 3 | `.join()` | String |
| 4 | `.replace()` | String |
| 5 | `.lower()` | String |
| 6 | `.upper()` | String |
| 7 | `.format()` | String |
| 8 | `.startswith()` | String |
| 9 | `.endswith()` | String |
| 10 | `.find()` | String |
| 11 | `.count()` | String/List |
| 12 | `.title()` | String |
| 13 | `.capitalize()` | String |
| 14 | `.index()` | String/List/Tuple |
| 15 | `.encode()` | String |
| 16 | `.append()` | List |
| 17 | `.extend()` | List |
| 18 | `.insert()` | List |
| 19 | `.remove()` | List |
| 20 | `.pop()` | List/Dict |
| 21 | `.sort()` | List |
| 22 | `.reverse()` | List |
| 23 | `.copy()` | List/Dict |
| 24 | `.clear()` | List/Dict |
| 25 | `.get()` | Dict |
| 26 | `.keys()` | Dict |
| 27 | `.values()` | Dict |
| 28 | `.items()` | Dict |
| 29 | `.update()` | Dict |
| 30 | `.setdefault()` | Dict |
| 31 | `.popitem()` | Dict |
| 32 | `.add()` | Set |
| 33 | `.discard()` | Set |
| 34 | `.union()` | Set |
| 35 | `.intersection()` | Set |
| 36 | `.difference()` | Set |
| 37 | `.lstrip()` | String |
| 38 | `.rstrip()` | String |
| 39 | `.swapcase()` | String |
| 40 | `.casefold()` | String |
| 41 | `.zfill()` | String |
| 42 | `.isdigit()` | String |
| 43 | `.isalpha()` | String |
| 44 | `.isspace()` | String |
| 45 | `.splitlines()` | String |
| 46 | `.partition()` | String |
| 47 | `.center()` | String |
| 48 | `.ljust()` / `.rjust()` | String |
| 49 | `.fromkeys()` | Dict |
| 50 | `.union()` (frozenset) | Set |

---

## 21. Interview Tips for Each Important Function

| Function/Concept | Interview Tip |
|---|---|
| `sort()` vs `sorted()` | Hamesha bolo: "sort() in-place hai aur None return karta hai, sorted() naya list return karta hai" |
| `is` vs `==` | Bolo: "is identity check karta hai (memory address), == value check karta hai" |
| Mutable vs Immutable | List/Dict/Set = mutable, String/Tuple/Int = immutable — example ke saath explain karo |
| `*args` vs `**kwargs` | args = positional (tuple), kwargs = keyword (dict) — dono ka use case bolna zaroori hai |
| `append()` vs `extend()` | append ek item add karta hai (even if list), extend elements merge karta hai |
| `deep copy` vs `shallow copy` | shallow copy sirf top-level copy karta hai, nested objects same reference rehte hain — `copy.deepcopy()` bolna important hai |
| Exception Handling | Specific exceptions catch karna best practice hai, generic `except:` avoid karo — bolo "fail fast, fail clear" |
| `lambda` | Bolo: "single expression ke liye hai, complex logic ke liye normal function better hai" |
| List Comprehension | Bolo: "readability aur performance dono behtar hoti hai simple loops ke comparison mein" |
| GIL (Global Interpreter Lock) | Agar multi-threading pucha jaye, bolo "Python GIL ki wajah se true parallel threading CPU-bound tasks mein nahi hoti, isliye multiprocessing use karte hain" |
| `async`/`await` | Bolo: "I/O-bound tasks (API calls, DB queries) ke liye best hai, CPU-bound ke liye nahi" |
| `self` keyword | Bolo: "current instance ko refer karta hai, Python explicitly pass karta hai jabke doosri languages mein implicit hota hai" |
| `__init__` vs `__new__` | Advanced question — bolo "`__new__` object create karta hai, `__init__` usko initialize karta hai" |
| Generators (`yield`) | Bolo: "memory-efficient hain kyunki poori list memory mein nahi rakhte, ek time par ek value generate karte hain" |

---

## 22. Memory Tricks (Yaad Rakhne Ke Tarike)

| Confusing Pair | Trick |
|---|---|
| `append()` vs `extend()` | **A**ppend = **A**dd one thing. **E**xtend = **E**xpand with many things |
| `remove()` vs `pop()` | remove() = value se dhoondo (**r**emove by value). pop() = position se nikalo (**p**op by **p**osition) |
| `find()` vs `index()` | find() **f**riendly hai (error nahi deta, -1 deta hai). index() **i**mpatient hai (error de deta hai) |
| `sort()` vs `sorted()` | sort() **s**ame list ko badalta hai. sorted() **s**eparate naya banata hai |
| `is` vs `==` | is = "**i**dentical object hai kya?" == = "value **s**ame hai kya?" |
| `get()` vs `[]` | get() = "**g**entle" (safe, default deta hai). `[]` = "**b**rutal" (error de sakta hai) |
| `str.lower()` vs `casefold()` | casefold() = lower() ka **"case"** wala **"full"** version — extra aggressive |
| `json.dumps` vs `json.dump` | Extra **"s"** = **s**tring ke liye. Bina "s" = file ke liye |
| Mutable vs Immutable | **L**ist, **D**ict, **S**et = changeable (LDS = "**L**arge **D**ynamic **S**tuff"). String, Tuple, Int = fixed |
| `args` vs `kwargs` | args = **a**nonymous values (tuple, no name). kwargs = **k**eyword values (dict, has name) |

---

## 23. Beginner Mistakes and How to Avoid Them

| Mistake | Sahi Tareeqa |
|---|---|
| `list2 = list1` (copy samajh kar) | `list2 = list1.copy()` use karo warna dono same object honge |
| Mutable default argument: `def f(x=[]):` | `def f(x=None): if x is None: x = []` use karo |
| Bare `except:` | Specific exception catch karo: `except ValueError:` |
| `==` ki jagah `is` use karna values compare karne ke liye | `==` values ke liye, `is` sirf `None`/identity ke liye |
| File `close()` karna bhool jaana | Hamesha `with open()` use karo |
| `input()` ka result number samajh lena | `int(input())` ya `float(input())` explicitly convert karo |
| Infinite loop (`while` mein counter update na karna) | Loop ke andar counter/condition update karna na bhoolo |
| Indentation errors | Consistent 4-space indentation use karo, tabs aur spaces mix mat karo |
| Global variables ka overuse | Functions ko parameters aur return values ke through data pass karao |
| `print()` aur `return` confuse karna | `print()` sirf dikhata hai, `return` value deta hai use karne ke liye |
| SQL query mein string formatting (`f"SELECT * WHERE name={name}"`) | Parameterized queries use karo (`?` placeholders) — SQL injection se bachne ke liye |
| Dictionary/list ko loop mein modify karna | Copy par loop karo ya naya list/dict banao, original ko iterate karte hue modify mat karo |
| Circular imports | Modules ko properly structure karo, imports ko function ke andar move karo agar zaroori ho |
| `.format()` aur f-strings mix karna inconsistently | Ek hi project mein consistent style use karo — modern projects mein f-strings preferred hain |

---

## 24. Bonus: Extra Topics You Should Also Know

Ye kuch aur cheezein hain jo real projects mein bohot common hain aur beginners ko pata honi chahiye:

### Generators aur `yield`

```python
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

for num in count_up_to(5):
    print(num)  # 1 2 3 4 5
```
Generators memory-efficient hote hain — poori list ek sath memory mein nahi rakhte.

### Context Managers (`with`)

`with open()` sirf files ke liye nahi — database connections, locks, aur custom resources ke liye bhi use hota hai.

### `datetime` module

```python
from datetime import datetime

now = datetime.now()
print(now.strftime("%Y-%m-%d"))  # e.g. 2026-07-30
```

### `pathlib` (modern file paths)

```python
from pathlib import Path

p = Path("data") / "file.txt"
print(p.exists())
```

### Decorators

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function runs")
        result = func(*args, **kwargs)
        print("After function runs")
        return result
    return wrapper

@my_decorator
def greet():
    print("Hello!")

greet()
```
FastAPI/Flask ke `@app.get()` jaise routes decorators hi hote hain!

### Type Hints

```python
def add(a: int, b: int) -> int:
    return a + b
```
Type hints code ko readable banate hain aur IDE errors catch karne mein madad karti hain (khaas kar FastAPI/Pydantic mein zaroori hain).

### Virtual Environments

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install package_name
```
Har project ke liye alag dependencies rakhne ke liye zaroori hai.

### Environment Variables (`.env`)

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
```
Secrets (API keys, passwords) ko code mein hardcode karne ki bajaye `.env` file mein rakhna best practice hai.

---

## 🎯 Final Note

Ye notes ek reference guide hain — inhe ek baar mein poora yaad karne ki koshish mat karo. Jab bhi kisi project mein koi function/method dikhe jo samajh na aaye, wapas is file mein aakar dhoondo. Practice se hi ye sab dimaag mein permanently set ho jayega.

**Best way to learn:** Har concept ko chhote se project mein use karke dekho — jaise ek to-do list app, ek simple API, ya ek file organizer script. Real practice se hi confidence aata hai! 🚀
