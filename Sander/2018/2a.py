# coding: utf-8
with open('input2.txt') as f:
    words = [line.strip() for line in f]
    
from collections import Counter
counts = [Counter(word) for word in words]
sum(2 in count.values() for count in counts)*sum(3 in count.values() for count in counts)
