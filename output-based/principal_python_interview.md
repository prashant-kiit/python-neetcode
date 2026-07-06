# Principal AI/ML Engineer — Python Deep-Dive Interview
### Conducted by Dario Amodei (CTO & Co-founder, Anthropic)
**Format:** Output-prediction only. No theory questions. 50 questions, progressive difficulty (10% Medium / 30% Hard / 60% Extremely Hard).

---

Before we start — welcome. This interview is pure Python execution semantics. I'm not going to ask you about transformers or distributed training today. I want to know if you *actually* understand the language we build all of this on top of. Read each snippet carefully. Don't run it in your head like a compiler — think like the CPython interpreter. Take your time.

---

## Question 1
```python
x = 5
def outer():
    x = x + 1
    return x
print(outer())
```
**Candidate Task:** Predict the exact output.

**Answer:** Raises `UnboundLocalError: local variable 'x' referenced before assignment`.

**Explanation:** Because `x` is assigned anywhere inside `outer`, Python's compiler marks `x` as local to the entire function scope (LEGB — the L is determined at compile time, not runtime). The `x + 1` on the right-hand side tries to read the *local* `x` before it has been bound, even though a global `x` exists. This is a classic "compile-time scope determination" trap — the presence of `x = ...` anywhere in the function body shadows the outer `x` for the whole function.

**Difficulty:** Medium — **Success rate:** ~65%
**Topics Tested:** LEGB, local/global variable resolution, compile-time scoping

---

## Question 2
```python
def make_multipliers():
    return [lambda x: x * i for i in range(3)]

fns = make_multipliers()
print([f(10) for f in fns])
```
**Answer:** `[20, 20, 20]`

**Explanation:** Closures in Python capture variables **by reference**, not by value. All three lambdas share the same cell for `i`. By the time the list comprehension finishes, `i` is `2` (the last value from `range(3)`). This is "late binding" — the lambda body doesn't evaluate `i` until it's *called*, and by then the loop has finished. Common fix: default-arg capture `lambda x, i=i: x * i`.

**Difficulty:** Medium — **Success rate:** ~60%
**Topics Tested:** Closures, late binding, lambda, list comprehensions

---

## Question 3
```python
def f(a, b=[]):
    b.append(a)
    return b

print(f(1))
print(f(2))
print(f(3, []))
print(f(4))
```
**Answer:** `[1]`, `[1, 2]`, `[3]`, `[1, 2, 4]`

**Explanation:** Default arguments are evaluated **once**, at function-definition time, and the same list object is reused across calls unless explicitly overridden. Calls 1, 2, and 4 all mutate the same shared default list object bound to `b`. Call 3 passes a fresh list explicitly, bypassing the shared default entirely.

**Difficulty:** Medium — **Success rate:** ~70%
**Topics Tested:** Mutable default arguments, object identity, function definition semantics

---

## Question 4
```python
a = 256
b = 256
print(a is b)

c = 257
d = 257
print(c is d)
```
**Answer:** `True`, then implementation-dependent — typically `False` in a plain script but can be `True` in an interactive REPL due to peephole/constant folding differences.

**Explanation:** CPython pre-caches small integers in the range **-5 to 256** as singletons (the "small int cache"). `256` will always be `is`-identical. `257` falls outside that cache, so two separately-created `257` objects are normally distinct objects — *except* CPython's peephole optimizer may fold literal constants defined in the same code object, making REPL/script behavior diverge. This is a well-known CPython implementation detail, **not part of the language spec** — Jython/PyPy behave differently.

**Difficulty:** Hard — **Success rate:** ~45%
**Topics Tested:** Object identity vs equality, CPython small-int caching, `is` vs `==`, implementation-specific behavior

---

## Question 5
```python
class Meta(type):
    def __new__(mcs, name, bases, ns):
        print(f"Creating {name}")
        ns['created_by'] = mcs.__name__
        return super().__new__(mcs, name, bases, ns)

class Base(metaclass=Meta):
    pass

class Child(Base):
    pass

print(Child.created_by)
print(Base.created_by)
```
**Answer:**
```
Creating Base
Creating Child
Meta
Meta
```

**Explanation:** `Meta.__new__` runs once per class *definition* (not instantiation) — for `Base` and for `Child`, since `Child` inherits the metaclass from `Base` automatically. Both get `created_by = 'Meta'` injected into their own namespace at class-creation time. Print order follows definition order: `Base` first, `Child` second.

**Difficulty:** Hard — **Success rate:** ~40%
**Topics Tested:** Metaclasses, `__new__` vs `__init__`, class creation order, metaclass inheritance

---

## Question 6
```python
class A:
    def who(self):
        return "A"

class B(A):
    def who(self):
        return "B"

class C(A):
    def who(self):
        return "C"

class D(B, C):
    pass

print(D().who())
print([c.__name__ for c in D.__mro__])
```
**Answer:**
```
B
['D', 'B', 'C', 'A', 'object']
```

**Explanation:** `D` has no `who`, so Python resolves via `D.__mro__`, computed with the **C3 linearization** algorithm. C3 guarantees a monotonic, consistent ordering: `D` → `B` → `C` → `A` → `object`. `B` is checked before `C`, so `B.who()` wins — this is the classic diamond-inheritance resolution order.

**Difficulty:** Hard — **Success rate:** ~55%
**Topics Tested:** MRO, C3 linearization, multiple inheritance, diamond problem

---

## Question 7
```python
def gen():
    print("start")
    x = yield 1
    print("received", x)
    y = yield 2
    print("received", y)
    return "done"

g = gen()
print(next(g))
print(g.send("hello"))
try:
    g.send("world")
except StopIteration as e:
    print("StopIteration:", e.value)
```
**Answer:**
```
start
1
received hello
2
received world
StopIteration: done
```

**Explanation:** `next(g)` runs the generator to the first `yield 1`, printing `start` then yielding `1`. `g.send("hello")` resumes execution, binds `x = "hello"`, prints, runs to `yield 2`. The final `send("world")` binds `y`, prints, hits the `return "done"`, which raises `StopIteration` whose `.value` attribute carries the return value — this is exactly the mechanism `yield from` and coroutine chaining rely on.

**Difficulty:** Hard — **Success rate:** ~50%
**Topics Tested:** Generator execution model, `send()`, `StopIteration.value`, generator-based coroutines

---

