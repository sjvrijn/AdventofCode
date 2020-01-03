from collections import namedtuple
from enum import IntEnum
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


from intcode import IntCode, ReturnCode, read_instructions


class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class Report(IntEnum):
    WALL = 0
    MOVED = 1
    FOUND = 2


class Maze(IntEnum):
    WALL = -1
    UNKNOWN = 0
    SPACE = 3
    OXYGEN = 2
    CUR_POS = 5


Point = namedtuple('Point', 'x y')
def add(self, other):
    return Point(self.x+other.x, self.y+other.y)
Point.__add__ = add
def sub(self, other):
    return Point(self.x-other.x, self.y-other.y)
Point.__sub__ = sub


instructions = read_instructions('input15.txt')


directions = {
    Direction.NORTH: Point(-1, 0),
    Direction.SOUTH: Point(1, 0),
    Direction.WEST: Point(0, -1),
    Direction.EAST: Point(0, 1),
}

inv_directions = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
    Direction.EAST: Direction.WEST,
}


maze = np.zeros((41, 41))
pos = Point(21, 21)

maze[pos] = Maze.SPACE

inputs = []
droid = IntCode(instructions, inputs)



def update(maze, pos, outcome):
    # new_pos = pos + directions[direction]
    if outcome == Report.WALL:
        maze[pos] = Maze.WALL
    elif outcome == Report.MOVED:
        maze[pos] = Maze.SPACE
    elif outcome == Report.FOUND:
        maze[pos] = Maze.OXYGEN
    else:
        raise ValueError(f"invalid outcome '{outcome}'")


step_count = -1
plt.figure(figsize=(10, 10), dpi=200)
plot_path = Path('./plots-2019-15/')
plot_path.mkdir(exist_ok=True)


def recurse_through_maze(maze, cur_pos, depth=1, draw_map=False, verbose=False):

    global step_count
    if verbose:
        print(f"D{depth:4d}")

    for dir_, move in directions.items():

        step_count += 1
        if verbose:
            print(f"D{depth:4d}:    {step_count:3d}: {repr(cur_pos)}")
            print(f"D{depth:4d}:    {step_count:3d}: {repr(dir_)}")

        new_pos = cur_pos + move

        if maze[new_pos] != 0:
            if verbose:
                print(f"D{depth:4d}:    {step_count:3d}: SKIPPED")
            continue

        inputs.append(dir_)

        output, rc = droid.intcode()
        out = output[0]
        if verbose:
            print(f"D{depth:4d}:    {step_count:3d}: {repr(Report(out))}")

        update(maze, new_pos, out)


        if draw_map and step_count % 1 == 0 and step_count > 0:
            maze[cur_pos] = Maze.CUR_POS
            plt.imshow(maze)
            plt.title(str(step_count))
            plt.savefig(plot_path / f"15a-{step_count:04d}.png")
            maze[cur_pos] = Maze.SPACE
            plt.clf()

        if out == Report.MOVED or out == Report.FOUND:
            recurse_through_maze(maze, new_pos, depth=depth+1,
                                 draw_map=draw_map, verbose=verbose)
            # undo move:
            inputs.append(inv_directions[dir_])
            output, rc = droid.intcode()

        if out == Report.FOUND:
            print(f"Found it! {depth} steps taken from the start")

        if rc == ReturnCode.BREAK:
            break
        if rc == ReturnCode.ERROR:
            raise Exception("Intcode stopped with an error")


recurse_through_maze(maze, cur_pos=pos, draw_map=False)

plt.imshow(maze)
plt.title(str(step_count))
plt.savefig(plot_path / f"15a-{step_count:04d}.png")
plt.clf()
