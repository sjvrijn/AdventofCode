from collections import namedtuple
from string import ascii_letters
from numbers import Number

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

    def __init__(self, orig_tunnels):
        self.orig_map = orig_tunnels
        self.map = self._parse_map(orig_tunnels)
        self.max_x, self.max_y = self.map.shape
        self.entrance = Point(*np.argwhere(self.map == self.ENTRANCE)[0])
        self.img = None


    def is_point_valid(self, p: Point) -> bool:
        return 0 <= p.x <= self.max_x and 0 <= p.y <= self.max_y


    def _parse_map(self, orig_map):
        return np.array([
            [
                self._numify(n)
                for n in line.strip()
            ]
            for line in orig_map
        ])


    @staticmethod
    def _numify(n: str) -> Number:
        if n == '.':
            return Tunnel.SPACE
        if n == '#':
            return Tunnel.WALL
        if n == '@':
            return Tunnel.ENTRANCE
        return Tunnel.SPACE


    def flood_fill(self, start=None, enable_visuals=False):
        start = start if start is not None else Point(*self.entrance)
        front = [start]
        dist = 0

        if enable_visuals:
            self.show(title=f'Distance: {dist}')

        while not self.is_filled():
            dist += 1
            new_front = []
            for point in front:
                for d in directions:
                    new_point = point + d
                    if self.is_point_valid(new_point) and self.map[new_point] == Tunnel.SPACE:
                        self.map[new_point] = dist
                        new_front.append(new_point)

            if enable_visuals:
                self.show(title=f'Distance: {dist}')

            front = new_front


    def is_filled(self):
        return np.sum(self.map == Tunnel.SPACE) == 0


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
########################""".splitlines()

    tunnels = Tunnel(orig_tunnels)
    tunnels.flood_fill(enable_visuals=True)

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
#################""".splitlines()

    tunnels = Tunnel(orig_tunnels)
    tunnels.flood_fill(enable_visuals=True)

    _ = input('Done, press any key to finish...')
    plt.close()


def test_3():
    orig_tunnels = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""".splitlines()

    tunnels = Tunnel(orig_tunnels)
    tunnels.flood_fill(enable_visuals=True)

    _ = input('Done, press any key to finish...')
    plt.close()


def main():
    with open('input18.txt') as f:
        orig_tunnels = f.readlines()

    tunnels = Tunnel(orig_tunnels)
    tunnels.flood_fill(enable_visuals=True)

    _ = input('Done, press any key to finish...')
    plt.close()


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    main()
