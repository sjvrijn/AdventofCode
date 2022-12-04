from pathlib import Path

import parse


def a(sections):
    """Solve day 04 part 1"""
    return sum(
        (a <= c and d <= b) or (c <= a and b <= d)
        for a, b, c, d in sections
    )


def b(sections):
    """Solve day 04 part 2"""
    return sum(
        a <= c <= b or a <= d <= b or c <= a <= d or c <= b <= d
        for a, b, c, d in sections
    )


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    template = parse.compile("{:d}-{:d},{:d}-{:d}")
    lines = f.read_text().splitlines()
    return [template.parse(line).fixed for line in lines]


def main():
    """Main function to wrap variables"""
    files = [
        'input04-test1.txt',
        'input04.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
