from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

from more_itertools import chunked
import numpy as np
import parse

directions = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0),
}


def follow(head, tail):
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    dist = abs(dx) + abs(dy)
    if dist >= 3:
        dx = -1 if dx < 0 else 1
        dy = -1 if dy < 0 else 1
        tail = tail[0] + dx, tail[1] + dy
    elif dist == 2 and dx == 0:
        tail = tail[0], tail[1] + dy // 2
    elif dist == 2 and dy == 0:
        tail = tail[0] + dx // 2, tail[1]
    return tail


def a(lines):
    """Solve day 09 part 1"""
    head = 0, 0
    tail = 0, 0
    visited = {tail}
    for instr, steps in lines:
        dxy = directions[instr]
        for _ in range(steps):
            head = head[0] + dxy[0], head[1] + dxy[1]
            tail = follow(head, tail)
            visited.add(tail)
    return len(visited)



def b(lines):
    """Solve day 09 part 2"""
    knots = [(0, 0) for _ in range(10)]
    visited = {knots[-1]}
    for instr, steps in lines:
        dxy = directions[instr]
        for _ in range(steps):
            knots[0] = knots[0][0] + dxy[0], knots[0][1] + dxy[1]
            for i in range(1, 10):
                knots[i] = follow(knots[i-1], knots[i])
            visited.add(knots[-1])
    return len(visited)


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = [line.split() for line in f.read_text().splitlines()]
    return [(instr, int(steps)) for instr, steps in lines]


def main():
    """Main function to wrap variables"""
    files = [
        'input09-test1.txt',
        'input09-test2.txt',
        'input09.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
