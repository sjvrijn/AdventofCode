from enum import IntEnum
from itertools import product

import numpy as np
import matplotlib.pyplot as plt


class Landscape(IntEnum):
    OPEN       = 1
    TREES      = 2
    LUMBERYARD = 3


symbols = {
    '.': Landscape.OPEN,
    '|': Landscape.TREES,
    '#': Landscape.LUMBERYARD,
}


def transform(subgrid):
    if subgrid[1,1] == Landscape.OPEN:
        if np.sum(subgrid == Landscape.TREES) >= 3:
            return Landscape.TREES
    elif subgrid[1,1] == Landscape.TREES:
        if np.sum(subgrid == Landscape.LUMBERYARD) >= 3:
            return Landscape.LUMBERYARD
    elif subgrid[1,1] == Landscape.LUMBERYARD:
        if (
            np.sum(subgrid == Landscape.LUMBERYARD) == 1
            or np.sum(subgrid == Landscape.TREES) == 0
        ):
            return Landscape.OPEN

    return subgrid[1,1]


grid_size = 50
size = (grid_size+2, grid_size+2)
field = np.zeros(size, dtype=np.int)


with open('input18.txt') as f:
    for row_idx, line in enumerate(f, start=1):
        field_row = [symbols[s] for s in line.strip()]
        field[row_idx, 1:len(field_row) + 1] = field_row

grid_size = len(field_row)

# np.set_printoptions(linewidth=300, edgeitems=50)
# print(field)


def update(prev):
    cur = np.copy(prev)
    for i, j in product(range(1, grid_size+1), repeat=2):
        cur[i, j] = transform(prev[i - 1:i + 2, j - 1:j + 2])
    return cur

num_minutes = 10


def plot_field(minute, show=False):
    plt.imshow(field[:grid_size + 2, :grid_size + 2])
    plt.title(f"minute {minute}: {np.sum(field == Landscape.TREES) * np.sum(field == Landscape.LUMBERYARD)}")
    plt.savefig(f"18_min_{minute}.png")
    if show:
        plt.show()
    plt.clf()


plot_field(0)

print(0, np.sum(field == Landscape.TREES) * np.sum(field == Landscape.LUMBERYARD))

for minute in range(1, num_minutes+1):
    field = update(field)
    print(minute, np.sum(field == Landscape.TREES) * np.sum(field == Landscape.LUMBERYARD))

    plot_field(minute)


print(minute, np.sum(field == Landscape.TREES) * np.sum(field == Landscape.LUMBERYARD))


