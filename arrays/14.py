# unpacking

arr = [1, 2, 3]

a = arr
print(a)

# a, b = arr throws error -> ValueError: too many values to unpack (expected 2)
# print(a, b)

a, b, c = arr
print(a, b, c)

# a, b, c, d = arr throws error -> ValueError: not enough values to unpack (expected 4, got 3)
# print(a, b, c, d)
