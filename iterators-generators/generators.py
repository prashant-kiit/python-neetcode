def get_natural_numbers():
    yield 0
    yield 1
    yield 2
    yield 3

def get_inifite_natural_numbers():
    n=1
    while True:
        yield n
        n+=1

print("Lesson 0")

print(get_natural_numbers) # <function get_natural_numbers at 0x102f7b2e0>
print(get_natural_numbers()) # <generator object get_natural_numbers at 0x100bee610>
print(list(get_natural_numbers())) # [0, 1, 2, 3]

print("Lesson 1")

# Different generators in both print. Thus each of them starts from beginning.
print(next(get_natural_numbers())) # 0
print(next(get_natural_numbers())) # 0
print(next(get_natural_numbers())) # 0
print(next(get_natural_numbers())) # 0
print(next(get_natural_numbers())) # 0

print("Lesson 2")

gen = get_natural_numbers()
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
try:
    print(next(gen))
except StopIteration as e:
    print(e)
    
else:
    print("No exception occurred.")
finally:
    print("Done")

print("Lesson 3")

infi_gen = get_inifite_natural_numbers()
print(next(infi_gen))
print(next(infi_gen))
print(next(infi_gen))
print(next(infi_gen))
try:
    print(next(infi_gen))
except StopIteration as e:
    print(e)
    
else:
    print("No exception occurred.")
finally:
    print("Done")

print("Lesson 3")

infi_gen_0 = get_inifite_natural_numbers()
for n in infi_gen_0:
    print(n)
    if n==10:
        break

print("Lesson 4")

squares = (x * x for x in range(5))
for n in squares:
    print(n)
