import numpy as np

grid_size = 300 + 1

S = 9995
rack_ids = np.arange(grid_size) + 10
Y = np.arange(grid_size).reshape(-1, 1)


cells = (rack_ids * Y) + S
cells *= rack_ids
cells = (cells // 100) % 10
cells -= 5


best_max, best_where, best_size = 0, None, 0
for sub_size in range(1, grid_size):

    sums = np.zeros((grid_size, grid_size))
    offset = sub_size - 1

    for x in range(1, grid_size - offset):
        for y in range(1, grid_size - offset):
            sums[x, y] = np.sum(cells[x:x+sub_size, y:y+sub_size])

    maxsum = np.max(sums)
    if maxsum > best_max:
        best_max = maxsum
        best_where = np.argwhere(sums == np.max(sums))
        best_size = sub_size
        print("Y,X,size:", best_where, best_size)

print("final:")
print("Y,X,size:", best_where, best_size)
