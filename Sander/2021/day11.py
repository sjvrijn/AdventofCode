from itertools import product, count

import numpy as np


def a(grid):
    num_steps = 100
    num_flashed = 0
    for step in range(1, num_steps+1):
        grid += 1
        to_flash = np.argwhere(grid == 10).tolist()

        while to_flash:
            octopus = to_flash.pop(0)
            for neighbor in get_neighbors(octopus):
                neighbor_val = grid[neighbor]
                if np.isnan(neighbor_val) or neighbor_val >= 10:
                    continue
                elif neighbor_val == 9:
                    to_flash.append(neighbor)
                grid[neighbor] += 1

        flashed = grid == 10
        grid[flashed] = 0
        num_flashed += np.sum(flashed)

    return num_flashed


def b(grid):
    for step in count(1):
        grid += 1
        to_flash = np.argwhere(grid == 10).tolist()

        while to_flash:
            octopus = to_flash.pop(0)
            for neighbor in get_neighbors(octopus):
                neighbor_val = grid[neighbor]
                if np.isnan(neighbor_val) or neighbor_val >= 10:
                    continue
                elif neighbor_val == 9:
                    to_flash.append(neighbor)
                grid[neighbor] += 1

        flashed = grid == 10
        grid[flashed] = 0
        if np.nansum(grid) == 0:
            break

    return step


def get_neighbors(location):
    x, y = location
    return [
        (x+dx, y+dy)
        for dx, dy in product([-1, 0, 1], repeat=2)
        if not (dx == 0 and dy == 0)
    ]


if __name__ == '__main__':
    files = [
        'input11-test1.txt',
        'input11-test2.txt',
        'input11.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            input_grid = [
                [int(height) for height in line]
                for line in f.read().splitlines()
            ]

        grid = np.full((len(input_grid) + 2, len(input_grid[0]) + 2), np.nan)
        grid[1:-1, 1:-1] = input_grid

        print(f'A: {a(np.copy(grid))}')
        print(f'B: {b(np.copy(grid))}')
