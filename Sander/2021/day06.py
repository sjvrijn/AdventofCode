from collections import Counter

import numpy as np


def simulate(timers, n):
    """Inefficient implementation initially used for A.
    Efficient implementation was coded faster than this one could run for B.
    """
    timers = np.array(timers)
    for _ in range(n):
        timers -= 1
        where_to_reset = timers == -1
        num_to_add = sum(where_to_reset)
        timers[where_to_reset] = 6
        if num_to_add > 0:
            timers = np.append(timers, [8]*num_to_add)

    return len(timers)


def simulate2(timers, n):
    counts = Counter(timers)
    timers = [counts[i] for i in range(7)] + [0, 0]
    for _ in range(n):
        num_spawning = timers[0]
        timers[7] += num_spawning
        timers[:8] = timers[1:]
        timers[8] = num_spawning

    return sum(timers)


def a(timers):
    return simulate2(timers, n=80)

def b(timers):
    return simulate2(timers, n=256)


if __name__ == '__main__':
    files = [
        'input06-test1.txt',
        'input06.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            line = f.read().strip()
        timers = list(map(int, line.split(',')))

        print(f'A: {a(timers)}')
        print(f'B: {b(timers)}')
