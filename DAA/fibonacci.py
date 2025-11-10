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
    for _ in range(2, n):
        prev, curr = curr, prev + curr
        iterations += 1

    return curr, iterations


def fib_recursive(n, calls=0):
    calls += 1

    if n <= 2:
        return n - 1, calls
    val1, c1 = fib_recursive(n - 1, calls)
    val2, c2 = fib_recursive(n - 2, c1)

    return val1 + val2, c2


def fib_memo(n):
    def helper(k, counter, memo):
        counter[0] += 1
        if k <= 2:
            return k - 1
        if k in memo:
            return memo[k]
        memo[k] = helper(k - 1, counter, memo) + helper(k - 2, counter, memo)
        return memo[k]

    counter = [0]
    res = helper(n, counter, {1: 0, 2: 1})
    return res, counter[0]


def main():
    for n in [1, 5, 10, 20, 30, 35]:
        print()
        for fn in (fib_iterative, fib_recursive, fib_memo):
            (value, count), avg_time, peak = timed_peak(fn, n)
            name = f"{fn.__name__[4:].title()}({n})"
            print(
                f"{name:>13} = {value:<10} {'Iterations':>10} = {count:<10} {'time(ms)':>10} ≈ {avg_time:<10} {'peak(KB)':>10} ≈ {peak:<10}"
            )


if __name__ == "__main__":
    main()
