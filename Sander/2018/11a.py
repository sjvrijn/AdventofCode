import numpy as np

size = 300

S = 9995
rack_ids = np.arange(size+1)+10
Y = np.arange(size+1).reshape(-1, 1)


cells = (rack_ids * Y) + S
cells *= rack_ids
cells = (cells // 100) % 10
cells -= 5

sums = np.zeros((size+1, size+1))
for x in range(1, size-1):
    for y in range(1, size-1):
        sums[x, y] = np.sum(cells[x:x+3, y:y+3])


maxsum = np.max(sums)
where = np.argwhere(sums == np.max(sums))
print("Y, X:", where)
