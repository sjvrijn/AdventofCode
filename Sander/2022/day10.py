from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def a(lines):
    """Solve day 10 part 1"""
    clock = 1
    register_x = 1
    signal_strengths = 0
    for instruction in lines:
        clock += 1
        if clock % 20 == 0 and clock % 40 != 0:
            signal_strengths += clock*register_x
        if 'addx' in instruction:
            register_x += int(instruction[5:])
            clock += 1
            if clock % 20 == 0 and clock % 40 != 0:
                signal_strengths += clock * register_x
    return signal_strengths


def draw_pixel(clock, register, screen):
    row, pixel = divmod(clock, 40)
    pixel -= 1
    if abs(register - pixel) <= 1:
        screen[row, pixel] = 1


def b(lines):
    """Solve day 10 part 2"""
    screen = np.zeros((6,40))
    clock = 1
    register_x = 1
    for instruction in lines:
        clock += 1
        draw_pixel(clock, register_x, screen)
        if 'addx' in instruction:
            register_x += int(instruction[5:])
            clock += 1
            draw_pixel(clock, register_x, screen)
    print('\n'.join(''.join('#' if pix else '.' for pix in row) for row in screen))
    plt.imshow(screen)
    plt.show()


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = f.read_text().splitlines()
    return lines


def main():
    """Main function to wrap variables"""
    files = [
        'input10-test1.txt',
        'input10.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
