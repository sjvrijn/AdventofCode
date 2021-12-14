from collections import defaultdict
from copy import copy


def a(edges):
    options = set(edges.keys()) - {'start'}
    route = ['start']
    routes = build_single_visit_routes(route, options, edges)
    return len(routes)


def b(edges):
    options = set(edges.keys()) - {'start'}
    route = ['start']
    routes = build_double_visit_routes(route, options, edges)
    return len(routes)


def build_single_visit_routes(route, options, edges):
    if len(options) == 0:
        return []
    routes = []
    for option in options:
        if option in edges[route[-1]]:
            new_route = copy(route) + [option]
            if option == 'end':
                routes.append(new_route)
            elif option.islower():
                routes.extend(build_single_visit_routes(new_route, options - {option}, edges))
            else:
                routes.extend(build_single_visit_routes(new_route, options, edges))
    return routes


def build_double_visit_routes(route, options, edges):
    if len(options) == 0:
        return []
    routes = []
    for option in options:
        if option in edges[route[-1]]:
            new_route = copy(route) + [option]
            if not is_double_visit_safe(new_route):
                continue
            if option == 'end':
                routes.append(new_route)
            else:
                routes.extend(build_double_visit_routes(new_route, options, edges))
    return routes


def is_double_visit_safe(route):
    counts = [route.count(x) for x in set(route) if x.islower()]
    at_most_one_visited_more_than_once = sum(count >= 2 for count in counts) < 2
    none_visited_thrice = sum(count > 2 for count in counts) < 1
    return at_most_one_visited_more_than_once and none_visited_thrice


if __name__ == '__main__':
    files = [
        'input12-test1.txt',
        'input12-test2.txt',
        'input12-test3.txt',
        'input12.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            lines = f.read().splitlines()  # multi-line file

        edges = defaultdict(list)
        for line in lines:
            start, end = line.split('-')
            edges[start].append(end)
            edges[end].append(start)

        print(f'A: {a(edges)}')
        print(f'B: {b(edges)}')
