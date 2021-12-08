from functools import lru_cache

import numpy as np


def a(positions):
    positions = np.array(positions)
    max_pos = np.max(positions)

    best_fuel_use, best_pos = np.inf, -1
    for pos in range(max_pos+1):
        fuel_use = np.sum(np.abs(positions - pos))
        if fuel_use < best_fuel_use:
            best_fuel_use, best_pos = fuel_use, pos

    return best_fuel_use


def b(positions):
    positions = np.array(positions)
    max_pos = np.max(positions)

    best_fuel_use, best_pos = np.inf, -1
    for pos in range(max_pos + 1):
        fuel_use = np.sum(triangle_num(np.abs(positions - pos)))
        if fuel_use < best_fuel_use:
            best_fuel_use, best_pos = fuel_use, pos

    return best_fuel_use


@lru_cache(maxsize=None)
def triangle_num(n):
    return np.sum(np.arange(1, n+1))


triangle_num = np.vectorize(triangle_num)


if __name__ == '__main__':
    files = [
        'input07-test1.txt',
        'input07.txt',
    ]

    for filename in files:
        print(filename)
        with open(filename) as f:
            positions = list(map(int, f.read().strip().split(',')))

        print(f'A: {a(positions)}')
        print(f'B: {b(positions)}')
