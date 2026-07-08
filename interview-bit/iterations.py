# -------------------------------
# 1. Creation
# -------------------------------

r = range(5)                    # range (lazy sequence)
it = iter(r)                    # iterator
g = (x*x for x in range(5))      # generator


# -------------------------------
# 2. Types
# -------------------------------

print(type(r))   # <class 'range'>
print(type(it))  # <class 'range_iterator'>
print(type(g))   # <class 'generator'>


# -------------------------------
# 3. All are iterable
# -------------------------------

print(list(r))    # [0, 1, 2, 3, 4]
print(list(it))   # [0, 1, 2, 3, 4]
print(list(g))    # [0, 1, 4, 9, 16]


# -------------------------------
# 4. Lazy (nothing computed until needed)
# -------------------------------

r = range(1_000_000_000)
it = iter(r)
g = (x*x for x in r)

print(next(it))   # 0
print(next(g))    # 0


# -------------------------------
# 5. Reusable?
# -------------------------------

r = range(3)
print(list(r))    # [0,1,2]
print(list(r))    # [0,1,2]   ✅ reusable

it = iter(range(3))
print(list(it))   # [0,1,2]
print(list(it))   # []        ❌ exhausted

g = (x for x in range(3))
print(list(g))    # [0,1,2]
print(list(g))    # []        ❌ exhausted


# -------------------------------
# 6. Indexing
# -------------------------------

r = range(5)
print(r[3])       # 3

# it[3]           # TypeError
# g[3]            # TypeError


# -------------------------------
# 7. Length
# -------------------------------

print(len(r))     # 5

# len(it)         # TypeError
# len(g)          # TypeError


# -------------------------------
# 8. next()
# -------------------------------

# next(r)         # TypeError (range is NOT an iterator)

it = iter(range(3))
print(next(it))   # 0
print(next(it))   # 1

g = (x for x in range(3))
print(next(g))    # 0
print(next(g))    # 1


# -------------------------------
# 9. Can create multiple iterators
# -------------------------------

r = range(3)

it1 = iter(r)
it2 = iter(r)

print(next(it1))  # 0
print(next(it2))  # 0 (independent)

g = (x for x in range(3))

# it1 = iter(g)
# it2 = iter(g)
# it1 and it2 are actually the SAME generator object


# -------------------------------
# 10. Equality
# -------------------------------

print(range(5) == range(5))          # True

print(iter(range(5)) == iter(range(5)))   # False

print((x for x in range(5)) == (x for x in range(5)))  # False


# -------------------------------
# 11. Memory
# -------------------------------

import sys

r = range(10_000_000)
g = (x for x in range(10_000_000))

print(sys.getsizeof(r))   # small
print(sys.getsizeof(g))   # small


# -------------------------------
# 12. Summary
# -------------------------------

# range
# - lazy sequence
# - reusable
# - indexing
# - len()
# - not an iterator

# iterator
# - lazy
# - one-pass
# - next()
# - no indexing
# - no len()

# generator
# - special iterator
# - lazy
# - one-pass
# - next()
# - can execute arbitrary code using yield


g = (x for x in range(5))

iter(g) is g        # True
iter(g) == g        # True

g1 = (x for x in range(5))
g2 = (x for x in range(5))

g1 is g2            # False
g1 == g2            # False

# iter(generator) → returns the same generator
it1 = iter(g) 
it2 = iter(g)

print(it1 is it2)   # True