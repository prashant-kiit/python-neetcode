from functools import wraps


def coroutine(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        print('auto-priming the printer (runs on once)')
        next(gen)  # auto-prime
        return gen
    return wrapper

def printer():
    while True:
        line = yield
        print("Got:", line)

wrapper = coroutine(printer)
gen = wrapper()
# coroutine wrapper is only for auto priming
gen.send("hello")   # Got: hello
gen.send("world")   # Got: world

# -----------annotated version-------------------------

def coroutine(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        print('auto-priming the printer (runs on once)')
        next(gen)  # auto-prime
        return gen
    return wrapper

@coroutine
def printer():
    while True:
        line = yield
        print("Got:", line)

gen = printer()
# coroutine wrapper is only for auto priming
gen.send("hello")   # Got: hello
gen.send("world")   # Got: world