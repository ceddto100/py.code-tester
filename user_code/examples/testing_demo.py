"""
Sample Testing Script
-------------------
This script demonstrates unit testing with pytest.
"""
import pytest
import numpy as np

# Function to test: calculate statistics for a list of numbers
def calculate_stats(numbers):
    """
    Calculate basic statistics for a list of numbers.
    
    Args:
        numbers: List or array of numeric values
        
    Returns:
        dict: Dictionary containing mean, median, std_dev, min, and max
    """
    if not numbers:
        raise ValueError("Input list cannot be empty")
    
    numbers = np.array(numbers)
    
    return {
        'mean': float(np.mean(numbers)),
        'median': float(np.median(numbers)),
        'std_dev': float(np.std(numbers)),
        'min': float(np.min(numbers)),
        'max': float(np.max(numbers))
    }

# Function to test: classify a number based on its value
def classify_number(num):
    """
    Classify a number as 'negative', 'zero', or 'positive'.
    
    Args:
        num: A numeric value
        
    Returns:
        str: Classification as 'negative', 'zero', or 'positive'
    """
    if not isinstance(num, (int, float)):
        raise TypeError("Input must be a number")
    
    if num < 0:
        return 'negative'
    elif num == 0:
        return 'zero'
    else:
        return 'positive'

# Function to test: filter a list by removing elements that don't meet criteria
def filter_numbers(numbers, min_val=None, max_val=None):
    """
    Filter a list of numbers to only include values within specified range.
    
    Args:
        numbers: List of numeric values
        min_val: Minimum value to include (inclusive)
        max_val: Maximum value to include (inclusive)
        
    Returns:
        list: Filtered list of numbers
    """
    if not isinstance(numbers, (list, tuple, np.ndarray)):
        raise TypeError("Input must be a list or array")
    
    result = []
    for num in numbers:
        if not isinstance(num, (int, float)):
            continue
        
        if min_val is not None and num < min_val:
            continue
        if max_val is not None and num > max_val:
            continue
        
        result.append(num)
    
    return result

# Tests for calculate_stats function
def test_calculate_stats_basic():
    """Test basic functionality of calculate_stats"""
    result = calculate_stats([1, 2, 3, 4, 5])
    
    assert result['mean'] == 3.0
    assert result['median'] == 3.0
    assert pytest.approx(result['std_dev']) == 1.4142135623730951
    assert result['min'] == 1.0
    assert result['max'] == 5.0

def test_calculate_stats_empty():
    """Test calculate_stats with empty input"""
    with pytest.raises(ValueError):
        calculate_stats([])

def test_calculate_stats_single_value():
    """Test calculate_stats with a single value"""
    result = calculate_stats([42])
    
    assert result['mean'] == 42.0
    assert result['median'] == 42.0
    assert result['std_dev'] == 0.0
    assert result['min'] == 42.0
    assert result['max'] == 42.0

# Tests for classify_number function
def test_classify_number_positive():
    """Test classify_number with positive input"""
    assert classify_number(5) == 'positive'
    assert classify_number(0.1) == 'positive'

def test_classify_number_zero():
    """Test classify_number with zero input"""
    assert classify_number(0) == 'zero'
    assert classify_number(0.0) == 'zero'

def test_classify_number_negative():
    """Test classify_number with negative input"""
    assert classify_number(-5) == 'negative'
    assert classify_number(-0.1) == 'negative'

def test_classify_number_invalid():
    """Test classify_number with invalid input"""
    with pytest.raises(TypeError):
        classify_number("not a number")

# Tests for filter_numbers function
def test_filter_numbers_no_constraints():
    """Test filter_numbers with no min/max constraints"""
    numbers = [1, 2, 3, 4, 5]
    assert filter_numbers(numbers) == numbers

def test_filter_numbers_min_only():
    """Test filter_numbers with only min constraint"""
    assert filter_numbers([1, 2, 3, 4, 5], min_val=3) == [3, 4, 5]

def test_filter_numbers_max_only():
    """Test filter_numbers with only max constraint"""
    assert filter_numbers([1, 2, 3, 4, 5], max_val=3) == [1, 2, 3]

def test_filter_numbers_min_and_max():
    """Test filter_numbers with both min and max constraints"""
    assert filter_numbers([1, 2, 3, 4, 5], min_val=2, max_val=4) == [2, 3, 4]

def test_filter_numbers_invalid_elements():
    """Test filter_numbers with invalid elements in the list"""
    assert filter_numbers([1, "two", 3, None, 5]) == [1, 3, 5]

def test_filter_numbers_invalid_input():
    """Test filter_numbers with invalid input"""
    with pytest.raises(TypeError):
        filter_numbers("not a list")

# Run the tests (only when this file is executed directly)
if __name__ == "__main__":
    print("Running tests...")
    # Run the tests
    pytest.main(["-v", __file__])
    
    # Also demonstrate the functions with examples
    print("\nFunction Examples:")
    
    # Example 1: calculate_stats
    sample_data = [12, 18, 23, 7, 15, 10, 8, 19]
    print(f"\nSample data: {sample_data}")
    stats = calculate_stats(sample_data)
    print("Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Example 2: classify_number
    numbers_to_classify = [-10, 0, 42]
    print("\nClassifying numbers:")
    for num in numbers_to_classify:
        classification = classify_number(num)
        print(f"  {num} is {classification}")
    
    # Example 3: filter_numbers
    mixed_data = [5, -3, 10, 0, 8, -1, 12]
    print(f"\nOriginal data: {mixed_data}")
    filtered_positive = filter_numbers(mixed_data, min_val=0)
    print(f"Positive numbers only: {filtered_positive}")
    filtered_range = filter_numbers(mixed_data, min_val=-2, max_val=10)
    print(f"Numbers between -2 and 10: {filtered_range}")
    
    print("\nTesting complete!") 