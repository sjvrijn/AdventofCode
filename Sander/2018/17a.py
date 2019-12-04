import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

xmax, ymax = 1001, 1850
WATER = 0
CLAY = 1

disp_dpi = 50
disp_range = (slice(0, 30, 1), slice(450, 550, 1))
save_format = 'png'


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
sources = [(0, 500)]

for c in coords:
    ground[c] = CLAY
ground[sources[0]] = WATER

plt.figure(figsize=((xmax/disp_dpi)+1, (ymax/disp_dpi)+1))
plt.imshow(ground[disp_range], cmap='viridis')
plt.savefig('17a_init.{}'.format(save_format))

counter = 0
while sources and counter < 10:
    counter += 1
    y, x = sources.pop(0)
    print("checking source {}, {}...".format(y, x))
    print("dropping down")
    for y_idx in range(y+1, ymax):
        if ground[y_idx, x] == CLAY:
            break
        else:
            ground[y_idx, x] = WATER
    y = y_idx-1

    print("going right")
    for x_idx in range(x+1, xmax):
        if ground[y, x_idx] == CLAY:
            break
        else:
            ground[y, x_idx] = WATER

        if ground[y+1, x_idx] != CLAY:
            sources.append((y, x_idx))
            break

    print("going left")
    for x_idx in range(x-1, 0, -1):
        if ground[y, x_idx] == CLAY:
            break
        else:
            ground[y, x_idx] = WATER

        if ground[y+1, x_idx] != CLAY:
            sources.append((y, x_idx))
            break

    #plt.imshow(ground[disp_range], cmap='viridis_r')
    #plt.savefig('17a-{}-hor.{}'.format(counter, save_format))
    #input("waiting...")

