from enum import IntEnum

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class SoilType(IntEnum):
    DRY     = 0
    FLOWING = 1
    STILL   = 2
    CLAY    = 3


class Direction(IntEnum):
    LEFT  = -1
    DOWN  =  0
    RIGHT =  1


class ReturnCode(IntEnum):
    OFF_MAP        = 0
    HIT_WALL       = 1
    JOINED_WATER   = 2
    REACHED_SOURCE = 3


xmax, ymax = 1001, 1850
# plotting helpers
plot_start = 0
plot_interval = 250
disp_dpi = 50
disp_range = (slice(3, 1802, 1), slice(0, 1000, 1))
save_format = 'png'

x_disp, y_disp = (disp_range[1].stop - disp_range[1].start,
                  disp_range[0].stop - disp_range[0].start)

coords = []
with open('input17.txt') as f:
    for line in f:
        a, b = line.split(', ')
        axis_a, val1 = a.split('=')
        val1 = int(val1)
        axis_b, vals = b.split('=')
        val2, val3 = list(map(int, vals.split('..')))
        vals = slice(val2, val3+1)

        if axis_a == 'y':
            coords.append((val1, vals))
        else:
            coords.append((vals, val1))

ground = np.full((ymax, xmax), fill_value=SoilType.DRY)
for c in coords:
    ground[c] = SoilType.CLAY

ymin = np.min((ground == SoilType.CLAY).nonzero()[0])
ymax = np.max((ground == SoilType.CLAY).nonzero()[0])

source = (0, 500)
ground[source] = SoilType.FLOWING

count = 0


def recursive_dinges(source, direction, verbose=False):
    y, x = source

    global count
    global ground

    if verbose:
        print(count)
    if count >= plot_start and count % plot_interval == 0 and verbose:
        plt.imshow(ground[disp_range], cmap='viridis_r')
        plt.tight_layout()
        plt.savefig('17a-step-{}.{}'.format(count, save_format))
        #input("waiting...")

    count += 1

    # Flow sideways
    if direction != Direction.DOWN:
        while x in range(xmax):
            if ground[y, x] == SoilType.CLAY:
                if verbose:
                    dir_txt = 'left' if direction == Direction.LEFT else 'right'
                    print("hit wall: {}".format(dir_txt))
                return ReturnCode.HIT_WALL, x - direction

            ground[y, x] = SoilType.FLOWING

            if ground[y+1, x] == SoilType.DRY:
                ret, _ = recursive_dinges((y, x), direction=Direction.DOWN, verbose=verbose)
                if ret in [ReturnCode.OFF_MAP, ReturnCode.JOINED_WATER]:
                    if verbose:
                        print("off map (recursive, down flow)")
                    return ReturnCode.OFF_MAP, None
                else:
                    if verbose:
                        print("Checking if dry soil is now still:")
                        print(ground[y+1, x] == SoilType.STILL)
            x += direction

    # Flow down
    while ground[y+1, x] == SoilType.DRY:
        y += 1
        ground[y, x] = SoilType.FLOWING
        if y >= ymax:
            if verbose:
                print("off map (going down)")
            return ReturnCode.OFF_MAP, None

    if ground[y+1, x] == SoilType.FLOWING:
        if verbose:
            print("Joined already flowing water, I'm done here")
        return ReturnCode.JOINED_WATER, None

    # Flow splits & moves up while contained
    done = False
    while not done:
        ret1, x1 = recursive_dinges((y, x+Direction.LEFT), Direction.LEFT,
                                    verbose=verbose)
        ret2, x2 = recursive_dinges((y, x+Direction.RIGHT), Direction.RIGHT,
                                    verbose=verbose)

        if ret1 == ReturnCode.HIT_WALL and ret2 == ReturnCode.HIT_WALL:
            if verbose:
                print("moving up")
            ground[y, x1:x2+1] = SoilType.STILL
            y -= 1
            if y == source[0]:
                return ReturnCode.REACHED_SOURCE, None
        else:
            done = True

    if verbose:
        print("off map (recursive)")
    return ReturnCode.OFF_MAP, None


verbose = False

if verbose:
    plt.figure(figsize=((xmax/disp_dpi)+1, (ymax/disp_dpi)+1))
    plt.imshow(ground[disp_range], cmap='viridis')
    plt.tight_layout()
    plt.savefig('17a_init.{}'.format(save_format))

recursive_dinges(source, Direction.DOWN, verbose=verbose)

if verbose:
    plt.imshow(ground[disp_range], cmap='viridis_r')
    plt.tight_layout()
    plt.savefig('17a-final.{}'.format(save_format))


clay_count = np.sum(ground == SoilType.CLAY, axis=1)


print(ymin, ymax)
water_count = ground[ymin:ymax+1]

print("Amount of water in ground:")
print(np.sum(water_count == SoilType.FLOWING) +
      np.sum(water_count == SoilType.STILL))

print("Amount of still water in ground:")
print(np.sum(water_count == SoilType.STILL))
