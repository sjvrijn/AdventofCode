# coding: utf-8
import string
import numpy as np

tasks = {letter: [] for letter in string.ascii_uppercase}

with open('input7.txt') as f:
    for line in f:
        _, pre, _, _, _, _, _, post, _, _ = line.split() 
        tasks[post].append(pre)

todo = set(string.ascii_uppercase)
task_time = {letter: 61+i for i, letter in enumerate(string.ascii_uppercase)}
def next_task(tasklist):
    for task in string.ascii_uppercase:
        try:
            if len(tasklist[task]) == 0:
                return task
        except KeyError:
            pass
        
def set_task_done(task, tasklist):
    for dependencies in tasklist.values():
        try:
            dependencies.remove(task)
        except ValueError:
            pass
        
order = []
while tasks:
    task = next_task(tasks)
    order.append(task)
    del tasks[task]
    set_task_done(task, tasks)
       
order
