import more_itertools
import numpy as np

with open('input12.txt') as f:
    init = next(f).split()[2]
    next(f)
    rules = dict([tuple(rule.strip().split(' => ')) for rule in f])

num_generations = 20
buffer = '.'*((num_generations*2) + 2)
state = buffer + init + buffer

for i in range(num_generations):
    statelist = ['.', '.']
    for window in more_itertools.windowed(state, 5):
        statelist.append(rules[''.join(window)])
    statelist.extend(['.', '.'])
    state = ''.join(statelist)
    print(state)

indices = np.argwhere(np.array([s for s in state]) == '#')
print(np.sum(indices - len(buffer)))
