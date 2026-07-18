natural_numbers = [1, 2, 3, 4, 5]

print("Lesson 0")

print(natural_numbers) # [1, 2, 3, 4, 5]
for n in natural_numbers:
    print(n)

print("Lesson 1")

natural_numbers_iter = iter(natural_numbers)

print(next(natural_numbers_iter)) # 1
print(next(natural_numbers_iter)) # 2
print(next(natural_numbers_iter)) # 3
print(next(natural_numbers_iter)) # 4   
print(next(natural_numbers_iter)) # 5   
try:
    print(next(natural_numbers_iter)) # Throws error
except StopIteration as e:
    print(e)
else:
    print("No exception occurred.")
finally:
    print("Done") 

print("Lesson 2")

natural_numbers_iter_0 = iter(natural_numbers)

print(next(natural_numbers_iter_0)) # 1
print(next(natural_numbers_iter_0)) # 2
print(next(natural_numbers_iter_0)) # 3
print(next(natural_numbers_iter_0)) # 4   
print(next(natural_numbers_iter_0)) # 5   
try:
    print(next(natural_numbers_iter_0)) # Throws error
except StopIteration as e:
    print(e)
else:
    print("No exception occurred.")
finally:
    print("Done") 

print("Lesson 3")

natural_numbers_iter_1 = iter(natural_numbers)

print(list(natural_numbers_iter_1)) # [1, 2, 3, 4]

print("Lesson 4")

new_gen_0 = iter(natural_numbers)
for n in new_gen_0:
    print(n) # 1 2 3
    if n==3:
        break

print("Lesson 5")
new_gen_1 = iter(new_gen_0)
print(next(new_gen_1)) # 4

"""
Iterator requires its iterable to hashable ao that it can traverse by identifing each item in the iterable
"""

print("Lesson 6")

class CountToThree:
    def __init__(self):
        self.num = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.num > 3:
            raise StopIteration
        value = self.num
        self.num += 1
        return value

counter = CountToThree()

for i in counter:
    print(i)