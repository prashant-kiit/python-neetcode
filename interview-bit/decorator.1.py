from functools import wraps

def my_decorator_0(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator_0
def greet(name):
    """Greets a person."""
    print(f"Hi, {name}!")

print(greet.__name__)  # "wrapper"
print(greet.__doc__)   # None


def my_decorator_1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator_1
def greet(name):
    """Greets a person."""
    print(f"Hi, {name}!")

print(greet.__name__)  # greet (not "wrapper")
print(greet.__doc__)   # Greets a person.