# coding: utf-8
def check(n):
    n = [d for d in str(n)]
    return (len(set(n)) <= 5) and (sorted(n) == n)

with open('input4.txt') as f:
    start, end = list(map(int, next(f).split('-')))
print(sum(check(i) for i in range(start, end)))

