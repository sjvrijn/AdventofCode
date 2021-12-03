import copy


def a(lines):
    counts = [0] * len(lines[0])
    for line in lines:
        for idx, bit in enumerate(line):
            counts[idx] += int(bit)

    gamma = [1 if c > (len(lines) / 2) else 0 for c in counts]
    epsilon = [1-g for g in gamma]

    gamma, epsilon = ''.join(map(str, gamma)), ''.join(map(str, epsilon))
    return int(gamma, base=2) * int(epsilon, base=2)


def b(lines):
    oxy_options = lines
    co2_options = copy.copy(lines)

    for idx, _ in enumerate(lines[0]):

        if len(oxy_options) > 1:
            oxy_count = sum(int(binary[idx]) for binary in oxy_options)
            oxy_select = '1' if oxy_count >= len(oxy_options) / 2 else '0'
            oxy_options = [binary for binary in oxy_options if binary[idx] == oxy_select]

        if len(co2_options) > 1:
            co2_count = sum(int(binary[idx]) for binary in co2_options)
            co2_select = '1' if co2_count < len(co2_options) / 2 else '0'
            co2_options = [binary for binary in co2_options if binary[idx] == co2_select]

        if len(oxy_options) == 1 and len(co2_options) == 1:
            break

    return int(oxy_options[0], base=2) * int(co2_options[0], base=2)


if __name__ == '__main__':
    files = [
        'input03.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            lines = f.read().splitlines()

        print(f'A: {a(lines)}')
        print(f'B: {b(lines)}')
