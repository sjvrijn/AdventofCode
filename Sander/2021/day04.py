import numpy as np
from more_itertools import chunked
import parse


def bingo(board):
    row_bingo = any(np.all(np.isnan(board), axis=1))
    column_bingo = any(np.all(np.isnan(board), axis=0))
    return row_bingo or column_bingo


def a(numbers, boards):
    for n in numbers:
        for board in boards:
            board[board == n] = np.nan
            if bingo(board):
                return int(np.nansum(board) * n)


def b(numbers, boards):
    num_boards = len(boards)
    bingo_boards = []
    for n in numbers:
        for board in boards:
            board[board == n] = np.nan
            if bingo(board):
                bingo_boards.append(board)
        boards = [b for b in boards if not bingo(b)]
        if len(bingo_boards) == num_boards:
            break
    return int(np.nansum(bingo_boards[-1])) * n


board_line = parse.compile('{:d} {:d} {:d} {:d} {:d}')
def parse_board(lines):
    return np.array([
        board_line.parse(line).fixed
        for line in lines
    ], dtype=float)


if __name__ == '__main__':
    files = [
        'input04-test1.txt',
        'input04.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            lines = f.read().splitlines()

        numbers = list(map(int, lines[0].split(',')))
        boards = [
            parse_board(chunk[1:])
            for chunk in chunked(lines[1:], 6)
        ]

        print(f'A: {a(numbers, boards)}')
        print(f'B: {b(numbers, boards)}')  # 16524 too high
