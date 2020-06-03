from collections import namedtuple
from itertools import product

from more_itertools import split_at
import numpy as np

from intcode import IntCode, ReturnCode, read_instructions


Point = namedtuple('Point', 'x y')
def add(self, other):
    return Point(self.x+other.x, self.y+other.y)
Point.__add__ = add
def sub(self, other):
    return Point(self.x-other.x, self.y-other.y)
Point.__sub__ = sub

neighbors = [
    Point(-1, 0),
    Point(1, 0),
    Point(0, -1),
    Point(0, 1),
]


instructions = read_instructions('input17.txt')

space_roomba = IntCode(instructions)
output, rc = space_roomba.intcode()

split_output = list(split_at(output, lambda x: x==10))
for line in split_output:
    print(''.join(map(chr, line)))

scaffold = np.array(split_output[:-2])

max_x, max_y = scaffold.shape
crossings = []
for x, y in product(range(1, max_x-1), range(1, max_y-1)):
    coord = Point(x, y)

    if scaffold[coord] == ord('#') and all(
        scaffold[coord + neighbor] == ord('#') for neighbor in neighbors
    ):
        crossings.append(coord)

param_sum = sum(cross.x * cross.y for cross in crossings)
print(param_sum)
