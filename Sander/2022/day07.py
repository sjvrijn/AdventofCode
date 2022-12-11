from pathlib import Path

import parse


def calc_size(folder):
    if '_size' in folder:
        return folder['_size']
    size = sum(
        value if isinstance(value, int)
        else calc_size(value)
        for value in folder.values()
    )

    folder['_size'] = size
    return size


def a(filesystem):
    """Solve day 07 part 1"""
    calc_size(filesystem)
    small_dir_size = 100_000
    sum_small_dirs = 0

    dirs_to_check = [filesystem]
    while dirs_to_check:
        current_dir = dirs_to_check.pop(0)
        if current_dir['_size'] <= small_dir_size:
            sum_small_dirs += current_dir['_size']
        dirs_to_check.extend(
            file_or_dir
            for file_or_dir in current_dir.values()
            if isinstance(file_or_dir, dict)
        )
    return sum_small_dirs


def b(filesystem):
    """Solve day 07 part 2"""
    calc_size(filesystem)
    total_size = 70_000_000
    current_free_space = total_size - filesystem['_size']
    space_needed = 30_000_000 - current_free_space
    sizes_greater_than_needed = []

    dirs_to_check = [filesystem]
    while dirs_to_check:
        current_dir = dirs_to_check.pop(0)
        if current_dir['_size'] >= space_needed:
            sizes_greater_than_needed.append(current_dir['_size'])
        dirs_to_check.extend(
            file_or_dir
            for file_or_dir in current_dir.values()
            if isinstance(file_or_dir, dict)
        )
    return min(sizes_greater_than_needed)


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = f.read_text().splitlines()
    assert lines[0] == '$ cd /'

    filesystem = {}
    cur_path = [filesystem]
    file_line_template = parse.compile("{:d} {}")

    for line in lines[1:]:
        if line.startswith('$ cd ..'):
            cur_path.pop(-1)
        elif line.startswith('$ cd'):
            cur_path.append(cur_path[-1][line[5:]])
        elif line.startswith('dir'):
            cur_path[-1][line[4:]] = {}
        elif not line.startswith('$ ls'):
            size, filename = file_line_template.parse(line)
            cur_path[-1][filename] = size

    return filesystem


def main():
    """Main function to wrap variables"""
    files = [
        'input07-test1.txt',
        'input07.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
