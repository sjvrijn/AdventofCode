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
    
print(np.sum(np.sum(distances, axis=2) < 10_000))
