def execute_turn(cur_direction, turn, degrees):
    directions = 'NESW'
    cur_idx = directions.index(cur_direction)
    change = degrees//90
    if turn == 'L':
        change *= -1
    return directions[(cur_idx + change) % 4]


def turn_wp(wp_ew, wp_ns, turn, degrees):
    right_turns = degrees // 90 if turn == 'R' else 4 - (degrees // 90)
    if right_turns == 1:
        return wp_ns, -wp_ew
    if right_turns == 2:
        return -wp_ew, -wp_ns
    if right_turns == 3:
        return -wp_ns, wp_ew


def a(instructions):
    eastwest, northsouth, direction = 0, 0, 'E'
    for instruction in instructions:
        action, value = instruction[0], int(instruction[1:])
        if action == 'F':
            action = direction

        if action == 'N':
            northsouth += value
        elif action == 'S':
            northsouth -= value
        elif action == 'E':
            eastwest += value
        elif action == 'W':
            eastwest -= value
        elif action in 'RL':
            direction = execute_turn(direction, action, value)

    return abs(eastwest) + abs(northsouth)


def b(instructions):
    pos_eastwest, pos_northsouth, wp_eastwest, wp_northsouth = 0, 0, 10, 1
    for instruction in instructions:
        action, value = instruction[0], int(instruction[1:])
        if action == 'F':
            pos_eastwest += value * wp_eastwest
            pos_northsouth += value * wp_northsouth
        elif action == 'N':
            wp_northsouth += value
        elif action == 'S':
            wp_northsouth -= value
        elif action == 'E':
            wp_eastwest += value
        elif action == 'W':
            wp_eastwest -= value
        elif action in 'RL':
            wp_eastwest, wp_northsouth = turn_wp(wp_eastwest, wp_northsouth, action, value)

    return abs(pos_eastwest) + abs(pos_northsouth)


if __name__ == '__main__':
    with open('input12.txt') as f:
        instructions = [line.strip() for line in f]

    print(a(instructions))
    print(b(instructions))
