from copy import deepcopy
from pathlib import Path

import parse


def a(stacks, moves):
    """Solve day 05 part 1"""
    for num, from_stack, to_stack in moves:
        # adjust for 0-indexing
        to_stack, from_stack = to_stack-1, from_stack-1
        stacks[to_stack] = stacks[from_stack][:num][::-1] + stacks[to_stack]
        stacks[from_stack] = stacks[from_stack][num:]
    return ''.join(stack[0] for stack in stacks)


def b(stacks, moves):
    """Solve day 06 part 2"""
    for num, from_stack, to_stack in moves:
        # adjust for 0-indexing
        to_stack, from_stack = to_stack-1, from_stack-1
        stacks[to_stack] = stacks[from_stack][:num] + stacks[to_stack]
        stacks[from_stack] = stacks[from_stack][num:]
    return ''.join(stack[0] for stack in stacks)


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    move_template = parse.compile("move {:d} from {:d} to {:d}")
    lines = f.read_text().splitlines()

    stack_lines = []
    for line in lines:
        if '[' in line:
            stack_lines.append(line[1::4])
        else:
            break
    stacks = [''.join(stack).strip() for stack in zip(*stack_lines)]
    moves = [move_template.parse(line).fixed for line in lines if 'move' in line]

    return stacks, moves

def main():
    """Main function to wrap variables"""
    files = [
        'input05-test1.txt',
        'input05.txt',
    ]
    for filename in files:
        print(filename)
        stacks, moves = parse_file(Path(filename))

        print(f'A: {a(deepcopy(stacks), moves)}')
        print(f'B: {b(stacks, moves)}')


if __name__ == '__main__':
    main()
