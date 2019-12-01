# coding: utf-8
import numpy as np
with open('input1.txt') as f:
    masses = np.array(list(map(int, f)))
    fuel_needed = np.sum((masses // 3) - 2)
    
print(fuel_needed)
