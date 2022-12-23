import math
from pathlib import Path

import parse

RESOURCE_IDX = {'geode': 3, 'obsidian': 2, 'clay': 1, 'ore': 0}

class State:
    def __init__(self, blueprint, minutes, resources=None, robots=None, max_robots=None):
        self.blueprint = blueprint
        self.minutes = minutes
        if resources is None:
            self.resources = (0, 0, 0, 0)
            self.robots = (1, 0, 0, 0)
            self.max_robots = {
                'ore':      max(blueprint['ore'][0], blueprint['clay'][0], blueprint['obsidian'][0], blueprint['geode'][0]),
                'clay':     max(blueprint['ore'][1], blueprint['clay'][1], blueprint['obsidian'][1], blueprint['geode'][1]),
                'obsidian': max(blueprint['ore'][2], blueprint['clay'][2], blueprint['obsidian'][2], blueprint['geode'][2]),
                'geode':    minutes,
            }
        else:
            self.resources = resources
            self.robots = robots
            self.max_robots = max_robots

    def __repr__(self):
        return f"<State({self.minutes}] {self.resources} from {self.robots})>"
    __str__ = __repr__


    def harvest(self, resources):
        return tuple(
            current + robots
            for current, robots in zip(resources, self.robots)
        )

    def add_robot(self, robot):
        new_robot = [0,0,0,0]
        new_robot[RESOURCE_IDX[robot]] = 1
        return tuple(r+n for r, n in zip(self.robots, new_robot))

    def try_to_buy_robot(self, robot):
        if self.minutes == 1:
            resources = self.harvest(self.resources)
            return State(self.blueprint, 0, resources, self.robots, self.max_robots)

        if self.max_robots[robot] <= self.robots[RESOURCE_IDX[robot]]:
            raise ValueError

        cost = self.blueprint[robot]

        if (cost[1] > 0 and self.robots[1] == 0) or (cost[2] > 0 and self.robots[2] == 0):
            raise ValueError

        minutes_left = self.minutes
        resources = self.resources
        while any(r < c for r, c in zip(resources, cost)):
            resources = self.harvest(resources)
            minutes_left -= 1
            if minutes_left == 1:
                resources = self.harvest(self.resources)
                return State(self.blueprint, 0, resources, self.robots, self.max_robots)

        resources = tuple(r-c for r, c in zip(resources, cost))
        robots = self.add_robot(robot)
        resources = self.harvest(resources)
        return State(self.blueprint, minutes_left-1, resources, robots, self.max_robots)

    def max_possible_geodes(self):
        triangle_max = ((self.minutes-1)*(self.minutes) // 2)
        return self.resources[3] + (self.robots[3] * self.minutes) + triangle_max


def calc_max_geodes(blueprint, time_left):
    states = [State(blueprint, time_left)]
    best_state = None
    cur_max_geodes = 0


    while states:
        state = states.pop(0)
        if state.max_possible_geodes() < cur_max_geodes:
            continue

        for robot in RESOURCE_IDX.keys():
            try:
                new_state = state.try_to_buy_robot(robot)
            except ValueError:
                continue
            if new_state.minutes == 0:
                if new_state.resources[3] > cur_max_geodes:
                    best_state = new_state
                    cur_max_geodes = new_state.resources[3]
            else:
                states.insert(0, new_state)
                # states.append(new_state)

    print(best_state)
    return cur_max_geodes


def a(blueprints):
    """Solve day 19 part 1"""
    return sum(
        calc_max_geodes(blueprint, 24) * bp_id
        for bp_id, blueprint in enumerate(blueprints, start=1)
    )


def b(blueprints):
    """Solve day 19 part 2"""
    max_geodes = [
        calc_max_geodes(blueprint, 32)
        for blueprint in blueprints[:3]
    ]
    # wrong answer: 437976
    return math.prod(sorted(max_geodes)[-3:])


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    # Blueprint 1:
    #   Each ore robot costs 4 ore.
    #   Each clay robot costs 2 ore.
    #   Each obsidian robot costs 3 ore and 14 clay.
    #   Each geode robot costs 2 ore and 7 obsidian.
    template_single = parse.compile("{type1} robot costs {ore:d} ore.")
    template_double = parse.compile("{type1} robot costs {:d} ore and {:d}{type2}")
    lines = f.read_text().splitlines()
    blueprints = []
    for line in lines:
        _, ore, clay, obsidian, geode = line.split(' Each ')
        blueprints.append({
            'ore': (template_single.parse(ore)['ore'], 0, 0, 0),
            'clay': (template_single.parse(clay)['ore'], 0, 0, 0),
            'obsidian': (*template_double.parse(obsidian).fixed, 0, 0),
            'geode': (template_double.parse(geode)[0], 0, template_double.parse(geode)[1], 0)
        })

    # pprint(blueprints)
    return blueprints


def main():
    """Main function to wrap variables"""
    files = [
        'input19-test1.txt',
        'input19.txt',
    ]

    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
