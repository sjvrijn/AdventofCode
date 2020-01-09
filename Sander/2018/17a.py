import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

xmax, ymax = 1001, 1850
### CONSTANTS ###
# blocks
WATER = 0
CLAY = 1
# directions
LEFT = -1
RIGHT = 1
# return codes
OFF_MAP = 0
HITWALL = 1

# plotting helpers
plot_start = 2320
plot_interval = 5
disp_dpi = 50
disp_range = (slice(0, 1820, 1), slice(250, 700, 1))
save_format = 'png'

x_disp, y_disp = (disp_range[1].stop - disp_range[1].start,
                  disp_range[0].stop - disp_range[0].start)

coords = []
with open('input17.txt') as f:
    for line in f:
        a, b = line.split(', ')
        axis_a, val = a.split('=')
        val = int(val)
        axis_b, vals = b.split('=')
        vals = slice(*list(map(int, vals.split('..'))))

        if axis_a == 'y':
            coords.append((val, vals))
        else:
            coords.append((vals, val))

ground = np.full((ymax, xmax), fill_value=np.nan)
source = (0, 500)

for c in coords:
    ground[c] = CLAY
ymax = np.max((ground == CLAY).nonzero()[0])

ground[source] = WATER

plt.figure(figsize=((xmax/disp_dpi)+1, (ymax/disp_dpi)+1))
plt.imshow(ground[disp_range], cmap='viridis')
plt.tight_layout()
plt.savefig('17a_init.{}'.format(save_format))

count = 0

def recursive_dinges(source, direction):
    y, x = source

    global count
    global ground

    print(count)
    if count >= plot_start and count % plot_interval == 0:
        plt.imshow(ground[disp_range], cmap='viridis_r')
        plt.tight_layout()
        plt.savefig('17a-step-{}.{}'.format(count, save_format))
        #input("waiting...")

    count += 1

    # Flow sideways
    if direction != 0:
        while x in range(0, xmax):
            if ground[y, x] == CLAY:
                dir_txt = 'left' if direction == LEFT else 'right'
                #print("hit wall: {}".format(dir_txt))
                return HITWALL
            ground[y, x] = WATER

            if np.isnan(ground[y+1, x]):
                break
            x += direction

    # Flow down
    while np.isnan(ground[y+1, x]):
        y += 1
        ground[y, x] = WATER
        if y > ymax:
            print("off map (going down)")
            return OFF_MAP

    # Flow splits & moves up while contained
    done = False
    while not done:
        val1 = recursive_dinges((y, x+LEFT), LEFT)
        val2 = recursive_dinges((y, x+RIGHT), RIGHT)

        if val1 == HITWALL and val2 == HITWALL:
            print("moving up")
            y -= 1
        else:
            done = True

    print("off map (recursive)")
    return OFF_MAP


recursive_dinges(source, 0)
print(np.sum(ground == WATER))



#counter = 0
#while sources and counter < 10:
#    counter += 1
#    y, x = sources.pop(0)
#    print("checking source {}, {}...".format(y, x))
#    print("dropping down")
#    for y_idx in range(y+1, ymax):
#        if ground[y_idx, x] == CLAY:
#            break
#        else:
#            ground[y_idx, x] = WATER
#    y = y_idx-1
#
#    print("going right")
#    for x_idx in range(x+1, xmax):
#        if ground[y, x_idx] == CLAY:
#            break
#        else:
#            ground[y, x_idx] = WATER
#
#        if ground[y+1, x_idx] != CLAY:
#            sources.append((y, x_idx))
#            break
#
#    print("going left")
#    for x_idx in range(x-1, 0, -1):
#        if ground[y, x_idx] == CLAY:
#            break
#        else:
#            ground[y, x_idx] = WATER
#
#        if ground[y+1, x_idx] != CLAY:
#            sources.append((y, x_idx))
#            break


