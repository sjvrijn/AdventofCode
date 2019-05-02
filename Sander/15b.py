import numpy as np
from functools import total_ordering
from itertools import product, count


np.set_printoptions(edgeitems=20, linewidth=200)


who_hunts_who = {
    'E': 'G',
    'G': 'E',
}

@total_ordering
class Creature:

    default_strength = 3
    hitpoints = 200

    def __init__(self, kind, x, y, strength=None):
        self.kind = kind
        self.hunts = who_hunts_who[kind]
        self.x = x
        self.y = y
        self.strength = strength if strength else self.default_strength

    def hit_neighbor(self, neighbors):
        min_neighbor_hp = min(n.hitpoints for n in neighbors)
        target = [n for n in sorted(neighbors) if n.hitpoints == min_neighbor_hp][0]
        self.hit(target)
        return target

    def hit(self, other):
        if self.kind == other.kind:
            raise Exception(f"Bad {self.kind}, don't hit your own kind!")
        other.hitpoints -= self.strength

    def isneighborof(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) == 1

    def move(self, direction):
        if direction == 'up':
            self.x -= 1
        elif direction == 'down':
            self.x += 1
        if direction == 'left':
            self.y -= 1
        elif direction == 'right':
            self.y += 1

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
        return f'{self.kind} [{self.x},{self.y}] {self.hitpoints} HP'

    __str__ = __repr__

class Cave:

    def __init__(self, file_in, elf_strength=3, verbose=False):

        self.verbose = verbose
        with open(file_in) as f:
            self._cave = np.array([[c for c in line.strip('\n')] for line in f])

        self.all_creatures = {
            kind: [Creature(kind, a, b, strength) for a, b in np.argwhere(self._cave == kind)]
            for kind, strength in [('E', elf_strength), ('G', None)]
        }

        for c in self.creatures:
            self._cave[c.x, c.y] = '.'

    def __getitem__(self, item):
        return self._cave[item]

    @property
    def creatures(self):
        c = []
        for values in self.all_creatures.values():
            c.extend(values)
        return sorted(c)

    def kill(self, creature):
        try:
            self.all_creatures[creature.kind].remove(creature)
        except:
            pass  # already dead

    def fill_dists_to(self, kind):
        dists = np.empty(self._cave.shape)
        dists[:] = np.inf
        dists[self._cave == '#'] = np.nan
        for c in self.all_creatures[who_hunts_who[kind]]:
            dists[c.x, c.y] = np.nan
        for c in self.all_creatures[kind]:
            dists[c.x, c.y] = 0

        inf_count = np.sum(np.isinf(dists))
        any_inf_left = 0
        while any_inf_left < 2:
            for x, y in product(range(1, self._cave.shape[0]-1), range(1, self._cave.shape[1]-1)):
                dists[x, y] = min(dists[x, y],
                                  dists[x-1, y] + 1, dists[x+1, y] + 1,
                                  dists[x, y-1] + 1, dists[x, y+1] + 1)

            if np.sum(np.isinf(dists)) != inf_count:
                inf_count = np.sum(np.isinf(dists))
            else:
                any_inf_left += 1

        return dists

    def isfinished(self):
        return any(len(v) == 0 for v in self.all_creatures.values())

    def display(self):
        disp = self._cave.copy()
        for c in self.creatures:
            disp[c.x, c.y] = c.kind
        for line in disp:
            print(''.join(line))


    def simulate(self, allow_elf_death=True):
        n_rounds = 0
        ended_intermediately = False
        while not self.isfinished():

            if self.verbose:
                print(f'\nRound: {n_rounds + 1} [{len(self.creatures)} creatures, {sum(c.hitpoints for c in self.creatures)} HP]')
                print('----------------------------------------------------------------------------------')

            d = {'E': None, 'G': None}
            locations_changed = True

            for c in self.creatures:
                if self.isfinished():
                    ended_intermediately = True

                if c.hitpoints <= 0:
                    if not allow_elf_death and c.kind == 'E':
                        raise Exception('An elf died while this was not allowed')
                    self.kill(c)
                    locations_changed = True
                    continue

                if locations_changed or d[c.kind] is None:
                    d[c.kind] = self.fill_dists_to(c.hunts)
                    d[c.hunts] = self.fill_dists_to(c.kind)
                    locations_changed = False

                dist = d[c.kind]

                steps = [dist[c.x - 1, c.y], dist[c.x, c.y - 1],
                         dist[c.x, c.y + 1], dist[c.x + 1, c.y]]

                least_steps = np.nanmin(steps)

                if least_steps != np.inf and least_steps > 0:
                    locations_changed = True
                    if least_steps == steps[0]:
                        c.move('up')
                    elif least_steps == steps[1]:
                        c.move('left')
                    elif least_steps == steps[2]:
                        c.move('right')
                    else:
                        c.move('down')

                neighbors = [neighbor
                             for neighbor in self.all_creatures[c.hunts]
                             if c.isneighborof(neighbor)]

                if neighbors:
                    neighbor = c.hit_neighbor(neighbors)
                    if neighbor.hitpoints <= 0:
                        if not allow_elf_death and neighbor.kind == 'E':
                            raise Exception('An elf died while this was not allowed')
                        self.kill(neighbor)
                        locations_changed = True

            n_rounds += 1

        if ended_intermediately:
            n_rounds -= 1
        if verbose:
            self.display()

        return n_rounds, sum(c.hitpoints for c in self.creatures)



verbose = False

for elf_strength in count(4):
    print(elf_strength)
    cave = Cave('input15.txt', elf_strength=elf_strength)
    try:
        full_rounds, hp_sum = cave.simulate(allow_elf_death=False)
    except Exception as e:
        print(e)
        continue
    print(full_rounds, hp_sum, full_rounds*hp_sum)
    break
