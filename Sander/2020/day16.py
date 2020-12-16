from more_itertools import take
from parse import parse
import numpy as np


def a(valid_numbers, tickets):
    return sum(
        number
        for ticket in tickets
        for number in ticket
        if number not in valid_numbers
    )


def b(my_ticket, other_tickets, constraints):
    could_be_valid = []
    for ticket_field_values in zip(*other_tickets):  # row
        validity = [
            is_field_valid(constraint, ticket_field_values)
            for constraint in constraints.values()   # column
        ]
        could_be_valid.append(validity)
    could_be_valid = np.array(could_be_valid, dtype=np.int)

    ticket_format = [None for _ in my_ticket]
    constraint_names = list(constraints.keys())
    while any(constraint_names):
        row = (np.sum(could_be_valid, axis=1) == 1).tolist().index(True)
        col = (could_be_valid[row] == 1).tolist().index(True)
        ticket_format[row], constraint_names[col] = constraint_names[col], ticket_format[row]
        could_be_valid[row,:] = 0
        could_be_valid[:,col] = 0

    named_ticket = dict(zip(ticket_format, my_ticket))
    total = 1
    for name, val in named_ticket.items():
        if 'departure' in name:
            total *= val
    return total


def gather_valid_numbers(constraints):
    return set().union(*constraints.values())


def is_ticket_valid(ticket, valid_numbers):
    return all(n in valid_numbers for n in ticket)


def is_field_valid(constraint, ticket_field_values):
    return all(
        value in constraint
        for value in ticket_field_values
    )


def parse_tickets(lines):
    iter_lines = iter(lines)
    line = next(iter_lines)
    constraints = {}
    while line:
        name, start1, end1, start2, end2 = parse('{}: {:d}-{:d} or {:d}-{:d}', line)
        constraints[name] = {*range(start1, end1+1), *range(start2, end2+1)}
        line = next(iter_lines)

    assert next(iter_lines) == 'your ticket:'
    my_ticket = list(map(int, next(iter_lines).split(',')))

    assert take(2, iter_lines)[1] == 'nearby tickets:'
    other_tickets = [
        list(map(int, line.split(',')))
        for line in iter_lines
    ]

    return constraints, my_ticket, other_tickets


if __name__ == '__main__':
    with open('input16.txt') as f:
        lines = [line.strip() for line in f]
    constraints, my_ticket, other_tickets = parse_tickets(lines)
    valid_numbers = gather_valid_numbers(constraints)

    print(a(valid_numbers, other_tickets))

    valid_tickets = [ticket for ticket in other_tickets if is_ticket_valid(ticket, valid_numbers)]
    print(b(my_ticket, valid_tickets, constraints))
