from pathlib import Path


def a(elves):
    """Solve day 1 part 1"""
    return max(sum(map(int, elf)) for elf in elves)


def b(elves):
    """Solve day 1 part 2"""
    return sum(sorted(sum(map(int, elf)) for elf in elves)[-3:])


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = f.read_text().split('\n\n')
    return [elf.splitlines() for elf in lines]


def main():
    """Main function to wrap variables"""
    files = [
        'input01-test1.txt',
        'input01.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
