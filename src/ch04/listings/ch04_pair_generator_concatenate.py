def pair_generator_concatenate(n, t):
    distance = int(2 ** t) (1)
    suffix_count = int(2 ** t) (2)
    prefix_count = int(2 ** (n - t - 1)) (2)

    for p in range(prefix_count): (3)
        for s in range(suffix_count):
            k0 = p * suffix_count*2 + s
            # the 1 side of the pair
            k1 = k0 + distance
            # print("(%s, %s)" %(padded_bin(n, k0), padded_bin(n, k1)))
            yield k0, k1