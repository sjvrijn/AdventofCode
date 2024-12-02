from collections import Counter
from pathlib import Path

from pyprojroot import here


def a(id_lists):
    """Solve day 1 part 1"""
    sorted_ids = [sorted(ids) for ids in id_lists]
    return sum(abs(a-b) for a, b in zip(*sorted_ids))


def b(id_lists):
    """Solve day 1 part 2"""
    left, right = [Counter(id_list) for id_list in id_lists]
    return sum(num * left[num] * right[num] for num in left.keys())


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = f.read_text().splitlines()
    values = (map(int, line.split()) for line in lines)
    id_lists = list(zip(*values))

    return id_lists


def main():
    """Main function to wrap variables"""
    files = [
        '2024/inputs/input1-test1.txt',
        '2024/inputs/input1.txt',
    ]
    for filename in files:
        print(filename)
        id_lists = parse_file(here(filename))

        print(f'A: {a(id_lists)}')
        print(f'B: {b(id_lists)}')


if __name__ == '__main__':
    main()
