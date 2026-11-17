from line_profiler import LineProfiler

from profiler_optimized import (
    main,
    optimized_fast_function,
    optimized_memory_intensive_function,
    slow_function,
)


def profile_main():
    profiler = LineProfiler()
    profiler.add_function(slow_function)
    profiler.add_function(optimized_fast_function)
    profiler.add_function(optimized_memory_intensive_function)
    profiler.runcall(main)
    profiler.print_stats()


if __name__ == '__main__':
    profile_main()
