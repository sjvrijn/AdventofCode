# coding: utf-8
with open('input5.txt') as f:
    polymer = next(f).strip()
    
    
it = iter(polymer)
new_polymer = [next(it)]

for unit in it:
    if new_polymer and unit != new_polymer[-1] and unit.lower() == new_polymer[-1].lower():
        del new_polymer[-1]
    else:
        new_polymer.append(unit)
        
len(''.join(new_polymer))
