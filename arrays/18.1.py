# heaps

from heapq import heapify, heappop, heappush

arr0 = [5, 6, 9, 12, 3, 4]
heapify(arr0)
print(arr0)

arr1 = []
heappush(arr1, 5) # O(logn)
heappush(arr1, 6)
heappush(arr1, 9)
heappush(arr1, 12)
heappush(arr1, 3)
heappush(arr1, 4)
print(arr1)

heappop(arr1)
print(arr1)
heappop(arr1)
print(arr1)



