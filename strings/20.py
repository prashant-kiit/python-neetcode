# play with chars and strings and type casting

print(ord('A'))
print(ord('B'))

# print(int('abc')) throws error -> ValueError: invalid literal for int() with base 10: 'abc'

print(int('123'))

# print(int('123') + 'A') throws error -> TypeError: unsupported operand type(s) for +: 'int' and 'str'

print(str(123) + 'A')