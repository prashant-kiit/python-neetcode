Python uses a model that's neither strictly "pass by value" nor "pass by reference" — it's often called **"pass by object reference"** (or "pass by assignment").

### The core idea
When you call a function, the argument variable and the parameter name both end up pointing to the **same object** in memory. What happens next depends on whether that object is **mutable** or **immutable**.

### Immutable objects (int, float, str, tuple, bool)
Any "modification" inside the function actually creates a new object — the original outside the function is untouched.

```python
def modify(x):
    x = x + 1
    print("Inside:", x)

a = 5
modify(a)
print("Outside:", a)

# Inside: 6
# Outside: 5   <- unchanged
```

### Mutable objects (list, dict, set, custom objects)
Since the parameter refers to the *same* object, in-place changes are visible outside the function.

```python
def modify(lst):
    lst.append(4)

a = [1, 2, 3]
modify(a)
print(a)
# => [1, 2, 3, 4]   <- changed!
```

But if you **reassign** the parameter to a new object (instead of mutating it in place), the outside variable is unaffected — because now the parameter just points somewhere else:

```python
def modify(lst):
    lst = [9, 9, 9]  # reassignment, not mutation

a = [1, 2, 3]
modify(a)
print(a)
# => [1, 2, 3]   <- unchanged
```

### Summary
| Behavior | What happens |
|---|---|
| Mutating a mutable object (`.append()`, `[i] = x`, `.update()`) | Change is visible outside |
| Reassigning the parameter (`x = ...`) | Change is local only, original untouched |
| Passing immutable objects (int, str, tuple) | Original is never affected |

So it's more accurate to say: **Python passes references to objects by value** — the reference itself is copied, but it points to the same underlying object.