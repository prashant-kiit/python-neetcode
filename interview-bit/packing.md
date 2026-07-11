Python doesn't have a dedicated **spread operator** like JavaScript (`...`), but it provides similar unpacking syntax with `*` and `**`.

```python
# Lists/Tuples
a = [1, 2]
b = [*a, 3, 4]          # [1, 2, 3, 4]

# Function arguments
def f(x, y):
    print(x, y)

args = [1, 2]
f(*args)                # f(1, 2)

# Dictionaries
d1 = {"a": 1}
d2 = {**d1, "b": 2}     # {'a': 1, 'b': 2}

# Keyword arguments
kwargs = {"x": 1, "y": 2}
f(**kwargs)             # f(x=1, y=2)
```

* `*` → Unpacks iterables (lists, tuples, sets, etc.)
* `**` → Unpacks dictionaries into keyword arguments or merges dictionaries
