from enum import IntEnum


class Opcode(IntEnum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JMP_NZ = 5
    JMP_Z = 6
    LT = 7
    EQ = 8
    MV_REL= 9
    BREAK = 99


class Mode(IntEnum):
    POS = 0  # ITION
    IMM = 1  # EDIATE
    REL = 2  # ATIVE


def get_value(program, addr, mode, rel_base, verbose=False):
    if verbose:
        print(f"addr: {addr}, mode: {mode}, rel_base: {rel_base}")

    if mode == Mode.POS:
        return load_safe(program, addr)
    elif mode == Mode.IMM:
        return addr
    elif mode == Mode.REL:
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
    if mode == Mode.REL:
        addr += rel_base
    elif mode == Mode.IMM:
        raise ValueError('Write address may never be in mode 1')

    if addr < 0:
        raise ValueError(f'Invalid negative address {addr} encountered')

    if addr >= len(program):
        extension_len = (addr - len(program)) + 1
        program.extend([fill_val]*extension_len)

    program[addr] = value


def intcode(program, inputs=None, verbose=False):
    pc = 0  # program counter
    rel_base = 0
    opcode = program[pc]

    while opcode != Opcode.BREAK:
        if verbose:
            print(f"opcode: {opcode}, pc: {pc}")
        modes, opcode = divmod(opcode, 100)
        modes, mode1 = divmod(modes, 10)
        modes, mode2 = divmod(modes, 10)
        _, mode3 = divmod(modes, 10)

        if opcode == Opcode.ADD:
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

        elif opcode == Opcode.MUL:
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

        elif opcode == Opcode.INPUT:
            addr1 = program[pc + 1]
            if inputs:
                in_value = inputs.pop(0)
            else:
                in_value = int(input("Input required: "))

            write_safe(program, addr1, in_value, mode1, rel_base)
            pc += 2

        elif opcode == Opcode.OUTPUT:
            addr1 = program[pc + 1]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            if verbose:
                print(val1)
            yield val1
            pc += 2

        elif opcode == Opcode.JMP_NZ:
            addr1, addr2 = program[pc + 1:pc + 3]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            val2 = get_value(program, addr2, mode2, rel_base, verbose=verbose)
            if val1 != 0:
                pc = val2
            else:
                pc += 3

        elif opcode == Opcode.JMP_Z:
            addr1, addr2 = program[pc + 1:pc + 3]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            val2 = get_value(program, addr2, mode2, rel_base, verbose=verbose)
            if val1 == 0:
                pc = val2
            else:
                pc += 3

        elif opcode == Opcode.LT:
            addr1, addr2, addr3 = program[pc + 1:pc + 4]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            val2 = get_value(program, addr2, mode2, rel_base, verbose=verbose)
            if val1 < val2:
                outcome = 1
            else:
                outcome = 0
            write_safe(program, addr3, outcome, mode3, rel_base)
            pc += 4

        elif opcode == Opcode.EQ:
            addr1, addr2, addr3 = program[pc + 1:pc + 4]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            val2 = get_value(program, addr2, mode2, rel_base, verbose=verbose)
            if val1 == val2:
                outcome = 1
            else:
                outcome = 0
            write_safe(program, addr3, outcome, mode3, rel_base)
            pc += 4

        elif opcode == Opcode.MV_REL:
            addr1 = program[pc + 1]
            val1 = get_value(program, addr1, mode1, rel_base, verbose=verbose)
            rel_base += val1
            pc += 2

        elif opcode == Opcode.BREAK:
            if verbose:
                print('BREAK')
            break

        else:
            raise ValueError(f"Invalid opcode '{opcode}' encountered at pc {pc}.")

        opcode = program[pc]
        if verbose:
            print()


def read_instructions(fname):
    with open(fname) as f:
        return list(map(int, next(f).split(',')))
