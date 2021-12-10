MATCHING_PAIRS = {'(': ')', '[': ']', '{': '}', '<': '>'}


def a(lines):
    error_score = {')': 3, ']': 57,  '}': 1197, '>': 25137}
    total_score = 0
    for line in lines:
        stack = []
        for char in line:
            if char in ['(', '[', '{', '<']:
                stack.append(char)
            elif char == MATCHING_PAIRS[stack[-1]]:
                stack.pop()
            else:
                total_score += error_score[char]
                break
    return total_score


def b(lines):
    close_score = {')': 1, ']': 2,  '}': 3, '>': 4}
    scores = []
    for line in lines:
        stack = get_stack_to_complete(line)
        if not stack:
            continue
        completion_score = 0
        for char in reversed(stack):
            matching_char = MATCHING_PAIRS[char]
            completion_score = (completion_score*5) + close_score[matching_char]
        scores.append(completion_score)

    return sorted(scores)[len(scores)//2]


def get_stack_to_complete(line):
    stack = []
    for char in line:
        if char in ['(', '[', '{', '<']:
            stack.append(char)
        elif char == MATCHING_PAIRS[stack[-1]]:
            stack.pop()
        else:
            break
    else:
        return stack
    return None


if __name__ == '__main__':
    files = [
        'input10-test1.txt',
        'input10.txt',
    ]
    for filename in files:
        print(filename)
        with open(filename) as f:
            lines = f.read().splitlines()  # multi-line file

        print(f'A: {a(lines)}')
        print(f'B: {b(lines)}')
