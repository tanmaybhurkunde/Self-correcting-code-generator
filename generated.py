def second_largest(numbers):
    """
    Returns the second largest number in a list.

    Args:
        numbers (list): A list of numbers.

    Returns:
        int: The second largest number in the list.
    """
    if len(set(numbers)) < 2:
        return None  # If there's only one unique number, return None
    
    return sorted(set(numbers), reverse=True)[1]


# Test the function
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]
result = second_largest(numbers)
print("The second largest number is:", result)