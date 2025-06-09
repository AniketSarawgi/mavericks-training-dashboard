"""
Sample coding challenge solution for testing the Assessment Agent
Problem: Implement a function to find the maximum sum of a contiguous subarray (Kadane's Algorithm)
"""


def max_subarray_sum(arr):
    """
    Find the maximum sum of a contiguous subarray using Kadane's algorithm.
    
    Args:
        arr (list): List of integers
    
    Returns:
        int: Maximum sum of contiguous subarray
    """
    if not arr:
        return 0

    max_sum = current_sum = arr[0]

    # Iterate through the array starting from the second element
    for i in range(1, len(arr)):
        # Either extend the existing subarray or start a new one
        current_sum = max(arr[i], current_sum + arr[i])
        # Update the maximum sum found so far
        max_sum = max(max_sum, current_sum)

    return max_sum


def test_max_subarray_sum():
    """Test cases for the max_subarray_sum function"""

    # Test case 1: Mixed positive and negative numbers
    test1 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    result1 = max_subarray_sum(test1)
    expected1 = 6  # [4, -1, 2, 1]
    assert result1 == expected1, (f"Test 1 failed: expected {expected1}, "
                                  f"got {result1}")

    # Test case 2: All negative numbers
    test2 = [-2, -3, -1, -5]
    result2 = max_subarray_sum(test2)
    expected2 = -1  # Single element -1
    assert result2 == expected2, (f"Test 2 failed: expected {expected2}, "
                                  f"got {result2}")

    # Test case 3: All positive numbers
    test3 = [1, 2, 3, 4, 5]
    result3 = max_subarray_sum(test3)
    expected3 = 15  # Sum of all elements
    assert result3 == expected3, (f"Test 3 failed: expected {expected3}, "
                                  f"got {result3}")

    print("✅ All test cases passed!")


if __name__ == "__main__":
    # Run test cases
    test_max_subarray_sum()

    # Example usage
    example_array = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    result = max_subarray_sum(example_array)
    print(f"Maximum subarray sum for {example_array} is: {result}")
