# coding: utf-8
directions = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}
def make_step_tuples(start, step):
    """returns tuples of all visited (np.array) coordinates through this step
    
    `start` is expected to be an (x, y) tuple
    `step` is expected as a string: 'Dnnnn' where 'O' is an orientation (RLUD),
    and nnnn is a nonzero integer
    
    Example
    >>> make_step_tuples((0,0), (L3))
    [(0,-1), (0, -2), (0, -3)]"""
    x, y = start
    dx, dy = directions[step[0]]
    steps = []
    for _ in range(int(step[1:])):
        x, y = x+dx, y+dy
        steps.append((x, y))
    return steps


def make_step_set(instructions):
    start = (0,0)
    steps = []
    for step in instructions:
        steps.extend(make_step_tuples(start, step))
        start = steps[-1]
    return set(steps)

    
with open('input3.txt') as f:
    w1 = next(f).strip().split(',')
    w2 = next(f).strip().split(',')
    
s1 = make_step_set(w1)
s2 = make_step_set(w2)
crossings = s1.intersection(s2)


def make_step_list(instructions):
    start = (0,0)
    steps = []
    for step in instructions:
        steps.extend(make_step_tuples(start, step))
        start = steps[-1]
    return steps

l1 = make_step_list(w1)
l2 = make_step_list(w2)
delays = [l1.index(c) + l2.index(c) + 2 for c in crossings]
min(delays)
