from collections import namedtuple
from itertools import permutations, product
from numbers import Number
from string import ascii_lowercase
from time import time
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

    def __init__(self, orig_tunnels, enable_visuals=False):
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


    def flood_fill(self, start=None, goal='', keys='') -> Tuple[Union[Point, None], int]:
        if start is None:
            start = self.entrance
        front = [start]
        dist = 0
        keys = keys.upper()

        if self.enable_visuals:
            self.show(title=f'Distance: {dist}')

        goal_found_at = None

        while front:
            dist += 1
            new_front = []
            for point, d in product(front, directions):
                new_point = point + d
                if self.is_point_free(new_point, keys):
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


    def is_point_free(self, p: Point, keys: str) -> bool:
        try:
            is_free = self.map[p] == Tunnel.SPACE or self.map[p] == Tunnel.ENTRANCE
            is_blocked = self.orig_map[p.x][p.y].isupper() \
                         and self.orig_map[p.x][p.y] not in keys
        except IndexError as e:
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


def find_shortest_route(all_keys, tunnels):
    min_route, min_dist = None, float('inf')
    for perm in permutations(all_keys):
        collected_keys = ''
        route_dist = 0
        loc = tunnels.entrance

        for key in perm:
            loc, dist = tunnels.flood_fill(start=loc, goal=key, keys=collected_keys)
            tunnels.reset_map()
            if loc is None:
                route_dist = float('inf')
                break
            route_dist += dist
            collected_keys += key

        if route_dist < min_dist:
            min_route = perm
            min_dist = route_dist
            print(f"[improvement found] {''.join(min_route)}: {min_dist}")
    print(f"[final result] {''.join(min_route)}: {min_dist}")
    return min_dist, min_route



def test_1():
    orig_tunnels = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""

    all_keys = sorted(set(orig_tunnels) & set(ascii_lowercase))
    tunnels = Tunnel(orig_tunnels.splitlines(), enable_visuals=False)

    start = time()
    min_dist, min_route = find_shortest_route(all_keys, tunnels)
    duration = time() - start

    assert min_dist == 132
    assert ''.join(min_route) == 'bacdfeg'

    _ = input(f'Done in {duration:.3f} sec, press any key to finish...')
    plt.close()


def test_3():
    orig_tunnels = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""

    all_keys = sorted(set(orig_tunnels) & set(ascii_lowercase))
    tunnels = Tunnel(orig_tunnels.splitlines(), enable_visuals=False)

    start = time()
    min_dist, min_route = find_shortest_route(all_keys, tunnels)
    duration = time() - start

    assert min_dist == 136
    assert ''.join(min_route) == 'afbjgnhdloepcikm'

    _ = input(f'Done in {duration:.3f} sec, press any key to finish...')
    plt.close()


def test_2():
    orig_tunnels = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""

    all_keys = sorted(set(orig_tunnels) & set(ascii_lowercase))
    tunnels = Tunnel(orig_tunnels.splitlines(), enable_visuals=False)

    start = time()
    min_dist, min_route = find_shortest_route(all_keys, tunnels)
    duration = time() - start

    assert min_dist == 81
    assert ''.join(min_route) == 'acfidgbeh'

    _ = input(f'Done in {duration:.3f} sec, press any key to finish...')
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
