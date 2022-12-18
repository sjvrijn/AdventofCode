from operator import itemgetter
from pathlib import Path

import parse
from tqdm import trange


def a(sensors, target_y):
    """Solve day 15 part 1"""
    ex_ranges = []
    for (sensx, sensy), (beacx, beacy) in sensors:
        dist = abs(sensx - beacx) + abs(sensy - beacy)
        dist_at_ty = dist - abs(target_y - sensy)
        if dist_at_ty > 0:
            ex_ranges.append((sensx-dist_at_ty, sensx+dist_at_ty))
    ex_ranges.sort(key=itemgetter(0))

    idx = 0
    while idx < len(ex_ranges)-1:
        r1start, r1end = ex_ranges[idx]
        r2start, r2end = ex_ranges[idx+1]
        if r2end <= r1end:
            del ex_ranges[idx+1]
        elif r2start <= r1end < r2end:
            ex_ranges[idx] = (r1start, r2end)
            del ex_ranges[idx+1]
        else:
            idx += 1

    return sum(end-start for start, end in ex_ranges)


def b(sensors, half_size):
    """Solve day 15 part 2"""
    for target_y in trange(2*half_size + 1):
        ex_ranges = []
        for (sensx, sensy), (beacx, beacy) in sensors:
            dist = abs(sensx - beacx) + abs(sensy - beacy)
            dist_at_ty = dist - abs(target_y - sensy)
            if dist_at_ty > 0:
                ex_ranges.append((sensx-dist_at_ty, sensx+dist_at_ty))
        ex_ranges.sort(key=itemgetter(0))

        idx = 0
        while idx < len(ex_ranges)-1:
            r1start, r1end = ex_ranges[idx]
            r2start, r2end = ex_ranges[idx+1]
            if r2end <= r1end:
                del ex_ranges[idx+1]
            elif r2start <= r1end < r2end or r2start == (r1end+1):
                ex_ranges[idx] = (r1start, r2end)
                del ex_ranges[idx+1]
            else:
                idx += 1

        if len(ex_ranges) != 1:
            (_, r1end), (r2start, _) = ex_ranges
            return ((r1end+r2start)//2 * 4_000_000) + target_y


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = f.read_text().splitlines()
    template = parse.compile("Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}")
    sensors = []
    for line in lines:
        sensx, sensy, beacx, beacy = template.parse(line)
        sensors.append(((sensx, sensy), (beacx, beacy)))

    return sensors


def main():
    """Main function to wrap variables"""
    files = [
        ('input15-test1.txt', 10),
        ('input15.txt', 2_000_000),
    ]
    for filename, target_y in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data, target_y)}')
        print(f'B: {b(data, half_size=target_y)}')


if __name__ == '__main__':
    main()
