# coding: utf-8
current = 0
from itertools import cycle
with open('input1.txt') as f:
    changes = [eval(x.strip()) for x in f]
    
seen = {0}
for change in cycle(changes):
    current += change
    if current in seen:
        print(current)
        break
    else:
        seen.add(current)
        
