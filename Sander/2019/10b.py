import numpy as np
# import matplotlib.pyplot as plt


ast_to_num = {'.': np.nan, '#': 0}
with open('input10.txt') as f:
    belt = np.array([[ast_to_num[ast] for ast in line.strip()] for line in f])

asteroids = np.argwhere(np.isfinite(belt))

max_idx = None
max_visible = 0

for idx, asteroid in enumerate(asteroids):
    non_self_asteroids = np.concatenate((asteroids[:idx], asteroids[idx+1:]))
    rel_locs = non_self_asteroids - asteroid
    gcds = np.gcd(*rel_locs.T).reshape(-1, 1)
    vision_lines = rel_locs / gcds
    unique_visible = set(tuple(x) for x in vision_lines)
    if len(unique_visible) > max_visible:
        max_idx = idx
        max_visible = len(unique_visible)

print(asteroids[max_idx])

asteroid = asteroids[max_idx]
non_self_asteroids = np.concatenate((asteroids[:max_idx], asteroids[max_idx+1:]))
rel_locs = non_self_asteroids - asteroid
degrees = (np.rad2deg(np.arctan2(*rel_locs.T)) + 90) % 360

checklist = list(sorted(set(degrees)))

goal = 200
last_deg = None
num_destroyed = 0
for idx in np.argsort(degrees):
    if degrees[idx] == last_deg:
        continue

    last_deg = degrees[idx]
    num_destroyed += 1

    y, x = asteroids[idx]
    # belt[y, x] = num_destroyed
    # plt.imshow(belt)
    # plt.show()

    print(num_destroyed, degrees[idx], checklist[num_destroyed-1])
    if num_destroyed == 200:
        print(x*100 + y)
        break


