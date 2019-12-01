# coding: utf-8
import numpy as np
from datetime import datetime
with open('input4.txt') as f:
    lines = [line.split('] ') for line in f]
    
for line in lines:
    line[0] = datetime.strptime(line[0], '[%Y-%m-%d %H:%M')
    
lines.sort(key=lambda x: x[0])
for line in lines:
    if 'Guard' in line[1]:
        maxguard = max(int(line[1].split()[1].replace('#', '')), maxguard)
        
asleep = np.zeros((3100, 61))
cur_guard = 0
start = 0
for dt, line in lines:
    if 'Guard' in line:
        cur_guard = int(line.split()[1].replace('#', ''))
    elif 'falls' in line:
        start = dt.minute
    elif 'wakes' in line:
        asleep[cur_guard, start:dt.minute] += 1
        
sumsleep = np.sum(asleep, axis=1)
np.argmax(sumsleep), np.max(sumsleep)
1823*41
np.argwhere(asleep == np.max(asleep))
3011*44
