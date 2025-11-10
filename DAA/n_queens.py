def n_queens(n):
    solutions = []
    board = [-1] * n

    def backtrack(row, cols, diagonal1, diagonal2):
        if row == n:
            solutions.append(board[:])
            return

        for col in range(n):
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
    return solutions


def main():
    n = 5
    a = n_queens(n)
    boards = []

    for solution in a:
        board = [[" " for _ in range(n)] for _ in range(n)]
        for i, place in enumerate(solution):
            board[i][place] = "Q"
        boards.append(board)

    for board in boards:
        for row in board:
            print(row)
        print()


if __name__ == "__main__":
    main()
