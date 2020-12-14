from operator import itemgetter


def a(start, busses):
    valid_busses = [
        int(b)
        for b in busses.split(',')
        if b != 'x'
    ]
    wait_times = [
        b - (start % b)
        for b in valid_busses
    ]
    earliest_bus, wait_time = min(zip(valid_busses, wait_times), key=itemgetter(1))
    return earliest_bus * wait_time


def linear_congruence(a, b, m):
    """Source: https://stackoverflow.com/questions/48252234/how-to-solve-a-congruence-system-in-python"""
    if b == 0:
        return 0

    if a < 0:
        a = -a
        b = -b

    b %= m
    while a > m:
        a -= m

    return (m * linear_congruence(m, -b, a) + b) // a


def combine_bus_constraints(residual1, modulus1, residual2, modulus2):
    """performs modulo arithmetic"""
    new_residual = residual2 - residual1

    new_residual = linear_congruence(modulus1, new_residual, modulus2)
    new_residual = (new_residual * modulus1) + residual1

    new_modulus = modulus1*modulus2

    return new_residual, new_modulus

def b(busses):
    bus_offsets = sorted(
        [
            ((int(bus) - offset)%int(bus), int(bus))
            for offset, bus in enumerate(busses.split(','))
            if bus != 'x'
        ],
        key=itemgetter(1),
    )
    offset, combined_bus_ids = bus_offsets[0]
    for idx, (extra_offset, bus_id) in enumerate(bus_offsets[1:], start=1):
        offset, combined_bus_ids = combine_bus_constraints(offset, combined_bus_ids, extra_offset, bus_id)
    return offset


if __name__ == '__main__':
    with open('input13.txt') as f:
        start_time = int(next(f))
        bus_lines = next(f).strip()

    print(a(start_time, bus_lines))
    print(b(bus_lines))
