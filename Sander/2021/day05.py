from collections import namedtuple

import numpy as np
import matplotlib.pyplot as plt
import parse


Point = namedtuple('Point', 'x y')
LINESPEC = parse.compile('{:d},{:d} -> {:d},{:d}')


def a(lines, visual=False):
    grid = np.zeros((1000, 1000))
    for line in lines:
        p1, p2 = line
        if is_horizontal(p1, p2):
            if p1.x > p2.x:
                p1, p2 = p2, p1
            grid[p1.x : p2.x+1, p1.y] += 1
        elif is_vertical(p1, p2):
            if p1.y > p2.y:
                p1, p2 = p2, p1
            grid[p1.x, p1.y : p2.y+1] += 1

    if visual:
        plt.imshow(grid.T)
        plt.show()

    return np.sum(grid > 1)


def b(lines, visual=False):
    grid = np.zeros((1000, 1000))
    for line in lines:
        p1, p2 = line
        if is_horizontal(p1, p2):
            if p1.x > p2.x:
                p1, p2 = p2, p1
            grid[p1.x : p2.x+1, p1.y] += 1
        elif is_vertical(p1, p2):
            if p1.y > p2.y:
                p1, p2 = p2, p1
            grid[p1.x, p1.y : p2.y+1] += 1
        else:
            xstep = 1 if p1.x <= p2.x else -1
            ystep = 1 if p1.y <= p2.y else -1
            for x, y in zip(range(p1.x, p2.x+xstep, xstep), range(p1.y, p2.y+ystep, ystep)):
                grid[x,y] += 1

    if visual:
        plt.imshow(grid.T)
        plt.show()

    return np.sum(grid > 1)


def is_horizontal(p1, p2):
    return p1.y == p2.y


def is_vertical(p1, p2):
    return p1.x == p2.x


def parse_line(line):
    x, y, z, w = LINESPEC.parse(line)
    return Point(x, y), Point(z, w)


if __name__ == '__main__':
    files = [
        'input05-test1.txt',
        'input05.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            lines = [parse_line(line) for line in  f.read().splitlines()]

        print(f'A: {a(lines)}')
        print(f'B: {b(lines)}')
