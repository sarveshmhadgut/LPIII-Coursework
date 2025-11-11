import time
from numpy import mean
import random
import tracemalloc


def compute_complexity(func, arr):
    tracemalloc.start()
    t0 = time.perf_counter_ns()

    res, count = func(arr)

    t1 = time.perf_counter_ns()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return res, count, (t1 - t0) / 1000, peak / 1024


def deterministic_quicksort(arr):
    def helper(arr):
        count = 1
        if len(arr) <= 1:
            return arr, count

        n = len(arr)
        pivot = arr[-1]
        low, high = [], []

        for i in range(n - 1):
            count += 1
            if arr[i] <= pivot:
                low.append(arr[i])
            else:
                high.append(arr[i])

        lower, c1 = helper(low)
        higher, c2 = helper(high)
        return lower + [pivot] + higher, count + c1 + c2

    return helper(arr)


def randomized_quicksort(arr):
    def helper(arr):
        count = 1
        if len(arr) <= 1:
            return arr, count

        n = len(arr)
        pivot_idx = random.randint(0, n - 1)
        pivot = arr[pivot_idx]
        low, high = [], []

        for i in range(n):
            count += 1
            if i == pivot_idx:
                continue

            if arr[i] <= pivot:
                low.append(arr[i])
            else:
                high.append(arr[i])

        lower, c1 = helper(low)
        higher, c2 = helper(high)

        return lower + [pivot] + higher, count + c1 + c2

    return helper(arr)


def simulate(arr):
    res_deterministic, res_random = set(), set()
    count_deterministic, count_random = [], []
    tc_deterministic, tc_random = [], []
    sc_deterministic, sc_random = [], []

    for _ in range(10):
        dres, dcount, dtc, dsc = compute_complexity(deterministic_quicksort, arr)
        rres, rcount, rtc, rsc = compute_complexity(randomized_quicksort, arr)

        res_deterministic.add(tuple(dres))
        res_random.add(tuple(rres))

        count_deterministic.append(dcount)
        count_random.append(rcount)

        tc_deterministic.append(dtc)
        tc_random.append(rtc)

        sc_deterministic.append(dsc)
        sc_random.append(rsc)

    print(
        f"{'Deterministic Quicksort on':>27} {arr}\n{'Sorted arrays':>25} = {list(res_deterministic)[0]}\n{'Iterations':>25} = {count_deterministic} (Mean = {round(mean(count_deterministic), 2)})\n{'Time Complexities':>25} = {tc_deterministic} (Mean = {round(mean(tc_deterministic), 2)} ms)\n{'Space Complexities':>25} = {round(mean(sc_deterministic), 2)} (Mean = {mean(sc_deterministic)} KB)"
    )

    print(
        f"\n{'Randomized Quicksort on':>27} {arr}\n{'Sorted arrays':>25} = {list(res_random)[0]}\n{'Iterations':>25} = {count_random} (Mean = {round(mean(count_random), 2)})\n{'Time Complexities':>25} = {tc_random} (Mean = {round(mean(tc_random))} ms)\n{'Space Complexities':>25} = {sc_random} (Mean = {round(mean(sc_random))} KB)\n"
    )


def main():
    arr = [1, 10, 4, 5, 3, 4, 6, 8, 1, 10]
    arr2 = list(range(10))

    simulate(arr=arr)
    simulate(arr=arr2)


if __name__ == "__main__":
    main()
