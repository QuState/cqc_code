from math import log2, sin, asin, sqrt, pi, cos

import numpy as np

from hume.simulator.circuit import QuantumRegister, QuantumCircuit
from hume.simulator.core import transform, init_state
from hume.simulator.gates import h, ry
from hume.tests.test_unitary import complex_sincd
from hume.utils.common import inner, is_close, all_close, complex_to_rgb, padded_bin


def inversion_with_inversion_0_uniform(state):
    n = int(log2(len(state)))
    for j in range(n):
        transform(state, j, h)
    state[0] *= -1
    for j in range(n):
        transform(state, j, h)
    # negative sign in theory
    for k in range(len(state)):
        state[k] *= -1


def inversion_with_inversion_0_binomial(state, phi):
    n = int(log2(len(state)))
    for j in range(n):
        transform(state, j, ry(-phi))
    state[0] *= -1
    for j in range(n):
        transform(state, j, ry(phi))
    for k in range(len(state)):
        state[k] *= -1


def oracle(state, predicate):
    for item in range(len(state)):
        if predicate(item):
            state[item] *= -1


def inversion(original, current):
    proj = inner(original, current)
    for k in range(len(current)):
        current[k] = 2*proj*original[k] - current[k]
        # assert is_close((original[k]*current[k].conjugate()).imag, 0) # in Grover iterate


def inversion_by_the_mean_direct(s, state):
    mean = 1/len(state)*sum(z for z in state)
    # print('\nmean', mean)
    proj = inner(s, state)

    for k in range(len(state)):
        # assert is_close(mean, proj*s[k])
        # state[k] = 2*proj*s[k] - state[k] # projection formula
        state[k] = 2*mean - state[k]


def grover_sim(state, predicate, iterations, phi=0):
    s = state.copy()

    # N = len(state)
    # count = [predicate(k) for k in range(N)].count(True)
    # theta = asin(sqrt(count/N))
    # p = 0
    # for item in range(len(state)):
    #     if predicate(item):
    #         p += abs(state[item])**2

    p = sum(abs(state[k])**2 for k in range(len(state)) if predicate(k))
    theta = asin(sqrt(p))
    assert is_close(inner(s, state), 1)

    # Grover iterate
    for it in range(1, iterations + 1):
        # oracle (reflection in bad state vector)
        oracle(state, predicate)

        # inversion (reflection in original state)
        inversion(s, state)
        # inversion_by_the_mean_direct(s, state) # works for uniform

        # alternative inversion
        # inversion_with_inversion_0_uniform(state)
        # inversion_with_inversion_0_binomial(state, phi)
        # print(f'iteration {it}', inner(s, state), cos(2*it*theta))
        assert is_close(inner(s, state), cos(2*it*theta))

        p = sum(abs(state[k])**2 for k in range(len(state)) if predicate(k))
        assert is_close(p, sin((2*it + 1)*theta)**2)


def random_transformation(n):
    import scipy.stats
    U = scipy.stats.unitary_group.rvs(2**n)

    def f_direct(state):
        assert(len(state) == 2**n)
        s = U @ state
        for k in range(len(s)):
            state[k] = s[k]

    def f_inverse(state):
        assert(len(state) == 2**n)
        s = np.conj(U.transpose()) @ state
        for k in range(len(s)):
            state[k] = s[k]

    return (f_direct, f_inverse)


def inversion_0_transformation(f, state):
    n = int(log2(len(state)))

    transform = f[0]
    inverse_transform = f[1]

    inverse_transform(state)
    inversion(init_state(n), state)
    transform(state)


def inversion_0_unitary(U, s):
    n = int(log2(len(s)))
    assert(U.shape[0] == 2**n)
    assert(U.shape[1] == 2**n)

    state = np.conj(U.transpose()) @ s

    # assert is_close(state[0].imag, 0) # only in Grover context

    # state[0] = state[0] - 2*state[0].conjugate()
    # for k in range(len(state)):
    #     state[k] = -state[k]

    inversion(init_state(n), state)

    state = U @ state

    for k in range(len(s)):
        s[k] = state[k]



def test_inversions_transformation():
    n = 3

    predicate = lambda k: True if k == 3 else False

    f = random_transformation(n)
    original_state = init_state(n)
    f[0](original_state)

    # seed = 777
    # state1 = generate_state(n, seed)
    state1 = original_state.copy()
    oracle(state1, predicate)
    inversion(original_state.copy(), state1)
    print('\n', state1)

    # state2 = generate_state(n, seed)
    state2 = original_state.copy()
    oracle(state2, predicate)
    inversion_0_transformation(f, state2)
    print('\n', state2)

    assert all_close(state1, state2)



