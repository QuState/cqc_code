from math import log2

def c_transform(state, c, t, gate): (1)
    n = int(log2(len(state)))
    for (k0, k1) in filter(lambda p: is_bit_set(p[0], c), pair_generator(n, t)): (2)
        process_pair(state, gate, k0, k1) (3)