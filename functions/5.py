a = 100

def muliply(n, m):
    global a
    a = 10

    A = -100

    def mulitplyByA(num):
        A = -10
        return num * A

    result = mulitplyByA(n * m * a)
    print(A)
    return result


print(muliply(2, 3))
print(a)