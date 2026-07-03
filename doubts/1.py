# Question: Complex Nos?

from cmath import polar, rect


a = 3 + 4j
print(a) 
print(a.real, a.imag)
print(a.conjugate())

b = complex(2, 5)
print(b)
print(b.real, b.imag)
print(b.conjugate())

c = a + b
print(c)

d = a - b
print(d)

e = a * b
print(e)

f = a / b
print(f)

print(abs(a))
print(abs(b))

magnitude, radian = polar(a)
print(magnitude, radian)
A = rect(magnitude, radian)
print(A)