# ordered list using dict
# TC O(n) SC O(n)
# Still acquire move space due to order array that supports the hash table
def removeduplicates(arr):
    return list(dict.fromkeys(arr))

print(removeduplicates([3, 1, 2, 3, 1, 4, 2]))