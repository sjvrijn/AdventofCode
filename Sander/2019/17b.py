from collections import namedtuple
from copy import copy
from enum import IntEnum
from itertools import product

from more_itertools import split_at
import numpy as np

from intcode import IntCode, ReturnCode, read_instructions


class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4



Point = namedtuple('Point', 'x y')
def add(self, other):
    return Point(self.x+other.x, self.y+other.y)
Point.__add__ = add
def sub(self, other):
    return Point(self.x-other.x, self.y-other.y)
Point.__sub__ = sub


directions = {
    Direction.NORTH: Point(-1, 0),
    Direction.WEST: Point(0, -1),
    Direction.SOUTH: Point(1, 0),
    Direction.EAST: Point(0, 1),
}

turn_left = {
    Direction.NORTH: Direction.WEST,
    Direction.WEST: Direction.SOUTH,
    Direction.SOUTH: Direction.EAST,
    Direction.EAST: Direction.NORTH,
}

turn_right = {
    Direction.NORTH: Direction.EAST,
    Direction.WEST: Direction.NORTH,
    Direction.SOUTH: Direction.WEST,
    Direction.EAST: Direction.SOUTH,
}


instructions = read_instructions('input17.txt')

space_roomba = IntCode(instructions)
output, rc = space_roomba.intcode()

split_output = list(split_at(output, lambda x: x==10))
scaffold = np.array(split_output[:-2])

cur_roomba_coords = Point(*np.argwhere(scaffold == ord('^'))[0])
cur_direction = Direction.NORTH
steps = []
step_count = 0

xrange = range(scaffold.shape[0])
yrange = range(scaffold.shape[1])

while True:

    coords_after_step = cur_roomba_coords + directions[cur_direction]
    if coords_after_step.x in xrange \
            and coords_after_step.y in yrange \
            and scaffold[coords_after_step] == ord('#'):
        step_count += 1
        cur_roomba_coords = coords_after_step
    elif scaffold[cur_roomba_coords + directions[turn_left[cur_direction]]] == ord('#'):
        steps.extend([str(step_count), 'L'])
        cur_direction = turn_left[cur_direction]
        cur_roomba_coords = cur_roomba_coords + directions[cur_direction]
        step_count = 1
    elif scaffold[cur_roomba_coords + directions[turn_right[cur_direction]]] == ord('#'):
        steps.extend([str(step_count), 'R'])
        cur_direction = turn_right[cur_direction]
        cur_roomba_coords = cur_roomba_coords + directions[cur_direction]
        step_count = 1
    else:
        steps.pop(0)
        steps.append(str(step_count))
        break


def to_ascii_list(iterable):
    ascii_list = []
    for item in iterable:
        for char in item:
            ascii_list.append(ord(char))
        ascii_list.append(ord(','))
    ascii_list.pop(-1)
    ascii_list.append(ord('\n'))
    return ascii_list


def matches(self, other):
    return all(a == b for a, b in zip(self, other))


for len_a, len_b, len_c in product(range(2, 11, 2), repeat=3):

    # make new local variables
    temp_steps = copy(steps)
    lengths = {
        'A': len_a,
        'B': len_b,
        'C': len_c,
    }
    programs = {
        'A': None,
        'B': None,
        'C': None,
    }
    final_program = []

    while temp_steps:

        for letter, program in programs.items():

            chunk = temp_steps[:lengths[letter]]

            # if a chunk is too long, it can't be a sub-program, try next length
            if len(to_ascii_list(chunk)) > 21:
                continue

            # Define a new sub-program A, B or C
            if program is None:
                programs[letter] = chunk
            # Check whether current chunk matches existing program
            elif not matches(chunk, program):
                continue

            # Recognise and record usage of a program A, B or C
            final_program.append(letter)
            temp_steps = temp_steps[lengths[letter]:]
            break

        # Chunk cannot be added as a new section, nor recognised: next lengths
        else:
            break

        # total program length may not be too long either
        if len(to_ascii_list(final_program)) > 21:
            break

    if temp_steps:
        continue

    print(final_program)
    for key, val in programs.items():
        print(key, val)
    break


# Program has been determined, now re_init space-roomba and do program
instructions = read_instructions('input17.txt')
instructions[0] = 2
inputs = list(to_ascii_list(final_program))
for program in programs.values():
    inputs.extend(to_ascii_list(program))
inputs.extend([ord('n'), 10])

space_roomba = IntCode(instructions, inputs=inputs)
output, rc = space_roomba.intcode()

print()
print(output[-1])

# split_output = list(split_at(output, lambda x: x==10))
# for line in split_output:
#     print(''.join(map(chr, line)))
