import numpy as np

ast_to_num = {'.': 0, '#': 1}
with open('input10.txt') as f:
    belt = np.array([[ast_to_num[ast] for ast in line.strip()] for line in f])

asteroids = np.argwhere(belt == 1)

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

print(max_idx, max_visible)
