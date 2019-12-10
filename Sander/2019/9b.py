from copy import copy
from itertools import permutations


def get_value(program, addr, mode, rel_base, verbose=False):
    if verbose:
        print(f"addr: {addr}, mode: {mode}, rel_base: {rel_base}")

    if mode == 0:
        return load_safe(program, addr)
    elif mode == 1:
        return addr
    elif mode == 2:
        return load_safe(program, addr+rel_base)
    else:
        raise ValueError(f"Invalid mode '{mode}'")


def load_safe(program, addr, fill_val=0):
    if addr < 0:
        raise ValueError(f'Invalid negative address {addr} encountered')
    if addr >= len(program):
        extension_len = (addr - len(program)) + 1
        program.extend([fill_val]*extension_len)

    return program[addr]


def write_safe(program, addr, value, mode, rel_base, fill_val=0):
    if mode == 2:
        addr += rel_base
    elif mode == 1:
        raise ValueError('Write address may never be in mode 1')

    if addr < 0:
        raise ValueError(f'Invalid negative address {addr} encountered')

    if addr >= len(program):
        extension_len = (addr - len(program)) + 1
        program.extend([fill_val]*extension_len)

    program[addr] = value


def intcode(program, inputs=None, print_out=False, verbose=False):
    pc = 0  # program counter
    rel_base = 0
    opcode = program[pc]

    while opcode != 99:
        if verbose:
            print(f"opcode: {opcode}, pc: {pc}")
        modes, opcode = divmod(opcode, 100)
        modes, mode1 = divmod(modes, 10)
        modes, mode2 = divmod(modes, 10)
        _, mode3 = divmod(modes, 10)

        if opcode == 1:
            addr1, addr2, addr3 = program[pc + 1:pc + 4]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            val2 = get_value(program, addr2, mode2, rel_base, verbose=verbose)

            if verbose:
                print(program[pc:pc + 4])
                print(f"{val1} {'used directly' if mode1 else 'loaded from'} "
                      f"{addr1 if mode1 else ''} [{mode1}]")
                print(f"{val2} {'used directly' if mode2 else 'loaded from'} "
                      f"{addr2 if mode2 else ''} [{mode2}]")
                print(f"storing {val1} + {val2} at {addr3}: {val1 + val2}")

            write_safe(program, addr3, val1+val2, mode3, rel_base)
            pc += 4

        elif opcode == 2:
            addr1, addr2, addr3 = program[pc + 1:pc + 4]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            val2 = get_value(program, addr2, mode2, rel_base, verbose=verbose)

            if verbose:
                print(program[pc:pc + 4])
                print(f"{val1} {'used directly' if mode1 else 'loaded from'} "
                      f"{addr1 if mode1 else ''} [{mode1}]")
                print(f"{val2} {'used directly' if mode2 else 'loaded from'} "
                      f"{addr2 if mode2 else ''} [{mode2}]")
                print(f"storing {val1} * {val2} at {addr3}: {val1 * val2}")

            write_safe(program, addr3, val1*val2, mode3, rel_base)
            pc += 4

        elif opcode == 3:
            addr1 = program[pc + 1]
            if inputs:
                in_value = inputs.pop(0)
            else:
                in_value = int(input("Input required: "))

            write_safe(program, addr1, in_value, mode1, rel_base)
            pc += 2

        elif opcode == 4:
            addr1 = program[pc + 1]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            if print_out:
                print(val1)
            else:
                yield val1
            pc += 2

        elif opcode == 5:
            addr1, addr2 = program[pc + 1:pc + 3]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            val2 = get_value(program, addr2, mode2, rel_base, verbose=verbose)
            if val1 != 0:
                pc = val2
            else:
                pc += 3

        elif opcode == 6:
            addr1, addr2 = program[pc + 1:pc + 3]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            val2 = get_value(program, addr2, mode2, rel_base, verbose=verbose)
            if val1 == 0:
                pc = val2
            else:
                pc += 3

        elif opcode == 7:
            addr1, addr2, addr3 = program[pc + 1:pc + 4]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            val2 = get_value(program, addr2, mode2, rel_base, verbose=verbose)
            if val1 < val2:
                outcome = 1
            else:
                outcome = 0
            write_safe(program, addr3, outcome, mode3, rel_base)
            pc += 4

        elif opcode == 8:
            addr1, addr2, addr3 = program[pc + 1:pc + 4]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            val2 = get_value(program, addr2, mode2, rel_base, verbose=verbose)
            if val1 == val2:
                outcome = 1
            else:
                outcome = 0
            write_safe(program, addr3, outcome, mode3, rel_base)
            pc += 4

        elif opcode == 9:
            addr1 = program[pc + 1]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            rel_base += val1
            pc += 2

        elif opcode == 99:
            if verbose:
                print('BREAK')
            break

        else:
            raise ValueError(f"Invalid opcode '{opcode}' encountered at pc {pc}.")

        opcode = program[pc]
        if pc > 200:
            pass
        if verbose:
            print()


def read_instructions(fname):
    with open(fname) as f:
        return list(map(int, next(f).split(',')))


test1 = list(map(int, "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(',')))
test2 = list(map(int, "1102,34915192,34915192,7,4,7,99,0".split(',')))
test3 = list(map(int, "104,1125899906842624,99".split(',')))

print(all(a == b for a, b in zip(list(intcode(test1)), test1)))
print(len(str(list(intcode(test2))[0])) == 16)
print(list(intcode(test3))[0] == test3[1])

instructions = read_instructions('input9.txt')
print(list(intcode(instructions, inputs=[2], verbose=False)))
