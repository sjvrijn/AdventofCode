from itertools import count, cycle
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROCK_SHAPES = [
    # ####
    ((4,2), (4,3), (4,4), (4,5)),
    # .#.
    # ###
    # .#.
    ((5,2), (4,3), (5,3), (6,3), (5,4)),
    # ..#
    # ..#
    # ###
    ((4,2), (4,3), (4,4), (5,4), (6,4)),
    # #
    # #
    # #
    # #
    ((4,2), (5,2), (6,2), (7,2)),
    # ##
    # ##
    ((4,2), (4,3), (5,2), (5,3)),
]


class Rock:
    def __init__(self, shape, cur_height):
        self.shape = np.array(shape).T
        self.shape[0] += cur_height

    def jet_push(self, jet, shaft):
        if jet == '<':
            if not np.any(self.shape[1] == 0):
                self.shape[1] -= 1
        elif jet == '>':
            if not np.any(self.shape[1] == shaft.shape[1]-1):
                self.shape[1] += 1

        if np.sum(shaft[self.astuple()]):
            self.shape[1] += 1 if jet == '<' else -1

    def drop(self):
        self.shape[0] -= 1

    def undo_drop(self):
        self.shape[0] += 1

    def astuple(self):
        return self.shape[0], self.shape[1]


def a(jet_pattern):
    """Solve day 17 part 1"""
    shaft = np.zeros((10_000, 7))
    shaft[0] = 2
    cur_height = 0
    jet_pattern = cycle(jet_pattern)
    for rock_idx, rock_shape in zip(range(2022), cycle(ROCK_SHAPES)):
        rock = Rock(rock_shape, cur_height)

        while not np.sum(shaft[rock.astuple()]):
            rock.jet_push(next(jet_pattern), shaft)
            rock.drop()

        rock.undo_drop()
        shaft[rock.astuple()] = 1
        cur_height = max(cur_height, max(rock.shape[0]))

    return np.max(np.where(np.sum(shaft, axis=1)))


def b(jet_pattern):
    """Solve day 17 part 2"""
    shaft = np.zeros((100_000, 7))
    shaft[0] = 2
    cur_height = 0
    jet_pattern = cycle(enumerate(jet_pattern))
    jet_idx = 0
    height_history = {}

    for rock_idx, rock_shape in cycle(enumerate(ROCK_SHAPES)):
        rock = Rock(rock_shape, cur_height)
        if (rock_idx, jet_idx) in height_history:
            print(rock_idx, jet_idx, height_history[(rock_idx, jet_idx)], cur_height)
        else:
            height_history[(rock_idx, jet_idx)] = cur_height

        if cur_height > 5500:
            break

        while not np.sum(shaft[rock.astuple()]):
            jet_idx, jet = next(jet_pattern)
            rock.jet_push(jet, shaft)
            rock.drop()

        rock.undo_drop()
        shaft[rock.astuple()] = 1
        cur_height = max(cur_height, max(rock.shape[0]))


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    return f.read_text().strip()


def main():
    """Main function to wrap variables"""
    files = [
        # 'input17-test1.txt',
        'input17.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
