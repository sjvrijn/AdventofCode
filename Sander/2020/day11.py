from itertools import product
import numpy as np



def update_cell(neighborhood):
    center = neighborhood[1, 1]
    if center < 0:
        return -1
    if center == 0:
        return 1 if np.sum(neighborhood == 1) == 0 else 0
    return 0 if np.sum(neighborhood == 1) >= 5 else 1


def step_grid(grid):
    temp_grid = np.copy(grid)
    rows, cols = grid.shape
    for row, col in product(range(1, rows-1), range(1, cols-1)):
        temp_grid[row, col] = update_cell(grid[row-1:row+2,col-1:col+2])
    return temp_grid


def hash_grid(grid):
    return ''.join(map(str, grid.flatten()))


def a(grid):
    states, grid_hash = set(), hash_grid(grid)
    while grid_hash not in states:
        states.add(grid_hash)
        grid = step_grid(grid)
        grid_hash = hash_grid(grid)

    return np.sum(grid == 1)


def b(grid):
    return ...


def lines_to_grid(lines):

    grid = np.full((len(lines)+2, len(lines[0])+2), -1)
    for row, line in enumerate(lines, start=1):
        grid[row,1:-1] = eval(line.replace('L', '0,').replace('.', '-1,'))
    return grid


if __name__ == '__main__':
    with open('input11.txt') as f:
        grid = lines_to_grid([line.strip() for line in f])

    print(a(grid))
    print(b(grid))
