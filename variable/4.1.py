# Constant

from typing import Final


BASE_URL: Final[str] = 'http://localhost:3000/api' # enforcable at lint time not compile
PORT = 3000

print(BASE_URL)

print(type(BASE_URL))
print(type(PORT))

a = (1, 2, 3)
b = a
c = (1, 2, 3)

print(id(a))
print(hash(a))
print(id(b))
print(hash(b))
print(id(c))
print(hash(c))

A = 20
B = 20

# In Python, id() returns an object's unique memory address, 
# while hash() returns a fixed integer representing an object's value to enable fast lookups in dictionaries and sets. 
# Every object in Python has a unique identity, but only immutable objects are hashable.
print(id(A) == id(B)) # same b.c of object pooling
print(hash(A) == hash(B)) # same b.c of value

mymain = {
    'name': 'Prashant',
    'work': lambda x: x*2
}

def foo():
    pass

print(foo)