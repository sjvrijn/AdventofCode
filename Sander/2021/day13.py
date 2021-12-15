import matplotlib.pyplot as plt
import numpy as np
import parse


def a(data):
    points, folds = data
    return len(fold_points(points, *folds[0]))


def b(data):
    points, folds = data
    for axis, n in folds:
        points = fold_points(points, axis, n)

    max_x, max_y = 0, 0
    for x, y in points:
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    grid = np.zeros((max_x+1, max_y+1))
    for x, y in points:
        grid[x,y] = 1
    plt.imshow(grid.T, origin='upper')
    plt.show()


def fold_points(points, axis, n):
    new_points = set()
    for point in points:
        x, y = point
        if axis == 'x' and x > n:
            new_points.add((2*n - x, y))
        elif axis == 'y' and y > n:
            new_points.add((x, 2*n - y))
        else:
            new_points.add(point)
    return new_points


def parse_input(lines):
    parse_point = parse.compile('{:d},{:d}')
    parse_fold = parse.compile('fold along {}={:d}')

    points, folds = [], []
    for line in lines:
        if ',' in line:
            points.append(parse_point.parse(line).fixed)
        elif '=' in line:
            folds.append(parse_fold.parse(line).fixed)

    return points, folds


if __name__ == '__main__':
    files = [
        'input13-test1.txt',
        'input13.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            lines = f.read().splitlines()  # multi-line file
        data = parse_input(lines)

        print(f'A: {a(data)}')
        b(data)
