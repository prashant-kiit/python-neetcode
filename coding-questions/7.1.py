# unordered using sets
# TC O(n) SC O(n)
# Still acquire less space as no order array that supports the hash table
def removeduplicates(arr):
    return list(set(arr))

print(removeduplicates([3, 1, 2, 3, 1, 4, 2]))