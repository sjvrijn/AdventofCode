from collections import namedtuple
from copy import copy
from itertools import product
from numbers import Number
from string import ascii_lowercase, ascii_uppercase
from typing import Tuple, Union

import numpy as np
import matplotlib.pyplot as plt



class Point(namedtuple('Point', 'x y')):
    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x+other.x, self.y+other.y)


directions = [
    Point( 0, -1),
    Point( 0,  1),
    Point(-1,  0),
    Point( 1,  0),
]


class Tunnel:
    WALL = -100     # '#'
    ENTRANCE = 600  # '@"
    SPACE = 0       # '.'
    VISITED = -1

    def __init__(self, orig_tunnels, blocking=ascii_uppercase, enable_visuals=False):
        self.blocking = blocking
        self.enable_visuals = enable_visuals
        self.orig_map = orig_tunnels
        self.map = self._parse_map(orig_tunnels)
        self.max_x, self.max_y = self.map.shape
        self.entrance = Point(*np.argwhere(self.map == self.ENTRANCE)[0])
        self.img = None


    def _parse_map(self, orig_map):
        return np.array([
            [
                self._numify(n)
                for n in line.strip()
            ]
            for line in orig_map
        ])


    def reset_map(self):
        self.map[self.map != Tunnel.WALL] = Tunnel.SPACE
        self.map[self.entrance] = Tunnel.ENTRANCE

        if self.enable_visuals:
            self.show()

    @staticmethod
    def _numify(n: str) -> Number:
        if n == '.':
            return Tunnel.SPACE
        if n == '#':
            return Tunnel.WALL
        if n == '@':
            return Tunnel.ENTRANCE
        return Tunnel.SPACE


    def flood_fill(self, start=None, goal='') -> Tuple[Union[Point, None], int]:
        if start is None:
            start = self.entrance
        front = [start]
        dist = 0

        if self.enable_visuals:
            self.show(title=f'Distance: {dist}')

        goal_found_at = None

        while front:
            dist += 1
            new_front = []
            for point, d in product(front, directions):
                new_point = point + d
                if self.is_point_free(new_point):
                    self.map[new_point] = dist
                    new_front.append(new_point)

                    if self.orig_map[new_point.x][new_point.y] == goal:
                        goal_found_at = new_point

            if self.enable_visuals:
                self.show(title=f'Distance: {dist}')

            if goal_found_at:
                return goal_found_at, dist

            front = new_front

        return None, dist


    def is_point_free(self, p: Point) -> bool:
        try:
            is_free = self.map[p] == Tunnel.SPACE
            is_blocked = self.orig_map[p.x][p.y] in self.blocking
        except IndexError as e:
            print(e)
            return False
        return is_free and not is_blocked


    def show(self, *, title=''):
        if self.img:
            self.img.set_data(np.ma.masked_equal(self.map, Tunnel.SPACE))
            plt.title(title)
            plt.draw()
            plt.pause(1e-6)
        else:
            plt.ion()
            self.img = plt.imshow(np.ma.masked_equal(self.map, Tunnel.SPACE))
            plt.title(title)
            plt.show()



def test_1():
    orig_tunnels = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""

    all_keys = sorted(set(orig_tunnels) & set(ascii_lowercase))
    tunnels = Tunnel(orig_tunnels.splitlines(), enable_visuals=True)

    for key in all_keys:
        print(tunnels.flood_fill(goal=key))
        tunnels.reset_map()


    _ = input('Done, press any key to finish...')
    plt.close()


def test_2():
    orig_tunnels = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""

    tunnels = Tunnel(orig_tunnels.splitlines(), enable_visuals=True)
    tunnels.flood_fill()

    _ = input('Done, press any key to finish...')
    plt.close()


def test_3():
    orig_tunnels = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""

    tunnels = Tunnel(orig_tunnels.splitlines(), enable_visuals=True)
    tunnels.flood_fill()

    _ = input('Done, press any key to finish...')
    plt.close()


def main():
    with open('input18.txt') as f:
        orig_tunnels = f.read()

    tunnels = Tunnel(orig_tunnels.splitlines(), enable_visuals=True)
    tunnels.flood_fill()

    _ = input('Done, press any key to finish...')
    plt.close()


if __name__ == '__main__':
    np.set_printoptions(linewidth=200, edgeitems=20)
    test_1()
    test_2()
    test_3()
    main()
