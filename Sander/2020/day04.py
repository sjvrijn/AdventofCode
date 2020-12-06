from re import fullmatch


def parse_passports(lines):
    passports = []
    passport = {}
    for line in lines:
        if not line:
            passports.append(passport)
            passport = {}
        else:
            for entry in line.split(' '):
                key, value = entry.split(':')
                passport[key] = value
    passports.append(passport)
    return passports


def is_valid_passport(passport):
    required_keys = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    given_keys = set(passport.keys())
    return len(required_keys - given_keys) == 0


def check_passport_data(passport):
    if passport['hgt'][-2:] == 'cm':
        hgt = 150 <= int(passport['hgt'][:-2]) <= 193
    elif passport['hgt'][-2:] == 'in':
        hgt = 59 <= int(passport['hgt'][:-2]) <= 76
    else:
        hgt = False

    result = [
        1920 <= int(passport['byr']) <= 2002,
        2010 <= int(passport['iyr']) <= 2020,
        2020 <= int(passport['eyr']) <= 2030,
        hgt,
        fullmatch('#[0-9a-f]{6}', passport['hcl']) is not None,
        passport['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
        fullmatch('\d{9}', passport['pid']) is not None,
    ]

    return all(result)


def a(passports):
    return sum(is_valid_passport(p) for p in passports)


def b(passports):
    return sum(is_valid_passport(p) and check_passport_data(p) for p in passports)


if __name__ == '__main__':
    with open('input04.txt') as f:
        passports = parse_passports([line.strip() for line in f])

    print(a(passports))
    print(b(passports))
