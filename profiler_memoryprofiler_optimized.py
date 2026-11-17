import time

import psutil
from memory_profiler import memory_usage, profile


@profile
def slow_function():
    time.sleep(2)
    total = 0
    for i in range(10000):
        total += i ** 2
    return total


@profile
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

    process = psutil.Process()
    baseline_rss_mib = process.memory_info().rss / (1024 ** 2)
    peak_memory_mib, result = memory_usage(
        (optimized_memory_intensive_function, (), {}),
        interval=0.1,
        max_usage=True,
        retval=True,
        max_iterations=1,
    )
    after_rss_mib = process.memory_info().rss / (1024 ** 2)

    print(f"Baseline process RSS: {baseline_rss_mib:.2f} MiB")
    print(f"Sampled peak during memory_intensive_function: {peak_memory_mib:.2f} MiB")
    print(f"Process RSS after execution: {after_rss_mib:.2f} MiB")
    print(f"memory_intensive_function returned: {result}")


if __name__ == '__main__':
    main()
