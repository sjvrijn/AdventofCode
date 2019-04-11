
recipes = [3, 7]
elf1, elf2 = 0, 1

start_idx = 320851

while len(recipes) < start_idx+10:
    new_recipe = recipes[elf1] + recipes[elf2]
    if new_recipe >= 10:
        recipes.extend([1, new_recipe %10])
    else:
        recipes.append(new_recipe)

    elf1 += 1+recipes[elf1]
    elf1 %= len(recipes)

    elf2 += 1+recipes[elf2]
    elf2 %= len(recipes)

print(''.join(map(str, recipes[-10:])))


