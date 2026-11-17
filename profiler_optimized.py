import time


def slow_function():
    time.sleep(2)
    total = 0
    for i in range(10000):
        total += i ** 2
    return total


def optimized_fast_function():
    count = 100
    # Sum i squared for i from 0 through count - 1.
    return count * (count - 1) * (2 * count - 1) // 6


def optimized_memory_intensive_function():
    count = 10000000
    # The same formula avoids building or iterating over a large range.
    return count * (count - 1) * (2 * count - 1) // 6


def main():
    slow_function()
    optimized_fast_function()
    optimized_memory_intensive_function()


if __name__ == '__main__':
    main()
