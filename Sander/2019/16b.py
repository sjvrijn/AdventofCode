from itertools import chain, repeat
import numpy as np

base_pattern = [1, 0, -1, 0]


def join(iterable):
    return ''.join(map(str, iterable))


with open('input16.txt') as f:
    raw_signal = next(f).strip()
    offset = int(raw_signal[:7])
    signal = list(map(int, raw_signal))
    print(len(signal))


num_repetitions = 10_000 - (offset // len(signal))

long_signal = list(chain.from_iterable(repeat(signal, num_repetitions)))
long_signal = list(reversed(long_signal[offset % len(signal):]))

for phase_idx in range(100):
    long_signal = np.cumsum(long_signal) % 10

print(join(list(reversed(long_signal.tolist()))[:8]))
