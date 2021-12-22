from dataclasses import dataclass, field
from operator import gt, lt, eq
from typing import Union

import numpy as np
from more_itertools import peekable, take


@dataclass()
class Packet:
    version: int
    type_id: int
    content: Union[int, list]=field(init=False)

    def __init__(self, version, type_id, content=None):
        self.version = version
        self.type_id = type_id
        self.content = content


def a(line):
    bits = ''.join(f'{int(char, base=16):04b}' for char in line)
    return sum_versions(parse_packets(bits))


def b(line):
    bits = ''.join(f'{int(char, base=16):04b}' for char in line)
    return eval_packet(parse_packets(bits))


def parse_packets(bitstring):
    bitstring = iter(bitstring)

    version = int(str_take(3, bitstring), base=2)
    packet_type = int(str_take(3, bitstring), base=2)
    packet = Packet(version, packet_type)

    if packet_type == 4:
        literal_bits = []

        chunk = str_take(5, bitstring)
        while chunk[0] == '1':
            literal_bits.append(chunk[1:])
            chunk = str_take(5, bitstring)
        literal_bits.append(chunk[1:])

        value = int(''.join(literal_bits), base=2)
        packet.content = value

    else:
        packet.content = []
        length_type_id = next(bitstring)
        if length_type_id == '0':
            bit_length = int(str_take(15, bitstring), base=2)
            sub_packets_bitstring = peekable(str_take(bit_length, bitstring))
            while sub_packets_bitstring:
                packet.content.append(parse_packets(sub_packets_bitstring))
        else:
            num_sub_packets = int(str_take(11, bitstring), base=2)
            for _ in range(num_sub_packets):
                packet.content.append(parse_packets(bitstring))

    return packet


def str_take(n, iterator):
    return ''.join(take(n, iterator))


def sum_versions(packet):
    if packet.type_id == 4:
        return packet.version
    return sum(sum_versions(p) for p in packet.content) + packet.version


def eval_packet(packet):
    operators = {0: sum, 1: np.product, 2: min, 3: max}
    comparators = {5: gt, 6: lt, 7: eq}
    if packet.type_id == 4:
        return packet.content
    if packet.type_id in [0, 1, 2, 3]:
        return operators[packet.type_id]([eval_packet(p) for p in packet.content])
    if packet.type_id in [5, 6, 7]:
        x, y = packet.content
        return int(comparators[packet.type_id](eval_packet(x), eval_packet(y)))


if __name__ == '__main__':
    # parse_cases = [
    #     ('D2FE28',                         (6, 4, 2021)),
    #     ('38006F45291200',                 (1, 6, [(..., ..., 10), (..., ..., 20)])),
    #     ('EE00D40C823060',                 (7, 3, [(..., ..., 1), (..., ..., 2), (..., ..., 3)])),
    #     ('8A004A801A8002F478',             (4, ..., [(1, ..., [(5, ..., [(6, ..., ...)])])])),
    # ]
    # for case, expected in parse_cases:
    #     print(case)
    #     print(a(case))
    #     print(expected)

    # eval_cases = [
    #     ('C200B40A82',                     (3)),
    #     ('04005AC33890',                   (54)),
    #     ('880086C3E88112',                 (7)),
    #     ('CE00C43D881120',                 (9)),
    #     ('D8005AC2A8F0',                   (1)),
    #     ('F600BC2D8F',                     (0)),
    #     ('9C005AC2F8F0',                   (0)),
    #     ('9C0141080250320F1802104A08',     (1)),
    # ]
    # for case, expected in eval_cases:
    #     print(case)
    #     print(b(case))
    #     print(expected)

    files = [
        'input16.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            line = f.read().strip()

        print(f'A: {a(line)}')
        print(f'B: {b(line)}')
