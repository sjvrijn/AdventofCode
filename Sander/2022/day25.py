from pathlib import Path


def snafu_to_int(snafu):
    snafu_digits = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
    return sum(snafu_digits[char]*(5**n) for n, char in enumerate(reversed(snafu)))


def int_to_snafu(n):
    reverse_base5_digits = []
    while n > 0:
        n, digit = divmod(n, 5)
        reverse_base5_digits.append(str(digit))

    base5_digits = {0: '0', 1: '1', 2: '2', -1: '-', -2: '='}
    snafu_digits = []
    carry = 0
    for digit in reverse_base5_digits:
        digit, carry = int(digit) + carry, 0
        if digit > 2:
            digit, carry = digit-5, 1

        snafu_digits.append(base5_digits[digit])

    return ''.join(reversed(snafu_digits))


def a(lines):
    """Solve day 25 part 1"""
    fuel = [snafu_to_int(snafu) for snafu in lines]
    return int_to_snafu(sum(fuel))


def b(_):
    """Solve day 25 part 2"""
    return "Start the blender!"


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = f.read_text().splitlines()
    return lines


def main():
    """Main function to wrap variables"""
    files = [
        'input25-test1.txt',
        # 'input25-test2.txt',
        'input25.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
