a = 100

def muliply(n, m):
    global a
    a = 10
    return n * m * a


print(muliply(2, 3))
print(a)