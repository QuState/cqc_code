def pair_generator_pattern(n, t):
    distance = int(2 ** t) (1)

    for j in range(2**(n-t-1)):
        for k0 in range(2*j*distance, (2*j+1)*distance): (2)
            k1 = k0 + distance (3)
            yield k0, k1