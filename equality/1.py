s1 = 'abc'
s2 = 'abc'
print(s1==s2)
print(s1 is s2)

t2 = (10, 20, 30)
t3 = (10, 20, 30)
print(t2==t3)
print(t2 is t3)

map1 = {
    (1, 2): 'A'
}

map2 = {
    (1, 2): 'A'
}
print(map1==map2)
print(map1 is map2)

class Person:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

p1 = Person("Alice")
p2 = Person("Alice")

print(p1 == p2)   # True