def second_largest(nums):
    """Return the second largest number in a list."""
    unique_nums = set(nums)
    sorted_nums = sorted(unique_nums, reverse=True)
    if len(sorted_nums) < 2:
        return None  # Return None if there is no second largest number
    return sorted_nums[1]

# Test the function
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]
result = second_largest(numbers)
print("The second largest number is:", result)