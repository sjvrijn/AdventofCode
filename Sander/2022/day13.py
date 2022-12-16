from functools import cmp_to_key
from itertools import zip_longest
import json
from pathlib import Path

from more_itertools import chunked


def are_in_right_order(packets_1, packets_2, depth=0):
    for a, b in zip_longest(packets_1, packets_2):
        if a is None and b is not None:
            return -1
        if a is not None and b is None:
            return 1
        if isinstance(a, list) or isinstance(b, list):
            if isinstance(a, int):
                a = [a]
            if isinstance(b, int):
                b = [b]
            tmp = are_in_right_order(a, b, depth=depth+1)
            if tmp == 0:
                continue
            else:
                return tmp
        if a < b:
            return -1
        if a > b:
            return 1
    return 0


def a(packets):
    """Solve day 13 part 1"""
    groups = chunked(packets, n=2)
    return sum(i for i, group in enumerate(groups, start=1) if are_in_right_order(*group) == -1)


def b(packets):
    """Solve day 13 part 2"""
    div1, div2 = [[2]], [[6]]
    packets.extend([div1, div2])
    packets.sort(key=cmp_to_key(are_in_right_order))
    # for p in packets:
    #     print(p)
    return (packets.index(div1)+1) * (packets.index(div2)+1)


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = f.read_text().splitlines()
    return [json.loads(line) for line in lines if line]


def main():
    """Main function to wrap variables"""
    files = [
        'input13-test1.txt',
        'input13.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
