def second_largest(numbers):
    """
    Returns the second largest number in a list of numbers.

    Args:
        numbers (list): A list of numbers.

    Returns:
        int: The second largest number in the list.

    Raises:
        ValueError: If the list has less than two unique numbers.
    """
    # Remove duplicates by converting the list to a set
    unique_numbers = set(numbers)
    
    # Check if the list has less than two unique numbers
    if len(unique_numbers) < 2:
        raise ValueError("The list must have at least two unique numbers.")
    
    # Sort the unique numbers in descending order
    sorted_unique_numbers = sorted(unique_numbers, reverse=True)
    
    # Return the second largest number
    return sorted_unique_numbers[1]

# Example usage
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]
print(second_largest(numbers))