from itertools import count
from more_itertools import windowed


def is_valid_preamble_sum(num, preamble):
    for num_a in preamble:
        num_b = num - num_a
        if num_b != num_a and num_b in preamble:
            return True
    return False


def a(numbers, preamble_size=25):
    preamble = set(numbers[:preamble_size])
    for idx, num in enumerate(numbers[preamble_size:]):
        if not is_valid_preamble_sum(num, preamble):
            return num
        preamble.remove(numbers[idx])
        preamble.add(num)

    raise ValueError


def b(numbers, first_invalid):
    for window_size in count(2):
        for window in windowed(numbers, window_size):
            if sum(window) == first_invalid:
                return min(window) + max(window)
    raise ValueError


if __name__ == '__main__':
    with open('input09.txt') as f:
        numbers = [int(line) for line in f]

    first_invalid = a(numbers)
    print(first_invalid)  # a
    print(b(numbers, first_invalid))
