from itertools import product
import numpy as np


directions = np.array([
    [-1, -1],  # NW
    [-1,  0],  # N
    [-1,  1],  # NE
    [ 0,  1],  # E
    [ 1,  1],  # SE
    [ 1,  0],  # S
    [ 1, -1],  # SW
    [ 0, -1],  # W
])



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


def update_longrange_cell(grid, row, col):
    center = grid[row, col]
    if center < 0:
        return -1
    num_occupied = 0
    for direction in directions:
        distance, neighbor = 0, -1
        while neighbor == -1:
            distance += 1
            drow, dcol = direction * distance
            if row+drow < 0 or col+dcol < 0:
                neighbor = -1
                break

            try:
                neighbor = grid[row+drow, col+dcol]
            except IndexError:
                neighbor = -1
                break
        num_occupied += int(neighbor == 1)

    if center == 0:
        return num_occupied == 0
    if center == 1:
        return num_occupied <= 4


def step_longrange_grid(grid):
    temp_grid = np.copy(grid)
    rows, cols = grid.shape
    for row, col in product(range(1, rows - 1), range(1, cols - 1)):
        temp_grid[row, col] = update_longrange_cell(grid, row, col)
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
    states, grid_hash = set(), hash_grid(grid)
    while grid_hash not in states:
        states.add(grid_hash)
        grid = step_longrange_grid(grid)
        grid_hash = hash_grid(grid)

    return np.sum(grid == 1)


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
