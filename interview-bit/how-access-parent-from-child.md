# Calling Parent Class Methods Without Creating a Parent Instance

**Yes** — this is actually the *normal* way it's done in Python. You never need to explicitly instantiate the parent to access its methods.

## 1. Via `super()` — no parent instance needed

```python
class Parent:
    def greet(self):
        return "Hello from Parent"

class Child(Parent):
    def greet(self):
        return super().greet() + " and Child"   # no Parent() instance anywhere

c = Child()
print(c.greet())   # Hello from Parent and Child
```

`super()` doesn't create a new `Parent` object — it returns a **proxy object** that routes method calls through the MRO, using the **existing `self`** (the `Child` instance).

## 2. Calling an instance method directly on the class, passing `self`

```python
class Parent:
    def greet(self):
        return "Hello from Parent"

class Child(Parent):
    def greet(self):
        return Parent.greet(self) + " and Child"   # self is the Child instance

c = Child()
print(c.greet())   # Hello from Parent and Child
```

No `Parent()` object is created — `self` (the `Child` instance) is passed manually as the first argument to the **unbound** method `Parent.greet`.

## 3. Calling a `@staticmethod` — genuinely no instance at all

```python
class Parent:
    @staticmethod
    def utility():
        return "Static utility from Parent"

class Child(Parent):
    def do_something(self):
        return Parent.utility()    # no self, no instance, nothing

print(Child().do_something())   # Static utility from Parent
print(Parent.utility())          # also works directly, no instance
```

## 4. Calling a `@classmethod` — uses the class, not an instance

```python
class Parent:
    count = 0

    @classmethod
    def increment(cls):
        cls.count += 1
        return cls.count

class Child(Parent):
    pass

print(Child.increment())   # 1 — no Parent() or Child() instance created
```

## 5. Accessing class attributes — no instance needed at all

```python
class Parent:
    species = "Human"

print(Parent.species)   # Human — direct class access, no instantiation
```

## Why this works — the key insight

Methods in Python are just **functions stored on the class**. `self` is simply the first parameter — Python doesn't require an "instance of Parent specifically," it just requires *something* to pass as `self`. Since `Child` **is-a** `Parent` (inheritance), a `Child` instance is perfectly valid to pass in.

```python
class Parent:
    def greet(self):
        return f"Hello from {type(self).__name__}"   # notice: uses type(self), not "Parent"

class Child(Parent):
    pass

c = Child()
print(Parent.greet(c))   # Hello from Child — Parent's method, but with Child's self!
```

This also shows *why* `super()` is preferred over `Parent.method(self)` — the parent's logic still runs correctly using whatever the actual runtime type is.

## Quick summary

| Access method | Needs Parent instance? |
|---|---|
| `super().method()` | ❌ No |
| `Parent.method(self)` | ❌ No — but needs *some* instance as `self` |
| `Parent.static_method()` | ❌ No — no instance at all |
| `Parent.class_method()` | ❌ No — uses the class, not an instance |
| `Parent.class_attribute` | ❌ No |

**Bottom line:** you never need to actually create a `Parent()` object just to reuse its methods or attributes from a child class — inheritance means the child already has access to all of it.