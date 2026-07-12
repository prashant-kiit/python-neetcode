Question: can we define a variable in lambda method in py?
Answer: Yes. There are a few ways.

### 1. Use the assignment expression (`:=`) (Python 3.8+)

```python
f = lambda x: (y := x * 2) + y

print(f(5))  # 20
```

Here, `y` is assigned within the lambda and can be reused in the same expression.

---

### 2. Use an inner lambda (works in all Python versions)

```python
f = lambda x: (lambda y: y + y)(x * 2)

print(f(5))  # 20
```

This simulates a local variable.

---

### 3. Capture a variable from the outer scope

```python
factor = 10
f = lambda x: x * factor
```

`factor` is not defined inside the lambda—it is captured from the enclosing scope.

---

### Limitation

A `lambda` can contain **only a single expression**, not statements. So this is **not allowed**:

```python
# SyntaxError
lambda x:
    y = x * 2
    y + 1
```

because `y = ...` is a statement.

### Summary

* ✅ `lambda x: (y := x * 2) + y` (Python 3.8+)
* ✅ `lambda x: (lambda y: y + y)(x * 2)` (all versions)
* ❌ Cannot use normal assignment (`=`) inside a lambda.
