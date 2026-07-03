def getMuliplier():
    A = 100 # stored in closure
    return lambda n, m: (num:= n * m) * A + num


print(getMuliplier()(2, 3))

# Python searches Local → Enclosing → Global → Built-ins.
# You cannot declare a local variable inside a Python lambda using normal assignment (=), because assignment is a statement, and lambdas can only contain a single expression.
# Python lambdas can only contain one expression, but that expression can span multiple lines using parentheses.