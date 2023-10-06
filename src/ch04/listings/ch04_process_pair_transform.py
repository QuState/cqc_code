def process_pair(state, gate, k0, k1):
    x = state[k0] (1)
    y = state[k1] (1)
    # new amplitudes
    state[k0] = x * gate[0][0] + y * gate[0][1] (2)
    state[k1] = x * gate[1][0] + y * gate[1][1] (2)

def transform(state, t, gate):
    n = int(log2(len(state))) (3)
    for (k0, k1) in pair_generator(n, t): (4)
        process_pair(state, gate, k0, k1) (5)