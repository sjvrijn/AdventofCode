from collections import defaultdict, namedtuple

from intcode import read_instructions, intcode


Point = namedtuple('Point', 'x y')
def add(self, other):
    return Point(self.x+other.x, self.y+other.y)
Point.__add__ = add
coords = Point(0, 0)

PAINT_ACTION = 0
TURN_ACTION = 1
cur_action = 0

TURN_LEFT = 0
TURN_RIGHT = 1

directions = [
    Point( 0,  1),
    Point( 1,  0),
    Point( 0, -1),
    Point(-1,  0),
]
cur_dir_idx = 0


paint = defaultdict(int)
painted = set()

instructions = read_instructions('input11.txt')
inputs = [0]

paint_bot = intcode(instructions, inputs=inputs)

for output in paint_bot:
    if cur_action == PAINT_ACTION:
        paint[coords] = output
        painted.add(coords)
    else:  # cur_action == TURN_ACTION
        if output == TURN_LEFT:
            cur_dir_idx -= 1
        else:
            cur_dir_idx += 1
        cur_dir_idx %= 4

        coords = coords + directions[cur_dir_idx]  # step
        inputs.append(paint[coords])

    cur_action = 1 - cur_action  # Toggle between turning and painting


print(len(painted))
