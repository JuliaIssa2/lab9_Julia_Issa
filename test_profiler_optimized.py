import time
import unittest

from profiler import (
    fast_function,
    memory_intensive_function,
    slow_function as original_slow_function,
)
from profiler_optimized import (
    optimized_fast_function,
    optimized_memory_intensive_function,
    slow_function as optimized_slow_function,
)


def sum_of_squares(count):
    return count * (count - 1) * (2 * count - 1) // 6


class TestOptimizedProfiler(unittest.TestCase):
    def time_function(self, function):
        start = time.perf_counter()
        result = function()
        duration = time.perf_counter() - start
        return result, duration

    def time_repeated_function(self, function, calls):
        start = time.perf_counter()
        for _ in range(calls):
            result = function()
        seconds_per_call = (time.perf_counter() - start) / calls
        return result, seconds_per_call

    def test_slow_function(self):
        original, original_seconds = self.time_function(original_slow_function)
        optimized, optimized_seconds = self.time_function(optimized_slow_function)

        self.assertEqual(optimized, sum_of_squares(10000))
        self.assertEqual(optimized, original)
        print(f"Original slow_function: {original_seconds:.3f} s")
        print(f"Optimized slow_function: {optimized_seconds:.3f} s")

    def test_fast_function(self):
        calls = 10000
        original, original_seconds = self.time_repeated_function(fast_function, calls)
        optimized, optimized_seconds = self.time_repeated_function(
            optimized_fast_function, calls
        )

        self.assertEqual(optimized, sum_of_squares(100))
        self.assertEqual(optimized, original)
        print(f"Original fast_function: {original_seconds * 1e6:.3f} us/call")
        print(f"Optimized fast_function: {optimized_seconds * 1e6:.3f} us/call")

    def test_memory_intensive_function(self):
        # Run the costly original function once in this test.
        original, original_seconds = self.time_function(memory_intensive_function)
        optimized, optimized_seconds = self.time_function(
            optimized_memory_intensive_function
        )

        self.assertEqual(optimized, sum_of_squares(10000000))
        self.assertEqual(optimized, original)
        print(f"Original memory_intensive_function: {original_seconds:.3f} s")
        print(f"Optimized memory_intensive_function: {optimized_seconds:.6f} s")


if __name__ == '__main__':
    unittest.main()
