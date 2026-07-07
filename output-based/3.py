collect = []
def foo0(item):
    collect.append(item)
    return collect

print(foo0(10))
print(foo0(20))
print(foo0(30))

print('---------------')

def foo1(item, collect = []):
    collect.append(item)
    return collect

print(foo1(10))
print(foo1(20))
print(foo1(30))