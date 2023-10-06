def classical_inverse_fourier(state, step, targets):
    n = len(targets)
    sq2 = sqrt(2)
    sq2i = 1/sqrt(2)
    for j in range(n)[::-1]:
        dist = 2**j
        rot = cis(-pi/dist)
        rots = [1 for _ in range(dist)]
        r = 1
        for m in range(dist):
            rots[m] = r
            r = r*rot

        for l in range(2**(n-j-1)):
            i = 0
            for k in range(2*l*dist, (2*l+1)*dist):
                state[k] = sq2i*(state[k] + state[k+dist])
                state[k+dist] = (state[k] - sq2*state[k+dist])*rots[i]
                i += 1