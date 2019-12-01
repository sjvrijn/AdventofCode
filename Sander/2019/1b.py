# coding: utf-8
import numpy as np
with open('input1.txt') as f:
    masses = np.array(list(map(int, f)))
    
def repeated_fuel_calc(mass):
    total = 0
    fuel = mass // 3 - 2
    while fuel > 0:
        total += fuel
        fuel = fuel // 3 - 2
    return total
    
fuel_needed = np.sum([repeated_fuel_calc(m) for m in masses])
print(fuel_needed)
