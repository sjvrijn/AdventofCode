# coding: utf-8
with open('input9.txt') as f:
    line = next(f).split()
    num_players, num_marbles = int(line[0]), int(line[6])

circle = [0, 2, 1]
scores = [0, 0, 0]
cur_idx = 1

for marble in range(3, num_marbles+1):
    if marble % 23 == 0:
        cur_idx -= 7
        if cur_idx < 0:
            cur_idx += len(circle)
        scores.append(marble + circle[cur_idx])
        del circle[cur_idx]
    else:
        cur_idx += 2
        if cur_idx > len(circle):
            cur_idx -= len(circle)
        scores.append(0)
        circle.insert(cur_idx, marble)

scores_per_player = [sum(scores[i::num_players]) for i in range(num_players)]
print(max(scores_per_player))
