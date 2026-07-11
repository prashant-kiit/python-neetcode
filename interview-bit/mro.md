# `super()` with Two (or More) Parents

When a class has multiple parents, `super()` doesn't just mean "my first/direct parent" — it means **"the next class in the MRO (Method Resolution Order)"**. Python computes a single linear order across *all* ancestors, and `super()` walks through that order.

## Basic multiple inheritance

```python
class Father:
    def skills(self):
        return "Gardening"

class Mother:
    def skills(self):
        return "Cooking"

class Child(Father, Mother):
    def skills(self):
        return super().skills()      # which one gets called?

c = Child()
print(c.skills())   # Gardening
```

`super().skills()` calls **`Father.skills()`**, because `Father` is listed first in `class Child(Father, Mother)`. Check the MRO to confirm:

```python
print(Child.__mro__)
# (Child, Father, Mother, object)
```

Python searches **left to right** as declared in the class definition — `super()` in `Child` looks at what comes right after `Child` in the MRO, which is `Father`.

## To reach the second parent, `Father` must also call `super()`

```python
class Father:
    def skills(self):
        return "Gardening"
        # no super() call — chain stops here

class Mother:
    def skills(self):
        return "Cooking"

class Child(Father, Mother):
    def skills(self):
        return super().skills()

c = Child()
print(c.skills())   # Gardening only — Mother never gets reached!
```

`Mother.skills()` never runs because `Father.skills()` doesn't call `super().skills()` itself. To chain through **all** parents cooperatively, every class in the chain must call `super()`:

```python
class Father:
    def skills(self):
        return "Gardening"

class Mother:
    def skills(self):
        return "Cooking"

class GrandParent:
    def skills(self):
        return "Wisdom"

class Father(GrandParent):
    def skills(self):
        return "Gardening, " + super().skills()

class Mother(GrandParent):
    def skills(self):
        return "Cooking, " + super().skills()

class Child(Father, Mother):
    def skills(self):
        return "Coding, " + super().skills()

c = Child()
print(c.skills())
# Coding, Gardening, Cooking, Wisdom

print(Child.__mro__)
# (Child, Father, Mother, GrandParent, object)
```

This is the **diamond inheritance** pattern — `Father` and `Mother` both inherit from `GrandParent`, and `Child` inherits from both. `super()` follows the MRO chain, calling **each class exactly once**, in a well-defined order, without skipping or duplicating `GrandParent`.

## `__init__` with two parents — the common real case

```python
class Father:
    def __init__(self, name):
        print("Father init")
        self.father_name = name

class Mother:
    def __init__(self, name):
        print("Mother init")
        self.mother_name = name

class Child(Father, Mother):
    def __init__(self, father_name, mother_name):
        print("Child init")
        super().__init__(father_name)     # calls Father.__init__ (next in MRO)
        # Mother's __init__ never runs unless Father also calls super()!

c = Child("John", "Jane")
# Child init
# Father init
print(c.father_name)    # John
print(hasattr(c, "mother_name"))   # False — Mother's __init__ was skipped
```

To properly initialize **both** parents, use **cooperative multiple inheritance** with `**kwargs`:

```python
class Father:
    def __init__(self, father_name, **kwargs):
        print("Father init")
        self.father_name = father_name
        super().__init__(**kwargs)     # passes remaining kwargs along the MRO

class Mother:
    def __init__(self, mother_name, **kwargs):
        print("Mother init")
        self.mother_name = mother_name
        super().__init__(**kwargs)

class Child(Father, Mother):
    def __init__(self, father_name, mother_name):
        print("Child init")
        super().__init__(father_name=father_name, mother_name=mother_name)

c = Child("John", "Jane")
# Child init
# Father init
# Mother init
print(c.father_name, c.mother_name)   # John Jane
```

This works because **each class only needs to know about the next one in line**, not the whole hierarchy — `super()` handles routing automatically based on MRO.

## Calling a *specific* parent (bypassing MRO order)

If you genuinely need one particular parent's method (not "next in MRO"), call it directly instead of using `super()`:

```python
class Father:
    def skills(self):
        return "Gardening"

class Mother:
    def skills(self):
        return "Cooking"

class Child(Father, Mother):
    def skills(self):
        father_skill = Father.skills(self)    # explicit, bypasses MRO
        mother_skill = Mother.skills(self)     # explicit, bypasses MRO
        return f"{father_skill} and {mother_skill}"

c = Child()
print(c.skills())   # Gardening and Cooking
```

This is less "cooperative" (doesn't respect MRO chaining) but guarantees you get exactly the class you name.

## How MRO order is decided (quick refresher)

Order depends on **declaration order in the class definition**:

```python
class Child(Father, Mother):   # Father checked before Mother
    pass
# MRO: Child → Father → Mother → ... → object

class Child(Mother, Father):   # swapped — Mother checked before Father
    pass
# MRO: Child → Mother → Father → ... → object
```

You can always check it directly:
```python
print(Child.__mro__)
# or
print(Child.mro())
```

## Quick summary

| Scenario | Behavior |
|---|---|
| `super()` in a class with 2 parents | Goes to next class in MRO (left-to-right as declared) |
| Want both parents reached | Every class in the chain must call `super()` |
| Want one *specific* parent, ignoring order | Call `ParentName.method(self)` directly |
| `**kwargs` cooperative pattern | Standard way to safely init multiple parents via `super()` |
| Check the actual order | `ClassName.__mro__` |

**Key mental model:** `super()` never means "my parent" literally — it means **"whoever's next in this class's MRO,"** which Python computes once for the whole hierarchy using the C3 linearization algorithm.