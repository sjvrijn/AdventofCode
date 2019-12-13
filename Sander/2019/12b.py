# coding: utf-8
import re

class Coords:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = self.vy = self.vz = 0

    def __repr__(self):
        return '<x={x}, y={y}, z={z}, vx={vx}, vy={vy}, vz={vz}>'.format(
            x=self.x, y=self.y, z=self.z, 
            vx=self.vx, vy=self.vy, vz=self.vz
        )
    __str__ = __repr__

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

regex = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')

moons = []
with open('input12.txt') as f:
    for line in f:
        moons.append(Coords(*map(int, regex.match(line).groups())))
        
def apply_gravity(A, B, coord='xyz'):
    if 'x' in coord:
        if A.x > B.x:
            A.vx -= 1
            B.vx += 1
        elif A.x < B.x:
            A.vx += 1
            B.vx -= 1

    if 'y' in coord:
        if A.y > B.y:
            A.vy -= 1
            B.vy += 1
        elif A.y < B.y:
            A.vy += 1
            B.vy -= 1

    if 'z' in coord:
        if A.z > B.z: 
            A.vz -= 1
            B.vz += 1
        elif A.z < B.z: 
            A.vz += 1
            B.vz -= 1
        
from itertools import combinations, product

moonstates = {'x': {}, 'y': {}, 'z': {}}
coord_loop_lengths = []

def juple(coord, moons):
    properties = (coord, 'v{}'.format(coord))
    return tuple(getattr(m, p) for m, p in product(moons, properties))

from copy import copy

for coord in 'xyz':
    new_moons = [copy(m) for m in moons]
    step = 0
    
    cur_state = juple(coord, new_moons)
    
    while cur_state not in moonstates[coord]:
        moonstates[coord][cur_state] = step

        for moon_a, moon_b in combinations(new_moons, 2):
            apply_gravity(moon_a, moon_b)
        for moon in new_moons:
            moon.move()
        
        cur_state = juple(coord, new_moons)
        step += 1

    coord_loop_lengths.append(len(moonstates[coord]) - moonstates[coord][cur_state])

    
def get_prime_factors(n):
    factors = []
    while not n % 2:
        factors.append(2)
        n /= 2

    f = 3
    while n > 1:
        if n % f:
            f += 2
        else:
            n /= f
            factors.append(f)

    return factors


def safe_remove(l, val):
    try:
        l.remove(val)
    except ValueError:
        pass


fx, fy, fz = [get_prime_factors(n) for n in coord_loop_lengths]
total = 1
while fx or fy or fz:
    for f in fx:
        total *= f
        safe_remove(fx, f)
        safe_remove(fy, f)
        safe_remove(fz, f)
        
    for f in fy:
        total *= f
        safe_remove(fx, f)
        safe_remove(fy, f)
        safe_remove(fz, f)
        
    for f in fz:
        total *= f
        safe_remove(fx, f)
        safe_remove(fy, f)
        safe_remove(fz, f)

print(total)
