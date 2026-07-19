from typing import Any


from collections import deque

person = {
    "name": "Prashant",
    "location": "Bangalore"
}
job = {
    "designation": "Engineer",
    "experience": 5
}
print(person, job)

# unpacking
print({**person, **job})
print({*{1, 2}, *{3, 4}})
print([*[1, 2], *[3, 4]])
print((*(1, 2), *(3, 4)))
print(*"12", *"34")

# concat
# print(person + job) # TypeError: unsupported operand type(s) for +: 'dict' and 'dict'
# print({1, 2} + {3, 4}) # TypeError: unsupported operand type(s) for +: 'dict' and 'dict'
# print(deque([1, 2] + deque[3, 4])) # TypeError: can only concatenate list (not "types.GenericAlias") to list
print([1, 2] + [3, 4])
print((1, 2) + (3, 4))
print("12" + "34")

# zip
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30]
print(list(zip(names, ages)))
for name, age in zip(names, ages):
    print(name, age)
# unzip
zipped_list = list(zip(names, ages))
names, ages = zip(*zipped_list)
print(names, ages)
