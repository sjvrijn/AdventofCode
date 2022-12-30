from collections import defaultdict
from pathlib import Path

import numpy as np


def neighbors(x, y):
    #               0 NW      1 N      2 NE    3 E     4 SE     5 S     6 SW    7 W
    for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
        yield x+dx, y+dy


def move_north(has_neighbors, elf):
    if not (has_neighbors[0] or has_neighbors[1] or has_neighbors[2]):
        return elf[0]-1, elf[1]
    return None


def move_south(has_neighbors, elf):
    if not (has_neighbors[4] or has_neighbors[5] or has_neighbors[6]):
        return elf[0]+1, elf[1]
    return None


def move_west(has_neighbors, elf):
    if not (has_neighbors[0] or has_neighbors[6] or has_neighbors[7]):
        return elf[0], elf[1]-1
    return None


def move_east(has_neighbors, elf):
    if not (has_neighbors[2] or has_neighbors[3] or has_neighbors[4]):
        return elf[0], elf[1]+1
    return None


def move_elf(elf, all_elves, move_order):
    has_neighbors = [
        n in all_elves
        for n in neighbors(*elf)
    ]
    if not any(has_neighbors):
        return elf

    for move_func in move_order:
        move = move_func(has_neighbors, elf)
        if move is not None:
            return move
    return elf


def simualte_elves(lines, report_empty_at=None):
    """Solve day 23 part 1"""
    elves = {
        (x, y)
        for x, line in enumerate(lines)
        for y, char in enumerate(line)
        if char == '#'
    }

    move_order = [move_north, move_south, move_west, move_east]
    have_any_moved = True

    i = 0
    while have_any_moved:
        moves = {}
        proposed_moves = defaultdict(list)
        for elf in elves:
            move = move_elf(elf, elves, move_order)
            moves[elf] = move
            proposed_moves[move].append(elf)

        new_elves = set()
        have_any_moved = False
        for move, sources in proposed_moves.items():
            if len(sources) == 1:
                new_elves.add(move)
                have_any_moved = have_any_moved or (move != sources[0])
            else:
                for elf in sources:
                    new_elves.add(elf)

        elves = new_elves
        move_order = move_order[1:] + move_order[:1]

        minx, maxx, miny, maxy = 0,0,0,0
        for x, y in elves:
            if minx is None or x < minx:
                minx = x
            if maxx is None or x > maxx:
                maxx = x
            if miny is None or y < miny:
                miny = y
            if maxy is None or y > maxy:
                maxy = y

        area = np.zeros((maxx-minx+1, maxy-miny+1))
        for x, y in elves:
            area[x-minx, y-miny] = 1

        i += 1
        if report_empty_at is not None and i == report_empty_at:
            area_size = ((maxx-minx)+1) * ((maxy-miny)+1)
            return area_size - len(elves)

    return i


def a(lines):
    """Solve day 23 part 1"""
    return simualte_elves(lines, report_empty_at=10)


def b(lines):
    """Solve day 23 part 2"""
    return simualte_elves(lines)


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    return f.read_text().splitlines()


def main():
    """Main function to wrap variables"""
    files = [
        # 'input23-test1.txt',
        # 'input23-test2.txt',
        'input23.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        # print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
