from pathlib import Path

import numpy as np


neighbors = (
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
)


def a(heights):
    """Solve day 12 part 1"""
    start = tuple(np.argwhere(heights == ord('S'))[0])
    distances = calc_steps_to_summit(heights)
    return distances[start]


def b(heights):
    """Solve day 12 part 2"""
    distances = calc_steps_to_summit(heights)
    return np.min(distances[heights==ord('a')])


def calc_steps_to_summit(heights):
    start = tuple(np.argwhere(heights == ord('S'))[0])
    end = tuple(np.argwhere(heights == ord('E'))[0])
    heights[start] = ord('a')
    heights[end] = ord('z')
    max_dist = heights.size
    distances = np.full_like(heights, fill_value=max_dist, dtype=np.int16)
    distances[end] = 0
    to_check = [end]
    while to_check:
        x, y = to_check.pop(0)
        cur_height = heights[x, y]
        for dx, dy in neighbors:
            newx, newy = x+dx, y+dy
            if (newx < 0 or newx >= heights.shape[0])\
                    or (newy < 0 or newy >= heights.shape[1])\
                    or (distances[newx, newy] != max_dist)\
                    or ((cur_height - heights[newx,newy]) > 1):
                continue
            distances[newx, newy] = distances[x,y] + 1
            to_check.append((newx, newy))
    return distances


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = f.read_text().splitlines()
    return np.array([
        [ord(square) for square in line]
        for line in lines
    ], dtype=np.int8)


def main():
    """Main function to wrap variables"""
    files = [
        'input12-test1.txt',
        'input12.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data.copy())}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
