from enum import IntEnum
from pathlib import Path

from functools import reduce
import re

from more_itertools import flatten
from parse import findall, parse
import numpy as np


class Direction(IntEnum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3


TURN = {
    ('R', Direction.EAST): Direction.SOUTH,
    ('R', Direction.SOUTH): Direction.WEST,
    ('R', Direction.WEST): Direction.NORTH,
    ('R', Direction.NORTH): Direction.EAST,
    ('L', Direction.EAST): Direction.NORTH,
    ('L', Direction.SOUTH): Direction.EAST,
    ('L', Direction.WEST): Direction.SOUTH,
    ('L', Direction.NORTH): Direction.WEST,
}
DXY = {
    Direction.EAST: (0, 1),
    Direction.WEST: (0, -1),
    Direction.SOUTH: (1, 0),
    Direction.NORTH: (-1, 0),
}
VOID = ord(' ')
EMPTY = ord('.') - VOID
WALL = ord('#') - VOID


# Cube net border definitions in the form of {0: (E,S,W,N), ...} where E/S/W/N
# compass side combinations to encode coord transformations

# ..0.
# 123.
# ..45
CUBE_1 = {# EAST                  SOUTH                 WEST                  NORTH
    0: ((5, Direction.EAST),  (3, Direction.NORTH), (2, Direction.NORTH), (1, Direction.NORTH)),
    1: ((2, Direction.WEST),  (4, Direction.SOUTH), (5, Direction.SOUTH), (0, Direction.NORTH)),
    2: ((3, Direction.WEST),  (4, Direction.WEST),  (1, Direction.EAST),  (0, Direction.WEST)),
    3: ((5, Direction.NORTH), (4, Direction.NORTH), (2, Direction.EAST),  (0, Direction.SOUTH)),
    4: ((5, Direction.WEST),  (1, Direction.SOUTH), (2, Direction.SOUTH), (3, Direction.SOUTH)),
    5: ((0, Direction.EAST),  (1, Direction.WEST),  (4, Direction.EAST),  (3, Direction.EAST)),
}

# .01
# .2.
# 34.
# 5..
CUBE_2 = {# EAST                  SOUTH                 WEST                  NORTH
    0: ((1, Direction.WEST),  (2, Direction.NORTH), (3, Direction.WEST),  (5, Direction.WEST)),
    1: ((4, Direction.EAST),  (2, Direction.EAST),  (0, Direction.EAST),  (5, Direction.SOUTH)),
    2: ((1, Direction.SOUTH), (4, Direction.NORTH), (3, Direction.NORTH), (0, Direction.SOUTH)),
    3: ((4, Direction.WEST),  (5, Direction.NORTH), (0, Direction.WEST),  (2, Direction.WEST)),
    4: ((1, Direction.EAST),  (5, Direction.EAST),  (3, Direction.EAST),  (2, Direction.SOUTH)),
    5: ((4, Direction.SOUTH), (1, Direction.NORTH), (0, Direction.NORTH), (3, Direction.SOUTH)),
}


class Square:
    def __init__(self, square, sx, sy, north=None, east=None, south=None, west=None):
        self.sx = sx
        self.sy = sy
        self.square = square
        self.size = square.shape[0]
        self.north = north
        self.east = east
        self.south = south
        self.west = west

    def __repr__(self):
        return f"Square(sx={self.sx}, sy={self.sy})"


def squares_array_to_flat_squares(squares):
    squares = [
        [Square(square, sx, sy) if square is not None else None for sy, square in enumerate(row)]
        for sx, row in enumerate(squares)
    ]
    nrows = len(squares)
    ncols = len(squares[0])
    start_square = None
    for r_idx, row in enumerate(squares):
        for c_idx, square in enumerate(row):
            if square is None:
                continue
            if start_square is None:
                start_square = square

            r_north = (r_idx - 1) % nrows
            while squares[r_north][c_idx] is None:
                r_north = (r_north - 1) % nrows
            r_south = (r_idx + 1) % nrows
            while squares[r_south][c_idx] is None:
                r_south = (r_south + 1) % nrows

            c_east = (c_idx + 1) % ncols
            while squares[r_idx][c_east] is None:
                c_east = (c_east + 1) % ncols
            c_west = (c_idx - 1) % ncols
            while squares[r_idx][c_west] is None:
                c_west = (c_west - 1) % ncols

            square.north = squares[r_north][c_idx]
            square.east = squares[r_idx][c_east]
            square.south = squares[r_south][c_idx]
            square.west = squares[r_idx][c_west]

    return squares, start_square


def step(x, y, num_steps, facing, square):
    dx, dy = DXY[facing]
    nsquare = square
    for _ in range(num_steps):
        nx, ny = x+dx, y+dy
        if nx < 0:
            nx = nsquare.size-1
            nsquare = square.north
        elif nx >= nsquare.size:
            nx = 0
            nsquare = square.south
        if ny < 0:
            ny = nsquare.size-1
            nsquare = square.west
        elif ny >= nsquare.size:
            ny = 0
            nsquare = square.east

        if nsquare.square[nx, ny] == WALL:
            break
        x, y, square = nx, ny, nsquare

    return x, y, square


def a(squares, instructions):
    """Solve day 22 part 1"""
    squares, cur_square = squares_array_to_flat_squares(squares)
    x, y, facing = 0, 0, Direction.EAST
    while cur_square.square[x,y] == WALL:
        y+=1

    num_steps, instructions = parse("{:d}{}", instructions)
    x, y, cur_square = step(x, y, num_steps, facing, cur_square)
    for turn, num_steps in findall('{:l}{:d}', instructions):
        facing = TURN[turn, facing]
        x, y, cur_square = step(x, y, num_steps, facing, cur_square)

    x += (cur_square.sx * cur_square.size) + 1
    y += (cur_square.sy * cur_square.size) + 1
    return 1_000*x + 4*y + facing


def fill_cube_neighbors(squares, encoding):
    flat_squares = [s for s in flatten(squares) if s is not None]
    for sq_idx, neighbors in encoding.items():
        square = flat_squares[sq_idx]
        square.east  = flat_squares[neighbors[Direction.EAST][0]],  neighbors[Direction.EAST][1]
        square.south = flat_squares[neighbors[Direction.SOUTH][0]], neighbors[Direction.SOUTH][1]
        square.west  = flat_squares[neighbors[Direction.WEST][0]],  neighbors[Direction.WEST][1]
        square.north = flat_squares[neighbors[Direction.NORTH][0]], neighbors[Direction.NORTH][1]


def squares_array_to_cube(squares, encoding):
    squares = [
        [Square(square, sx, sy) if square is not None else None for sy, square in enumerate(row)]
        for sx, row in enumerate(squares)
    ]
    start_square = None
    for row in squares:
        for square in row:
            if square is None:
                continue
            if start_square is None:
                start_square = square

    fill_cube_neighbors(squares, encoding)
    return squares, start_square


def cross_cube_edge(facing: Direction, to_side: Direction, x: int, y: int, square_size: int):
    crossing_coord = y if facing in [Direction.NORTH, Direction.SOUTH] else x
    square_size -= 1
    if facing in [Direction.NORTH, Direction.EAST]:
        if to_side == Direction.NORTH:
            return 0, square_size-crossing_coord, Direction.SOUTH
        elif to_side == Direction.EAST:
            return square_size-crossing_coord, square_size, Direction.WEST
        elif to_side == Direction.SOUTH:
            return square_size, crossing_coord, Direction.NORTH
        elif to_side == Direction.WEST:
            return crossing_coord, 0, Direction.EAST

    elif facing in [Direction.SOUTH, Direction.WEST]:
        if to_side == Direction.NORTH:
            return 0, crossing_coord, Direction.SOUTH
        elif to_side == Direction.EAST:
            return crossing_coord, square_size, Direction.WEST
        elif to_side == Direction.SOUTH:
            return square_size, square_size-crossing_coord, Direction.NORTH
        elif to_side == Direction.WEST:
            return square_size-crossing_coord, 0, Direction.EAST


def cube_step(x, y, num_steps, facing, square):
    nsquare = square
    for _ in range(num_steps):
        dx, dy = DXY[facing]
        nx, ny = x+dx, y+dy
        to_side, nfacing = None, None
        if nx < 0:
            nsquare, to_side = square.north
        elif nx >= nsquare.size:
            nsquare, to_side = square.south
        if ny < 0:
            nsquare, to_side = square.west
        elif ny >= nsquare.size:
            nsquare, to_side = square.east

        if to_side is not None:
            nx, ny, nfacing = cross_cube_edge(facing, to_side, x, y, square.size)

        if nsquare.square[nx, ny] == WALL:
            break
        x, y, square = nx, ny, nsquare
        if nfacing is not None:
            facing = nfacing

        square.square[x,y] = ord({Direction.NORTH:'^',Direction.EAST:'>',Direction.SOUTH:'v',Direction.WEST:'<'}[facing])

    return x, y, facing, square


def b(squares, instructions, cube_encoding):
    """Solve day 22 part 2"""
    squares, cur_square = squares_array_to_cube(squares, cube_encoding)
    x, y, facing = 0, 0, Direction.EAST
    while cur_square.square[x,y] == WALL:
        y += 1

    num_steps, instructions = parse("{:d}{}", instructions)
    x, y, facing, cur_square = cube_step(x, y, num_steps, facing, cur_square)

    for turn, num_steps in findall('{:l}{:d}', instructions):
        facing = TURN[turn, facing]
        x, y, facing, cur_square = cube_step(x, y, num_steps, facing, cur_square)

    x += (cur_square.sx * cur_square.size) + 1
    y += (cur_square.sy * cur_square.size) + 1
    return 1_000*x + 4*y + facing


def display_square(square):
    char = {VOID: ' ', WALL: '#', EMPTY: '.',
            ord('>'): '>', ord('v'): 'v', ord('<'): '<', ord('^'): '^'}
    print(square.sx, square.sy)
    for row in square.square:
        print(''.join(char[c] for c in row))
    print()


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    map_, instructions = f.read_text().split('\n\n')
    lines = [
        [ord(char) for char in line]
        for line in map_.splitlines()
    ]
    map_width = max(len(line) for line in lines)
    map_ = np.full((len(lines), map_width), fill_value=VOID)
    for idx, line in enumerate(lines):
        map_[idx, :len(line)] = line
    map_ -= VOID
    square_size = np.sqrt(np.count_nonzero(map_) // 6)
    squares = np.split(map_, map_.shape[0] // square_size, axis=0)

    squares = [
        np.split(row, map_.shape[1] // square_size, axis=1)
        for row in squares
    ]
    squares = [
        [square if np.count_nonzero(square) else None for square in row]
        for row in squares
    ]

    return squares, instructions


def main():
    """Main function to wrap variables"""
    files = [
        ('input22-test1.txt', CUBE_1),
        ('input22.txt', CUBE_2),
    ]
    for filename, cube_encoding in files:
        print(filename)
        squares, instructions = parse_file(Path(filename))

        print(f'A: {a(squares, instructions)}')
        print(f'B: {b(squares, instructions, cube_encoding)}')


if __name__ == '__main__':
    main()
