def transform(state, gate):
    assert(len(state) == 2) (1)
    # assert norm close to 1
    z0 = state[0]
    z1 = state[1]
    state[0] = gate[0][0]*z0 + gate[0][1]*z1 (2)
    state[1] = gate[1][0]*z0 + gate[1][1]*z1 (3)