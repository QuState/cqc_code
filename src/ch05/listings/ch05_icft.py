def icft(state):
    N = len(state)
    s = [state[k] for k in range(N)]

    for i in range(N):
        state[i] = inner(s, fourier_basis(N, i))