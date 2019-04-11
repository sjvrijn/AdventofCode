import sys


recipes = [3, 7]
elf1, elf2 = 0, 1

target = '320851'

it = 0

while target not in ''.join(map(str, recipes[-20:])):
    new_recipe = recipes[elf1] + recipes[elf2]
    if new_recipe >= 10:
        recipes.extend([1, new_recipe % 10])
    else:
        recipes.append(new_recipe)

    elf1 += 1+recipes[elf1]
    elf1 %= len(recipes)

    elf2 += 1+recipes[elf2]
    elf2 %= len(recipes)

    it += 1
    if it % 1_000_000 == 0:
        print(it)
        sys.stdout.flush()


if target == ''.join(map(str, recipes[-6:])):
    print(len(recipes)-6)
else:
    print(len(recipes)-7)

print(f'{len(recipes)}: {recipes[-10:]}')

