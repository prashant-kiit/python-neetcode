# various operation on array

nums = [1, 2, 3]

# reverse
nums.reverse()
print(nums)

# sort
nums.sort()
print(nums)

nums.sort(reverse=True)
print(nums)

# sorting chars and strings
lines = ['U am going.', 'I am staying.', 'Are we playing?'] 

lines.sort() # unicode based sorting
print(lines)

# custom sort using key
lines.sort(key=lambda x: len(x))
print(lines)