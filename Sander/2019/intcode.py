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


class ReturnCode(IntEnum):
    BREAK = 0
    INPUT = 1
    ERROR = 2


class IntCode:

    def __init__(self, program, inputs=None, verbose=False):
        self.program = program
        self.inputs = inputs
        self.verbose = verbose

        self.pc = 0
        self.rel_base = 0


    def ensure_program_length(self, addr, fill_val=0):
        if addr >= len(self.program):
            extension_len = (addr - len(self.program)) + 1
            self.program.extend([fill_val]*extension_len)


    def get_value(self, addr, mode, verbose=False):
        if verbose:
            print(f"addr: {addr}, mode: {mode}, rel_base: {self.rel_base}")

        if mode == Mode.POS:
            return self.load_safe(addr)
        elif mode == Mode.IMM:
            return addr
        elif mode == Mode.REL:
            return self.load_safe(addr + self.rel_base)
        else:
            raise ValueError(f"Invalid mode '{mode}'")


    def load_safe(self, addr, fill_val=0):
        if addr < 0:
            raise ValueError(f'Invalid negative address {addr} encountered')
        self.ensure_program_length(addr, fill_val)

        return self.program[addr]


    def write_safe(self, addr, value, mode, fill_val=0):
        if mode == Mode.REL:
            addr += self.rel_base
        elif mode == Mode.IMM:
            raise ValueError('Write address may never be in mode 1')

        if addr < 0:
            raise ValueError(f'Invalid negative address {addr} encountered')

        self.ensure_program_length(addr, fill_val)
        self.program[addr] = value


    def intcode(self):
        opcode = self.program[self.pc]
        output = []

        while opcode != Opcode.BREAK:
            if self.verbose:
                print(f"opcode: {opcode}, pc: {self.pc}")
            modes, opcode = divmod(opcode, 100)
            modes, mode1 = divmod(modes, 10)
            modes, mode2 = divmod(modes, 10)
            _, mode3 = divmod(modes, 10)

            if opcode == Opcode.ADD:
                addr1, addr2, addr3 = self.program[self.pc + 1:self.pc + 4]
                val1 = self.get_value(addr1, mode1)
                val2 = self.get_value(addr2, mode2)

                if self.verbose:
                    print(self.program[self.pc:self.pc + 4])
                    print(f"{val1} {'used directly' if mode1 else 'loaded from'} "
                          f"{addr1 if mode1 else ''} [{mode1}]")
                    print(f"{val2} {'used directly' if mode2 else 'loaded from'} "
                          f"{addr2 if mode2 else ''} [{mode2}]")
                    print(f"storing {val1} + {val2} at {addr3}: {val1 + val2}")

                self.write_safe(addr3, val1 + val2, mode3)
                self.pc += 4

            elif opcode == Opcode.MUL:
                addr1, addr2, addr3 = self.program[self.pc + 1:self.pc + 4]
                val1 = self.get_value(addr1, mode1)
                val2 = self.get_value(addr2, mode2)

                if self.verbose:
                    print(self.program[self.pc:self.pc + 4])
                    print(f"{val1} {'used directly' if mode1 else 'loaded from'} "
                          f"{addr1 if mode1 else ''} [{mode1}]")
                    print(f"{val2} {'used directly' if mode2 else 'loaded from'} "
                          f"{addr2 if mode2 else ''} [{mode2}]")
                    print(f"storing {val1} * {val2} at {addr3}: {val1 * val2}")

                self.write_safe(addr3, val1 * val2, mode3)
                self.pc += 4

            elif opcode == Opcode.INPUT:
                addr1 = self.program[self.pc + 1]
                if self.inputs:
                    in_value = self.inputs.pop(0)
                else:
                    return output, ReturnCode.INPUT

                self.write_safe(addr1, in_value, mode1)
                self.pc += 2

            elif opcode == Opcode.OUTPUT:
                addr1 = self.program[self.pc + 1]
                val1 = self.get_value(addr1, mode1)
                if self.verbose:
                    print(val1)
                output.append(val1)
                self.pc += 2

            elif opcode == Opcode.JMP_NZ:
                addr1, addr2 = self.program[self.pc + 1:self.pc + 3]
                val1 = self.get_value(addr1, mode1)
                val2 = self.get_value(addr2, mode2)
                if val1 != 0:
                    self.pc = val2
                else:
                    self.pc += 3

            elif opcode == Opcode.JMP_Z:
                addr1, addr2 = self.program[self.pc + 1:self.pc + 3]
                val1 = self.get_value(addr1, mode1)
                val2 = self.get_value(addr2, mode2)
                if val1 == 0:
                    self.pc = val2
                else:
                    self.pc += 3

            elif opcode == Opcode.LT:
                addr1, addr2, addr3 = self.program[self.pc + 1:self.pc + 4]
                val1 = self.get_value(addr1, mode1)
                val2 = self.get_value(addr2, mode2)
                outcome = 1 if val1 < val2 else 0
                self.write_safe(addr3, outcome, mode3)
                self.pc += 4

            elif opcode == Opcode.EQ:
                addr1, addr2, addr3 = self.program[self.pc + 1:self.pc + 4]
                val1 = self.get_value(addr1, mode1)
                val2 = self.get_value(addr2, mode2)
                outcome = 1 if val1 == val2 else 0
                self.write_safe(addr3, outcome, mode3)
                self.pc += 4

            elif opcode == Opcode.MV_REL:
                addr1 = self.program[self.pc + 1]
                val1 = self.get_value(addr1, mode1)
                self.rel_base += val1
                self.pc += 2

            elif opcode == Opcode.BREAK:
                if self.verbose:
                    print('BREAK')
                return output, ReturnCode.BREAK

            else:
                raise ValueError(f"Invalid opcode '{opcode}' encountered at pc {self.pc}.")

            opcode = self.program[self.pc]
            if self.verbose:
                print()

        return output, ReturnCode.BREAK


def read_instructions(fname):
    with open(fname) as f:
        return list(map(int, next(f).split(',')))
