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
            x=self.x, y=self.y, z=self.z, vx=self.vx, vy=self.vy, vz=self.vz
        )
    __str__ = __repr__

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    @property
    def pot(self):
        return abs(self.x) + abs(self.y) + abs(self.z)
        
    @property
    def kin(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)
        
    @property
    def total(self):
        return self.pot * self.kin 

regex = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')

moons = []
with open('input12.txt') as f:
    for line in f:
        moons.append(Coords(*map(int, regex.match(line).groups())))
        
def apply_gravity(A, B):
    if A.x > B.x:
        A.vx -= 1
        B.vx += 1
    elif A.x < B.x:
        A.vx += 1
        B.vx -= 1
        
    if A.y > B.y:
        A.vy -= 1
        B.vy += 1
    elif A.y < B.y:
        A.vy += 1
        B.vy -= 1

    if A.z > B.z: 
        A.vz -= 1
        B.vz += 1
    elif A.z < B.z: 
        A.vz += 1
        B.vz -= 1
        
from itertools import combinations

for step in range(1000):
    for moon_a, moon_b in combinations(moons, 2):
        apply_gravity(moon_a, moon_b)
    for moon in moons:
        moon.move()
        
print(sum(m.total for m in moons))
