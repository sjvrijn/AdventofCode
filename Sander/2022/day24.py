from pathlib import Path

import numpy as np


EMPTY = 0
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
REACHABLE = 16


def step_blizzards(valley):
    moved = np.zeros(valley.shape, dtype=int)
    # move all blizzards one step
    moved[1:-2,:]  = valley[2:-1,:] & NORTH
    moved[:,2:-1] += valley[:,1:-2] & EAST
    moved[2:-1,:] += valley[1:-2,:] & SOUTH
    moved[:,1:-2] += valley[:,2:-1] & WEST

    # wrap blizzards around the edges
    moved[-2,:] += valley[1,:] & NORTH
    moved[:,1] += valley[:,-2] & EAST
    moved[1,:] += valley[-2,:] & SOUTH
    moved[:,-2] += valley[:,1] & WEST

    return moved


def expand_reachable(prev_valley, next_valley):
    # mask of expanded reachability
    reachable = prev_valley & REACHABLE
    reachable_mask = np.copy(reachable)
    reachable_mask[:-1,:] |= reachable[1:,:]
    reachable_mask[1:,:] |= reachable[:-1,:]
    reachable_mask[:,:-1] |= reachable[:,1:]
    reachable_mask[:,1:] |= reachable[:,:-1]

    # clear edges, but remember the start and end
    start_reachable, target_reachable = reachable_mask[0,1], reachable_mask[-1,-2]
    reachable_mask[0,:] = EMPTY
    reachable_mask[-1,:] = EMPTY
    reachable_mask[:,0] = EMPTY
    reachable_mask[:,-1] = EMPTY
    # reset start/end
    reachable_mask[0,1] = start_reachable
    reachable_mask[-1,-2] = target_reachable

    next_valley[next_valley == 0] |= reachable_mask[next_valley == 0]
    return next_valley


def a(valley):
    """Solve day 24 part 1"""

    i = 0
    while valley[-1,-2] != REACHABLE:
        new_valley = step_blizzards(valley)
        valley = expand_reachable(valley, new_valley)
        i+=1

    return i


def b(valley):
    """Solve day 24 part 2"""

    i = 0
    while valley[-1,-2] != REACHABLE:
        new_valley = step_blizzards(valley)
        valley = expand_reachable(valley, new_valley)
        i+=1

    valley[valley==REACHABLE] = EMPTY
    valley[-1,-2] = REACHABLE
    while valley[0,1] != REACHABLE:
        new_valley = step_blizzards(valley)
        valley = expand_reachable(valley, new_valley)
        i+=1

    valley[valley==REACHABLE] = EMPTY
    valley[0,1] = REACHABLE
    while valley[-1,-2] != REACHABLE:
        new_valley = step_blizzards(valley)
        valley = expand_reachable(valley, new_valley)
        i+=1

    return i


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    transform = {
        '#': EMPTY,
        '.': EMPTY,
        '^': NORTH,
        '>': EAST,
        'v': SOUTH,
        '<': WEST,
    }

    lines = f.read_text().splitlines()
    valley = np.array([
        [transform[char] for char in line]
        for line in lines
    ])
    valley[0,1] = REACHABLE
    return valley


def main():
    """Main function to wrap variables"""
    files = [
        'input24-test1.txt',
        'input24-test2.txt',
        'input24.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
