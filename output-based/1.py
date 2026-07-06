x = 5
def outer():
    # global x
    x = 10
    x = x + 1
    return x
print(outer())

