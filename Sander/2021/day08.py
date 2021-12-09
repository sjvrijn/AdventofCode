from collections import Counter
from itertools import chain
from typing import Iterable


def a(lines):
    num_1478 = 0
    for line in lines:
        for pattern in line[1].split():
            if len(pattern) in [2, 3, 4, 7]:
                num_1478 += 1
    return num_1478


def b(lines):
    value_total = 0
    for signals, digits in lines:
        mapping = identify_numbers(list(map(set, signals.split())))
        digits = [''.join(sorted(d)) for d in digits.split()]
        value = int(''.join(mapping[d] for d in digits))
        value_total += value

    return value_total


def identify_numbers(signals: Iterable[set]):
    """Given a set of 10 signals, returns a mapping {signal: 0...9}"""
    identify_by_length = {2: 1, 3: 7, 4: 4, 5: None, 6: None, 7: 8}
    signals_235, signals_690 = [], []
    mapping = {n: None for n in range(10)}

    # identify 1, 4, 7 and 8
    # meanwhile, keep rest separate by length for later
    for s in signals:
        if n := identify_by_length[len(s)]:
            mapping[n] = s
        elif len(s) == 5:
            signals_235.append(s)
        else:
            signals_690.append(s)

    # identify 2
    # segment f appears in all except 2
    [(f, _)] = Counter(chain.from_iterable(signals)).most_common(1)
    for s in signals:
        if f not in s:
            mapping[2] = s
            break
    signals_235.remove(mapping[2])

    # identify 3 and 5
    # of len(signal) == 5: 2 and 3 match in 3 segments, 2 and 5 match in 4
    if len(signals_235[0].intersection(mapping[2])) == 4:
        mapping[3], mapping[5] = signals_235[0], signals_235[1]
    else:
        mapping[3], mapping[5] = signals_235[1], signals_235[0]

    # identify 6
    c = mapping[1].intersection(mapping[2])
    mapping[6] = mapping[8] - c
    signals_690.remove(mapping[6])

    # identify 9
    e = mapping[2].difference(mapping[3])
    mapping[9] = mapping[8] - e
    signals_690.remove(mapping[9])

    # identify 0
    mapping[0] = signals_690.pop()

    return {  # invert mapping
        ''.join(sorted(signal)): str(num)
        for num, signal in mapping.items()
    }


if __name__ == '__main__':
    files = [
        'input08-test1.txt',
        'input08-test2.txt',
        'input08.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            lines = [l.split(' | ') for l in f.read().splitlines()]

        print(f'A: {a(lines)}')
        print(f'B: {b(lines)}')
