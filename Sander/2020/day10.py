import numpy as np
from collections import Counter
from itertools import groupby
from operator import mul
from functools import reduce


def num_possible_combinations(n):
    if n in [0, 1]:
        return 1
    return sum(
        '111' not in binary
        for binary in map(lambda x: bin(x)[2:], range(2 ** (n - 1)))
    )


def a(adapters):
    jolts = [0, *adapters, adapters[-1] + 3]
    print(np.diff(jolts))
    jump_counts = Counter(np.diff(jolts))
    return (jump_counts[1]) * (jump_counts[3])


def b(adapters):
    jolts = [0, *adapters, adapters[-1] + 3]
    jumps = np.diff(jolts)

    num_consecutive_ones = [
        sum(1 for _ in j)
        for i, j in groupby(jumps) if i == 1
    ]
    combos = [num_possible_combinations(n) for n in num_consecutive_ones]
    return reduce(mul, combos, 1)


if __name__ == '__main__':
    with open('input10.txt') as f:
        adapters = sorted([int(line) for line in f])

    print(a(adapters))
    print(b(adapters))
