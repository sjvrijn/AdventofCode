from pathlib import Path
from pprint import pprint

import parse

RESOURCE_IDX = {'ore': 0, 'clay': 1, 'obsidian': 2, 'geode': 3}

class State:
    def __init__(self, blueprint, minutes, resources=None, robots=None):
        self.blueprint = blueprint
        self.minutes = minutes
        if resources is None:
            self.resources = (0, 0, 0, 0)
            self.robots = (0, 0, 0, 0)
        else:
            self.resources = resources
            self.robots = robots


    def harvest(self):
        resources = tuple(
            current + robots
            for current, robots in zip(self.resources, self.robots)
        )

    def try_to_buy_robot(self, robot):
        if robot is not None:
            cost = self.blueprint[robot]
            for c, r in zip(cost, self.resources):
                if c > r:
                    raise ValueError


        return


def calc_max_geodes(blueprint, time_left, resources=None, robots=None):
    ...


def a(blueprints):
    """Solve day 19 part 1"""
    ...


def b(blueprints):
    """Solve day 19 part 2"""
    ...


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
            'ore': (template_single.parse(ore)['ore'], 0, 0),
            'clay': (template_single.parse(clay)['ore'], 0, 0),
            'obsidian': (*template_double.parse(obsidian).fixed, 0),
            'geode': (template_double.parse(geode)[0], 0, template_double.parse(geode)[1])
        })

    pprint(blueprints)
    return blueprints


def main():
    """Main function to wrap variables"""
    files = [
        # 'input19-test1.txt',
        'input19.txt',
    ]

    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
