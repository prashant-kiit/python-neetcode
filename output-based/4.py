# Small Int Caching (Data Pool Pre-caching at Compiled Time)
a = 256
b = 256
print(a is b) 

# Constant Folding (Data Pool for Constant at Compiled Time)
c = 257
d = 257
print(c is d)

# Constant Folding (Data Pool for Constant at Compiled Time)
e = 257.1
f = 257.1
print(e is f)

# Small Int Caching (Data Pool Pre-caching at Compiled Time)
g = True
h = True
print(g is h)

# Small Int Caching (Data Pool Pre-caching at Compiled Time)
i = None
j = None
print(i is j)

# Data Pooling at Run time
k = "hello"
l_ = "hello"
print(k is l_)

# Small Int Caching (Data Pool Pre-caching at Compiled Time) and Data Pooling at Run time
m = int('123')
n = int('123')
o = 123
print(m is n)
print(m is o)

# No Optimization b/c more than 256, no constant and no pooling
m = int('257')
n = int('257')
o = 257
print(m is n)
print(m is o)

# No Optimization b/c more than 256, no constant and no pooling
x = float("257.1")
y = float("257.1")
print(x is y)