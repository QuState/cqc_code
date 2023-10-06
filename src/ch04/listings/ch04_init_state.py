def init_state(n):
    state = [0 for _ in range(2 ** n)] (1)
    state[0] = 1 (2)
    return state