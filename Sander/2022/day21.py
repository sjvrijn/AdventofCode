from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

from more_itertools import chunked
import numpy as np
import parse


class MonkeyMath:
    def __init__(self, monkeys):
        self.monkeys = monkeys
        self.cached = {}

    def calc(self, monkey):
        result = self.cached.get(monkey, None)
        if result is not None:
            return result

        result = self.monkeys[monkey]
        if isinstance(result, int):
            self.cached[monkey] = result
            return result

        monkey_a, operand, monkey_b = result
        if operand == '+':
            result = self.calc(monkey_a) + self.calc(monkey_b)
        elif operand == '-':
            result = self.calc(monkey_a) - self.calc(monkey_b)
        elif operand == '*':
            result = self.calc(monkey_a) * self.calc(monkey_b)
        elif operand == '/':
            result = self.calc(monkey_a) // self.calc(monkey_b)
        self.cached[monkey] = result
        return result

    def equality_calc(self, monkey):
        result = self.cached.get(monkey, None)
        if result is not None:
            return result
        if monkey == 'humn':
            return 'humn'

        result = self.monkeys[monkey]
        if isinstance(result, int):
            self.cached[monkey] = result
            return result

        monkey_a, operand, monkey_b = result
        result_a = self.equality_calc(monkey_a)
        result_b = self.equality_calc(monkey_b)

        if monkey == 'root':
            result = (result_a, '=', result_b)
        elif isinstance(result_a, tuple) or isinstance(result_b, tuple)\
                or 'humn' in [result_a, result_b]:
            result = (result_a, operand, result_b)
        elif operand == '+':
            result = result_a + result_b
        elif operand == '-':
            result = result_a - result_b
        elif operand == '*':
            result = result_a * result_b
        elif operand == '/':
            result = result_a // result_b
        self.cached[monkey] = result
        return result


def solve_equation(equation):
    while isinstance(equation, tuple):
        ab, eq, c = equation
        if isinstance(c, tuple):
            ab, c = c, ab
        if not isinstance(ab, tuple):
            return c

        a, operand, b = ab
        if isinstance(a, tuple) or a == 'humn':
            if operand == '+':
                c = c - b
            elif operand == '-':
                c = c + b
            elif operand == '*':
                c = c // b
            elif operand == '/':
                c = c * b
            equation = (a, '=', c)
        elif isinstance(b, tuple) or b == 'humn':
            if operand == '+':
                c = c - a
            elif operand == '-':
                c = a - c
            elif operand == '*':
                c = c // a
            elif operand == '/':
                c = a // c
            equation = (b, '=', c)


def a(monkeys):
    """Solve day 21 part 1"""
    mmath = MonkeyMath(monkeys)
    return mmath.calc('root')


def b(monkeys):
    """Solve day 21 part 2"""
    mmath = MonkeyMath(monkeys)
    equation = mmath.equality_calc('root')
    result = solve_equation(equation)
    return result

def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    leaf_template = parse.compile("{:w}: {:d}")
    node_template = parse.compile("{:w}: {:w} {} {:w}")
    lines = f.read_text().splitlines()
    monkeys = {}
    for line in lines:
        if match := leaf_template.parse(line):
            monkeys[match[0]] = match[1]
        else:
            match = node_template.parse(line)
            monkeys[match[0]] = match[1:]

    return monkeys


def main():
    """Main function to wrap variables"""
    files = [
        'input21-test1.txt',
        'input21.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
