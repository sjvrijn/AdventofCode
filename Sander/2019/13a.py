from more_itertools import chunked

from intcode import IntCode, read_instructions


instructions = read_instructions('input13.txt')

display, _ = IntCode(instructions).intcode()

field = {(x, y): kind for x, y, kind in chunked(display, 3)}
print(field.values().count(2))