def grover_sim_unitary(U, predicate, iterations):
    assert(U.shape[0] == U.shape[1])
    n = int(log2(U.shape[0]))

    state = U @ init_state(n)

    # Grover iterate
    for _ in range(iterations):
        # oracle (reflection in bad state vector)
        oracle(state, predicate)

        # inversion (reflection in original state)
        # inversion(s, state)
        # inversion_direct(s, state)
        inversion_0_unitary(U, state)

    return state


def test_grovers():
    n = 3

    items = [3, 5]
    predicate = lambda i: True if i in items else False

    import scipy.stats
    U = scipy.stats.unitary_group.rvs(2**n)

    s = U[:, 0] # state prepared by U

    iterations = 1

    state1 = s.tolist()
    grover_sim(state1, predicate, iterations)
    print('\n', np.array(state1))

    state2 = grover_sim_unitary(U, predicate, iterations)
    print('\n', state2)

    assert all_close(state1, state2)


# n = number of qubits,
# l = number of items
# j = iteration number
def target_amplitude_uniform(n, l, j):
    theta = asin(sqrt(l/2**n))
    return sin((2*j+1)*theta)/sqrt(l) # (-1)**j* without - in iterate
    # return sin((2*j+1)*asin(sqrt(l/2**n)))/sqrt(l)


# n = number of qubits,
# it = iteration number
# k = outcome
# phi = angle of ry rotations
def target_amplitude_binomial(n, it, k, phi):
    m = bin(k).count("1")
    theta = asin(sin(phi/2) ** m * cos(phi/2) ** (n - m))
    return sin((2*it+1)*theta)


def grover_circuit(A, O, iterations):
    n = sum(A.regs)
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    qc.append(A, q)

    for i in range(1, iterations + 1):
        qc.append(grover_iterate_circuit(A, O), q)

    return qc


def is_bit_not_set(m, k):
    return not (m & (1 << k))


def phase_oracle_match(n, items):
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    for m in items:
        for i in range(n):
            if is_bit_not_set(m, i):
                qc.x(q[i])

        qc.mcp(pi, [q[i] for i in range(len(q) - 1)], q[len(q) - 1])

        for i in range(n):
            if is_bit_not_set(m, i):
                qc.x(q[i])
    return qc


def inversion_circuit(prepare):
    n = sum(prepare.regs)
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    qc.append(prepare.inverse(), q)

    # for i in range(n):
    #     qc.x(q[i])
    #
    # # controlled Z
    # qc.mcp(pi, [q[i] for i in range(n - 1)], q[n - 1])
    #
    # for i in range(n):
    #     qc.x(q[i])
    qc.append(inversion_0_circuit(n), q)

    qc.append(prepare, q)

    return qc


def inversion_0_circuit(n):
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    for i in range(n):
        qc.x(q[i])

    # controlled Z
    qc.mcp(pi, [q[i] for i in range(n - 1)], q[n - 1])

    for i in range(n):
        qc.x(q[i])


    return qc


def grover_iterate_circuit(prepare, oracle):
    n = sum(oracle.regs)
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    # oracle
    qc.append(oracle, q)

    # inversion by the mean
    qc.append(inversion_circuit(prepare), q)

    return qc


def amplitude_estimation_circuit(n, prepare, oracle, swap=True):
    c = QuantumRegister(n)
    q = QuantumRegister(sum(prepare.regs))
    qc = QuantumCircuit(c, q)

    qc.append(prepare, q)
    qc.report('A')

    for i in range(n):
        qc.h(c[i])

    for i in range(n):
        for _ in range(2**i):
            if swap:
                qc.c_append(grover_iterate_circuit(prepare, oracle), c[i], q)
            else:
                qc.c_append(grover_iterate_circuit(prepare, oracle), c[n-1-i], q)

    qc.iqft(c if swap else c[::-1], swap)

    return qc


def simple_amplitude_estimation_circuit(prepare, oracle, iterations):
    c = QuantumRegister(1)
    q = QuantumRegister(sum(prepare.regs))
    qc = QuantumCircuit(c, q)

    qc.append(prepare, q)
    qc.report('A')

    qc.h(c[0])

    for _ in range(iterations):
            qc.c_append(grover_iterate_circuit(prepare, oracle), c[0], q)

    qc.h(c[0])

    return qc


