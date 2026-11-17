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
def fast_function():
    total = 0
    for i in range(100):
        total += i ** 2
    return total


def memory_intensive_function():
    total = 0
    for i in range(10000000):
        total += i ** 2
    return total


def main():
    slow_function()
    fast_function()

    process = psutil.Process()
    baseline_rss_mib = process.memory_info().rss / (1024 ** 2)
    peak_memory_mib, result = memory_usage(
        (memory_intensive_function, (), {}),
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
