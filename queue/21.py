# list and stack

from collections import deque
from typing import Any

arr = [1, 2, 3]
arr.remove(2) # O(n)
arr.append(5) # O(1)
arr.insert(1, 7) # O(n)
arr.pop() # O(1)
print(arr)

# queue
queue = deque[Any]()
queue.append(1) # O(1)
queue.append(2)
queue.append(3)

queue.appendleft(-1) # O(1)
queue.appendleft(-2)
queue.appendleft(-3)

queue.pop() # O(1)
queue.popleft() # O(1)

print(queue)



