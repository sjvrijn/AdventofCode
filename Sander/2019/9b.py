from intcode import read_instructions, intcode


test1 = list(map(int, "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(',')))
test2 = list(map(int, "1102,34915192,34915192,7,4,7,99,0".split(',')))
test3 = list(map(int, "104,1125899906842624,99".split(',')))

print(all(a == b for a, b in zip(list(intcode(test1)), test1)))
print(len(str(list(intcode(test2))[0])) == 16)
print(list(intcode(test3))[0] == test3[1])

instructions = read_instructions('input9.txt')
print(list(intcode(instructions, inputs=[2], verbose=False)))
