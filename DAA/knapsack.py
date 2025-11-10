import time
import tracemalloc


def compute_complexity(func, costs, weights, limit):
    tracemalloc.start()

    t0 = time.perf_counter_ns()
    res = func(costs, weights, limit)
    t1 = time.perf_counter_ns()

    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return res, (t1 - t0) / 1000, peak / 1024


def caculate_total_cost(items):
    return sum(c for c, _ in items)


def caculate_total_weight(items):
    return sum(w for _, w in items)


def knapsack_recursive(costs, weights, limit, n=None):
    if n is None:
        n = len(weights) - 1
    if limit == 0 or n < 0:
        return []
    if weights[n] > limit:
        return knapsack_recursive(costs, weights, limit, n - 1)

    include_items = knapsack_recursive(costs, weights, limit - weights[n], n - 1) + [
        (costs[n], weights[n])
    ]
    exclude_items = knapsack_recursive(costs, weights, limit, n - 1)

    return (
        include_items
        if caculate_total_cost(include_items) > caculate_total_cost(exclude_items)
        else exclude_items
    )


def knapsack_memoization(costs, weights, limit, n=None, memo=None):
    if n is None:
        n = len(weights) - 1
    if memo is None:
        memo = {}

    key = (n, limit)
    if key in memo:
        return memo[key]
    if limit == 0 or n < 0:
        memo[key] = []
        return memo[key]
    if weights[n] > limit:
        memo[key] = knapsack_memoization(costs, weights, limit, n - 1, memo)
        return memo[key]

    include_items = knapsack_memoization(
        costs, weights, limit - weights[n], n - 1, memo
    ) + [(costs[n], weights[n])]
    exclude_items = knapsack_memoization(costs, weights, limit, n - 1, memo)

    memo[key] = (
        include_items
        if caculate_total_cost(include_items) > caculate_total_cost(exclude_items)
        else exclude_items
    )
    return memo[key]


def knapsack_dp(costs, weights, limit):
    n = len(weights)
    dp = [0] * (limit + 1)
    keep = [[False] * (limit + 1) for _ in range(n)]

    for i in range(n):
        for w in range(limit, weights[i] - 1, -1):
            if dp[w - weights[i]] + costs[i] > dp[w]:
                dp[w] = dp[w - weights[i]] + costs[i]
                keep[i][w] = True

    w = limit
    selected_items = []
    for i in range(n - 1, -1, -1):
        if keep[i][w]:
            selected_items.append((costs[i], weights[i]))
            w -= weights[i]

    return selected_items[::-1]


def main():
    items_store = None
    limit = 100

    reversed_store = {weight: item for item, weight in items_store.items()}
    reversed_store = dict(sorted(reversed_store.items()))

    weights, costs = list(reversed_store.keys()), list(reversed_store.values())

    methods = [knapsack_recursive, knapsack_memoization, knapsack_dp]
    names = ["Recursive", "Memoization", "Dynamic Programming"]
    for n, f in zip(names, methods):
        res, tc, sc = compute_complexity(f, costs, weights, limit)

        profit = caculate_total_cost(res)
        total_weight = caculate_total_weight(res)
        print(
            f"{n:>20} : {res}\n{'Profit':>20} : ${profit}\n{'Weight':>20} : {total_weight} kg\n{'Time Complexity':>20} : {tc} ms\n{'Space Complexity':>20} : {sc} KB\n"
        )


if __name__ == "__main__":
    main()


"""
items_store = {
        10: 2,
        30: 3,
        60: 5,
        50: 6,
        80: 7,
        90: 8,
        100: 9,
        95: 10,
        110: 11,
        130: 12,
        125: 13,
        140: 14,
        150: 15,
        160: 16,
        175: 17,
        180: 18,
        190: 19,
        200: 20,
        210: 21,
        220: 22,
        230: 23,
        250: 24,
        260: 25,
        270: 26,
        290: 27,
        300: 28,
        310: 29,
        320: 30,
        330: 31,
        350: 32,
    }
"""
