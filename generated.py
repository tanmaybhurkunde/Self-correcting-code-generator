def second_largest(numbers):
    """
    Returns the second largest number in a list.
    
    Args:
        numbers (list): A list of integers.
    
    Returns:
        int: The second largest number in the list.
    """
    # Remove duplicates by converting the list to a set
    unique_numbers = set(numbers)
    
    # Check if the list has at least two unique elements
    if len(unique_numbers) < 2:
        return None
    
    # Sort the unique numbers in descending order
    sorted_numbers = sorted(unique_numbers, reverse=True)
    
    # Return the second largest number
    return sorted_numbers[1]

# Test the function
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]
result = second_largest(numbers)
print("The second largest number is:", result)