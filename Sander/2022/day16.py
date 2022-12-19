from pathlib import Path

import numpy as np
import parse
from tqdm import tqdm
import xarray as xr


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

    named_dists = xr.DataArray(data=distances, coords={'src': valve_names, 'tgt': valve_names})

    return named_dists


def calc_max_flow(valves, distances, time_left=30,
                  so_far=None, cur_flow=0, total_flow=0, depth=0):
    if not so_far:
        so_far = ['AA']
    # print(f"{'    '*depth}[t={time_left}], {so_far}, {cur_flow}, ({total_flow})")
    best_flow = 0
    src = so_far[-1]

    if depth < 2:
        iterator = tqdm(valves, leave=False)
    else:
        iterator = valves

    for valve, flow in iterator:
        if valve in so_far:
            continue
        dist = distances.sel(src=src, tgt=valve).values
        if dist >= time_left:
            continue
        # print(f"{'    ' * depth}  {valve}:{flow} @ {dist}")
        next_flow = calc_max_flow(
            valves, distances,
            time_left=time_left-(dist+1),
            so_far=so_far+[valve],
            cur_flow=cur_flow + flow,
            total_flow=total_flow + (cur_flow * (dist+1)),
            depth=depth+1
        )
        best_flow = max(best_flow, next_flow)

    best_flow = max(best_flow, total_flow + (cur_flow * time_left))
    return best_flow

def a(valves):
    """Solve day 16 part 1"""
    distances = calc_distances(valves)
    filtered_valves = tuple(
        (valve, flow)
        for valve, (flow, _) in valves.items()
        if flow != 0
    )
    return calc_max_flow(filtered_valves, distances)


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
