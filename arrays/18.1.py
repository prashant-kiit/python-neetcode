# heaps

from heapq import heapify, heappop, heappush

arr0 = [5, 6, 9, 12, 3, 4]
heapify(arr0) # O(n)
print(arr0)

arr1 = []
heappush(arr1, 5) # O(logn)
heappush(arr1, 6)
heappush(arr1, 9)
heappush(arr1, 12)
heappush(arr1, 3)
heappush(arr1, 4)
print(arr1)

heappop(arr1) # O(logn)
print(arr1) # O(n)
heappop(arr1)
print(arr1)

# heapsort is O(nlogn)

# | Operation                    | Time Complexity | Reason                                                |
# | ---------------------------- | --------------- | ----------------------------------------------------- |
# | Peek (get min/max)           | **O(1)**        | Root element is directly accessible.                  |
# | Insert                       | **O(log n)**    | Element may bubble up through the height of the heap. |
# | Extract Min/Max              | **O(log n)**    | Root is removed and heapified down.                   |
# | Delete arbitrary element     | **O(log n)**    | Replace with last element, then heapify up/down.      |
# | Increase/Decrease Key        | **O(log n)**    | Requires heapify up or down.                          |
# | Build Heap (from array)      | **O(n)**        | Bottom-up heapify, not O(n log n).                    |
# | Heapify (single node)        | **O(log n)**    | Traverses at most the height of the heap.             |
# | Search for arbitrary element | **O(n)**        | Heap is only partially ordered, not fully sorted.     |




