from math import log2, cos, sin, ceil, floor, isclose
from random import choices
from collections import Counter


def is_power_of_two(m):
    return ceil(log2(m)) == floor(log2(m))


def prepare_state(*a):
    state = [a[k] for k in range(len(a))]
    assert(is_power_of_two(len(state)))
    assert(isclose(sum([abs(state[k])**2 for k in range(len(state))]), 1.0, rel_tol=1e-05))
    return state


def init_state(n):
    state = [0 for _ in range(2 ** n)]
    state[0] = 1
    return state


def is_bit_set(m, k):
    return m & (1 << k)


def pair_generator_check_digit(n, t):
    distance = int(2 ** t)

    for k0 in range(2**n):
        if not is_bit_set(k0, t):
            k1 = k0 + distance
            yield k0, k1


def pair_generator_concatenate(n, t):
    distance = int(2 ** t)
    suffix_count = int(2 ** t)
    prefix_count = int(2 ** (n - t - 1))

    for p in range(prefix_count):
        for s in range(suffix_count):
            k0 = p * suffix_count*2 + s
            # the 1 side of the pair
            k1 = k0 + distance
            # print("(%s, %s)" %(padded_bin(n, k0), padded_bin(n, k1)))
            yield k0, k1


def pair_generator_pattern(n, t):
    distance = int(2 ** t)

    for j in range(2**(n-t-1)):
        for k0 in range(2*j*distance, (2*j+1)*distance):
            k1 = k0 + distance
            yield k0, k1

# TODO: check this is best place to define pair_generator
pair_generator = pair_generator_concatenate


def process_pair(state, gate, k0, k1):
    x = state[k0]
    y = state[k1]
    # new amplitudes
    state[k0] = x * gate[0][0] + y * gate[0][1]
    state[k1] = x * gate[1][0] + y * gate[1][1]


def transform(state, t, gate):
    n = int(log2(len(state)))
    for (k0, k1) in pair_generator(n, t):
        process_pair(state, gate, k0, k1)


def c_transform(state, c, t, gate):
    n = int(log2(len(state)))
    for (k0, k1) in filter(lambda p: is_bit_set(p[0], c), pair_generator(n, t)):
        process_pair(state, gate, k0, k1)


def mc_transform(state, cs, t, gate):
    assert not t in cs
    n = int(log2(len(state)))
    for (k0, k1) in filter(lambda p: all([is_bit_set(p[0], c) for c in cs]), pair_generator(n, t)):
        process_pair(state, gate, k0, k1)


def measure(state, shots):
    samples = choices(range(len(state)), [abs(state[k])**2 for k in range(len(state))], k=shots)
    counts = {}
    for (k, v) in Counter(samples).items():
        counts[k] = v
    return counts


def cis(theta):
    return cos(theta) + 1j*sin(theta)