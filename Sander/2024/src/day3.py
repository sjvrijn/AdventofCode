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
    #    r"         # use a raw string to avoid having to do extra 'escaping' (https://docs.python.org/3/reference/lexical_analysis.html#escape-sequences)
    #      do       # match the text "do"
    #        \(     # match an open bracket '('
    #          \)   # match a closing bracket ')'
    #            "  # end the string
    do = r"do\(\)"
    #      r"            # use a raw string
    #        don't       # match the text "don't"
    #             \(\)   # match the open and close brackets ()
    #                 "  # end the string
    dont = r"don\'t\(\)"
    #     r"                     # use a raw string
    #       mul\(                # match the text "mul("
    #            (               # open a 'group' so we can extract the value from it
    #             \d+            # \d means a digit [0-9], and + means 1 or more of them sequentially
    #                )           # close the group, so match only the aforementioned set of digits
    #                 ,          # match a plain comma ","
    #                  (\d+)     # open and match another group searching for a set of digits (see above)
    #                       \)   # match a closing bracket ")"
    #                         "  # end the string
    mul = r"mul\((\d+),(\d+)\)"

    # "|" means 'or', so if we have three smaller expressions A, B and C,  r"A|B|C" will match any one of them
    all_patterns = r"|".join([mul, do, dont])

    sum_multiplications = 0
    do_mul = True

    # `re.findall()` would only return the matched strings, but we still want to access the matched groups
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
