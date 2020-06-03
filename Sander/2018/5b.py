# coding: utf-8
from string import ascii_lowercase
with open('input5.txt') as f:
    polymer = next(f).strip()
    
    
def collapse(polymer, ignore):
    ignore = ignore.lower()
    it = iter(polymer)
    new_polymer = [next(it)]

    for unit in it:
        if unit.lower() == ignore:
            pass
        elif new_polymer and unit != new_polymer[-1] and unit.lower() == new_polymer[-1].lower():
            del new_polymer[-1]
        else:
            new_polymer.append(unit)
    
    return len(''.join(new_polymer))
min(
    ((letter, collapse(polymer, letter)) for letter in ascii_lowercase),
    key=lambda x: x[1],
)
