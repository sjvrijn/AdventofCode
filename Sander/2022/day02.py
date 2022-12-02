from pathlib import Path


WIN = 6
DRAW = 3
LOSS = 0


def a(lines):
    """Solve day 2 part 1"""
    scores = {
        'X': 1,
        'Y': 2,
        'Z': 3,
    }
    rock_paper_scissors = {
        'A': {
            'X': DRAW,
            'Y': WIN,
            'Z': LOSS,
        },
        'B': {
            'X': LOSS,
            'Y': DRAW,
            'Z': WIN,
        },
        'C': {
            'X': WIN,
            'Y': LOSS,
            'Z': DRAW,
        },
    }
    return sum(rock_paper_scissors[p1][p2] + scores[p2] for p1, p2 in lines)


def b(lines):
    """Solve day 2 part 2"""
    scores = {
        'rock': 1,
        'paper': 2,
        'scissors': 3,
        'X': LOSS,
        'Y': DRAW,
        'Z': WIN,
    }
    rock_paper_scissors = {
        'X': {
            'A': 'scissors',
            'B': 'rock',
            'C': 'paper',
        },
        'Y': {
            'A': 'rock',
            'B': 'paper',
            'C': 'scissors',
        },
        'Z': {
            'A': 'paper',
            'B': 'scissors',
            'C': 'rock',
        },
    }
    return sum(scores[rock_paper_scissors[p2][p1]] + scores[p2] for p1, p2 in lines)


def parse_file(f: Path):
    """Parse the input file into relevant data structure"""
    lines = f.read_text().splitlines()

    return [line.split() for line in lines]


def main():
    """Main function to wrap variables"""
    files = [
        'input02-test1.txt',
        # 'input02-test2.txt',
        # 'input02-test3.txt',
        'input02.txt',
    ]
    for filename in files:
        print(filename)
        data = parse_file(Path(filename))

        print(f'A: {a(data)}')
        print(f'B: {b(data)}')


if __name__ == '__main__':
    main()
