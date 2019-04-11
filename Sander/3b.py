# coding: utf-8
import numpy as np
with open('input3.txt') as f:
    claims = [x.strip() for x in f]

fabric = np.zeros((1000, 1000))
overlapping = {0}
for claim in claims:
    idx, _, loc, size = claim.split(' ')
    locx, locy = map(int, loc.replace(':', '').split(','))
    sizex, sizey = map(int, size.split('x'))
    
    already_there = set(fabric[locx:locx+sizex, locy:locy+sizey].flatten())
    if already_there != {0}:
        overlapping |= already_there.union([int(idx[1:])])
        
    fabric[locx:locx+sizex, locy:locy+sizey] = int(idx[1:])
    
print(set(range(int(max(overlapping)+1))) - overlapping)