## Question 8
```python
class Descriptor:
    def __init__(self, name):
        self.name = name
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, "default")
    def __set__(self, obj, value):
        print(f"setting {self.name} = {value}")
        obj.__dict__[self.name] = value

class Foo:
    x = Descriptor("x")

f = Foo()
print(f.x)
f.x = 10
print(f.x)
print(Foo.x)
```
**Answer:**
```
default
setting x = 10
10
<__main__.Descriptor object at 0x...>
```

**Explanation:** `Descriptor` implements `__get__` and `__set__`, making it a **data descriptor**, which takes priority over instance `__dict__`. `f.x` on an unset instance falls into the `.get(..., "default")` branch. Assignment invokes `__set__`, printing and storing into `f.__dict__`. Accessing on the class itself (`Foo.x`) passes `obj=None`, returning the descriptor instance itself, not a value — a subtle trap many candidates miss.

**Difficulty:** Very Hard — **Success rate:** ~35%
**Topics Tested:** Descriptor protocol, data vs non-data descriptors, attribute lookup order

---

## Question 9
```python
import functools

@functools.lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

print(fib(10))
print(fib.cache_info())
fib.cache_clear()
print(fib.cache_info())
```
**Answer:**
```
55
CacheInfo(hits=8, misses=11, maxsize=None, currsize=11)
CacheInfo(hits=0, misses=0, maxsize=None, currsize=0)
```

**Explanation:** `fib(10)` triggers 11 unique calls (`fib(0)`...`fib(10)`) — 11 misses — and 8 repeated lookups hit the cache due to overlapping subproblems in the naive recursive tree. `cache_clear()` resets all counters and evicts stored results.

**Difficulty:** Hard — **Success rate:** ~45%
**Topics Tested:** Decorators, memoization internals, `functools.lru_cache`, call-graph counting

---

## Question 10
```python
class Meta(type):
    def __call__(cls, *args, **kwargs):
        print("Meta.__call__")
        instance = super().__call__(*args, **kwargs)
        print("instance created")
        return instance

class Foo(metaclass=Meta):
    def __new__(cls):
        print("Foo.__new__")
        return super().__new__(cls)
    def __init__(self):
        print("Foo.__init__")

f = Foo()
```
**Answer:**
```
Meta.__call__
Foo.__new__
Foo.__init__
instance created
```

**Explanation:** `Foo()` actually invokes `type(Foo).__call__(Foo)`, i.e. `Meta.__call__`, **not** `Foo.__new__` directly. Inside `Meta.__call__`, `super().__call__()` (which is `type.__call__`) is what internally invokes `Foo.__new__` then `Foo.__init__`, in that order, before control returns to `Meta.__call__` to finish and print "instance created". This reveals the full object-instantiation pipeline that most engineers never trace through.

**Difficulty:** Very Hard — **Success rate:** ~30%
**Topics Tested:** Metaclasses, `__call__` vs `__new__` vs `__init__`, instantiation protocol

---

## Question 11
```python
class Node:
    __slots__ = ('value', 'next')
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

n = Node(1)
try:
    n.extra = 5
except AttributeError as e:
    print("Error:", e)

print(hasattr(n, '__dict__'))
```
**Answer:**
```
Error: 'Node' object has no attribute 'extra'
False
```

**Explanation:** `__slots__` suppresses the automatic creation of a per-instance `__dict__`, replacing attribute storage with fixed descriptor-backed slots for memory efficiency. Assigning an undeclared attribute raises `AttributeError` at assignment time, and `hasattr(n, '__dict__')` is `False` since no dict was ever allocated — a key production optimization for large object counts (e.g., token/node graphs).

**Difficulty:** Hard — **Success rate:** ~55%
**Topics Tested:** `__slots__`, memory optimization, attribute storage internals

---

## Question 12
```python
import asyncio

async def task(name, delay):
    print(f"{name} start")
    await asyncio.sleep(delay)
    print(f"{name} end")
    return name

async def main():
    results = await asyncio.gather(
        task("A", 0.2),
        task("B", 0.1),
        task("C", 0.3),
    )
    print(results)

asyncio.run(main())
```
**Answer:**
```
A start
B start
C start
B end
A end
C end
['A', 'B', 'C']
```

**Explanation:** `asyncio.gather` schedules all three coroutines onto the event loop essentially simultaneously — each runs up to its first `await` before yielding control, so all three "start" prints happen back-to-back in creation order. Then the event loop resumes whichever sleep timer expires first (`B` at 0.1s, `A` at 0.2s, `C` at 0.3s). Critically, `gather` preserves the **original input order** in its returned results list regardless of completion order.

**Difficulty:** Very Hard — **Success rate:** ~40%
**Topics Tested:** `async`/`await`, event loop scheduling, `asyncio.gather`, cooperative concurrency

---

## Question 13
```python
class Base:
    def __init_subclass__(cls, **kwargs):
        print(f"Subclassing {cls.__name__} with {kwargs}")
        super().__init_subclass__()

class Sub(Base, extra="hello"):
    pass
```
**Answer:**
```
Subclassing Sub with {'extra': 'hello'}
```

**Explanation:** `__init_subclass__` is an implicit classmethod hook invoked automatically whenever `Base` is subclassed, receiving keyword arguments passed in the class statement (`extra="hello"`) that are **not** part of the normal `bases` tuple — these are consumed by `__init_subclass__` and never seen by `__new__`/metaclass machinery unless explicitly forwarded. This is a lighter-weight alternative to metaclasses for subclass registration/validation, commonly used in plugin/registry systems.

**Difficulty:** Very Hard — **Success rate:** ~30%
**Topics Tested:** `__init_subclass__`, class creation hooks, keyword class arguments

---

## Question 14
```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(100000):
        counter += 1

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(counter)
```
**Answer:** Some value **less than or equal to 400000**, non-deterministic (e.g. `387452`), almost never exactly `400000`.

