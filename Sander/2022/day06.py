from pathlib import Path

from more_itertools import windowed


def a(signal):
    """Solve day 06 part 1"""
    for idx, window in enumerate(windowed(signal, 4), start=4):
        if len(set(window)) == 4:
            return idx


def b(signal):
    """Solve day 06 part 2"""
    for idx, window in enumerate(windowed(signal, 14), start=14):
        if len(set(window)) == 14:
            return idx


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    return f.read_text()


def main():
    """Main function to wrap variables"""
    files = [
        'input06-test1.txt',
        'input06-test2.txt',
        'input06-test3.txt',
        'input06.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
