# min heapify method

def heapify(arr):
    n = len(arr)

    def sift_down(i):
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and arr[left] < arr[smallest]:
                smallest = left

            if right < n and arr[right] < arr[smallest]:
                smallest = right

            if smallest == i:
                break

            arr[i], arr[smallest] = arr[smallest], arr[i]
            i = smallest

    # Start from last non-leaf node
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i)
