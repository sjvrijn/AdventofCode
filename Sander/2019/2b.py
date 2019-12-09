# coding: utf-8
from copy import copy
from itertools import product


def intcode(instructions):
    instr_idx = 0
    instruction = instructions[instr_idx]
    while instruction != 99:
        in1, in2, out = instructions[instr_idx + 1:instr_idx + 4]

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


for noun, verb in product(range(100), repeat=2):
    current_instructions = copy(orig_instructions)
    current_instructions[1] = noun
    current_instructions[2] = verb
    try:
        intcode(current_instructions)
    except IndexError:
        print(noun, verb)
        continue

    if current_instructions[0] == 19690720:
        print(100*noun + verb)
        break
    # else:
    #     print(noun, verb, current_instructions[0])
