from pathlib import Path

import numpy as np
import parse


def calc_distances(valves):
    adjacency = np.eye(len(valves), dtype=int)
    valve_names = sorted(valves.keys())
    valve_indices = {
        valve: idx
        for idx, valve in enumerate(valve_names)
    }
    # fill adjacency matrix
    for valve, (_, tunnels) in valves.items():
        vidx = valve_indices[valve]
        for tunnel in tunnels:
            tidx = valve_indices[tunnel]
            adjacency[vidx, tidx] = 1

    # calc distances (https://en.wikipedia.org/wiki/Adjacency_matrix#Matrix_powers)
    distances = np.copy(adjacency)
    paths = np.copy(adjacency)
    dist = 2
    while np.sum(distances == 0):
        paths = np.dot(paths, adjacency)
        distances[(paths > 0) & (distances == 0)] = dist
        dist += 1

    return distances


def a(valves):
    """Solve day 16 part 1"""
    distances = calc_distances(valves)
    print(distances)


def b(valves):
    """Solve day 16 part 2"""
    pass


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    template = parse.compile("Valve {} has flow rate={:d}; {tunnel:w} {leads:w} to {valve:w} {}")
    lines = f.read_text().splitlines()
    valves = {}
    for line in lines:
        valve, flow, tunnels = template.parse(line).fixed
        valves[valve] = (flow, tunnels.split(', '))
    return valves


def main():
    """Main function to wrap variables"""
    files = [
        'input16-test1.txt',
        'input16.txt',
    ]

    np.set_printoptions(linewidth=80, edgeitems=10)

    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        # print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
