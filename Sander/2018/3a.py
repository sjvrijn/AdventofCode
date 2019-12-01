# coding: utf-8
import numpy as np
with open('input3.txt') as f:
    claims = [x.strip() for x in f]
    
fabric = np.zeros((1000, 1000))
for claim in claims:
    idx, _, loc, size = claim.split(' ')
    locx, locy = map(int, loc.replace(':', '').split(','))
    sizex, sizey = map(int, size.split('x'))
    fabric[locx:locx+sizex, locy:locy+sizey] += 1
    
print(np.sum(fabric > 1))
