import numpy as np
import matplotlib.pyplot as plt
from more_itertools import chunked

from intcode import IntCode, read_instructions, ReturnCode


instructions = read_instructions('input13.txt')
instructions[0] = 2

# xs, ys = zip(*list(field.keys()))
# print(min(xs), max(xs), min(ys), max(ys))  # 0 37 0 20

WIDTH = 38
HEIGHT = 21
field = np.full((HEIGHT, WIDTH), np.nan)
inputs = []


def read_field(pixels, field):

    pixels = chunked(pixels, 3)
    for count, (y, x, kind) in zip(range(WIDTH*HEIGHT), pixels):
        field[x, y] = kind

    y, x, score = next(pixels)
    print(f'Score: {score}')


def update_pixel(update, field):
    y, x, kind = update
    if y != -1:
        field[x, y] = kind
    else:
        print(f'Score: {kind}')


arcade = IntCode(instructions, inputs=inputs)
init_display, code = arcade.intcode()


read_field(init_display, field)
plt.imshow(field)
plt.show()


while code != ReturnCode.BREAK:
    changes, code = arcade.intcode()
    changes = chunked(changes, 3)
    for change in changes:
        update_pixel(change, field)

    # plt.imshow(field)
    # plt.show()

    paddle_x, paddle_y = np.argwhere(field == 3)[0]
    ball_x, ball_y = np.argwhere(field == 4)[0]

    # print(f"P: [{paddle_x, paddle_y}], B: [{ball_x, ball_y}]")

    if paddle_y < ball_y:
        inputs.append(1)
    elif paddle_y > ball_y:
        inputs.append(-1)
    else:
        inputs.append(0)
