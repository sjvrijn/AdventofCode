# coding: utf-8
with open('input2.txt') as f:
    words = [x.strip() for x in f]
    
from itertools import combinations
for A,B in combinations(words, 2):
    diffs = [a == b for a,b in zip(A,B)]
    if sum(diffs) == len(diffs)-1:
        print(A)
        print(B)
        print(''.join([a for a, diff in zip(A, diffs) if diff]))
        
