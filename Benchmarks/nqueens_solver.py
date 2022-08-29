import sys


def is_safe(board, r, c):
    for i in range(r):
        if board[i][c] == 'Q':
            return False

    (i, j) = (r, c)
    while i >= 0 and j >= 0:
        if board[i][j] == 'Q':
            return False
        i = i - 1
        j = j - 1

    (i, j) = (r, c)
    while i >= 0 and j < len(board):
        if board[i][j] == 'Q':
            return False
        i = i - 1
        j = j + 1

    return True


def print_solution(board):
    for r in board:
        print(str(r).replace(',', '').replace('\'', ''))
    print()


def solve_nqueen(board, r):
    if r == len(board):
        # print_solution(board)
        return

    for i in range(len(board)):
        if is_safe(board, r, i):
            board[r][i] = 'Q'
            solve_nqueen(board, r + 1)
            board[r][i] = '–'


def main(N: int):
    print("test")
    board = [['–' for x in range(N)] for y in range(N)]
    solve_nqueen(board, 0)


if __name__ == '__main__':
    N = int(sys.argv[1])
    # main()
    for i in range(20):
        main(N)
