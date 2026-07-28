def second_largest(nums):
    first =  second = float("-inf")
    
    for i in range(len(nums)):
        if nums[i] > first:
            second = first
            first = nums[i]
        if second < nums[i] < first:
            second = nums[i]

    return second
    
print(second_largest([5, 1, 8, 3, 8, 6]))