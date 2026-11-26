# Python Concepts for AI Engineering — Complete Recap Guide

> Yeh file un tamam Python concepts ka collection hai jo AI/ML engineering mein commonly use hotay hain. Har concept ke sath short explanation + code example diya gaya hai taake sirf ek nazar mein sab yaad aa jaye.

---

## Table of Contents

1. [Basic Data Types](#1-basic-data-types)
2. [Strings & String Methods](#2-strings--string-methods)
3. [Lists](#3-lists)
4. [Tuples](#4-tuples)
5. [Sets](#5-sets)
6. [Dictionaries](#6-dictionaries)
7. [Loops](#7-loops)
8. [Comprehensions](#8-comprehensions)
9. [Conditional Statements](#9-conditional-statements)
10. [Functions](#10-functions)
11. [Lambda, Map, Filter, Reduce](#11-lambda-map-filter-reduce)
12. [File Handling](#12-file-handling)
13. [Exception Handling](#13-exception-handling)
14. [OOP (Object Oriented Programming)](#14-oop-object-oriented-programming)
15. [Iterators & Generators](#15-iterators--generators)
16. [Decorators](#16-decorators)
17. [Context Managers (with statement)](#17-context-managers-with-statement)
18. [Hashing & Hashable Objects](#18-hashing--hashable-objects)
19. [Copy vs Deepcopy](#19-copy-vs-deepcopy)
20. [Modules & Packages](#20-modules--packages)
21. [Regular Expressions (regex)](#21-regular-expressions-regex)
22. [JSON Handling](#22-json-handling)
23. [Working with Dates & Time](#23-working-with-dates--time)
24. [Type Hinting](#24-type-hinting)
25. [Enumerate & Zip](#25-enumerate--zip)
26. [args and kwargs](#26-args-and-kwargs)
27. [Multithreading & Multiprocessing](#27-multithreading--multiprocessing)
28. [Virtual Environments & pip](#28-virtual-environments--pip)
29. [NumPy Essentials (AI ke liye zaroori)](#29-numpy-essentials-ai-ke-liye-zaroori)
30. [Pandas Essentials (AI ke liye zaroori)](#30-pandas-essentials-ai-ke-liye-zaroori)
31. [Useful Built-in Functions](#31-useful-built-in-functions)
32. [Best Practices for AI Engineering Code](#32-best-practices-for-ai-engineering-code)

---

## 1. Basic Data Types

Python mein har value ka ek type hota hai. Types automatically assign hotay hain (dynamic typing).

```python
x = 10          # int
y = 3.14        # float
name = "Ali"    # str
is_valid = True # bool
n = None        # NoneType
```

- **int** → whole numbers
- **float** → decimal numbers
- **str** → text
- **bool** → True/False
- **complex** → complex numbers (rare in AI code, used in signal processing)

```python
print(type(x))       # <class 'int'>
print(isinstance(x, int))  # True
```

---

## 2. Strings & String Methods

Strings AI engineering mein bohat use hoti hain — text preprocessing, prompts, logs waghera ke liye.

```python
s = "Hello World"

s.lower()          # 'hello world'
s.upper()          # 'HELLO WORLD'
s.strip()          # remove leading/trailing whitespace
s.split(" ")       # ['Hello', 'World']
"-".join(["a","b"])# 'a-b'
s.replace("World", "AI")
s.startswith("Hello")
s.endswith("World")
len(s)             # 11
s[0:5]             # slicing -> 'Hello'
f"Value is {x}"    # f-strings (formatting)
```

### f-strings (bohat important)
```python
name = "Sara"
age = 21
print(f"{name} is {age} years old")
```

---

## 3. Lists

List ek **ordered, mutable** collection hoti hai. Duplicate values allowed hain.

```python
nums = [1, 2, 3, 4, 5]

nums.append(6)         # add at end
nums.insert(0, 0)      # insert at index
nums.remove(3)         # remove by value
nums.pop()             # remove last
nums.pop(0)            # remove by index
nums.sort()            # sort ascending
nums.sort(reverse=True)
nums.reverse()
len(nums)
nums[1:3]              # slicing
nums.count(2)
nums.index(4)
nums.extend([7,8])
```

### List of lists (matrix-like — AI mein common)
```python
matrix = [[1,2,3],[4,5,6],[7,8,9]]
print(matrix[1][2])   # 6
```

---

## 4. Tuples

Tuple bhi ordered hoti hai lekin **immutable** (change nahi ho sakti). AI mein shapes, coordinates, ya fixed data ke liye use hoti hai.

```python
t = (1, 2, 3)
x, y, z = t          # unpacking
t2 = t + (4, 5)      # concatenation
t.count(1)
t.index(2)
```

- Tuple **memory-efficient** aur **fast** hoti hai lists ke muqable.
- Function se multiple values return karne ke liye use hoti hai:
```python
def get_min_max(nums):
    return min(nums), max(nums)

low, high = get_min_max([3,1,4,1,5])
```

---

## 5. Sets

Set ek **unordered**, **unique values** wali collection hai. Duplicates automatically remove ho jate hain.

```python
s1 = {1, 2, 3}
s2 = {3, 4, 5}

s1.add(6)
s1.remove(2)
s1.union(s2)          # {1,3,4,5,6}
s1.intersection(s2)   # common elements
s1.difference(s2)     # only in s1
s1.issubset(s2)
s1.issuperset(s2)
```

**AI use-case:** duplicate tokens/words remove karna, unique labels/classes nikalna, fast membership check (`in` operator O(1) hota hai set mein, list mein O(n)).

```python
unique_words = set(text.split())
```

---

## 6. Dictionaries

Dictionary **key-value pairs** store karti hai. AI mein config, JSON data, model parameters, mappings ke liye bohat use hoti hai.

```python
person = {"name": "Ali", "age": 22, "city": "Lahore"}

person["age"]              # access
person["email"] = "a@b.com" # add new key
person.get("age")          # safe access
person.get("salary", 0)    # default value if missing
person.pop("city")
person.keys()
person.values()
person.items()

for key, value in person.items():
    print(key, value)
```

### Nested Dictionary (AI configs mein common)
```python
model_config = {
    "layers": 3,
    "params": {"lr": 0.001, "batch_size": 32}
}
print(model_config["params"]["lr"])
```

### defaultdict & Counter (collections module)
```python
from collections import defaultdict, Counter

d = defaultdict(int)
d["a"] += 1        # no KeyError even if key doesn't exist

word_counts = Counter(["a","b","a","c","b","a"])
print(word_counts)   # Counter({'a': 3, 'b': 2, 'c': 1})
```

---

## 7. Loops

### for loop
```python
for i in range(5):
    print(i)

for item in ["a","b","c"]:
    print(item)
```

### while loop
```python
i = 0
while i < 5:
    print(i)
    i += 1
```

### break, continue, pass
```python
for i in range(10):
    if i == 5:
        break       # loop rok do
    if i % 2 == 0:
        continue    # is iteration ko skip karo
    pass            # kuch nahi karna (placeholder)
```

### Nested loops
```python
for i in range(3):
    for j in range(3):
        print(i, j)
```

---

## 8. Comprehensions

Comprehensions ek line mein loop + condition likhne ka tareeqa hain — AI code mein bohat clean aur fast hote hain.

### List Comprehension
```python
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
```

### Dict Comprehension
```python
squares_dict = {x: x**2 for x in range(5)}
```

### Set Comprehension
```python
unique_lengths = {len(word) for word in ["ai","ml","dl","ai"]}
```

### Generator Expression (memory efficient)
```python
gen = (x**2 for x in range(1000000))  # lazy evaluation
```

### Nested Comprehension
```python
matrix = [[1,2],[3,4]]
flat = [num for row in matrix for num in row]  # [1,2,3,4]
```

---

## 9. Conditional Statements

```python
x = 10

if x > 5:
    print("Greater")
elif x == 5:
    print("Equal")
else:
    print("Smaller")

# Ternary (one-line if-else)
result = "Yes" if x > 5 else "No"
```

---

## 10. Functions

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Ali")
greet("Ali", "Hi")
greet(name="Ali", greeting="Salam")
```

### Return multiple values
```python
def stats(nums):
    return min(nums), max(nums), sum(nums)/len(nums)
```

### Default & Keyword arguments
```python
def train_model(epochs=10, lr=0.001, verbose=False):
    pass
```

### Type hints in functions
```python
def add(a: int, b: int) -> int:
    return a + b
```

---

## 11. Lambda, Map, Filter, Reduce

```python
square = lambda x: x**2
square(5)  # 25

nums = [1,2,3,4,5]

# map -> har element pe function apply karo
squared = list(map(lambda x: x**2, nums))

# filter -> condition ke mutabiq values chuno
evens = list(filter(lambda x: x % 2 == 0, nums))

# reduce -> saari values ko combine kar ke ek result do
from functools import reduce
total = reduce(lambda a, b: a + b, nums)
```

**AI use-case:** data preprocessing pipelines, quick transformations on datasets.

---

## 12. File Handling

```python
# Reading a file
with open("data.txt", "r") as f:
    content = f.read()

# Reading line by line
with open("data.txt", "r") as f:
    for line in f:
        print(line.strip())

# Writing to a file
with open("output.txt", "w") as f:
    f.write("Hello AI\n")

# Appending
with open("output.txt", "a") as f:
    f.write("New line\n")
```

- `with` statement automatically file ko close kar deta hai (context manager).
- Modes: `"r"` read, `"w"` write (overwrite), `"a"` append, `"rb"/"wb"` binary.

### Reading CSV files
```python
import csv

with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
```

---

## 13. Exception Handling

AI pipelines mein errors handle karna zaroori hai (missing files, bad data, API errors waghera).

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print("Error:", e)
except Exception as e:
    print("Something went wrong:", e)
else:
    print("No error occurred")
finally:
    print("This always runs")
```

### Custom Exceptions
```python
class InvalidDataError(Exception):
    pass

def check_data(x):
    if x < 0:
        raise InvalidDataError("Data cannot be negative")
```

---

## 14. OOP (Object Oriented Programming)

AI mein models, layers, datasets sab classes ki shakal mein hote hain (PyTorch, sklearn waghera isi tarah kaam karte hain).

```python
class Model:
    def __init__(self, name, lr=0.01):
        self.name = name
        self.lr = lr

    def train(self):
        print(f"Training {self.name} with lr={self.lr}")

m = Model("NeuralNet")
m.train()
```

### Inheritance
```python
class BaseModel:
    def predict(self):
        print("Predicting...")

class CNNModel(BaseModel):
    def predict(self):
        print("CNN Predicting...")
        super().predict()
```

### Key OOP Concepts
- **Encapsulation** → data ko class ke andar band rakhna
- **Inheritance** → parent class se properties lena
- **Polymorphism** → same method, different behavior
- **Abstraction** → sirf zaroori cheezein expose karna

```python
from abc import ABC, abstractmethod

class Layer(ABC):
    @abstractmethod
    def forward(self):
        pass
```

---

## 15. Iterators & Generators

### Iterator
```python
nums = [1,2,3]
it = iter(nums)
print(next(it))  # 1
print(next(it))  # 2
```

### Generator (memory efficient — bade datasets ke liye zaroori)
```python
def data_loader(data):
    for item in data:
        yield item * 2

for value in data_loader([1,2,3]):
    print(value)
```

**AI use-case:** bade datasets ko batch-by-batch load karna bina pura data RAM mein rakhe.

---

## 16. Decorators

Function ko modify karne ka tareeqa bina uska code change kiye. AI mein timing, logging, caching ke liye use hote hain.

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Time taken: {time.time()-start}s")
        return result
    return wrapper

@timer
def train():
    time.sleep(2)

train()
```

### Caching decorator (model inference speed up)
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def expensive_computation(n):
    return n ** 2
```

---

## 17. Context Managers (with statement)

Resources (files, DB connections, GPU sessions) ko safely open/close karne ke liye.

```python
class ManagedResource:
    def __enter__(self):
        print("Resource opened")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Resource closed")

with ManagedResource() as r:
    print("Using resource")
```

---

## 18. Hashing & Hashable Objects

Hashing ka use dictionaries/sets ke fast lookup ke peeche hota hai, aur AI mein caching, data deduplication, embeddings indexing ke liye important hai.

```python
print(hash("hello"))     # integer hash value
print(hash(42))
print(hash((1,2,3)))     # tuples hashable hain
```

- **Hashable** → int, float, str, tuple, frozenset (immutable objects)
- **Not hashable** → list, dict, set (mutable objects)

```python
# Isliye set/dict ki keys hamesha immutable honi chahiye
d = {(1,2): "point"}   # valid — tuple hashable hai
# d = {[1,2]: "point"} # invalid — list not hashable
```

### hashlib (cryptographic hashing — data integrity/checksums ke liye)
```python
import hashlib

text = "hello world"
hash_value = hashlib.sha256(text.encode()).hexdigest()
print(hash_value)
```

**AI use-case:** dataset versioning, checking duplicate records, model checkpoint verification.

---

## 19. Copy vs Deepcopy

```python
import copy

original = {"a": [1,2,3]}

shallow = copy.copy(original)      # nested objects shared rehte hain
deep = copy.deepcopy(original)     # pura naya independent copy
```

- **Shallow copy** → sirf top-level copy hota hai, nested objects same reference share karte hain.
- **Deep copy** → har cheez independently copy hoti hai.

**AI use-case:** model weights ya config dictionaries copy karte waqt accidental overwrite se bachne ke liye.

---

## 20. Modules & Packages

```python
import math
from math import sqrt
import numpy as np
from sklearn.model_selection import train_test_split

print(math.pi)
print(sqrt(16))
```

### Apna module banana
```python
# utils.py
def clean_text(text):
    return text.lower().strip()

# main.py
from utils import clean_text
```

---

## 21. Regular Expressions (regex)

Text preprocessing / NLP mein bohat use hota hai.

```python
import re

text = "My email is ali@example.com"

re.findall(r"\S+@\S+", text)             # find emails
re.sub(r"[^a-zA-Z\s]", "", text)         # remove special chars/numbers
re.match(r"^My", text)                    # match from start
re.search(r"email", text)                 # search anywhere
re.split(r"\s+", text)                    # split by whitespace
```

---

## 22. JSON Handling

APIs aur model configs mostly JSON format mein hote hain.

```python
import json

data = {"name": "Ali", "score": 95.5}

json_string = json.dumps(data)          # dict -> JSON string
parsed = json.loads(json_string)        # JSON string -> dict

# File se
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

with open("data.json", "r") as f:
    loaded = json.load(f)
```

---

## 23. Working with Dates & Time

```python
from datetime import datetime, timedelta

now = datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")

future = now + timedelta(days=7)
```

**AI use-case:** logging timestamps, experiment tracking, time-series data.

---

## 24. Type Hinting

Code ko readable aur bugs se pak rakhne ke liye.

```python
from typing import List, Dict, Tuple, Optional, Union

def process(data: List[int]) -> Dict[str, int]:
    return {"sum": sum(data)}

def find_user(id: int) -> Optional[str]:
    return None

def combine(a: Union[int, float], b: Union[int, float]) -> float:
    return a + b
```

---

## 25. Enumerate & Zip

```python
names = ["Ali", "Sara", "Ahmed"]

# enumerate -> index + value
for i, name in enumerate(names):
    print(i, name)

# zip -> multiple lists ko parallel combine karna
ages = [20, 22, 25]
for name, age in zip(names, ages):
    print(name, age)
```

**AI use-case:** batch processing mein features aur labels ko saath saath iterate karna.

---

## 26. args and kwargs

Jab function ko flexible number of arguments chahiye hon (jaise model layers, hyperparameters).

```python
def my_func(*args, **kwargs):
    print(args)     # tuple of positional args
    print(kwargs)   # dict of keyword args

my_func(1, 2, 3, lr=0.01, epochs=10)
```

---

## 27. Multithreading & Multiprocessing

Bade datasets ya parallel tasks (data loading, API calls) ke liye.

```python
import threading
import multiprocessing

def worker():
    print("Working...")

# Threading -> I/O bound tasks (API calls, file reading)
t = threading.Thread(target=worker)
t.start()
t.join()

# Multiprocessing -> CPU bound tasks (heavy computation)
p = multiprocessing.Process(target=worker)
p.start()
p.join()
```

---

## 28. Virtual Environments & pip

```bash
python -m venv myenv          # environment banana
source myenv/bin/activate     # activate (Linux/Mac)
myenv\Scripts\activate        # activate (Windows)

pip install numpy pandas torch
pip freeze > requirements.txt
pip install -r requirements.txt
```

---

## 29. NumPy Essentials (AI ke liye zaroori)

```python
import numpy as np

arr = np.array([1,2,3,4,5])
matrix = np.array([[1,2],[3,4]])

arr.shape
arr.reshape(5,1)
np.zeros((3,3))
np.ones((2,2))
np.arange(0,10,2)
np.linspace(0,1,5)

arr.mean()
arr.sum()
arr.max()
arr.min()
arr.std()

# Element-wise operations
arr * 2
arr + arr

# Matrix multiplication
np.dot(matrix, matrix)

# Broadcasting
matrix + np.array([1,0])
```

---

## 30. Pandas Essentials (AI ke liye zaroori)

```python
import pandas as pd

df = pd.read_csv("data.csv")

df.head()
df.info()
df.describe()
df.shape
df.columns

df["column_name"]
df[["col1","col2"]]
df.loc[0]              # row by label
df.iloc[0]             # row by index

df.dropna()
df.fillna(0)
df.groupby("category").mean()
df.sort_values("column_name")
df["new_col"] = df["col1"] + df["col2"]

df.to_csv("output.csv", index=False)
```

---

## 31. Useful Built-in Functions

```python
len([1,2,3])
sum([1,2,3])
max([1,2,3])
min([1,2,3])
sorted([3,1,2])
reversed([1,2,3])
abs(-5)
round(3.14159, 2)
any([True, False])
all([True, True])
type(x)
isinstance(x, int)
id(x)
range(10)
input("Enter value: ")
str(123)
int("123")
float("3.14")
list("abc")
```

---

## 32. Best Practices for AI Engineering Code

- Hamesha **type hints** use karein — readability behtar hoti hai.
- Data preprocessing ke liye **list/dict comprehensions** use karein, loops se fast hote hain.
- Bade datasets ke liye **generators** use karein taake memory bachay.
- File aur resource handling ke liye hamesha **`with` statement** use karein.
- Errors ko **specific except blocks** se handle karein, generic `except:` se bachein.
- Config/hyperparameters ke liye **dictionaries** use karein, hard-coded values se bachein.
- Repeated computations ke liye **caching (`lru_cache`)** use karein.
- Code ko **functions/classes** mein modular rakhein — reusability ke liye.
- **Virtual environments** har project ke liye alag rakhein.
- **Logging** use karein `print()` ki jagah production code mein.

---

### 📌 Quick Reference: Which Structure to Use When?

| Need | Use |
|---|---|
| Ordered, duplicate values allowed, changeable | **List** |
| Ordered, fixed/unchangeable data | **Tuple** |
| Unique values, fast membership check | **Set** |
| Key-value mapping | **Dictionary** |
| Large data, memory efficient iteration | **Generator** |
| Fast lookup by unique key | **Hashing (dict/set)** |

---

*Yeh guide AI engineering interviews, projects, aur daily coding recap ke liye ek complete cheat-sheet hai. Jab bhi Python concepts bhool jayen, isi file ko dekh kar fori revise kar sakte hain.*
