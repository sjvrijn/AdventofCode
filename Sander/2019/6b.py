from collections import defaultdict
import networkx as nx


with open('input6.txt') as f:
    direct_orbits = [line.strip().split(')') for line in f]

G = nx.Graph()
G.add_edges_from(direct_orbits)

# -1 for edge-list -> edges
path_len = len(nx.shortest_path(G, 'YOU', 'SAN'))-1

#-2 to exclude 'YOU' and 'SAN'
print(path_len - 2)
