from copy import copy
from collections import namedtuple


opcodes = [
    'addr', 'addi', 'mulr', 'muli',
    'banr', 'bani', 'borr', 'bori',
    'setr', 'seti', 'gtir', 'gtri',
    'gtrr', 'eqir', 'eqri', 'eqrr',
]


def elf_eval(instruction, A, B, C, registers): 
    reg = copy(registers)

    if instruction == 'addr':
        reg[C] = reg[A] + reg[B]
    elif instruction == 'addi':
        reg[C] = reg[A] + B
    elif instruction == 'mulr':
        reg[C] = reg[A] * reg[B]
    elif instruction == 'muli':
        reg[C] = reg[A] * B
    elif instruction == 'banr':
        reg[C] = reg[A] & reg[B]
    elif instruction == 'bani':
        reg[C] = reg[A] & B
    elif instruction == 'borr':
        reg[C] = reg[A] | reg[B]
    elif instruction == 'bori':
        reg[C] = reg[A] | B
    elif instruction == 'setr':
        reg[C] = reg[A]
    elif instruction == 'seti':
        reg[C] = A
    elif instruction == 'gtir':
        reg[C] = int(A > reg[B])
    elif instruction == 'gtri':
        reg[C] = int(reg[A] > B)
    elif instruction == 'gtrr':
        reg[C] = int(reg[A] > reg[B])
    elif instruction == 'eqir':
        reg[C] = int(A == reg[B])
    elif instruction == 'eqri':
        reg[C] = int(reg[A] == B)
    elif instruction == 'eqrr':
        reg[C] = int(reg[A] == reg[B])
    else:
        raise ValueError(f"Invalid instruction '{instruction}'")

    return reg


Case = namedtuple('Case', ['before', 'inst', 'after'])

    
with open('input16.txt') as f:
    cases = []
    before = next(f).strip()
    while 'Before:' in before:
        before = eval(before[8:])
        inst = tuple(map(int, next(f).split()))
        after = eval(next(f)[8:])
        next(f)

        cases.append(Case(before, inst, after))
        before = next(f)

    next(f)
    program = [list(map(int, line.split())) for line in f]


possible_opcodes = {i: [] for i in range(len(opcodes))}
for case in cases:
    possible = set()
    for op in opcodes:
        if elf_eval(op, *case.inst[1:], case.before) == case.after:
            possible.add(op)
    possible_opcodes[case.inst[0]].append(possible)

# Sanity check, although apparently not actually needed: take intersection
for i, ops in possible_opcodes.items():
    if len(ops) == 1:
        possible_opcodes[i] = ops[0]
    else:
        possible_opcodes[i] = ops[0].intersection(*ops[1:])


indexed_opcodes = {i: None for i in range(len(opcodes))}
while possible_opcodes:
    for i, ops in possible_opcodes.items():
        if len(ops) == 1:
            op = list(ops)[0]
            indexed_opcodes[i] = op
            break
    for ops in possible_opcodes.values():
        ops.discard(op)
    del possible_opcodes[i]


registers = [0, 0, 0, 0]

for instruction, A, B, C in program:
    registers = elf_eval(indexed_opcodes[instruction], A, B, C, registers)

print(registers)
