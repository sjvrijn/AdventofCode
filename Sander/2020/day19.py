from itertools import product

from more_itertools import all_equal, chunked
from parse import parse


def a(rule_list, messages):
    return sum(m in rule_list[0] for m in messages)


def create_rule_list(rules):
    rule_list = parse_rules(rules)
    completed_rules = {
        num
        for num, rule in rule_list.items()
        if isinstance(rule, set)
    }
    uncompleted_rules = set(rule_list.keys()) - completed_rules
    while uncompleted_rules:
        for rule_num in uncompleted_rules:
            if not can_be_replaced(rule_num, rule_list, completed_rules):
                continue

            new_set = set()
            for tuple_ in rule_list[rule_num]:
                if len(tuple_) == 1:
                    new_set = new_set.union(rule_list[tuple_[0]])
                else:
                    tuple_ = [rule_list[t] for t in tuple_]
                    for combos in product(*tuple_):
                        new_set.add(''.join(combos))
            rule_list[rule_num] = new_set
            completed_rules.add(rule_num)

        uncompleted_rules -= completed_rules

    return rule_list


def parse_rules(rules):
    rule_list = {}
    for rule in rules.split('\n'):
        num, definition = parse('{:d}: {}', rule.strip())

        if '"' in definition:
            rule_list[num] = set(definition[1])
        else:
            rule_list[num] = [
                tuple(map(int, def_set.split(' ')))
                for def_set in definition.split(' | ')
            ]
    return rule_list


def can_be_replaced(rule_num, rule_list, completed_rules):
    return all(
            rule_num in completed_rules
            for def_set in rule_list[rule_num]
            for rule_num in def_set
    )


def b(rule_list, messages):

    valid_messages = {m for m in messages if m in rule_list[0]}
    leftover_messages = set(messages) - valid_messages

    chunk_lengths = [len(r) for r in rule_list[42].union(rule_list[31])]
    if not all_equal(chunk_lengths):
        raise ValueError('Unexpected rule: not all parts have the same length')
    chunk_length = chunk_lengths[0]

    for m in leftover_messages:
        chunks = [''.join(chunk) for chunk in chunked(m, chunk_length)]
        print(chunks)
        valid_42, valid_31 = 0, 0
        valid_in_42 = [False for _ in chunks]
        valid_in_31 = [False for _ in chunks]
        for idx, chunk in enumerate(chunks):
            if chunk not in rule_list[42]:
                break
            valid_42 += 1
            valid_in_42[idx] = True
        for idx, chunk in enumerate(reversed(chunks), start=1):
            if chunk not in rule_list[31]:
                break
            valid_31 += 1
            valid_in_31[-idx] = True

        print(valid_in_42)
        print(valid_in_31)


        if valid_42 >= 2 and\
                valid_31 >= 1 and\
                valid_42 > valid_31:
            print('valid')
            valid_messages.add(m)
        else:
            print('invalid')

        print()

    print(valid_messages)

    return len(valid_messages)




if __name__ == '__main__':
    with open('input19-test3.txt') as f:
        rules, messages = f.read().split('\n\n')

    messages = messages.split('\n')
    rule_list = create_rule_list(rules)

    print(a(rule_list, messages))
    print(b(rule_list, messages))
