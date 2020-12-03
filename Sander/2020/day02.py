# coding: utf-8
from parse import parse
pattern = '{:d}-{:d} {:l}: {:l}'


def is_valid_password(entry):
    minimum, maximum, letter, password = parse(pattern, entry)
    return minimum <= password.count(letter) <= maximum


def is_extra_valid_password(entry):
    minimum, maximum, letter, password = parse(pattern, entry)
    check1 = password[minimum-1] == letter
    check2 = password[maximum-1] == letter
    return check1 + check2 == 1


def a(entries):
    return sum(is_valid_password(entry) for entry in entries)


def b(entries):
    return sum(is_extra_valid_password(entry) for entry in entries)



if __name__ == '__main__':
    with open('input02.txt') as f:
        entries = [line.strip() for line in f.readlines()]

    print(a(entries))
    print(b(entries))

