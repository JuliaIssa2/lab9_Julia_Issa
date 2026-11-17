import statistics
import time

from profiler import fast_function, memory_intensive_function
from profiler_optimized import (
    optimized_fast_function,
    optimized_memory_intensive_function,
)


def time_repeated(function, calls):
    """Time repeated calls and return the last result for a correctness check."""
    start = time.perf_counter()
    for _ in range(calls):
        result = function()
    elapsed = time.perf_counter() - start
    return elapsed, result


def compare_functions(label, original, optimized, original_calls, optimized_calls, trials):
    """Compare median seconds per call without profiling instrumentation."""
    original_times = []
    optimized_times = []
    expected = None
    for trial in range(trials):
        # Alternate order to reduce the effect of warming and background activity.
        measurements = [
            (original, original_calls, original_times),
            (optimized, optimized_calls, optimized_times),
        ]
        if trial % 2:
            measurements.reverse()

        trial_results = []
        for function, calls, times in measurements:
            elapsed, result = time_repeated(function, calls)
            trial_results.append(result)
            times.append(elapsed / calls)

        if trial_results[0] != trial_results[1]:
            raise ValueError(f"{label}: original and optimized results differ")
        if expected is None:
            expected = trial_results[0]
        elif trial_results[0] != expected:
            raise ValueError(f"{label}: a trial returned a different result")

    original_median = statistics.median(original_times)
    optimized_median = statistics.median(optimized_times)
    speedup = original_median / optimized_median

    print(f"{label}:")
    print(f"  Equal result: {expected}")
    print(f"  Original median: {original_median:.9f} s/call "
          f"({original_calls} calls/trial, {trials} trials)")
    print(f"  Optimized median: {optimized_median:.9f} s/call "
          f"({optimized_calls} calls/trial, {trials} trials)")
    print(f"  Speedup: {speedup:.2f}x")


def main():
    compare_functions(
        "fast_function",
        fast_function,
        optimized_fast_function,
        original_calls=50000,
        optimized_calls=50000,
        trials=5,
    )
    compare_functions(
        "memory_intensive_function",
        memory_intensive_function,
        optimized_memory_intensive_function,
        original_calls=1,
        optimized_calls=100000,
        trials=3,
    )
    print("cProfile and line_profiler add overhead; interpret their timings separately.")


if __name__ == '__main__':
    main()
