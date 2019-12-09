# coding: utf-8
from copy import copy


def intcode(instructions):
    instr_idx = 0
    instruction = instructions[instr_idx]
    while instruction != 99:
        in1, in2, out = instructions[instr_idx+1:instr_idx+4]
        
        data1, data2 = instructions[in1], instructions[in2]
        if instruction == 1:
            instructions[out] = data1 + data2
        elif instruction == 2:
            instructions[out] = data1 * data2
        else:
            raise IndexError 

        instr_idx += 4
        instruction = instructions[instr_idx]


with open('input2.txt') as f:
    orig_instructions = list(map(int, next(f).strip().split(',')))

instructions = copy(orig_instructions)
instructions[1] = 12
instructions[2] = 2
intcode(instructions)
print(instructions[0])
