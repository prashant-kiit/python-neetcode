An **iterable** in Python is **any object that can be looped over** (iterated one element at a time).

An object is iterable if it implements either:

* `__iter__()` (preferred), or
* `__getitem__()` with integer indexes starting from `0` (legacy support).

### Common iterables

```python
# List
nums = [1, 2, 3]

# Tuple
t = (1, 2, 3)

# String
s = "hello"

# Dictionary (iterates over keys)
d = {"a": 1, "b": 2}

# Set
st = {1, 2, 3}

# Range
r = range(5)

# Generator
g = (x * x for x in range(3))
```

All of these can be used in a `for` loop:

```python
for x in nums:
    print(x)
```

---

## How an iterable works

When you write:

```python
for x in nums:
    print(x)
```

Python internally does something similar to:

```python
it = iter(nums)   # Get an iterator

while True:
    try:
        x = next(it)
        print(x)
    except StopIteration:
        break
```

* `iter()` converts an **iterable** into an **iterator**.
* `next()` retrieves one item at a time.

---

## Checking if something is iterable

```python
from collections.abc import Iterable

print(isinstance([1, 2], Iterable))     # True
print(isinstance("abc", Iterable))      # True
print(isinstance(10, Iterable))         # False
```

Or:

```python
iter([1, 2])      # Works
iter(10)          # TypeError
```

---

## Creating your own iterable

```python
class CountToThree:
    def __iter__(self):
        return iter([1, 2, 3])

obj = CountToThree()

for x in obj:
    print(x)
```

Output:

```
1
2
3
```

---

## Iterable vs Iterator

| Feature                | Iterable    | Iterator            |
| ---------------------- | ----------- | ------------------- |
| Can be looped over     | ✅           | ✅                   |
| Has `__iter__()`       | ✅           | ✅                   |
| Has `__next__()`       | ❌           | ✅                   |
| Stores iteration state | ❌           | ✅                   |
| Can restart iteration  | Usually yes | No (once exhausted) |

Example:

```python
nums = [1, 2, 3]       # Iterable

it = iter(nums)        # Iterator

print(next(it))        # 1
print(next(it))        # 2
print(next(it))        # 3
```

---

### Key takeaway

* **Iterable** = Something you can iterate over (e.g., list, tuple, string, set, dict, range, generator).
* **Iterator** = The object that actually produces the next item using `next()`.
* `iter(iterable)` → returns an **iterator**.
* `next(iterator)` → returns the next element until it raises `StopIteration`.
