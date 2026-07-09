def gen():
    print("start")
    x = yield 1
    print("received", x)
    y = yield 2
    print("received", y)
    yield 3
    return "done"

g = gen()
print(next(g))
print(g.send("hello"))
print(g.send("world"))
try:
    next(g)
except StopIteration as exception:
    print(exception)
    print(exception.value)