def make_multipliers():
    return [lambda x: x * i for i in range(3)]

fns = make_multipliers() 
print(fns)
print([f for f in fns])

# [20, 20, 20] — because of late binding of closures in Python.