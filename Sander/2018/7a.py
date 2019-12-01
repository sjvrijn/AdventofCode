# coding: utf-8
import string
import numpy as np

tasks = {letter: [] for letter in string.ascii_uppercase}

with open('input7.txt') as f:
    for line in f:
        _, pre, _, _, _, _, _, post, _, _ = line.split() 
        tasks[post].append(pre)

todo = set(string.ascii_uppercase)
order = []

while todo:
    task, length = None, np.inf
    for t, pre_list in tasks.items():
        if len(pre_list) < length:
            task, length = t, len(pre_list)

    order.append(task)
    del tasks[task]
    todo.remove(task)
    
    for pre_list in tasks.values():
        if task in pre_list:
            pre_list.remove(task)
        
print(''.join(order))
