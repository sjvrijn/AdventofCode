def simulate_code(code):
    acc, ip, visited_instructions = 0, 0, set()
    while ip not in visited_instructions:
        visited_instructions.add(ip)
        try:
            instruction, value = code[ip].split(' ')
        except IndexError:
            return acc

        if instruction == 'nop':
            ip += 1
        elif instruction == 'acc':
            acc += int(value)
            ip += 1
        elif instruction == 'jmp':
            ip += int(value)
        else:
            raise ValueError
    raise ValueError


def a(code):
    acc, ip, visited_instructions = 0, 0, set
    while ip not in visited_instructions:
        visited_instructions.add(ip)
        instruction, value = code[ip].split(' ')
        if instruction == 'nop':
            ip += 1
        elif instruction == 'acc':
            acc += int(value)
            ip += 1
        elif instruction == 'jmp':
            ip += int(value)
        else:
            raise ValueError

    return acc


def b(code):
    for idx, line in enumerate(code):
        if 'acc' in line or line == 'nop +0':
            continue
        elif 'nop' in line:
            old_line = line
            code[idx] = 'jmp' + line[3:]
        elif 'jmp' in line:
            old_line = line
            code[idx] = 'nop' + line[3:]

        try:
            acc = simulate_code(code)
        except ValueError:
            code[idx] = old_line
            continue

        return acc


if __name__ == '__main__':
    with open('input08.txt') as f:
        code = [line.strip() for line in f]

    print(a(code))
    print(b(code))
