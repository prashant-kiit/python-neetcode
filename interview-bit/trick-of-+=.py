# Why can x = x + [1] behave differently than x += [1]? in py in short.

# x = x + [1] creates a new list, while x += [1] modifies the existing list in place.

# For mutable types
# such as List
# = operator
x = [1, 2]
y = x
x = x + [3]     # New list
print(x)        # [1, 2, 3]
print(y)        # [1, 2]

# += operator
x = [1, 2]
y = x
x += [3]        # In-place modification
print(x)        # [1, 2, 3]
print(y)        # [1, 2, 3]

# such as Dict
# = operator
d = {"a": 1}
e = d
d = d | {"b": 2}     # New dictionary (Python 3.9+)
print(e)             # {'a': 1}

# |= operator
d = {"a": 1}
e = d
d |= {"b": 2}        # In place (Python 3.9+)