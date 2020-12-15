def determine_age(last, history, turn):
    if last not in history:
        return 0
    return turn - history[last] - 1


def a(values, end_at_turn=2020):
    history = {v: t for t, v in enumerate(values[:-1], start=1)}
    last_spoken = values[-1]
    for turn in range(len(values) + 1, end_at_turn + 1):
        to_speak = determine_age(last_spoken, history, turn)
        history[last_spoken] = turn - 1
        last_spoken = to_speak

    return to_speak


def b(values):
    return a(values, end_at_turn=30_000_000)


if __name__ == '__main__':
    with open('input15.txt') as f:
        values = list(map(int, next(f).strip().split(',')))

    print(a(values))
    print(b(values))
