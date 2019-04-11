# coding: utf-8
with open('input8.txt') as f:
    tree_spec = list(map(int, next(f).split()))
    
def meta_sum(spec):
    total = 0
    num_nodes = spec.pop(0)
    num_meta = spec.pop(0)
    for _ in range(num_nodes):
        total += meta_sum(spec)
    for _ in range(num_meta):
        total += spec.pop(0)
    return total
meta_sum(tree_spec)
