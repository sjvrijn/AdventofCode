# coding: utf-8
from itertools import product


def a(iterable):
    for v1, v2 in product(iterable, repeat=2):
        if v1 + v2 == 2020:
            return v1*v2


def b(iterable):
    for v1, v2, v3 in product(iterable, repeat=3):
        if v1 + v2 + v3 == 2020:
            return v1*v2*v3


if __name__ == "__main__":
    with open('input01.txt') as f:
        values = list(map(int, f.readlines()))

    print(f"Day  1-A: {a(values)}")
    print(f"Day  1-B: {b(values)}")

