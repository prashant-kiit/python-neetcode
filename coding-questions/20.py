def flatten(nums):
    flat_nums = []
    for num in nums:
        if isinstance(num, list):            
            flat_nums.extend(flatten(num))
        else:
            flat_nums.append(num)
    return flat_nums

print(flatten(
  [5, 1, [5, [5, 1, 8, 3, 8, 6], 8, [5, 1, 8, 3, 8, 6], 8, 6], 3, [5, 1, 8, [5, 1, 8, 3, 8, 6], 8, 6], 6]))

# [5, 1, 5, 5, 1, 8, 3, 8, 6, 8, 5, 1, 8, 3, 8, 6, 8, 6, 3, 5, 1, 8, 5, 1, 8, 3, 8, 6, 8, 6, 6]