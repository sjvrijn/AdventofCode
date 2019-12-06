from collections import defaultdict
import networkx as nx


with open('input6.txt') as f:
    direct_orbits = [line.strip().split(')') for line in f]

G = nx.DiGraph()
G.add_edges_from(direct_orbits)

for node, in_degree in G.in_degree():
    if in_degree == 0:
        root = node
        
print(root)

tracker = defaultdict(list)

dist = 0
tracker[dist] = [root]

while tracker[dist]:
    for node in tracker[dist]:
        tracker[dist+1].extend(list(G[node]))
    dist += 1

print(dist)

orbit_sum = 0
for i in range(dist):
    orbit_sum += i * len(tracker[i])
    
print(orbit_sum)
