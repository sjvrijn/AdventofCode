from itertools import product
from parse import parse


def int_as_36bits(value):
    return f'{int(bin(int(value))[2:]):036}'


def apply_mask(bits, mask):
    return ''.join(b if m == 'X' else m for b, m in zip(bits, mask))


def a(lines):
    memory, mask = {}, None
    for line in lines:
        op, value = parse('{} = {}', line)
        if 'mask' in op:
            mask = value
        else:
            number = int_as_36bits(value)
            address = parse('mem[{:d}]', op)[0]
            memory[address] = int(apply_mask(number, mask), 2)
    return sum(memory.values())


def gather_addresses(bits, mask):
    address_bits = []
    for b, m in zip(bits, mask):
        if m == '0':
            address_bits.append(b)
        elif m == '1':
            address_bits.append('1')
        elif m == 'X':
            address_bits.append('01')
    return [int(a, 2) for a in map(''.join, product(*address_bits))]


def b(lines):
    memory, mask = {}, None
    for line in lines:
        op, value = parse('{} = {}', line)
        if 'mask' in op:
            mask = value
        else:
            number = int(value)
            address = parse('mem[{:d}]', op)[0]
            addresses = gather_addresses(int_as_36bits(address), mask)
            for addr in addresses:
                memory[addr] = number
    return sum(memory.values())


if __name__ == '__main__':
    with open('input14.txt') as f:
        lines = [line.strip() for line in f]

    print(a(lines))
    print(b(lines))
