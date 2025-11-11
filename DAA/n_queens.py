import time
import tracemalloc


def compute_complexity(func, n):
    tracemalloc.start()
    t0 = time.perf_counter_ns()
    res, iterations = func(n)
    t1 = time.perf_counter_ns()

    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return res, iterations, (t1 - t0) / 1000, peak / 1024


def n_queens(n):
    solutions = []
    board = [-1] * n
    iterations = []
    itr = 0

    def backtrack(row, cols, diagonal1, diagonal2):
        nonlocal itr
        itr += 1
        if row == n:
            solutions.append(board[:])
            iterations.append(itr)
            return

        for col in range(n):
            itr += 1
            if col in cols or row + col in diagonal1 or row - col in diagonal2:
                continue

            board[row] = col
            cols.add(col)
            diagonal1.add(row + col)
            diagonal2.add(row - col)

            backtrack(row + 1, cols, diagonal1, diagonal2)

            cols.remove(col)
            diagonal1.remove(row + col)
            diagonal2.remove(row - col)

    backtrack(0, set(), set(), set())
    return solutions, iterations


def main():
    n = 5
    res, iterations, tc, sc = compute_complexity(n_queens, n)
    boards = []

    for solution in res:
        board = [[" " for _ in range(n)] for _ in range(n)]
        for i, place in enumerate(solution):
            board[i][place] = "Q"
        boards.append(board)

    print("Solutions:")
    for board in boards:
        for row in board:
            print("\t", row)
        print()

    print(
        f"\nAnalysis:\n{'Iterations':>17} = {iterations}\n{'Time Complexity':>17} = {tc} ms\n{'Space Complexity':>17} = {sc} KB"
    )


if __name__ == "__main__":
    main()
