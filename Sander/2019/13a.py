from more_itertools import chunked

from intcode import IntCode, read_instructions


instructions = read_instructions('input13.txt')

field = {}
display, _ = IntCode(instructions).intcode()

for x, y, kind in chunked(display, 3):
    field[(x, y)] = kind

print(sum(1 for k in field.values() if k == 2))
