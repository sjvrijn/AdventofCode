from itertools import product

import numpy as np


def a(grid):
    return int(sum(
        grid[point] + 1
        for point in product(range(1, grid.shape[0]-1), range(1, grid.shape[1]-1))
        if is_lowest(grid, point)
    ))


def b(grid):
    low_points = [
        point
        for point in product(range(1, grid.shape[0]-1), range(1, grid.shape[1]-1))
        if is_lowest(grid, point)
    ]

    basin_sizes = []
    for low_point in low_points:
        to_process = [low_point]
        basin = set()
        while to_process:
            point = to_process.pop(0)
            for neighbor in neighbors(point):
                if neighbor not in basin and grid[neighbor] < 9:
                    basin.add(neighbor)
                    to_process.append(neighbor)
        basin_sizes.append(len(basin))

    x, y, z = sorted(basin_sizes)[-3:]
    return x*y*z


def is_lowest(grid, point):
    return all(
        grid[neighbor] > grid[point]
        for neighbor in neighbors(point)
    )


def neighbors(point):
    x, y = point
    return (x+1, y), (x-1, y), (x, y+1), (x, y-1)


if __name__ == '__main__':
    files = [
        'input09-test1.txt',
        'input09.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            input_grid = [
                [int(height) for height in line]
                for line in f.read().splitlines()
            ]

        grid = np.full((len(input_grid)+2, len(input_grid[0])+2), np.inf)
        grid[1:-1, 1:-1] = input_grid

        print(f'A: {a(grid)}')
        print(f'B: {b(grid)}')
