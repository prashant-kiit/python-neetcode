# loop over arrays

# loop over single array
nums = [1, 2, 3]

for num in nums:
    print(num)

print('------')

for i in range(len(nums)):
    print(nums[i])

print('------')

for inum in enumerate(nums):
    print(inum)

print('-------')

for i, num in enumerate(nums):
    print(i, num)

print('------')

# loop over multiple array
nums1 = [1, 2, 3]
nums2 = [10, 20, 30]

for n1n2 in zip(nums1, nums2):
    print(n1n2)

print('------')

for n1, n2 in zip(nums1, nums2):
    print(n1, n2)
