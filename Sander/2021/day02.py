import numpy as np
import parse


command = parse.compile('{} {:d}')


def a(lines):
    commands = {
        'forward': np.array([1,  0]),
        'down':    np.array([0,  1]),
        'up':      np.array([0, -1]),
    }
    position = np.array([0,0])
    for line in lines:
        c, n = command.parse(line)
        position += commands[c] * n

    return np.product(position)


def b(lines):
    adjust_aim = {
        'down': 1,
        'up': -1,
    }
    position, aim = np.array([0,0]), 0
    for line in lines:
        c, n = command.parse(line)
        if c == 'forward':
            position += np.array([n, n*aim])
        else:
            aim += n * adjust_aim[c]

    return np.product(position)


if __name__ == '__main__':
    files = [
        'input02.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            lines = f.read().splitlines()

        print(f'A: {a(lines)}')
        print(f'B: {b(lines)}')
