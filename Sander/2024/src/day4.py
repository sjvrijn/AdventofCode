from collections import defaultdict
from itertools import product
from pathlib import Path

import numpy as np
from pyprojroot import here


DIRECTIONS = {
    'North': np.array([[-1,  0], [-2,  0], [-3,  0]]),
    'East':  np.array([[ 0,  1], [ 0,  2], [ 0,  3]]),
    'South': np.array([[ 1,  0], [ 2,  0], [ 3,  0]]),
    'West':  np.array([[ 0, -1], [ 0, -2], [ 0, -3]]),
}


def a(word_search):
    """Solve day 4 part 1"""
    num_xmas = 0
    for y, x in product(range(word_search.shape[0]), range(word_search.shape[1])):
        if word_search[(y, x)] != 'X':
            continue
        for directions in valid_directions(y, x, word_search.shape):
            test_direction = sum(DIRECTIONS[direction] for direction in directions) + np.array([y, x])
            if "".join(word_search[tuple(idx)] for idx in test_direction) == "MAS":
                num_xmas += 1
    return num_xmas


def valid_directions(y, x, shape):
    directions = {
        ('North',),
        ('North', 'East'),
        ('East',),
        ('South', 'East'),
        ('South',),
        ('South', 'West'),
        ('West',),
        ('North', 'West'),
    }
    if y < 3:
        directions -= {('North', 'West'), ('North',), ('North', 'East')}
    if shape[0]-y < 4:
        directions -= {('South', 'West'), ('South',), ('South', 'East')}

    if x < 3:
        directions -= {('North', 'West'), ('West',), ('South', 'West')}
    if shape[1]-x < 4:
        directions -= {('North', 'East'), ('East',), ('South', 'East')}

    return directions


def b(word_search):
    """Solve day 4 part 2"""
    num_x_mas = 0
    for x, y in product(range(1, word_search.shape[0]-1), range(1, word_search.shape[1]-1)):
        if word_search[x, y] != 'A':
            continue
        counts = defaultdict(int)
        for i, j in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            counts[word_search[x+i, y+j]] += 1

        if counts['M'] == 2 and counts['S'] == 2 and word_search[x-1, y-1] != word_search[x+1, y+1]:
            num_x_mas += 1
            # if word_search[x-1, y-1] == word_search[x+1, y+1]:
            #     print(f"{word_search[x-1, y-1]} {word_search[x-1, y+1]}\n A\n{word_search[x+1, y-1]} {word_search[x+1, y+1]}\n")

    return num_x_mas


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    word_search = np.array([list(line) for line in f.read_text().splitlines()])
    return word_search


def main():
    """Main function to wrap variables"""
    files = [
        'Sander/2024/inputs/input4-test1.txt',
        'Sander/2024/inputs/input4.txt',
    ]
    for filename in files:
        print(filename)
        word_search = parse_file(here(filename))

        print(f'A: {a(word_search)}')
        print(f'B: {b(word_search)}')


if __name__ == '__main__':
    main()
