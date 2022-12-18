from pathlib import Path

from more_itertools import windowed
import numpy as np

AIR = 0
ROCK = 1
SAND = 2



def a(shapes):
    """Solve day 14 part 1"""
    area = np.zeros((200,600))
    for shape in shapes:
        for (x1, y1), (x2, y2) in windowed(shape, n=2):
            if x2 < x1:
                x1, x2 = x2, x1
            if y2 < y1:
                y1, y2 = y2, y1
            area[x1:x2+1, y1:y2+1] = ROCK
    max_x = np.max(np.where(np.sum(area == ROCK, axis=1))[0])

    x, y = 0, 500
    while x <= max_x:
        if area[x+1, y] == AIR:
            x += 1
        elif area[x+1, y-1] == AIR:
            x, y = x+1, y-1
        elif area[x+1, y+1] == AIR:
            x, y = x+1, y+1
        else:
            area[x, y] = SAND
            x, y = 0, 500

    return np.sum(area == SAND)


def b(shapes):
    """Solve day 14 part 2"""
    area = np.zeros((200,1_000))
    for shape in shapes:
        for (x1, y1), (x2, y2) in windowed(shape, n=2):
            if x2 < x1:
                x1, x2 = x2, x1
            if y2 < y1:
                y1, y2 = y2, y1
            area[x1:x2+1, y1:y2+1] = ROCK
    max_x = np.max(np.where(np.sum(area == ROCK, axis=1))[0])

    area[max_x+2] = ROCK

    x, y = 0, 500
    while True:
        if area[x+1, y] == AIR:
            x += 1
        elif area[x+1, y-1] == AIR:
            x, y = x+1, y-1
        elif area[x+1, y+1] == AIR:
            x, y = x+1, y+1
        elif x == 0 and y == 500:
            area[x,y] = SAND
            break
        else:
            area[x, y] = SAND
            x, y = 0, 500

    return np.sum(area == SAND)


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = f.read_text().splitlines()
    shapes = []
    for line in lines:
        shape = []
        for coord in line.split(' -> '):
            y, x = coord.split(',')
            shape.append((int(x), int(y)))
        shapes.append(shape)
    return shapes


def main():
    """Main function to wrap variables"""
    files = [
        'input14-test1.txt',
        'input14.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
