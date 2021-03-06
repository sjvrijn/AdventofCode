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
        print(before, before[8:], eval(before[8:]))
        before = eval(before[8:])
        inst = tuple(map(int, next(f).split()))
        after = eval(next(f)[8:])
        next(f)

        cases.append(Case(before, inst, after))
        before = next(f)


#from pprint import pprint
#pprint(cases)



num_cases = 0
for case in cases:
    num_possible = 0
    for op in opcodes:
        if elf_eval(op, *case.inst[1:], case.before) == case.after:
            num_possible += 1
    
    num_cases += num_possible >= 3

print(num_cases)



















