# sets
from collections import deque

s1 = {1, 2, 2}
print(s1)

s2 = {1, "hello", (1, 2)}
print(s2)

try:
    s2 = {
        1,
        "hello",
        (1, 2),
        deque[int]([10, 20]),
        [10, 20],
    }  # throws error -> TypeError: unhashable type
    print(s2)
except Exception as ex:
    print(ex)

s3 = set()
s3.add(2)
s3.add('4')

print(len(s3))
print(2 in s3)

s4 = set([1, 2, 3, 4])
s4.remove(3) # O(1) Makes the value None against the index pointer (key pointer)
print(s4) # O(n) iterates over the indexes or keys of map or table (these indexes are derived from keys and keys from hash function)
