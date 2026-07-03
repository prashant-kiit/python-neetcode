from typing import Any

t1 = tuple[Any]([1, 2, 3])
print(t1)

t2 = (10, 20, 30)
print(t2)

print(t2[0])
print(t2[-1])
print(t1[1:3])

print(len(t1))
print(hash(t2))

map1 = {
    (1, 2): 'A'
}
print(map1)



