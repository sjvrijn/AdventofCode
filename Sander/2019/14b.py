from math import ceil
import re

import networkx as nx


G_init = nx.DiGraph()

regex = re.compile(r'(\d+) ([A-Z]+)')
with open('input14.txt') as f:
    for line in f:
        chemicals = regex.findall(line)
        chem_in, chem_out = chemicals[:-1], chemicals[-1]
        # print(chem_in, chem_out)

        G_init.add_node(chem_out[1], output=int(chem_out[0]), amount=0)
        for val, chem in chem_in:
            G_init.add_edge(chem_out[1], chem, weight=int(val))

G_init.nodes['ORE']['output'] = 1
G_init.nodes['ORE']['amount'] = 0

ore_limit = 1_000_000_000_000
search_val = 1
search_step = 1
overshot = False

while search_step >= 1:

    G = G_init.copy()
    G.nodes['FUEL']['amount'] = search_val
    to_process = ["FUEL"]

    while to_process:
        chem_out = to_process.pop(0)
        for chem_in in list(G.successors(chem_out)):
            units_needed = ceil(G.nodes[chem_out]['amount'] / G.nodes[chem_out]['output'])
            amount_needed = units_needed * G.edges[chem_out, chem_in]['weight']

            G.nodes[chem_in]['amount'] += amount_needed

            G.remove_edge(chem_out, chem_in)
            if len(list(G.predecessors(chem_in))) == 0:
                to_process.append(chem_in)

    ore_needed = G.nodes['ORE']['amount']

    print(f"{search_val} Fuel --> {ore_needed} Ore")
    if overshot:
        search_step //= 2
    else:
        search_step *= 2

    if ore_needed < ore_limit:
        search_val += search_step
    elif ore_needed > ore_limit:
        search_val -= search_step
        overshot = True
    elif ore_needed == ore_limit:
        break
