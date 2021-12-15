from collections import Counter

from more_itertools import pairwise
import parse


def a(data):
    template, rules = data
    for _ in range(10):
        template = apply_rules(template, rules)
    c = Counter(template).most_common()
    return c[0][1] - c[-1][1]


def b(data):
    template, rules = data
    for _ in range(40):
        template = apply_rules(template, rules)
    c = Counter(template).most_common()
    return c[0][1] - c[-1][1]


def apply_rules(template, rules):
    new_template = []
    for a, b in pairwise(template):
        new_template.extend([a, rules[(a, b)]])
    new_template.append(template[-1])
    return ''.join(new_template)


def parse_input(lines):
    template = lines[0]
    parse_rule = parse.compile('{}{} -> {}')
    rules = {}
    for line in lines[2:]:
        a, b, c = parse_rule.parse(line)
        rules[(a, b)] = c
    return template, rules


if __name__ == '__main__':
    files = [
        'input14-test1.txt',
        'input14.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            lines = f.read().splitlines()  # multi-line file
        data = parse_input(lines)

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')
