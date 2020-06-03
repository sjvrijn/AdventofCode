import more_itertools
import numpy as np

with open('input12.txt') as f:
    init = next(f).split()[2]
    next(f)
    rules = dict(rule.strip().split(' => ') for rule in f)

num_generations = 120
buffer = '.'*((num_generations*2) + 2)
state = buffer + init + buffer

for _ in range(num_generations):
    statelist = ['.', '.']
    for window in more_itertools.windowed(state, 5):
        statelist.append(rules[''.join(window)])
    statelist.extend(['.', '.'])
    state = ''.join(statelist)
    print(state[len(buffer)-2:])

indices = np.argwhere(np.array([s for s in state]) == '#')
sum_result = np.sum(indices - len(buffer))
print(sum_result)

print(sum_result + 5*(50_000_000_000 - num_generations))
