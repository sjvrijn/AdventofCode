from pathlib import Path

from more_itertools import chunked


def calc_priority(char):
    value = ord(char) - 38
    return value if value <= 52 else value-58


def a(lines):
    """Solve day 03 part 1"""
    half_lengths = [len(line)//2 for line in lines]
    items = [set(line[:hl]) & set(line[hl:]) for hl, line in zip(half_lengths, lines)]
    return sum(calc_priority(item.pop()) for item in items)


def b(lines):
    """Solve day 03 part 2"""
    return sum(
        calc_priority((set(elf1) & set(elf2) & set(elf3)).pop())
        for elf1, elf2, elf3 in chunked(lines, 3)
    )



def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    return f.read_text().splitlines()


def main():
    """Main function to wrap variables"""
    files = [
        'input03-test1.txt',
        'input03.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
