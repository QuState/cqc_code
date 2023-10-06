from math import log2, ceil, floor, isclose

def is_power_of_two(m):
    return ceil(log2(m)) == floor(log2(m))

def prepare_state(*a):
    state = [a[k] for k in range(len(a))]
    assert(is_power_of_two(len(state))) (1)
    assert(isclose(sum([abs(state[k])**2 for k in range(len(state))]), 1.0, rel_tol=1e-05)) (2)
    return state (3)