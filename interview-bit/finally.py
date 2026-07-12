# Why is Python designed this way?
# finally exists to guarantee cleanup (closing files, releasing locks, etc.) before a function exits.
# To preserve that guarantee, Python delays the actual return/exception until after finally finishes.
# If finally itself changes the control flow (with return, raise, break, or continue), that new control flow takes precedence over the pending one.

# example 1 
def f():
    try:
        return 1
    finally:
        return 2

print(f())   # 2

# example 2
def f():
    try:
        raise ValueError()
    finally:
        return 42

print(f())   # 42