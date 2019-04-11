# coding: utf-8
def meta_ref(spec):
    total = 0
    num_nodes = spec.pop(0)
    num_meta = spec.pop(0)
    print(num_nodes, num_meta)
    if num_nodes == 0:
        total = sum(spec.pop(0) for _ in range(num_meta))
        print('total ', total)
    else:
        node_values = [meta_ref(spec) for _ in range(num_nodes)]
        print('values', node_values)
        metas = []
        for _ in range(num_meta):
            idx = spec.pop(0)
            metas.append(idx)
            try:
                total += node_values[idx-1]
            except IndexError:
                total += 0
        print('metas ', metas)
        print('total ', total)
    return total
with open('input8.txt') as f:
    tree_spec = list(map(int, next(f).split()))
meta_ref(tree_spec)
