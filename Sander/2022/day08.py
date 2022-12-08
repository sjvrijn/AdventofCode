from itertools import product
from pathlib import Path

import numpy as np


def a(trees):
    """Solve day 08 part 1"""
    is_visible = np.zeros(trees.shape, dtype=np.int8)

    for row_idx, row in enumerate(trees):
        # left-to-right
        cur_size = -1
        for col_idx, tree in enumerate(row):
            if tree > cur_size:
                is_visible[row_idx,col_idx] = 1
                cur_size = tree
            if cur_size == 9:
                break

        # right-to-left
        cur_size = -1
        for col_idx, tree in enumerate(row[::-1], start=1):
            if tree > cur_size:
                is_visible[row_idx,-col_idx] = 1
                cur_size = tree
            if cur_size == 9:
                break

    for col_idx, column in enumerate(trees.T):
        # left-to-right
        cur_size = -1
        for row_idx, tree in enumerate(column):
            if tree > cur_size:
                is_visible[row_idx, col_idx] = 1
                cur_size = tree
            if cur_size == 9:
                break

        # right-to-left
        cur_size = -1
        for row_idx, tree in enumerate(column[::-1], start=1):
            if tree > cur_size:
                is_visible[-row_idx,col_idx] = 1
                cur_size = tree
            if cur_size == 9:
                break

    return np.sum(is_visible)


def b(trees):
    """Solve day 08 part 2"""
    view_distances = np.zeros((*trees.shape, 4), dtype=int)

    nrows, ncols = trees.shape
    for x, y in product(range(nrows), range(ncols)):
        max_size = trees[x,y]

        # up
        view_dist = 0
        for new_x in range(x-1, -1, -1):
            view_dist += 1
            if trees[new_x,y] >= max_size:
                break
        view_distances[x, y, 0] = view_dist

        # down
        view_dist = 0
        for new_x in range(x+1, ncols):
            view_dist += 1
            if trees[new_x,y] >= max_size:
                break
        view_distances[x, y, 3] = view_dist

        # west
        view_dist = 0
        for new_y in range(y-1, -1, -1):
            view_dist += 1
            if trees[x,new_y] >= max_size:
                break
        view_distances[x, y, 1] = view_dist

        # east
        view_dist = 0
        for new_y in range(y+1, nrows):
            view_dist += 1
            if trees[x,new_y] >= max_size:
                break
        view_distances[x, y, 2] = view_dist

    return np.max(np.product(view_distances, axis=2))


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = f.read_text().splitlines()
    return np.array([
        list(map(int, line))
        for line in lines
    ])


def main():
    """Main function to wrap variables"""
    files = [
        'input08-test1.txt',
        'input08.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
