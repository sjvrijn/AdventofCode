from itertools import product
import numpy as np


def update_state(cube):
    cur_state = cube[1,1,1]
    active_neighbors = np.sum(cube == 1)
    if cur_state == 1 and 3 <= active_neighbors <= 4:
        return 1
    if cur_state == 0 and active_neighbors == 3:
        return 1
    return 0


def update_state_4d(hypercube):
    cur_state = hypercube[1,1,1,1]
    active_neighbors = np.sum(hypercube == 1)
    if cur_state == 1 and 3 <= active_neighbors <= 4:
        return 1
    if cur_state == 0 and active_neighbors == 3:
        return 1
    return 0


def a(lines, num_iters=6):
    grid_size = 2 + 2*num_iters + max(len(lines), len(lines[0]))
    z_size = 2*num_iters + 3
    grid = np.zeros((grid_size, grid_size, z_size))

    z = num_iters+1
    for row, line in enumerate(lines, start=num_iters+1):
        for col, char in enumerate(line, start=num_iters+1):
            grid[row,col,z] = char == '#'

    new_grid = np.copy(grid)
    for _ in range(num_iters):
        for row, col, z in product(range(1, grid_size), range(1, grid_size), range(1, z_size)):
            new_grid[row,col,z] = update_state(grid[row-1:row+2,col-1:col+2,z-1:z+2])
        grid, new_grid = new_grid, grid

    return np.sum(grid == 1)


def b(lines, num_iters=6):
    grid_size = 2 + 2*num_iters + max(len(lines), len(lines[0]))
    z_size = 2*num_iters + 3
    grid = np.zeros((grid_size, grid_size, z_size, z_size))

    w, z = num_iters+1, num_iters+1
    for row, line in enumerate(lines, start=num_iters+1):
        for col, char in enumerate(line, start=num_iters+1):
            grid[row,col,z,w] = char == '#'

    new_grid = np.copy(grid)
    for _ in range(num_iters):
        for row, col, z, w in product(
                range(1, grid_size), range(1, grid_size),
                range(1, z_size), range(1, z_size)
        ):
            new_grid[row,col,z,w] = update_state_4d(grid[row-1:row+2,col-1:col+2,z-1:z+2,w-1:w+2])
        grid, new_grid = new_grid, grid

    return np.sum(grid == 1)


if __name__ == '__main__':
    with open('input17.txt') as f:
        lines = [line.strip() for line in f]

    print(a(lines))
    print(b(lines))
