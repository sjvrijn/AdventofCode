from collections import defaultdict
from dataclasses import dataclass
from itertools import count, product
from pathlib import Path
from math import sqrt

import matplotlib.pyplot as plt
import parse


@dataclass
class State:
    x: int
    y: int
    dx: int
    dy: int

    def __next__(self):
        return State(
            self.x + self.dx,
            self.y + self.dy,
            max(self.dx-1, 0),
            self.dy-1
        )

    def __gt__(self, other: 'Target'):
        return self.x > other.xmax or self.y < other.ymin


@dataclass(init=False)
class Target:
    xmin: int
    xmax: int
    ymin: int
    ymax: int

    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.xrange = range(xmin, xmax+1)
        self.yrange = range(ymin, ymax+1)

    def __contains__(self, item: State):
        return item.x in self.xrange and item.y in self.yrange


def a(target, strict=False):
    """Solve day 17 part 1"""
    if strict:
        # assert target's xrange can be easily reached
        x_reached = False
        for dx in count():
            end_x = dx*(dx+1)
            if end_x in target.xrange:
                x_reached = True
                print(f'Target can be reached easily with {dx=}')
                break
            if end_x > target.xmax:
                break
        assert x_reached

    best_dy = abs(target.ymin) - 1
    return best_dy*(best_dy+1)//2  # max_height


def b(target):
    """Solve day 17 part 2"""

    # for dy = -target.ymin ... best_dy:
    #     determine number of simulation steps to reach target.yrange
    yspeeds_by_num_steps = defaultdict(list)
    for dy in range(target.ymin, abs(target.ymin)):
        first_step, last_step = steps_to_target(dy, target, is_x=False)
        # print(dy, first_step, last_step)
        if first_step:
            for step in range(first_step, last_step):
                yspeeds_by_num_steps[step].append(dy)

    max_y_steps = max(yspeeds_by_num_steps.keys()) + 1

    # Given that n**2 < 2x < (n+1)**2  (from x = n*(n+1)/2 )
    # for dx ~= sqrt(2*target.xmin) ... target.xmax:
    #     determine number of simulation steps to reach target.xrange
    xspeeds_by_num_steps = defaultdict(list)
    for dx in range(int(sqrt(2*target.xmin)), target.xmax+1):
        first_step, last_step = steps_to_target(dx, target, is_x=True)
        # print(dx, first_step, last_step)
        if first_step:
            for step in range(first_step, min(last_step, max_y_steps)):
                xspeeds_by_num_steps[step].append(dx)

    num_steps = set(xspeeds_by_num_steps.keys()).union(set(yspeeds_by_num_steps.keys()))
    velocities = set()
    for n in num_steps:
        for dx, dy in product(xspeeds_by_num_steps[n], yspeeds_by_num_steps[n]):
            velocities.add((dx, dy))

    return len(velocities)


def steps_to_target(dxy, target, is_x):

    xyrange = target.xrange if is_x else target.yrange
    xy = 0
    first_step = None
    for num_steps in count():
        if not first_step and xy in xyrange:
            first_step = num_steps
        if (is_x and xy > target.xmax) or (not is_x and xy < target.ymin):
            last_step = num_steps
            break
        if is_x and dxy == 0:
            last_step = float('inf')
            break
        xy += dxy
        dxy -= 1

    return first_step, last_step


def simulate(target, state, plot=False):
    states = [state]
    for step in count():
        print(state)
        state = next(state)
        states.append(state)
        if state in target:
            print(state)
            print(f'Target reached in {step} steps')
            break
        if state > target:
            print(state)
            print(f'Target overshot after {step} steps')
            break

    maxy = max(s.y for s in states)
    init_dy = states[0].dy
    print(f'Max height: {maxy}; dy(dy+1)/2 = {init_dy*(init_dy+1)//2}')

    if plot:
        plt.plot(*zip(*[(s.x, s.y) for s in states]))
        plt.show()


def parse_file(filename: Path):
    """Parse the input file into relevant data structure"""
    line = filename.read_text()
    template = 'target area: x={:d}..{:d}, y={:d}..{:d}'
    params = parse.parse(template, line).fixed
    return Target(*params)


def main():
    """Main function to wrap variables"""
    files = [
        'input17-test1.txt',
        'input17.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data, strict=True)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
