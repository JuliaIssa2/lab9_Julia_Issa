import time
import unittest

import memory_profiler

from profiler import fast_function, memory_intensive_function, slow_function


def sum_of_squares(count):
    """Return the sum of i squared for i in range(count)."""
    return count * (count - 1) * (2 * count - 1) // 6


class TestProfiler(unittest.TestCase):
    def time_function(self, function):
        """Return a function's result and its elapsed time in seconds."""
        start = time.perf_counter()
        result = function()
        duration = time.perf_counter() - start
        return result, duration

    def test_slow_function(self):
        result, duration = self.time_function(slow_function)
        print(f"slow_function executed in {duration:.2f} seconds.")
        self.assertEqual(result, sum_of_squares(10000))
        self.assertGreaterEqual(duration, 1.95)

    def test_fast_function(self):
        result, duration = self.time_function(fast_function)
        print(f"fast_function executed in {duration:.2f} seconds.")
        self.assertEqual(result, sum_of_squares(100))

    def test_memory_intensive_function(self):
        memory_before = memory_profiler.memory_usage()[0]
        result, duration = self.time_function(memory_intensive_function)
        memory_after = memory_profiler.memory_usage()[0]

        print(f"memory_intensive_function executed in {duration:.2f} seconds.")
        print(f"Memory usage before: {memory_before:.2f} MiB")
        print(f"Memory usage after: {memory_after:.2f} MiB")
        self.assertEqual(result, sum_of_squares(10000000))


if __name__ == '__main__':
    unittest.main()
