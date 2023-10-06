def is_bit_set(m, k):
    return m & (1 << k)

def pair_generator_check_digit(n, t):
    distance = int(2 ** t) (1)

    for k0 in range(2**n): (2)
        if not is_bit_set(k0, t): (3)
            k1 = k0 + distance (4)
            yield k0, k1