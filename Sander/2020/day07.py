from parse import parse
import networkx as nx


def a(bag_rules):
    return len(nx.algorithms.ancestors(bag_rules, 'shiny gold'))


def b(bag_rules):
    return count_required_bags(bag_rules, bag='shiny gold') - 1


def count_required_bags(bag_rules, bag):

    num_bags = 1
    for inner_bag, attr in bag_rules[bag].items():
        num_bags += count_required_bags(bag_rules, inner_bag) * attr['num']
    return num_bags


if __name__ == '__main__':

    line_template = '{} bags contain {}.'
    bags_template = '{:d} {:l} {:l} {bags:l}'

    edge_list = []
    with open('input07.txt') as f:
        for line in f:
            outer, inner = parse(line_template, line)
            if inner == 'no other bags':
                continue
            for entry in inner.split(', '):
                num, shade, color = parse(bags_template, entry)
                edge_list.append((outer, ' '.join([shade, color]), {'num': num}))

    bag_rules = nx.DiGraph(edge_list)

    print(a(bag_rules))
    print(b(bag_rules))
