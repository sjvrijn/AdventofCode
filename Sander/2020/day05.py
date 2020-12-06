# coding: utf-8


def calc_id(boarding_pass):
    low, high, size = 0, 127, 64
    for char in boarding_pass[:7]:
        if char == 'F':
            high -= size
        elif char == 'B':
            low += size
        else:
            raise ValueError
        size //= 2
    row = low

    low, high, size = 0, 7, 4
    for char in boarding_pass[7:]:
        if char == 'L':
            high -= size
        elif char == 'R':
            low += size
        else:
            raise ValueError
        size //= 2
    seat = low

    return row*8 + seat


def a(boarding_passes):
    return max(calc_id(p) for p in boarding_passes)


def b(boarding_passes):
    all_ids = [calc_id(p) for p in boarding_passes]
    missing_passes = set(range(min(all_ids), max(all_ids))) - set(all_ids)
    if len(missing_passes) == 1:
        return missing_passes.pop()
    else:
        raise ValueError("Number of missing passes is not 1")


if __name__ == '__main__':
    with open('input05.txt') as f:
        passes = [line.strip() for line in f]

    print(a(passes))
    print(b(passes))
