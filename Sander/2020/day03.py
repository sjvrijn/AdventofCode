def encounter_trees(grid, slope=3, step=1):
    for i, line in enumerate(grid[::step]):
        yield line[(i*slope) % len(line)] == '#'


def a(grid):
    return sum(encounter_trees(grid))


def b(grid):
    total = 1
    for slope in [1, 3, 5, 7]:
        total *= sum(encounter_trees(grid, slope))
    total *= sum(encounter_trees(grid, slope=1, step=2))
    return total


if __name__ == '__main__':
    with open('input03.txt') as f:
        grid = list(line.strip() for line in f.readlines())

    print(a(grid))
    print(b(grid))