**Explanation:** Despite the GIL, `counter += 1` is **not atomic** — it compiles to a `LOAD_GLOBAL`, `BINARY_ADD`, `STORE_GLOBAL` sequence, and the GIL can switch threads between bytecode instructions (governed by the interpreter's switch interval). Multiple threads can read the same stale value before writing back, causing lost updates — a classic race condition that surprises engineers who assume "the GIL makes things thread-safe."

**Difficulty:** Very Hard — **Success rate:** ~40%
**Topics Tested:** GIL implications, thread safety, race conditions, bytecode-level atomicity

---

## Question 15
```python
def outer():
    x = 10
    def inner():
        nonlocal x
        x += 5
        return x
    result1 = inner()
    x = 100
    result2 = inner()
    return result1, result2

print(outer())
```
**Answer:** `(15, 105)`

**Explanation:** `nonlocal x` binds `inner`'s `x` to the same cell as `outer`'s `x` — they share one cell object, not a copy. `inner()` first call: `10 + 5 = 15`, and `outer`'s `x` becomes `15`. Then `outer` reassigns `x = 100` (same cell, now `100`). Second `inner()` call reads that updated cell: `100 + 5 = 105`. This demonstrates closures over mutable shared cells rather than value-capture.

**Difficulty:** Hard — **Success rate:** ~50%
**Topics Tested:** Closures, `nonlocal`, cell variables, shared mutable state

---

## Question 16
```python
class Meta(type):
    def __new__(mcs, name, bases, ns):
        for key, val in list(ns.items()):
            if callable(val) and not key.startswith('__'):
                ns[key] = staticmethod(val)
        return super().__new__(mcs, name, bases, ns)

class Tool(metaclass=Meta):
    def run(x):
        return x * 2

print(Tool.run(5))
t = Tool()
print(t.run(5))
```
**Answer:**
```
10
10
```

**Explanation:** The metaclass rewrites every non-dunder callable in the class namespace into a `staticmethod` before the class is finalized. This strips the implicit `self`/descriptor binding, so `run` takes exactly one positional argument in both the class-level call and instance-level call (`t.run(5)` does **not** insert `t` as the first argument, because `staticmethod` descriptors don't bind). Without the metaclass, `t.run(5)` would raise `TypeError` from an extra positional argument.

**Difficulty:** Very Hard — **Success rate:** ~30%
**Topics Tested:** Metaclasses, `staticmethod` descriptor mechanics, namespace manipulation at class-creation time

---

## Question 17
```python
try:
    try:
        raise ValueError("inner")
    finally:
        print("finally 1")
        raise TypeError("from finally")
except TypeError as e:
    print("caught:", e)
    print("cause:", e.__context__)
```
**Answer:**
```
finally 1
caught: from finally
cause: inner
```

**Explanation:** When a `finally` block raises a new exception while another exception is already propagating, the **new exception replaces the original** as the one that continues to propagate — but Python preserves the original as `__context__` (implicit exception chaining), not `__cause__` (which is only set by explicit `raise ... from ...`). The original `ValueError("inner")` is silently superseded in the traceback chain but recoverable via `__context__`.

**Difficulty:** Very Hard — **Success rate:** ~35%
**Topics Tested:** Exception propagation, `finally` semantics, implicit exception chaining (`__context__`)

---

## Question 18
```python
class ContextMgr:
    def __enter__(self):
        print("enter")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit", exc_type)
        return True

with ContextMgr():
    print("body")
    raise ValueError("boom")

print("after")
```
**Answer:**
```
enter
body
exit <class 'ValueError'>
after
```

**Explanation:** `__exit__` returning `True` (truthy) tells Python the exception has been **handled/suppressed** — the `ValueError` never propagates past the `with` block, so execution continues normally to `print("after")`. This is a commonly-missed context-manager gotcha: silently swallowing exceptions is powerful but dangerous if done accidentally (e.g. by forgetting to `return False`/`None`).

**Difficulty:** Hard — **Success rate:** ~55%
**Topics Tested:** Context managers, `__exit__` return-value semantics, exception suppression

---

## Question 19
```python
class A:
    x = []
    def add(self, val):
        self.x.append(val)

a1 = A()
a2 = A()
a1.add(1)
a2.add(2)
print(a1.x, a2.x)
print(a1.x is a2.x)

a1.x = [99]
print(a1.x, a2.x)
```
**Answer:**
```
[1, 2] [1, 2]
True
[99] [1, 2]
```

**Explanation:** `x = []` is a **class attribute**, shared by all instances until an instance-level assignment shadows it. `a1.add`/`a2.add` both mutate the same shared list object (`self.x.append` doesn't rebind, it mutates in place), hence identical contents and `is` identity. `a1.x = [99]` creates a new **instance attribute** in `a1.__dict__`, shadowing the class attribute for `a1` only — `a2.x` still resolves to the original shared class-level list.

**Difficulty:** Hard — **Success rate:** ~50%
**Topics Tested:** Class vs instance attributes, mutable shared state, attribute shadowing

---

## Question 20
```python
import copy

class Box:
    def __init__(self, items):
        self.items = items

b1 = Box([1, [2, 3], 4])
b2 = copy.copy(b1)
b3 = copy.deepcopy(b1)

b1.items[1].append(99)
b1.items.append(100)

print(b1.items)
print(b2.items)
print(b3.items)
```
**Answer:**
```
[1, [2, 3, 99], 4, 100]
[1, [2, 3, 99], 4]
[1, [2, 3], 4]
```

**Explanation:** `copy.copy` (shallow) creates a new `Box` with a new outer `items` list object, but the **nested** `[2, 3]` list inside is shared by reference — so `b1`'s in-place mutation of the nested list (`.append(99)`) is visible through `b2` too. However, `b1.items.append(100)` rebinds the *outer* list only for `b1` (since `copy.copy` gave `b2` its own outer list object), so `100` does not appear in `b2`. `deepcopy` recursively clones everything, so `b3` is fully insulated from both mutations.

**Difficulty:** Very Hard — **Success rate:** ~35%
**Topics Tested:** Shallow vs deep copy, reference semantics, nested mutable objects

---

## Question 21
```python
def decorator(func):
    count = 0
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(f"Call #{count} to {func.__name__}")
        return func(*args, **kwargs)
    wrapper.get_count = lambda: count
    return wrapper

@decorator
def greet(name):
    return f"Hello, {name}"

greet("Alice")
greet("Bob")
print(greet.get_count())
print(greet.__name__)
```
**Answer:**
```
Call #1 to greet
Call #2 to greet
2
wrapper
```

**Explanation:** The closure variable `count` persists across calls because `wrapper` retains a reference to the same cell each invocation. `get_count` is an attribute attached directly to the `wrapper` function object, reading the shared closure cell. Since `functools.wraps` was **not** used, `greet.__name__` reports `'wrapper'`, not `'greet'` — a very common production bug (breaks introspection, logging, and frameworks relying on `__name__`).

**Difficulty:** Hard — **Success rate:** ~50%
**Topics Tested:** Decorators, closures, function metadata, `functools.wraps` omission trap

---

## Question 22
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    def describe(self):
        return f"Area is {self.area()}"

class Circle(Shape):
    def __init__(self, r):
        self.r = r

try:
    c = Circle(5)
except TypeError as e:
    print("Error:", e)
```
**Answer:**
```
Error: Can't instantiate abstract class Circle with abstract method area
```
*(Exact wording varies slightly by Python version, e.g. 3.12 says "without an implementation for abstract method 'area'".)*

**Explanation:** `Circle` inherits from `Shape` but never overrides `area`, so it still carries the abstract method in `Circle.__abstractmethods__`. `ABCMeta.__call__` checks this set before allowing instantiation and raises `TypeError` — enforcement happens at **instantiation time**, not class-definition time, meaning defining `Circle` itself is perfectly legal.

**Difficulty:** Medium — **Success rate:** ~65%
**Topics Tested:** Abstract Base Classes, `ABCMeta`, abstract method enforcement timing

---

## Question 23
```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

v1 = Vector(1, 2)
v2 = Vector(1, 2)
print(v1 == v2)
print(v1 is v2)
print({v1, v2})
```
**Answer:** `True`, `False`, then raises `TypeError: unhashable type: 'Vector'`.

**Explanation:** `v1 == v2` is `True` via the custom `__eq__`. `v1 is v2` is `False` — distinct objects. The trap: defining `__eq__` without also defining `__hash__` causes Python to set `__hash__` to `None` automatically (per the data model — a class that overrides `__eq__` becomes unhashable unless `__hash__` is explicitly restored), so attempting to put instances into a `set` raises `TypeError` immediately.

**Difficulty:** Hard — **Success rate:** ~45%
**Topics Tested:** `__eq__`/`__hash__` contract, hashability, operator overloading, sets

---

## Question 24
```python
import sys

def show():
    print(sys.getrefcount(obj))

obj = [1, 2, 3]
show()
ref2 = obj
show()
del ref2
show()
```
**Answer:** Three increasing-then-decreasing integers, e.g. `2`, `3`, `2` (exact numbers vary by call context, but the pattern — increase then decrease by 1 — is guaranteed).

**Explanation:** `sys.getrefcount` itself introduces one temporary extra reference (the argument binding inside the function call), so absolute numbers are always inflated by at least 1 relative to naive expectation. Creating `ref2 = obj` increments the true refcount by one; `del ref2` decrements it back. This demonstrates CPython's **reference counting** garbage collection mechanism directly, and the trap is candidates forgetting that the measurement function itself perturbs the count.

**Difficulty:** Very Hard — **Success rate:** ~30%
**Topics Tested:** CPython reference counting, garbage collection internals, `sys.getrefcount` measurement artifacts

---

## Question 25
```python
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("creating instance")
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, value):
        print("init called with", value)
        self.value = value

s1 = Singleton(1)
s2 = Singleton(2)
print(s1 is s2)
print(s1.value, s2.value)
```
**Answer:**
```
creating instance
init called with 1
init called with 2
True
2 2
```

**Explanation:** `__new__` only prints "creating instance" once, since subsequent calls return the cached `_instance`. But critically, `__init__` **always runs** after `__new__` returns an instance of `cls`, regardless of whether it's newly created or reused — this is a widely-misunderstood gotcha in singleton implementations. So `s2 = Singleton(2)` still calls `__init__` on the *same* object, overwriting `value` to `2` for both references.

**Difficulty:** Very Hard — **Success rate:** ~40%
**Topics Tested:** `__new__` vs `__init__` interplay, singleton pattern pitfalls, object identity

---

## Question 26
```python
d = {}
d[1] = 'int one'
d[1.0] = 'float one'
d[True] = 'bool true'
print(d)
print(len(d))
```
**Answer:**
```
{1: 'bool true'}
1
```

**Explanation:** `1`, `1.0`, and `True` all hash equal (`hash(1) == hash(1.0) == hash(True)`) and compare equal (`1 == 1.0 == True`), so all three assignments collapse into a **single dict key**. Critically, the dict retains the key **object from the first insertion** (`1`) but the **value from the last insertion** (`'bool true'`) — a subtle CPython dict-implementation detail: key identity is preserved on collision, but the value is always overwritten.

**Difficulty:** Very Hard — **Success rate:** ~35%
**Topics Tested:** Hashing/equality contract across types, dict key collision behavior, `bool` as `int` subclass

---

## Question 27
```python
def process():
    with open('nonexistent_file_xyz.txt') as f:
        data = f.read()
    return data

try:
    process()
except FileNotFoundError as e:
    print(type(e).__name__, e.errno)
finally:
    print("cleanup")
```
**Answer:**
```
FileNotFoundError 2
cleanup
```

**Explanation:** `open()` on a missing path raises `FileNotFoundError` (a subclass of `OSError`) **before** the `with` block's `__enter__` can complete, so the file is never opened and there's nothing to close. `errno` `2` is the POSIX `ENOENT` code, consistently surfaced across platforms via `OSError.errno`. The `finally` in the outer `try` always executes regardless of whether the exception was caught.

**Difficulty:** Medium — **Success rate:** ~65%
**Topics Tested:** File handling edge cases, exception hierarchy (`OSError`/`FileNotFoundError`), `errno`, context manager failure timing

---

## Question 28
```python
class LazyProperty:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = self.func(obj)
        obj.__dict__[self.name] = value
        return value

class Data:
    @LazyProperty
    def expensive(self):
        print("computing...")
        return 42

d = Data()
print(d.expensive)
print(d.expensive)
print(d.__dict__)
```
**Answer:**
```
computing...
42
42
{'expensive': 42}
```

**Explanation:** `LazyProperty` is a **non-data descriptor** (no `__set__`), so once `obj.__dict__[self.name] = value` stores the computed result directly into the instance dict, subsequent attribute lookups find `'expensive'` in `d.__dict__` **first** — instance `__dict__` takes priority over non-data descriptors in the attribute lookup chain — so the descriptor's `__get__` is never invoked again, and "computing..." prints only once.

**Difficulty:** Expert — **Success rate:** ~25%
**Topics Tested:** Data vs non-data descriptors, attribute lookup priority (`__getattribute__` resolution order), lazy evaluation caching pattern

---

## Question 29
```python
import re

pattern = re.compile(r'(\w+)@(\w+)\.(\w+)')
text = "Contact: alice@example.com or bob@test.org"
matches = pattern.findall(text)
print(matches)

for m in pattern.finditer(text):
    print(m.group(0), m.start(), m.end())
```
**Answer:**
```
[('alice', 'example', 'com'), ('bob', 'test', 'org')]
alice@example.com 10 28
bob@test.org 32 44
```

**Explanation:** `findall` with multiple capture groups returns a list of **tuples** (one element per group), not full matches — a common trap for engineers expecting the full matched string. `finditer` returns match objects, exposing `.group(0)` (the full match), `.start()`, `.end()` as character offsets into the original string.

**Difficulty:** Medium — **Success rate:** ~60%
**Topics Tested:** Regular expressions, `findall` vs `finditer`, capture groups, match object API

---

## Question 30
```python
class EventBus:
    _handlers = {}
    def __init_subclass__(cls, event=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if event:
            EventBus._handlers[event] = cls

class ClickHandler(EventBus, event="click"):
    pass

class HoverHandler(EventBus, event="hover"):
    pass

print(EventBus._handlers)
print(ClickHandler._handlers is HoverHandler._handlers)
```
**Answer:**
```
{'click': <class '__main__.ClickHandler'>, 'hover': <class '__main__.HoverHandler'>}
True
```

**Explanation:** `_handlers` is defined once on `EventBus` and never redefined on the subclasses, so both `ClickHandler._handlers` and `HoverHandler._handlers` resolve via MRO lookup to the **same dict object** on `EventBus` — mutating it via `EventBus._handlers[event] = cls` inside `__init_subclass__` is visible everywhere. This registry pattern is common in plugin architectures but is a trap for anyone assuming subclasses get independent copies of class attributes.

**Difficulty:** Expert — **Success rate:** ~25%
**Topics Tested:** `__init_subclass__`, shared mutable class attributes, registry/plugin pattern, class attribute lookup via MRO

---

## Question 31
```python
async def gen():
    for i in range(3):
        yield i

async def main():
    results = []
    async for x in gen():
        results.append(x)
    print(results)

    agen = gen()
    print(await agen.__anext__())
    print(await agen.__anext__())

import asyncio
asyncio.run(main())
```
**Answer:**
```
[0, 1, 2]
0
1
```

**Explanation:** `gen` is an **async generator** (contains `yield` inside an `async def`), consumed via `async for`, which repeatedly awaits `__anext__()` under the hood until `StopAsyncIteration`. The manual second block creates a fresh async generator instance and manually drives it with two `__anext__()` calls, demonstrating that async generators implement the same "explicit iterator protocol" as regular generators, just with async machinery layered on top.

**Difficulty:** Very Hard — **Success rate:** ~35%
**Topics Tested:** Async generators, `async for`, `__anext__`, `StopAsyncIteration`

---

## Question 32
```python
class Base:
    def __repr__(self):
        return "Base"
    def method(self):
        return self.__repr__()

class Proxy:
    def __init__(self, target):
        self._target = target
    def __getattr__(self, name):
        print(f"proxying {name}")
        return getattr(self._target, name)

p = Proxy(Base())
print(p.method())
print(p._target)
```
**Answer:**
```
proxying method
Base
Base
```

**Explanation:** `__getattr__` is only invoked when normal attribute lookup **fails** — so `p._target` resolves directly from `p.__dict__` without ever triggering `__getattr__` (no "proxying" print for it). `p.method` is not found on `Proxy` normally, so `__getattr__` fires, prints "proxying method", and returns `Base().method` bound method, which is then called — internally invoking `self.__repr__()` on the *original* `Base` instance, returning `"Base"`. This demonstrates that `__getattr__` proxying is selective, not universal, contrary to what many engineers assume.

**Difficulty:** Expert — **Success rate:** ~30%
**Topics Tested:** `__getattr__` vs normal attribute lookup, proxy pattern, delegation semantics

---

## Question 33
```python
def counter():
    i = 0
    while True:
        received = yield i
        if received == "reset":
            i = 0
        else:
            i += 1

c = counter()
print(next(c))
print(c.send("go"))
print(c.send("go"))
print(c.send("reset"))
print(next(c))
c.close()
try:
    next(c)
except StopIteration:
    print("generator closed")
```
**Answer:**
```
0
1
2
0
1
generator closed
```

**Explanation:** Each `send` resumes the generator, assigns the sent value to `received`, evaluates the conditional, then loops back to `yield i` with the updated `i`. `"go"` isn't `"reset"`, so it just increments. `.close()` raises `GeneratorExit` inside the generator at its current suspension point; since it's not caught, the generator terminates cleanly, and any further `next()` call raises `StopIteration`.

**Difficulty:** Hard — **Success rate:** ~45%
**Topics Tested:** Generator `send`, `GeneratorExit`, `.close()`, stateful coroutine-style generators

---

## Question 34
```python
import multiprocessing as mp

def worker(shared_list, val):
    shared_list.append(val)

if __name__ == "__main__":
    normal_list = [1, 2, 3]
    processes = [mp.Process(target=worker, args=(normal_list, i)) for i in range(3)]
    for p in processes: p.start()
    for p in processes: p.join()
    print(normal_list)
```
**Answer:** `[1, 2, 3]` (unchanged)

**Explanation:** Unlike threading, `multiprocessing.Process` forks (or spawns) **separate processes** with independent memory spaces. `normal_list` is a plain Python `list`, not a multiprocessing-aware shared object (`mp.Manager().list()` or shared memory would be needed). Each child process receives a **copy** (via pickling, on spawn platforms) of `normal_list`, mutates its own copy, and that mutation never propagates back to the parent's `normal_list`. This is one of the most common production bugs when engineers assume multiprocessing shares state like threading does.

**Difficulty:** Expert — **Success rate:** ~30%
**Topics Tested:** Multiprocessing memory isolation, process forking/spawning, pickling of arguments, false shared-state assumption

---

## Question 35
```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

t = Temperature(25)
print(t.fahrenheit)
t.fahrenheit = 32
print(t.celsius)
try:
    t.celsius = -300
except ValueError as e:
    print("caught:", e)
print(t.celsius)
```
**Answer:**
```
77.0
0.0
caught: Below absolute zero
0.0
```

**Explanation:** `t.fahrenheit` computes `25 * 9/5 + 32 = 77.0`. Setting `t.fahrenheit = 32` routes through the `fahrenheit.setter`, which computes celsius as `(32-32)*5/9 = 0.0` and delegates to `self.celsius = 0.0`, which passes the validation in `celsius.setter`. The failed assignment (`-300`) raises inside the setter **before** `self._celsius` is mutated, so the object's state remains unchanged at `0.0` — properties provide validated, encapsulated interfaces that look like plain attributes but run full method logic on every access.

**Difficulty:** Hard — **Success rate:** ~55%
**Topics Tested:** `@property`, property setters, encapsulation, validation-on-write pattern

---

## Question 36
```python
class A:
    def __enter__(self):
        print("A enter")
        return self
    def __exit__(self, *args):
        print("A exit")

class B:
    def __enter__(self):
        print("B enter")
        raise RuntimeError("B failed")
    def __exit__(self, *args):
        print("B exit")
        return False

try:
    with A(), B():
        print("body")
except RuntimeError as e:
    print("caught:", e)
```
**Answer:**
```
A enter
B enter
A exit
caught: B failed
```

**Explanation:** Multiple context managers in one `with` statement enter left-to-right. `B.__enter__` raises before returning, so `B`'s context is never considered "entered" — its `__exit__` is **never called**. However, `A` *was* successfully entered, so its `__exit__` still runs during unwind (context managers clean up in reverse order of successful entry). The body (`print("body")`) never executes since the exception happens during setup, before the `with` block's suite runs.

**Difficulty:** Expert — **Success rate:** ~25%
**Topics Tested:** Multiple context managers, partial entry/exit semantics, exception propagation during `__enter__`

---

## Question 37
```python
x = [1, 2, 3]
y = x
x += [4, 5]
print(x, y, x is y)

x = x + [6]
print(x, y, x is y)
```
**Answer:**
```
[1, 2, 3, 4, 5] [1, 2, 3, 4, 5] True
[1, 2, 3, 4, 5, 6] [1, 2, 3, 4, 5] False
```

**Explanation:** For mutable types like `list`, `+=` invokes `__iadd__`, which mutates the list **in place** and returns the same object — so `x is y` remains `True` after `x += [4, 5]`, and `y` reflects the change too. In contrast, `x = x + [6]` uses `__add__`, which always constructs and returns a **brand-new list**, rebinding `x` to it while `y` still points at the old object — this is the canonical demonstration that `+=` and `x = x + ...` are *not* equivalent for mutable sequence types.

**Difficulty:** Hard — **Success rate:** ~50%
**Topics Tested:** `__iadd__` vs `__add__`, in-place mutation vs rebinding, reference semantics

---

## Question 38
```python
import sys

def recurse(n):
    if n == 0:
        return 0
    return 1 + recurse(n - 1)

print(sys.getrecursionlimit())
sys.setrecursionlimit(50)
try:
    recurse(100)
except RecursionError as e:
    print("caught:", type(e).__name__)
sys.setrecursionlimit(1000)
print(recurse(100))
```
**Answer:**
```
1000
caught: RecursionError
100
```

**Explanation:** The default CPython recursion limit is `1000` (may vary slightly by version/build). Lowering it to `50` causes `recurse(100)` to exceed the limit and raise `RecursionError` (a subclass of `RuntimeError`) partway through the call chain — well before reaching the actual base case. Restoring the limit to `1000` allows the same call to succeed normally, returning `100`.

**Difficulty:** Medium — **Success rate:** ~65%
**Topics Tested:** Recursion limits, `RecursionError`, `sys.setrecursionlimit`, call-stack depth management

---

## Question 39
```python
class Meta(type):
    instances = {}
    def __call__(cls, *args, **kwargs):
        key = (cls, args)
        if key not in Meta.instances:
            print(f"new instance for {args}")
            Meta.instances[key] = super().__call__(*args, **kwargs)
        else:
            print(f"reusing instance for {args}")
        return Meta.instances[key]

class Connection(metaclass=Meta):
    def __init__(self, host):
        self.host = host

c1 = Connection("db1")
c2 = Connection("db1")
c3 = Connection("db2")
print(c1 is c2, c1 is c3)
```
**Answer:**
```
new instance for ('db1',)
reusing instance for ('db1',)
new instance for ('db2',)
True False
```

**Explanation:** This is a **flyweight/memoization pattern implemented at the metaclass level**, intercepting instantiation via `Meta.__call__` (the true entry point for `Connection(...)`) before `__new__`/`__init__` even run. Instances are cached keyed by `(cls, args)`, so identical arguments to the same class return the cached object rather than constructing a new one — `c1 is c2` is `True` since both used `"db1"`; `c3` used different args and gets a distinct instance.

**Difficulty:** Expert — **Success rate:** ~25%
**Topics Tested:** Metaclass `__call__` interception, flyweight pattern, object caching keyed by arguments

---

## Question 40
```python
class Base:
    def template(self):
        self.setup()
        try:
            return self.compute()
        except NotImplementedError:
            return "fallback"
    def setup(self):
        print("base setup")
    def compute(self):
        raise NotImplementedError

class Child(Base):
    def setup(self):
        super().setup()
        print("child setup")
    def compute(self):
        return 42

class Incomplete(Base):
    def setup(self):
        print("incomplete setup")

print(Child().template())
print(Incomplete().template())
```
**Answer:**
```
base setup
child setup
42
incomplete setup
fallback
```

**Explanation:** `Child.template()` (inherited from `Base`, unmodified) calls `self.setup()`, which resolves polymorphically to `Child.setup`, which itself calls `super().setup()` cooperatively before adding its own print — demonstrating the **Template Method pattern** with cooperative `super()` chaining. `Child.compute()` overrides the abstract stub, returning `42` directly. `Incomplete` never overrides `compute`, so `self.compute()` resolves to `Base.compute`, raising `NotImplementedError`, which is caught inside `template()` itself, returning the fallback string.

**Difficulty:** Hard — **Success rate:** ~50%
**Topics Tested:** Polymorphism, Template Method pattern, `super()` cooperative calls, exception-based control flow

---

## Question 41
```python
from collections import defaultdict, OrderedDict, Counter

d = defaultdict(lambda: defaultdict(int))
d['a']['x'] += 1
d['a']['y'] += 2
d['b']['x'] += 5
print(dict(d))

c = Counter("mississippi")
print(c.most_common(2))

od = OrderedDict()
od['b'] = 1
od['a'] = 2
od.move_to_end('b')
print(list(od.keys()))
```
**Answer:**
```
{'a': {'x': 1, 'y': 2}, 'b': {'x': 5}}
[('i', 4), ('s', 4)]
['a', 'b']
```

**Explanation:** Nested `defaultdict(lambda: defaultdict(int))` auto-vivifies missing keys at both levels, so `d['a']['x'] += 1` works without pre-initialization. `Counter.most_common(2)` returns the top-2 by frequency; `'i'` and `'s'` are tied at 4 occurrences each, and ties are broken by **first-encountered insertion order** in CPython's Counter implementation — `'i'` appears before `'s'` in `"mississippi"`. `move_to_end('b')` (default `last=True`) relocates key `'b'` to the end of the ordered mapping, yielding `['a', 'b']`.

**Difficulty:** Hard — **Success rate:** ~45%
**Topics Tested:** `collections` module, `defaultdict` auto-vivification, `Counter` tie-breaking, `OrderedDict.move_to_end`

---

## Question 42
```python
class Observable:
    def __set_name__(self, owner, name):
        self.name = "_" + name
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name, None)
    def __set__(self, obj, value):
        old = getattr(obj, self.name, None)
        setattr(obj, self.name, value)
        if old != value:
            print(f"{self.name[1:]} changed: {old} -> {value}")

class Model:
    status = Observable()

m = Model()
m.status = "pending"
m.status = "pending"
m.status = "done"
print(m.status)
```
**Answer:**
```
status changed: None -> pending
status changed: pending -> done
done
```

**Explanation:** `__set_name__` is called automatically at class-body-completion time, telling the descriptor its attribute name (`"status"`) so it can store the actual value under a mangled internal name (`"_status"`) on the instance, avoiding infinite recursion. Setting the same value twice (`"pending"` then `"pending"`) triggers the `old != value` check, which is `False` the second time, so no change is printed — only genuine value transitions get logged, mirroring real "dirty-checking"/observer patterns used in state-management systems.

**Difficulty:** Expert — **Success rate:** ~20%
**Topics Tested:** `__set_name__`, descriptor protocol, change-detection/observer pattern, avoiding descriptor recursion

---

## Question 43
```python
import weakref

class Resource:
    def __init__(self, name):
        self.name = name
    def __del__(self):
        print(f"deleting {self.name}")

r = Resource("R1")
weak = weakref.ref(r)
print(weak() is r)
del r
print(weak())
```
**Answer:**
```
deleting... 
```
Actually precise order:
```
True
deleting R1
None
```

**Explanation:** `weakref.ref(r)` creates a reference that does **not** increase `r`'s reference count, so `weak() is r` correctly reports `True` while `r` is alive. `del r` drops the only strong reference; CPython's reference-counting collector immediately finalizes the object, invoking `__del__` and printing `"deleting R1"` right at the `del` statement. Afterward, the weak reference no longer resolves to a live object, so calling `weak()` returns `None`.

**Difficulty:** Expert — **Success rate:** ~30%
**Topics Tested:** `weakref`, reference counting, `__del__` finalization timing, non-owning references

---

## Question 44
```python
def apply_decorators(*decorators):
    def wrapper(func):
        for dec in reversed(decorators):
            func = dec(func)
        return func
    return wrapper

def bold(func):
    def inner(*a, **kw):
        return f"<b>{func(*a, **kw)}</b>"
    return inner

def italic(func):
    def inner(*a, **kw):
        return f"<i>{func(*a, **kw)}</i>"
    return inner

@apply_decorators(bold, italic)
def text():
    return "hi"

print(text())
```
**Answer:** `<b><i>hi</i></b>`

**Explanation:** `@apply_decorators(bold, italic)` is equivalent to `text = apply_decorators(bold, italic)(text)`. Inside `wrapper`, iterating `reversed((bold, italic))` applies `italic` **first** (innermost), then `bold` (outermost) — so evaluation order is `bold(italic(text))`. Calling the final composed function wraps the innermost `<i>hi</i>` output with `<b>...</b>`, matching standard decorator-stacking semantics where the decorator closest to the function runs first, even though here it's programmatically composed rather than stacked with `@` syntax.

**Difficulty:** Very Hard — **Success rate:** ~35%
**Topics Tested:** Decorator composition/factories, decorator application order, higher-order functions

---

## Question 45
```python
class RangeLike:
    def __init__(self, n):
        self.n = n
    def __getitem__(self, idx):
        if idx >= self.n:
            raise IndexError
        return idx * idx

r = RangeLike(5)
print(list(r))
print(3 in r)
for x in r:
    if x > 8:
        break
    print(x, end=" ")
```
**Answer:**
```
[0, 1, 4, 9, 16]
False
0 1 4
```

**Explanation:** `RangeLike` has no `__iter__`, but implementing `__getitem__` with integer indices starting at `0` triggers Python's **legacy iteration fallback protocol**: `iter()` will call `__getitem__(0)`, `__getitem__(1)`, ... until `IndexError` is raised, which is treated as the natural stop condition — this is how `list(r)` and `for x in r` both work without an explicit iterator. `3 in r` similarly falls back to linear `__getitem__`-based membership testing; since squares `{0,1,4,9,16}` never equal `3`, it's `False`. The `for` loop prints `0 1 4` and breaks once `x=9 > 8`.

**Difficulty:** Expert — **Success rate:** ~25%
**Topics Tested:** Iterator protocol fallback via `__getitem__`, `IndexError`-as-StopIteration convention, membership testing (`in`) internals

---

## Question 46
```python
import sys

class Watcher:
    def __init__(self, name):
        self.name = name

modA = type(sys)('modA')
sys.modules['modA'] = modA
modA.value = 1

import modA as m1
import modA as m2
m1.value = 100
print(m2.value)
print(m1 is m2)

del sys.modules['modA']
import modA as m3
```
**Answer:**
```
100
True
```
then raises `ModuleNotFoundError: No module named 'modA'` at the final `import modA as m3`.

**Explanation:** `sys.modules` is the process-wide **module cache** — once `'modA'` is registered there, every subsequent `import modA` statement returns the exact same cached module object rather than re-executing/re-locating it, so `m1 is m2` is `True` and mutations via one alias are visible via the other. Removing the entry from `sys.modules` doesn't destroy the module object per se, but it does force the import system to re-resolve `'modA'` from scratch — and since it was never a real file on disk (only synthetically injected), the subsequent `import modA as m3` fails with `ModuleNotFoundError`.

**Difficulty:** Expert — **Success rate:** ~20%
**Topics Tested:** Import system internals, `sys.modules` caching, module identity, synthetic module injection

---

## Question 47
```python
class A:
    def __eq__(self, other):
        print("A.__eq__")
        return NotImplemented

class B:
    def __eq__(self, other):
        print("B.__eq__")
        return True

a = A()
b = B()
print(a == b)
print(b == a)
```
**Answer:**
```
A.__eq__
B.__eq__
True
B.__eq__
True
```

**Explanation:** `a == b` first tries `A.__eq__(a, b)`, which prints and returns `NotImplemented` (not an error — a signal to try the reflected operation). Python then falls back to `B.__eq__(b, a)` (the reflected `__eq__`, since `__eq__` is its own reflection), which prints and returns `True` — so the overall result is `True`, but note **both** dunder methods fired. `b == a` directly tries `B.__eq__(b, a)` first, which succeeds immediately, so `A.__eq__` never runs in that line.

**Difficulty:** Very Hard — **Success rate:** ~30%
**Topics Tested:** `NotImplemented` fallback protocol, reflected dunder methods, operator dispatch order

---

## Question 48
```python
async def fetch(n):
    if n == 2:
        raise ValueError(f"failed on {n}")
    return n * 10

async def main():
    import asyncio
    tasks = [asyncio.create_task(fetch(i)) for i in range(4)]
    results = []
    for t in tasks:
        try:
            results.append(await t)
        except ValueError as e:
            results.append(f"error: {e}")
    print(results)

import asyncio
asyncio.run(main())
```
**Answer:**
```
[0, 10, 'error: failed on 2', 30]
```

**Explanation:** `asyncio.create_task` schedules all four coroutines to run **concurrently** on the event loop immediately (not lazily like a bare coroutine object) — they all start executing as soon as the loop gets control. Awaiting each task in sequence in the `for` loop still preserves the original **task order** in `results`, regardless of internal scheduling, and exceptions raised inside a task only surface when that specific task is `await`-ed — here caught individually per-task rather than aborting the whole batch, unlike `asyncio.gather` without `return_exceptions=True`.

**Difficulty:** Expert — **Success rate:** ~25%
**Topics Tested:** `asyncio.create_task` eager scheduling, per-task exception handling, task ordering vs completion order

---

## Question 49
```python
class Meta(type):
    def __prepare__(name, bases, **kwargs):
        print("preparing namespace")
        return {"injected": 42}

class Foo(metaclass=Meta):
    print(injected)
    x = 1

print(Foo.injected)
print(hasattr(Foo, 'injected'))
```
**Answer:**
```
preparing namespace
42
42
True
```

**Explanation:** `__prepare__` is called **before** the class body even begins executing, and its return value becomes the namespace dict that the class body executes *inside* — so `injected` is already a valid name when `print(injected)` runs inside the class body itself (accessed as a bare name, since class bodies execute like a scope with their own local namespace). Because `injected` was never deleted from that namespace, it persists as a regular class attribute on `Foo` after class creation completes.

**Difficulty:** Expert — **Success rate:** ~15%
**Topics Tested:** `__prepare__` metaclass hook, custom class namespaces, class-body execution scope

---

## Question 50
```python
import gc

class Node:
    def __init__(self, name):
        self.name = name
        self.ref = None
    def __del__(self):
        print(f"deleted {self.name}")

def make_cycle():
    a = Node("A")
    b = Node("B")
    a.ref = b
    b.ref = a
    return None

gc.disable()
make_cycle()
print("after make_cycle, no output above")
gc.collect()
print("after manual collect")
gc.enable()
```
**Answer:**
```
after make_cycle, no output above
deleted A
deleted B
after manual collect
```
*(Order of "deleted A"/"deleted B" between the two is not strictly guaranteed but both occur only during `gc.collect()`.)*

**Explanation:** `a` and `b` form a **reference cycle** (`a.ref -> b`, `b.ref -> a`), so their reference counts never drop to zero purely from `make_cycle` returning — pure refcounting *cannot* collect cycles. With `gc.disable()`, the cyclic garbage collector's automatic periodic sweep is turned off, so the cycle leaks indefinitely until `gc.collect()` is called explicitly, which walks the object graph, detects the unreachable cycle, and finalizes both objects — hence both `__del__` prints appear only after the explicit `gc.collect()` call, not immediately after `make_cycle()` returns.

**Difficulty:** Expert — **Success rate:** ~20%
**Topics Tested:** Reference counting vs cyclic garbage collector, `gc.collect()`, reference cycles, `__del__` finalization timing under cycles

---

## Interview Wrap-Up

That's the full 50. A few notes on how I'd actually run this in a real loop:

- **Questions 1–10** calibrate baseline signal — if a candidate stumbles on closures, mutable defaults, or MRO here, I'd wrap the interview early.
- **Questions 11–30** are where I separate "strong senior engineer" from "principal-level" — descriptor protocol, metaclass instantiation order, and GIL/threading gotchas are the real filters.
- **Questions 31–50** are deliberately brutal — async scheduling internals, `sys.modules` cache manipulation, `__prepare__`, and cyclic GC are things I'd expect maybe 1 in 5 senior candidates to nail cleanly. Getting 60%+ of these right, with correct reasoning (not just correct output), is a strong signal for the kind of Python fluency we need building inference infrastructure, tooling, and research systems at this level.

**Scoring guide I use internally:**
- 40+/50 correct with clean reasoning → Strong hire signal on Python fundamentals
- 30–39/50 → Proceed to systems/infra round, some gaps to probe
- <30/50 → Likely not at principal-level Python depth yet

Good luck — and if you want, I'm happy to go through any of these in more depth or discuss the underlying CPython source (`ceval.c`, `typeobject.c`, `gcmodule.c`) for the ones you found hardest.
