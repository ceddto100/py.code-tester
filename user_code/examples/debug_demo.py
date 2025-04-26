"""
Debug Demo Script
---------------
This script intentionally contains errors to demonstrate debugging features.
"""

def calculate_factorial(n):
    """Calculate the factorial of a number."""
    if n < 0:
        raise ValueError("Input must be non-negative")
    
    if n == 0:
        return 1
    
    # Intentional error: forgot to return n * factorial of (n-1)
    calculate_factorial(n - 1)

def divide_numbers(a, b):
    """Divide a by b."""
    # Intentional error: no check for division by zero
    return a / b

def process_list(items):
    """Process each item in a list."""
    result = []
    # Intentional error: using range(1, len(items)) skips the first item
    for i in range(1, len(items)):
        result.append(items[i] * 2)
    return result

def access_dictionary(data, key):
    """Access a value in a dictionary using the given key."""
    # Intentional error: direct access without checking if key exists
    return data[key]

def main():
    print("Debug Demo Started")
    
    # Example 1: Factorial calculation (recursion error)
    try:
        print("\nCalculating factorial of 5:")
        result = calculate_factorial(5)
        print(f"Factorial: {result}")
    except Exception as e:
        print(f"Error in factorial calculation: {e}")
    
    # Example 2: Division by zero
    try:
        print("\nDividing 10 by 0:")
        result = divide_numbers(10, 0)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error in division: {e}")
    
    # Example 3: Off-by-one error in list processing
    try:
        print("\nProcessing list [1, 2, 3, 4, 5]:")
        numbers = [1, 2, 3, 4, 5]
        result = process_list(numbers)
        print(f"Processed list: {result}")
        print(f"Notice that the first item (1) is missing from the result!")
    except Exception as e:
        print(f"Error in list processing: {e}")
    
    # Example 4: KeyError in dictionary
    try:
        print("\nAccessing dictionary value:")
        data = {"name": "John", "age": 30}
        print(f"Dictionary: {data}")
        result = access_dictionary(data, "email")
        print(f"Email: {result}")
    except Exception as e:
        print(f"Error in dictionary access: {e}")
    
    # Example 5: Name error (undefined variable)
    try:
        print("\nTrying to use undefined variable:")
        # Intentional error: undefined_variable is not defined
        print(f"Value: {undefined_variable}")
    except Exception as e:
        print(f"Error with undefined variable: {e}")
    
    # Example 6: Type error
    try:
        print("\nAdding number and string:")
        # Intentional error: adding int and str
        result = 42 + "hello"
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error in addition operation: {e}")
    
    print("\nDebug Demo Completed")

if __name__ == "__main__":
    main() 