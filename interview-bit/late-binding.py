# Late binding means a closure (or lambda) captures the variable, not its value. 
# The variable is looked up when the function is called, not when it's created.

# Impure lambda function.
# Referencing the value (object), that referenced outside the lambda also 
# Like useeffect hook in React
funcs = []
for i in range(3):
    funcs.append(lambda: i)
print([f() for f in funcs])   # [2, 2, 2]


# Pure lambda function.
# Referencing the value (object), that referenced only inside the lambda in params 
# Like useeffect hook in React
funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)
print([f() for f in funcs])   # [0, 1, 2]