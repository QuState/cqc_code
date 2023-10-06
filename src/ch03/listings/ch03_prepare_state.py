from math import isclose

def prepare_state(*a):
    state = [a[k] for k in range(len(a))] (1)
    assert(len(state) == 2) (2)
    assert(isclose(sum([abs(state[k])**2 for k in range(len(state))]), 1)) (3)
    return state
