# coding: utf-8
import numpy as np
shape = (25, 6)
with open('input8.txt') as f:
    img = np.array(list(map(int, next(f).strip()))).reshape((-1, 6, 25))
    
zeros = img == 0
np.argmin(zeros.sum(axis=2).sum(axis=1))
print(np.sum(img[11] == 1) * np.sum(img[11] == 2))
