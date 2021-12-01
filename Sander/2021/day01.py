from more_itertools import sliding_window, pairwise


def a(depths):
    return sum(1 for x, y in pairwise(depths) if x < y)


def b(depths):
    window_depths = [sum(window) for window in sliding_window(depths, 3)]
    return a(window_depths)


if __name__ == '__main__':
    files = [
        'input01.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            lines = list(map(int, f.readlines()))

        print(a(lines))
        print(b(lines))
