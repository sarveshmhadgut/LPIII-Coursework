import time
import tracemalloc


def timed_peak(func, n):
    tracemalloc.start()

    t0 = time.perf_counter_ns()
    res = func(n)
    t1 = time.perf_counter_ns()

    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return res, (t1 - t0) / 1000, peak / 1024


def fib_iterative(n):
    iterations = 0

    if n <= 2:
        iterations += 1
        return n - 1, iterations

    prev, curr = 0, 1
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr
        iterations += 1

    return curr, iterations


def fib_recursive(n, calls=None):
    if calls is None:
        calls = 0
    calls += 1

    if n <= 2:
        return n - 1, calls
    val1, c1 = fib_recursive(n - 1, calls)
    val2, c2 = fib_recursive(n - 2, c1)

    return val1 + val2, c2


def fib_memoization(n, calls=None, memo=None):
    if calls is None:
        calls = 0
    if memo is None:
        memo = {}
    calls += 1

    if n <= 2:
        memo[n] = n - 1
        return memo[n], calls
    if n in memo:
        return memo[n], calls

    val1, c1 = fib_memoization(n - 1, calls, memo)
    val2, c2 = fib_memoization(n - 2, calls, memo)

    memo[n] = val1 + val2
    return memo[n], c1 + c2


def main():
    for n in [1, 2, 3, 4, 5, 10, 20, 30, 35]:
        print()
        for fn in (fib_recursive, fib_memoization, fib_iterative):
            (value, count), avg_time, peak = timed_peak(fn, n)
            name = f"{fn.__name__[4:].title()}({n})"
            print(
                f"{name:>15} = {value:<10} {'Iterations':>10} = {count:<10} {'time(ms)':>10} ≈ {avg_time:<10} {'peak(KB)':>10} ≈ {peak:<10}"
            )


if __name__ == "__main__":
    main()
