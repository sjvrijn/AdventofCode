import numpy as np

base_pattern = [0, 1, 0, -1]


def matrix_fft(data, num_phases):
    pattern = np.triu(np.ones((len(data), len(data)), dtype=np.int))

    for idx in range(len(data)//2):
        num_to_fill = len(data) - idx
        tiled_pattern = np.tile(np.repeat(base_pattern, idx+1), len(data)//4 + 1)
        pattern[idx, idx:] = tiled_pattern[:num_to_fill]

    dvec = np.array(data, dtype=np.int)
    for phase_idx in range(num_phases):
        dvec = np.abs(np.dot(pattern, dvec)) % 10

    return dvec.tolist()


def join(iterable):
    return ''.join(map(str, iterable))


def examples():
    signal = list(map(int, '12345678'))
    print(f"simple test:")

    out = matrix_fft(signal, num_phases=1)
    print(join(out) == '48226158')

    out = matrix_fft(signal, num_phases=2)
    print(join(out) == '34040438')

    out = matrix_fft(signal, num_phases=3)
    print(join(out) == '03415518')

    out = matrix_fft(signal, num_phases=4)
    print(join(out) == '01029498')
    print()


    signal = list(map(int, '80871224585914546619083218645595'))
    print(f"test 1:")
    out = matrix_fft(signal, num_phases=100)
    print(join(out[:8]) == '24176176')
    print()


    signal = list(map(int, '19617804207202209144916044189917'))
    print(f"test 2:")
    out = matrix_fft(signal, num_phases=100)
    print(join(out[:8]) == '73745418')
    print()


    signal = list(map(int, '69317163492948606335995924319873'))
    print(f"test 3:")
    out = matrix_fft(signal, num_phases=100)
    print(join(out[:8]) == '52432133')
    print()


examples()  # Passed


with open('input16.txt') as f:
    raw_signal = next(f).strip()
    signal = list(map(int, raw_signal))

out = matrix_fft(signal, num_phases=100)
print(join(out[:8]))
