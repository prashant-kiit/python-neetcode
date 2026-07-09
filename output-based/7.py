def count_up(n):
    i = 1
    while i <= n:
        result = yield i
        print(result)
        i += 1

gen = count_up(3)
print(gen)
# => <generator object count_up at 0x...>
print(next(gen))
print(next(gen))
print(next(gen))