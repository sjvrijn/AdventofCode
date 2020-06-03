def intcode(program, verbose=False):
    pc = 0  # program counter
    opcode = program[pc]

    while opcode != 99:
        if verbose:
            print(f"opcode: {opcode}, pc: {pc}")
        modes, opcode = divmod(opcode, 100)
        modes, mode1 = divmod(modes, 10)
        modes, mode2 = divmod(modes, 10)
        _, mode3 = divmod(modes, 10)

        if opcode == 1:
            addr1, addr2, addr3 = program[pc+1:pc+4]
            val1 = program[addr1] if mode1 == 0 else addr1
            val2 = program[addr2] if mode2 == 0 else addr2

            if verbose:
                print(program[pc:pc+4])
                print(f"{val1} {'used directly' if mode1 else 'loaded from'} "
                      f"{addr1 if mode1 else ''} [{mode1}]")
                print(f"{val2} {'used directly' if mode2 else 'loaded from'} "
                      f"{addr2 if mode2 else ''} [{mode2}]")
                print(f"storing {val1} + {val2} at {addr3}: {val1+val2}")

            program[addr3] = val1 + val2
            pc += 4

        elif opcode == 2:
            addr1, addr2, addr3 = program[pc+1:pc+4]
            val1 = program[addr1] if mode1 == 0 else addr1
            val2 = program[addr2] if mode2 == 0 else addr2

            if verbose:
                print(program[pc:pc+4])
                print(f"{val1} {'used directly' if mode1 else 'loaded from'} "
                      f"{addr1 if mode1 else ''} [{mode1}]")
                print(f"{val2} {'used directly' if mode2 else 'loaded from'} "
                      f"{addr2 if mode2 else ''} [{mode2}]")
                print(f"storing {val1} * {val2} at {addr3}: {val1*val2}")

            program[addr3] = val1 * val2
            pc += 4

        elif opcode == 3:
            addr1 = program[pc+1]
            program[addr1] = int(input("Input required: "))
            pc += 2

        elif opcode == 4:
            addr1 = program[pc+1]
            val1 = program[addr1] if mode1 == 0 else addr1
            print(val1)
            pc += 2

        elif opcode == 5:
            addr1, addr2 = program[pc+1:pc+3]
            val1 = program[addr1] if mode1 == 0 else addr1
            val2 = program[addr2] if mode2 == 0 else addr2
            if val1 != 0:
                pc = val2
            else:
                pc += 3

        elif opcode == 6:
            addr1, addr2 = program[pc+1:pc+3]
            val1 = program[addr1] if mode1 == 0 else addr1
            val2 = program[addr2] if mode2 == 0 else addr2
            if val1 == 0:
                pc = val2
            else:
                pc += 3

        elif opcode == 7:
            addr1, addr2, addr3 = program[pc+1:pc+4]
            val1 = program[addr1] if mode1 == 0 else addr1
            val2 = program[addr2] if mode2 == 0 else addr2
            program[addr3] = 1 if val1 < val2 else 0
            pc += 4

        elif opcode == 8:
            addr1, addr2, addr3 = program[pc+1:pc+4]
            val1 = program[addr1] if mode1 == 0 else addr1
            val2 = program[addr2] if mode2 == 0 else addr2
            program[addr3] = 1 if val1 == val2 else 0
            pc += 4

        elif opcode == 99:
            if verbose:
                print('BREAK')
            break

        else:
            raise ValueError(f"Invalid opcode '{opcode}' encountered at pc {pc}.")

        opcode = program[pc]


def read_instructions(fname):
    with open(fname) as f:
        return list(map(int, next(f).split(',')))


instructions = read_instructions('input5.txt')
intcode(instructions, verbose=False)
