def f0(a, b, *argv):
   print(argv)
f0(1, 2, 3, 4, 5)

# Gives error Only one '*' parameter allowed
# def f1(*args, *argv): 
#    print(argv)
# f1(1, 2, 3, 4, 5)

def f2(a, b, **argv):
   print(argv)
f2(1, 2)

# TypeError: f2() takes 2 positional arguments but 3 were given
# def f2(a, b, **argv):
#    print(argv)
# f2(1, 2, 3)

def f2(a, b, **argv):
   print(argv)
f2(1, 2, c='hello')