def eval_new_math(line):
    val = line.pop(0)
    if val == '(':
        val = eval_new_math(line)

    while line:
        operator = line.pop(0)
        if operator == ')':
            return val
        val2 = line.pop(0)
        if val2 == '(':
            val2 = eval_new_math(line)
        val = int(val)*int(val2) if operator == '*' else int(val)+int(val2)
    return val


def eval_newer_math(line):
    val = line.pop(0)
    if val == '(':
        val = eval_newer_math(line)

    val = int(val)
    prev_val = None
    while line:
        operator = line.pop(0)
        if operator == ')':
            if prev_val:
                val *= prev_val
            return val
        next_val = line.pop(0)
        if next_val == '(':
            next_val = eval_newer_math(line)

        if operator == '+':
            val += int(next_val)
        elif operator == '*':
            if prev_val:
                prev_val *= val
            else:
                prev_val = val
            val = int(next_val)

    if prev_val:
        val *= prev_val
    return val


def a(lines):
    return sum(eval_new_math(list(line)) for line in lines)


def b(lines):
    return sum(eval_newer_math(list(line)) for line in lines)


if __name__ == '__main__':
    with open('input18.txt') as f:
        lines = [line.strip().replace(' ', '') for line in f]

    print(a(lines))
    print(b(lines))
