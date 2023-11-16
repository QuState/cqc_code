from ch06.sim_core import *

def transform_u(state, U, t):
    assert(U.shape[0] == U.shape[1])
    m = int(log2(U.shape[0]))
    n = int(log2(len(state)))

    vec = [_ for _ in range(2**m)]

    for suffix in range(2**t):
        for prefix in range(2**(n-m-t)):
            for target in range(2**m):
                k = prefix*2**(t+m) + target*2**t + suffix
                vec[target] = state[k]

            vec_out = U @ vec

            for target in range(2**m):
                k = prefix*2**(t+m) + target*2**t + suffix
                state[k] = vec_out[target]


def c_transform_u(state, U, c, t):
    # print()
    # from sim import is_bit_set, pair_generator_concatenate
    # for (k0, k1) in filter(lambda p: is_bit_set(p[0], c), pair_generator_concatenate(4, t)):
    #     print(k0, k1)
    # vec = np.array([self.state[k0], self.state[k1]])
    # vec_out = U @vec
    # self.state[k0] = vec_out[0]
    # self.state[k1] = vec_out[1]

    assert(U.shape[0] == U.shape[1])
    m = int(log2(U.shape[0]))
    n = int(log2(len(state)))

    vec = [_ for _ in range(2**m)]

    for suffix in range(2**t):
        for prefix in range(2**(n-m-t)):
            targets = []
            for idx in range(2**m):
                k = prefix*2**(t+m) + idx*2**t + suffix
                if k & (1 << c):
                    # if is_bit_set(k, c):
                    vec[idx] = state[k]
                    targets.append(k)
            # print(f'processing set {[bin(l)[2:].zfill(n) for l in targets]}', [l for l in targets])

            vec_out = U @ vec

            for idx in range(2**m):
                k = prefix*2**(t+m) + idx*2**t + suffix
                if k & (1 << c):
                    # if is_bit_set(k, c):
                    state[k] = vec_out[idx]