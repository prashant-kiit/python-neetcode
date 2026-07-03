# loops on dict

map = {
    'A' : 1,
    'B' : 2
}

print(map)

for key in map:
    print(key)

for value in map.values():
    print(value)

for item in map.items():
    print(item, item[0], item[1])
    key, value = item
    print(key, value)

