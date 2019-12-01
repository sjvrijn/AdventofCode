# coding: utf-8
with open('input1.txt') as f:
    print(sum(eval(x.strip()) for x in f))
    
