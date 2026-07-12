# `finalize` in Python

There isn't a keyword called `finalize` in core Python OOP (unlike Java's `finalize()`). In Python, "finalization" refers to **cleanup logic that runs when an object is about to be destroyed** — and there are two main tools: `__del__` and `weakref.finalize`.

## 1. `__del__` — the destructor method

Called when an object is about to be garbage collected.

```python
class FileHandler:
    def __init__(self, filename):
        self.file = open(filename, "w")
        print("File opened")

    def __del__(self):
        self.file.close()
        print("File closed")

f = FileHandler("test.txt")
del f    # File closed
```

**Why it's used:** to release resources (files, network connections, locks) when an object is no longer needed — a safety net for cleanup.

### Problem: `__del__` is unreliable

```python
class Demo:
    def __del__(self):
        print("Cleaning up...")

d = Demo()
# if the program crashes, or there's a reference cycle,
# __del__ may never run — timing is NOT guaranteed
```

Issues:
- Exact timing depends on garbage collector — not deterministic like C++ destructors
- Reference cycles can delay or prevent it
- Exceptions inside `__del__` are mostly ignored/suppressed
- Never called if the program exits abruptly

This is why `__del__` is generally **discouraged** for critical cleanup.

## 2. `weakref.finalize` — the modern, reliable alternative

```python
import weakref

class FileHandler:
    def __init__(self, filename):
        self.file = open(filename, "w")
        # register cleanup — doesn't rely on __del__
        self._finalizer = weakref.finalize(self, self.file.close)

f = FileHandler("test.txt")
del f    # file.close() runs automatically
```

`weakref.finalize` is preferred because it:
- Runs cleanup exactly once, reliably
- Doesn't interfere with garbage collection like `__del__` can
- Can be manually triggered or checked (`f.alive`)

```python
import weakref

class Resource:
    def __init__(self, name):
        self.name = name

def cleanup(name):
    print(f"Cleaning up {name}")

r = Resource("db_connection")
finalizer = weakref.finalize(r, cleanup, r.name)

finalizer()          # Cleaning up db_connection — manual trigger
print(finalizer.alive)   # False — already ran, won't run twice
```

## The preferred approach: context managers instead of finalization

In practice, **most Python code avoids relying on `__del__`/`finalize` entirely** and uses `with` statements (`__enter__`/`__exit__`) for deterministic cleanup:

```python
class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, "w")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        print("File closed")

with FileHandler("test.txt") as f:
    f.write("Hello")
# File closed — happens immediately and predictably, no GC guesswork
```

This is why you'll rarely see `__del__` used in modern, well-written Python — context managers give **explicit, guaranteed** cleanup timing.

## Quick comparison

| Tool | Reliability | When it runs |
|---|---|---|
| `__del__` | ⚠️ Unreliable | Whenever GC decides (not guaranteed) |
| `weakref.finalize` | ✅ Reliable, runs once | On GC, but trackable/callable manually |
| Context manager (`with`) | ✅ Fully deterministic | Exactly when the `with` block exits |

## Quick summary

| Concept | Purpose |
|---|---|
| `__del__` | Destructor-like hook, cleanup before object is garbage collected |
| `weakref.finalize` | Safer, guaranteed-once cleanup registration |
| Context managers (`with`) | The recommended way to guarantee cleanup — deterministic, not GC-dependent |

**Bottom line:** "finalize" in Python is about resource cleanup — but unlike languages with deterministic destructors, Python favors **explicit** cleanup (context managers) over relying on garbage-collection timing.

If you meant something different by "finalize" (e.g., in a specific framework, or `Enum`'s `_ignore_`, or dataclasses' `__post_init__`), let me know and I can tailor the answer.