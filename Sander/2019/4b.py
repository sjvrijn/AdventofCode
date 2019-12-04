# coding: utf-8
def check(n):
    n = str(n)
    digits = [d for d in n]
    if sorted(digits) != digits:
        return False
    for i in range(10):
        i = str(i)
        if (''.join([i]*2) in n) and (''.join([i]*3) not in n):
            return True
    return False

with open('input4.txt') as f:
    start, end = list(map(int, next(f).split('-')))
print(sum(check(i) for i in range(start, end)))
