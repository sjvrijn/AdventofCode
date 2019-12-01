# coding: utf-8
import numpy as np
from collections import namedtuple
Coord = namedtuple('Coord', ['x', 'y'])
with open('input6.txt') as f:
    coords = [Coord(*map(int, line.split(','))) for line in f]
    
distances = np.zeros((361, 361, 50))
X = Y = np.arange(361)
Y = Y.reshape((-1,1))
for i, coord in enumerate(coords):
    distances[:,:,i] = np.abs(X-coord.x) + np.abs(Y-coord.y)
    
min_dist = np.min(distances, axis=2)
is_minimal = np.zeros(distances.shape)
for i in range(len(coords)):
    is_minimal[:,:,i] = distances[:,:,i] == min_dist
    
num_min_dist = np.sum(is_minimal, axis=2)
which_minimal = np.zeros(min_dist.shape)
for i in range(len(coords)):
    which_minimal[distances[:,:,i] == min_dist] = i+1
    
which_minimal[num_min_dist == 2] = 0
all_numbers = set(range(1, 51))
numbers = all_numbers - (set(which_minimal[0,:]) | set(which_minimal[-1,:]) | set(which_minimal[:,0]) | set(which_minimal[:,-1]))
best_num, size = 0, 0
for num in numbers:
    new_size = np.sum(which_minimal == num)
    if new_size > size:
        best_num, size = num, new_size
        
print(best_num, size)
