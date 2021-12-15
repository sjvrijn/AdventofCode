from collections import Counter
from functools import reduce
from operator import add

from more_itertools import pairwise
import parse


RULE_CACHE = {}  # global cache to allow function recursion


def a(data):
    c = calc_element_counts(data, 10)
    return c[0][1] - c[-1][1]


def b(data):
    c = calc_element_counts(data, 40)
    return c[0][1] - c[-1][1]


def calc_element_counts(data, n):
    template, rules = data
    counts = [cached_apply_rule(pair, n, rules) for pair in pairwise(template)]
    counts = reduce(add, counts)
    counts[template[-1]] += 1
    return counts.most_common()


def cached_apply_rule(pair, depth, rules):
    if (pair, depth) in RULE_CACHE:
        return RULE_CACHE[(pair, depth)]

    a, b = pair
    template = ''.join([a, rules[(a,b)], b])
    if depth == 1:
        counts = Counter(template[:2])
    else:
        part1 = cached_apply_rule(template[:2], depth-1, rules)
        part2 = cached_apply_rule(template[-2:], depth-1, rules)
        counts = part1 + part2

    RULE_CACHE[(pair, depth)] = counts
    return counts


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
        RULE_CACHE = {}  # clear cache for each new set of rules
        print(filename)
        with open(filename) as f:
            lines = f.read().splitlines()  # multi-line file
        data = parse_input(lines)

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')
