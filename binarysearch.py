def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    iterations = 0

    while low <= high:
        iterations += 1
        mid = (high + low) // 2

        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return iterations, arr[mid]

    # If the element is not found, return the number of iterations and the upper bound
    if low < len(arr):
        upper_bound = arr[low]
        return iterations, upper_bound
    else:
        # If x is greater than all elements, return the number of iterations and None
        return iterations, None


sorted_array = [1.2, 2.4, 3.6, 4.8, 6.0, 7.2, 8.4, 9.6]
search_value = 6.2

result = binary_search(sorted_array, search_value)
print(result)
print(f"Number of iterations: {result[0]}, Upper bound: {result[1]}")