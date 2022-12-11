from copy import deepcopy
from math import prod
from pathlib import Path


class Monkey:

    def __init__(self, items, operation, div_test, throws, all_monkeys):
        self.items = items
        self.operation = operation
        self.div_test = div_test
        self.throw_true, self.throw_false = throws
        self.all_monkeys = all_monkeys
        self.num_inspections = 0

    def operate_item(self, item, worry_reduces=True, max_mod=None):
        self.num_inspections += 1
        new_worry = self.operation(item)
        if worry_reduces:
            new_worry //= 3
        if max_mod:
            new_worry %= max_mod
        if new_worry % self.div_test == 0:
            next_monkey = self.throw_true
        else:
            next_monkey = self.throw_false
        self.all_monkeys[next_monkey].items.append(new_worry)

    def take_turn(self, worry_reduces=True, max_mod=None):
        while self.items:
            self.operate_item(self.items.pop(0), worry_reduces=worry_reduces, max_mod=max_mod)


def a(all_monkeys):
    """Solve day 11 part 1"""
    for _ in range(20):
        for monkey in all_monkeys:
            monkey.take_turn()
    inspections = list(sorted(m.num_inspections for m in all_monkeys))
    return inspections[-1] * inspections[-2]


def b(all_monkeys):
    """Solve day 11 part 2"""
    max_mod = prod(m.div_test for m in all_monkeys)
    for _ in range(10_000):
        for monkey in all_monkeys:
            monkey.take_turn(worry_reduces=False, max_mod=max_mod)
    inspections = list(sorted(m.num_inspections for m in all_monkeys))
    return inspections[-1] * inspections[-2]


def parse_operation(op_line):
    op, val = op_line[23:].split()
    if op == '*':
        return (lambda x: x*x) if val == 'old' else (lambda x: x*int(val))
    elif op == '+':
        return lambda x: x + int(val)


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    monkey_specs = f.read_text().split('\n\n')
    all_monkeys = []
    for spec in monkey_specs:
        lines = spec.splitlines()
        items = list(map(int, lines[1][18:].split(', ')))
        operation = parse_operation(lines[2])
        div_test = int(lines[3][21:])
        throws = int(lines[4][29:]), int(lines[5][30:])
        all_monkeys.append(Monkey(items, operation, div_test, throws, all_monkeys))
    return all_monkeys


def main():
    """Main function to wrap variables"""
    files = [
        'input11-test1.txt',
        'input11.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(deepcopy(data))}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
