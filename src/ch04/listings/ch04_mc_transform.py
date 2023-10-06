from math import log2

def mc_transform(state, cs, t, gate):
    assert not t in cs (1)
    n = int(log2(len(state)))
    for (k0, k1) in filter(lambda p: all([is_bit_set(p[0], c) for c in cs]), pair_generator(n, t)): (2)
        process_pair(state, gate, k0, k1) (3)