# coding: utf-8
import numpy as np
with open('input9.txt') as f:
    line = next(f).split()
    num_players, num_marbles = int(line[0]), int(line[6])*1

circle = np.zeros(num_marbles+2, dtype=np.int)
circle[:3] = [0, 2, 1]
scores = np.zeros(num_marbles+2, dtype=np.int)
cur_idx = 1
cur_length = 3

for marble in range(3, num_marbles+1):
    if marble % 23 == 0:
        cur_idx -= 7
        if cur_idx < 0:
            cur_idx += cur_length
        
        scores[marble] = marble + circle[cur_idx]
        
        #del circle[cur_idx]
        circle[cur_idx:cur_length+1] = circle[cur_idx+1:cur_length+2]
        
        cur_length -= 1
    else:
        cur_idx += 2
        if cur_idx > cur_length:
            cur_idx -= cur_length

        #circle.insert(cur_idx, marble)
        circle[cur_idx+1:cur_length+2] = circle[cur_idx:cur_length+1]
        circle[cur_idx] = marble
        
        cur_length += 1

scores_per_player = [np.sum(scores[i::num_players]) for i in range(num_players)]
print(np.max(scores_per_player))
