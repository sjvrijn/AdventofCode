from pathlib import Path
import re

import parse
from pyprojroot import here


def a(instructions):
    """Solve day 2 part 1"""
    template = "mul({a:d},{b:d})"
    return sum(match["a"]*match["b"] for match in parse.findall(template, instructions))


def b(instructions):
    """Solve day 2 part 2"""
    mul = r"mul\((\d+),(\d+)\)"
    do = r"do\(\)"
    dont = r"don\'t\(\)"

    all_patterns = r"|".join([mul, do, dont])

    sum_multiplications = 0
    do_mul = True
    for match in re.finditer(all_patterns, instructions):
        if match.group(0) == "do()":
            do_mul = True
            continue
        elif match.group(0) == "don't()":
            do_mul = False
            continue

        if do_mul:
            sum_multiplications += int(match.group(1)) * int(match.group(2))

    return sum_multiplications


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    instructions = f.read_text()

    return instructions


def main():
    """Main function to wrap variables"""
    files = [
        here('Sander/2024/inputs/input3-test1.txt'),
        here('Sander/2024/inputs/input3-test2.txt'),
        here('Sander/2024/inputs/input3.txt'),
    ]
    for filename in files:
        print(filename)
        instructions = parse_file(Path(filename))

        print(f'A: {a(instructions)}')
        print(f'B: {b(instructions)}')


if __name__ == '__main__':
    main()
