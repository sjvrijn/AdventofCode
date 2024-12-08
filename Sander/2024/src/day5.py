from collections import defaultdict
from copy import copy
from pathlib import Path

from pyprojroot import here


def a(rules, page_lists):
    """Solve day 5 part 1"""
    middle_sum = 0
    for page_list in page_lists:
        if is_correctly_ordered(rules, page_list):
            middle = len(page_list) // 2
            middle_sum += page_list[middle]
    return middle_sum


def is_correctly_ordered(rules, page_list):
    illegal_pages = set()
    for page in page_list:
        if page in illegal_pages:
            return False
        illegal_pages = illegal_pages.union(rules[page])
    return True


def b(rules, page_lists):
    """Solve day 5 part 2"""
    middle_sum = 0
    for page_list in page_lists:
        if not is_correctly_ordered(rules, page_list):
            page_list = order(rules, page_list)

            middle = len(page_list) // 2
            middle_sum += page_list[middle]
    return middle_sum


def order(rules, page_list):
    page_list = copy(page_list)
    # 'bubble sort' through the list: swapping elements in incorrect order
    for before in range(len(page_list)):
        for after in range(before+1, len(page_list)):
            if page_list[after] in rules[page_list[before]]:
                page_list[before], page_list[after] = page_list[after], page_list[before]
    return page_list


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = iter(f.read_text().splitlines())  # iterate only once over all lines
    rules = defaultdict(set)
    for line in lines:
        try:
            before, after = map(int, line.split('|'))
        except ValueError:
            break
        rules[after].add(before)

    page_lists = [list(map(int, line.split(','))) for line in lines]

    return rules, page_lists


def main():
    """Main function to wrap variables"""
    files = [
        'Sander/2024/inputs/input5-test1.txt',
        # 'Sander/2024/inputs/input5-test2.txt',
        # 'Sander/2024/inputs/input5-test3.txt',
        'Sander/2024/inputs/input5.txt',
    ]
    for filename in files:
        print(filename)
        rules, page_lists = parse_file(here(filename))

        print(f'A: {a(rules, page_lists)}')
        print(f'B: {b(rules, page_lists)}')


if __name__ == '__main__':
    main()
