from dataclasses import dataclass, field
import heapq
from itertools import product

from more_itertools import take
import numpy as np


@dataclass(order=True)
class Coord:
    dist: int
    coord: tuple[int, int]=field(compare=False)
    max_size: tuple[int, int]=field(compare=False)

    def neighbors(self):
        return [
            (self.coord[0]+i, self.coord[1]+j)
            for i, j in [(1, 0), (0, 1), (-1, 0), (0, -1)]
            if 0 <= self.coord[0] + i < self.max_size[0]
                and 0 <= self.coord[1] + j < self.max_size[1]
        ]


def a(grid):
    return do_dijkstra_old(grid)


def b(grid):
    return do_dijkstra_old(extend_grid(grid))


def extend_grid(grid):
    assert grid.shape[0] == grid.shape[1]  # assumes square grid
    addition = np.repeat(np.arange(5), repeats=grid.shape[0]).reshape(-1, 1)
    grid = np.tile(grid, (5, 5))
    grid += addition + addition.T
    where_wrap = grid >= 10
    grid[where_wrap] = (grid[where_wrap] + 1) % 10
    return grid


def do_dijkstra_old(grid):
    heap = []
    coord_grid = {}
    nrows, ncols = grid.shape
    for coord in product(range(nrows), range(ncols)):
        loc = Coord(np.inf, coord, max_size=grid.shape)
        heap.append(loc)
        coord_grid[coord] = loc

    goal = heap[-1].coord
    coord_grid[(0,0)].dist = 0
    cur = heapq.heappop(heap)
    visited = set()

    while heap:
        if cur.coord is None:
            cur = heapq.heappop(heap)
            continue
        for coord in cur.neighbors():
            if coord in visited:
                continue

            entry = coord_grid[coord]
            new_dist = grid[coord] + cur.dist
            if new_dist < entry.dist:
                new_entry = Coord(new_dist, entry.coord, max_size=entry.max_size)
                coord_grid[coord] = new_entry
                entry.coord = None
                heapq.heappush(heap, new_entry)

        visited.add(cur.coord)
        cur = heapq.heappop(heap)

        if coord_grid[goal].dist < cur.dist:
            break

    return coord_grid[goal].dist


def if_only_down_or_right(grid):
    total_risk_grid = np.copy(grid)
    rows, cols = grid.shape
    coords = product(range(rows-1, -1, -1), range(cols-1, -1, -1))
    take(1, coords)  # omit bottom-right corner
    for i, j in coords:
        choices = []
        if i != rows-1:
            choices.append(total_risk_grid[i+1, j])
        if j != cols-1:
            choices.append(total_risk_grid[i, j+1])
        total_risk_grid[i,j] += min(choices)
    return total_risk_grid[0,0] - grid[0,0]


if __name__ == '__main__':
    files = [
        'input15-test1.txt',
        # 'input15-test2.txt',
        # 'input15-test3.txt',
        'input15.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            lines = f.read().splitlines()  # multi-line file
        grid = np.array([list(map(int, line)) for line in lines])

        print(f'A: {a(grid)}')
        print(f'B: {b(grid)}')
