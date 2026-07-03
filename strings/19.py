s = 'abc'

print(s[0], s[1], s[2], s[-1], s[-2], s[-3])

# s[0] = 'A' throws error -> TypeError: 'str' object does not support item assignment

print(s[0:0])
print(s[0:1])
print(s[0:2])
print(s[0:3])
print(s[1:3])
print(s[2:3])
print(s[3:3])

# s[0]='A' throws error -> TypeError: 'str' object does not support item assignment

S1 = s + 'def'
print(s)
print(S1)

S2 = ",".join([s, 'def'])
print(s)
print(S2)

