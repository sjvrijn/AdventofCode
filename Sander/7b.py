# coding: utf-8
import string
import numpy as np

task_time = {letter: 61+i for i, letter in enumerate(string.ascii_uppercase)}

def next_task(tasklist):
    for task in string.ascii_uppercase:
        try:
            if len(tasklist[task]) == 0:
                return task
        except KeyError:
            pass
    return None
        
def set_task_done(task, tasklist):
    for dependencies in tasklist.values():
        try:
            dependencies.remove(task)
        except ValueError:
            pass
        
todo = set(string.ascii_uppercase)
tasks = {letter: [] for letter in string.ascii_uppercase}
with open('input7.txt') as f:
    for line in f:
        _, pre, _, _, _, _, _, post, _, _ = line.split() 
        tasks[post].append(pre)
        
workers = [{'task': None, 'time': 0} for i in range(5)]
total_time = 0
while todo:
    for worker in workers:
        if worker['task'] is not None:
            continue
        task = next_task(tasks)
        if task is None:
            break
        worker['task'] = task
        worker['time'] = task_time[task]
        del tasks[task]
    #print(total_time, [f'{w["task"]}:{w["time"]}' for w in workers])
    
    time_step = min([w['time'] for w in workers if w['time'] != 0])

    for worker in workers:
        if worker['task'] is None:
            continue
        worker['time'] -= time_step
        if worker['time'] == 0:
            print(f"done: {worker['task']}")
            set_task_done(worker['task'], tasks)
            todo.remove(worker['task'])
            worker['task'] = None
    
    total_time += time_step
    
    #print(total_time, [f'{w["task"]}:{w["time"]}' for w in workers])

print(total_time)
