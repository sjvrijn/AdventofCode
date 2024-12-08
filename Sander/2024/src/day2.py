from itertools import pairwise
from pathlib import Path

from pyprojroot import here


def a(reports):
    """Solve day 2 part 1"""
    return sum(is_safe(report) for report in reports)


def is_safe(report):
    """A report is safe if all levels are either increasing or decreasing by 1, 2, or 3"""
    return (
        all(1 <= x-y <= 3 for x, y in pairwise(report)) or  # decreasing
        all(1 <= y-x <= 3 for x, y in pairwise(report))     # increasing
    )


def b(reports):
    """Solve day 2 part 2"""
    return sum(is_safe(report) or can_be_dampened(report) for report in reports)


def can_be_dampened(report):
    """A problem report can be dampened if it is safe with one level removed"""
    for omit_idx in range(len(report)):
        if is_safe(report[:omit_idx] + report[omit_idx+1:]):
            return True
    return False


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    reports = [list(map(int, line.split())) for line in f.read_text().splitlines()]
    return reports


def main():
    """Main function to wrap variables"""
    files = [
        'Sander/2024/inputs/input2-test1.txt',
        'Sander/2024/inputs/input2.txt',
    ]
    for filename in files:
        print(filename)
        reports = parse_file(here(filename))

        print(f'A: {a(reports)}')
        print(f'B: {b(reports)}')


if __name__ == '__main__':
    main()
