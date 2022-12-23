from pathlib import Path


class DoubleLinkedList:
    def __init__(self, values):
        self.length = len(values)
        self.start = Item(values[0], prev=None)
        self.orig_order = [self.start]
        prev = self.start
        for value in values[1:]:
            new_item = Item(value, prev)
            prev.next = new_item
            self.orig_order.append(new_item)
            prev = new_item
        # link start and end of list
        self.start.prev = prev
        self.start.prev.next = self.start
        self.item_zero = None

    def to_list(self, from_zero=False):
        start = self.item_zero if from_zero else self.start
        as_list = [start.value]
        next_ = start.next

        while next_ is not start:
            as_list.append(next_.value)
            next_ = next_.next
        return as_list

    def mix(self):
        for item in self.orig_order:
            if item.value == 0:
                self.item_zero = item
                continue

            # remove item from current position
            item.prev.next = item.next
            item.next.prev = item.prev

            num_steps = (item.value-1) % (self.length-1)
            new_next_item = item.next.next
            for _ in range(num_steps):
                new_next_item = new_next_item.next

            # insert item in new position
            item.next = new_next_item
            item.prev = new_next_item.prev
            item.prev.next = item
            item.next.prev = item


class Item:
    def __init__(self, value, prev, next_=None):
        self.value = value
        self.prev = prev
        self.next = next_


def a(values):
    """Solve day 20 part 1"""
    dll = DoubleLinkedList(values)
    dll.mix()
    aslist = dll.to_list(from_zero=True)
    coords = [
        aslist[1_000 % len(aslist)],
        aslist[2_000 % len(aslist)],
        aslist[3_000 % len(aslist)],
    ]
    return sum(coords)


def b(values):
    """Solve day 20 part 2"""
    key = 811_589_153
    values = [v*key for v in values]
    dll = DoubleLinkedList(values)
    for _ in range(10):
        dll.mix()
    aslist = dll.to_list(from_zero=True)
    coords = [
        aslist[1_000 % len(aslist)],
        aslist[2_000 % len(aslist)],
        aslist[3_000 % len(aslist)],
    ]
    return sum(coords)



def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    return list(map(int, f.read_text().splitlines()))  # 1 value per line


def main():
    """Main function to wrap variables"""
    files = [
        'input20-test1.txt',
        'input20.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
