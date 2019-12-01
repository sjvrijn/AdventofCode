import numpy as np
import matplotlib.pyplot as plt

points = []
with open('input10.txt') as f:
    for line in f:
        points.append([
            int(line[10:16]),
            int(line[18:24]),
            int(line[36:38]), 
            int(line[40:42])
        ])

points = np.array(points)
positions, velocities = points[:,:2], points[:,2:]
prev_spread = (np.max(positions, axis=0) - np.min(positions, axis=0))[0]
spread = prev_spread - 1
num_ticks = 0
    
while spread < prev_spread:
    num_ticks += 1
    positions += velocities
    prev_spread = spread
    spread = (np.max(positions, axis=0) - np.min(positions, axis=0))[0]
    
positions -= velocities
plt.figure(figsize=(10, 1.5))
plt.title(num_ticks-1)
plt.scatter(positions[:,0], -positions[:,1])
plt.tight_layout()
plt.savefig('10a.png')
plt.show()

