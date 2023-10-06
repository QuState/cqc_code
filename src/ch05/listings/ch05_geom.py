def geom(n, theta):
    N = 2**n
    return [sqrt(1/N) * cis(k*theta) for k in range(N)]