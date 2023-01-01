from pathlib import Path

import numpy as np


def a(cubes):
    """Solve day 18 part 1"""
    NEIGHBORS = np.array((
        (0,0,0,0,1,-1),
        (0,0,1,-1,0,0),
        (1,-1,0,0,0,0),
    ))

    boulder = np.zeros((25, 25, 25), dtype=int)
    exposed_sides = 0
    for cube in cubes:
        boulder[cube] = 1
        neighbors = np.array([cube]).T + NEIGHBORS
        exposed_sides += 6
        exposed_sides -= 2 * np.sum(boulder[neighbors[0], neighbors[1], neighbors[2]])
    return exposed_sides


def b(cubes):
    """Solve day 18 part 2"""
    NEIGHBORS = (
        (0,0,1),
        (0,0,-1),
        (0,1,0),
        (0,-1,0),
        (1,0,0),
        (-1,0,0),
    )
    AIR = 0
    LAVA = 1
    STEAM = 3
    boulder = np.zeros((22, 22, 22), dtype=int)
    for cube in cubes:
        boulder[cube] = LAVA

    expanding_steam = {(0,0,0)}
    while expanding_steam:
        steam = expanding_steam.pop()
        boulder[steam] = STEAM
        for nx, ny, nz in NEIGHBORS:
            x, y, z = steam[0]+nx, steam[1]+ny, steam[2]+nz
            x_in_bounds = 0 <= x < boulder.shape[0]
            y_in_bounds = 0 <= y < boulder.shape[1]
            z_in_bounds = 0 <= z < boulder.shape[2]
            if not (x_in_bounds and y_in_bounds and z_in_bounds):
                continue
            if boulder[x,y,z] == AIR:
                expanding_steam.add((x,y,z))

    A = np.sum(np.abs(boulder[1:,:,:] - boulder[:-1,:,:]) == STEAM-LAVA)
    B = np.sum(np.abs(boulder[:,1:,:] - boulder[:,:-1,:]) == STEAM-LAVA)
    C = np.sum(np.abs(boulder[:,:,1:] - boulder[:,:,:-1]) == STEAM-LAVA)
    D = np.sum((boulder[0,:,:] == LAVA) + (boulder[:,0,:] == LAVA) + (boulder[:,:,0] == LAVA))

    return A+B+C+D


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = f.read_text().splitlines()
    return [tuple(map(int, line.split(','))) for line in lines]


def main():
    """Main function to wrap variables"""
    files = [
        # 'input18-test1.txt',
        # 'input18-test2.txt',
        'input18.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
