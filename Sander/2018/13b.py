import numpy as np
import itertools
from functools import total_ordering
import sys

corners = {
    '/':  {'>': '^', '<': 'v', '^': '>', 'v': '<'},
    '\\': {'>': 'v', '<': '^', '^': '<', 'v': '>'},
}

intersections = {
    '>': {'left': '^', 'straight': '>', 'right': 'v'},
    '<': {'left': 'v', 'straight': '<', 'right': '^'},
    '^': {'left': '<', 'straight': '^', 'right': '>'},
    'v': {'left': '>', 'straight': 'v', 'right': '<'},
}

mapfix = {'>': '-', '<': '-', '^': '|', 'v': '|'}

@total_ordering
class Cart:
    __slots__ = ['x', 'y', 'direction', 'dx', 'dy', 'next_turn']

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.dx, self.dy = self.update_dxy()
        self.next_turn = itertools.cycle(['left', 'straight', 'right'])

    def move(self):
        self.x, self.y = self.x + self.dx, self.y + self.dy

    def intersection(self):
        self.direction = intersections[self.direction][next(self.next_turn)]
        self.dx, self.dy = self.update_dxy()

    def corner(self, corner):
        self.direction = corners[corner][self.direction]
        self.dx, self.dy = self.update_dxy()

    def update_dxy(self):
        if self.direction == '>':
            return 0, 1
        elif self.direction == '<':
            return 0, -1
        elif self.direction == '^':
            return -1, 0
        elif self.direction == 'v':
            return 1, 0
        raise ValueError(f"Invalid direction '{self.direction}'")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.x < other.x:
            return True
        elif other.x < self.x:
            return False
        elif self.y < other.y:
            return True
        else:
            return False

    def __repr__(self):
        return f"'{self.direction}' @ [{self.x}, {self.y}]"


with open('input13.txt') as f:
    tracks = np.array([[c for c in line.strip('\n')] for line in f])

carts = [Cart(x, y, '>') for x,y in np.argwhere(tracks == '>')]
carts.extend([Cart(x, y, '<') for x,y in np.argwhere(tracks == '<')])
carts.extend([Cart(x, y, '^') for x,y in np.argwhere(tracks == '^')])
carts.extend([Cart(x, y, 'v') for x,y in np.argwhere(tracks == 'v')])

for cart in carts:
    tracks[cart.x, cart.y] = mapfix[cart.direction]

while len(carts) > 1:
    carts.sort()
    to_remove = []
    for cart in carts:
        if cart in to_remove:
            continue
        cart.move()

        for c in carts:
            if cart == c and cart is not c:
                to_remove.append(cart)
                to_remove.append(c)
                break
        else:
            if tracks[cart.x, cart.y] == '+':
                cart.intersection()

            elif tracks[cart.x, cart.y] in ['/', '\\']:
                cart.corner(tracks[cart.x, cart.y])

            elif tracks[cart.x, cart.y] == ' ':
                print(f'Cart left the rails at {cart.x},{cart.y}')
                sys.exit()

    for cart in to_remove:
        carts.remove(cart)

print(carts[0].y, carts[0].x)
