# coding: utf-8
import numpy as np


class Marble:
    __slots__ = ['value', 'previous', 'next']
    
    def __init__(self, value, previous, next):
        self.value = value
        self.previous = previous
        self.next = next


class Circle:
    def __init__(self):
        self.current = Marble(0, None, None)
        self.start = self.current
        self.current.previous = self.current
        self.current.next = self.current
        self.length = 1

    def step(self, steps):
        if steps < 0:
            for _ in range(-steps):
                self.current = self.current.previous
        else:
            for _ in range(steps):
                self.current = self.current.next

    def insert(self, value):
        previous = self.current.previous
        next = self.current
        
        marble = Marble(value, previous, next)
        
        previous.next = marble
        next.previous = marble
        self.current = marble
        self.length += 1

    def remove_current(self):
        new_current = self.current.next
        previous = self.current.previous

        new_current.previous = previous
        previous.next = new_current 

        if self.start is self.current:
            self.start = new_current

        del self.current
        self.current = new_current
        self.length -= 1

    def as_list(self):
        aslist = []
        temp = self.start
        for _ in range(self.length):
            aslist.append(temp.value)
            temp = temp.next



with open('input9.txt') as f:
    line = next(f).split()
    num_players, num_marbles = int(line[0]), int(line[6])*1

def nine_b(num_players, num_marbles):
    circle = Circle()
    scores = np.zeros(num_players, dtype=np.int64)

    for marble in range(1, num_marbles+1):
        if marble % 23 == 0:
            circle.step(-7)
            scores[marble % num_players] += marble + circle.current.value
            circle.remove_current()
        else:
            circle.step(2)
            circle.insert(marble)

    return np.max(scores)


if __name__ == '__main__':
    import time

    with open('input9.txt') as f:
        line = next(f).split()
        num_players, num_marbles = int(line[0]), int(line[6])

    cases = [
        ( 9,   25), 
        (17, 1104), 
        (10, 1618), 
        (30, 5807),
        (21, 6111),
        (13, 7999),
        (num_players, num_marbles),
        (num_players, num_marbles*100),
    ]

    before = time.time()
    for case in cases:
        result = nine_b(*case)
        after = time.time()
        print(f'{case[0]} players, {case[1]} marbles: high score {result}  ({after - before} sec.)')
        before = after