def list_to_dict(state, show_binary=True):
    n = int(log2(len(state)))
    return dict(zip([str(k) + (('=' + padded_bin(n, k)) if show_binary else '') for k in range(len(state))],
                    [state[k] for k in range(len(state))]))


def plot_bars(bars, title, title_x, title_y, fig_name=None, plt=None):
    own_plt = plt is None
    if own_plt:
        import matplotlib.pyplot as plt

    if isinstance(bars, list):
        bars = dict(zip(range(len(bars)), bars))

    y_position = range(len(bars))
    plt.bar(y_position, [abs(v) for v in bars.values()], align='center', #width=0.257,
           color=[[x/255 for x in complex_to_rgb(round(v.real, 5) +1j*round(v.imag, 5))] for v in bars.values()])

    plt.xticks(y_position, bars.keys())
    if len(bars) > 32:
        plt.xticks(rotation=90, fontsize=6)
    else:
        plt.xticks(rotation=90, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel(title_x)
    plt.ylabel(title_y)
    plt.title(title)

    plt.tight_layout()
    fig = plt.gcf()
    if own_plt:
        plt.show()
    if fig_name:
        fig.savefig(fig_name)



def test_amplitude_estimation():
    n = 4
    m = 3

    for l in range(2**m):
        items = list(range(l))
        print('\nitems = ', list(items))
        qc = amplitude_estimation_circuit(n, prepare_uniform(m), phase_oracle_match(m, items), False)
        state = qc.run()
        # tabulate_state(state)

        probs = [0 for _ in range(2**n)]

        for j in range(2**n): # suffix
            for k in range(2**m): # prefix
                probs[j] += abs(state[k*2**n + j])**2


        # from count to v
        theta = 2*asin(sqrt(len(items)/2**m))
        v = theta/2/pi*2**n
        v = 2**n/pi*asin(sqrt(len(items)/2**m))

        sincd = [abs(a)**2 for a in complex_sincd(n-1, v)]

        for k in range(1, len(probs)//2):
            assert is_close(abs(probs[k])**2, abs(probs[len(probs) - k])**2)

        # print()
        # print([abs(state[k])**2 for k in range(2**(n+m))])

        # print('probs', probs)


        probs1 = [probs[0] + probs[len(probs)//2]] + [probs[k - len(probs)//2] + probs[k + len(probs)//2] for k in range(1, len(probs)//2)]

        # plot_bars(list_to_dict(probs), 'probs', '', '')
        # plot_bars(list_to_dict(probs1), 'probs1', '', '')
        # plot_bars(list_to_dict(sincd), 'sincd', '', '')

        assert all(abs(probs1[k] - abs(complex_sincd(n-1, v)[k])**2) < 0.01 for k in range(0, len(probs1)))
        # 0.0001 for m = 3, n = 8
        # 0.001 for m = 3, n = 7
        # 0.01 for m = 3, n = 4
        # assert all_close(probs1, sincd)

        # from v to count
        theta = v/2**n*pi*2
        count = 2**m * sin(theta/2)**2
        count = 2**m * sin(v*pi/2**n)**2
        assert(count, len(items))
        # print('count', count)

        if True:

            import matplotlib.pyplot as plt
            plot_bars(list_to_dict(probs, False), f'count={int(count)}, v={v}', 'Outcomes', 'Amplitudes')
            plot_bars(list_to_dict(probs1, False), f'count={int(count)}, v={v}', 'Outcomes', 'Amplitudes')
            plt.tight_layout()
            plt.show()

            amps = [0 for _ in range(2**n)]

            for j in range(2**n): # suffix
                for k in range(2**m): # prefix
                    amps[j] += state[k*2**n + j]

            # plot_bars(list_to_dict(amps, False), f'count={int(count)}, v={v}', 'Outcomes', 'Amplitudes')

        sines = {}
        for k, v in enumerate(probs[int(len(probs)/2):]):
            # key = 2**tgt_bits*np.round(np.cos(np.pi*k/2**ctrl_bits)**2, 4)
            key = 2**m*round(sin(k*pi/2**n)**2, 4)
            sines[key] = sines.get(key, 0) + round(v, 4)
        # print('sines', sines)
        # sorted_sines = sorted(sines.items(), key=lambda x: x[1], reverse=True)
        # print('sorted sines = ', sorted_sines)
        count = round(max(sines, key=sines.get))
        print('count ~ ', count)

        v = np.argmax(probs[int(len(probs)/2):])
        count1 = int(2**m*sin(v*pi/2**n)**2)
        print('count1 ~ ', count1)

        assert(count, len(items))

        # tabulate_state(probs)
        # tabulate_state(list(sines.values()))

