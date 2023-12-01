from math import pi

from hume.simulator.circuit import QuantumRegister, QuantumCircuit
from hume.simulator.gates import *
from hume.utils.common import all_close, print_state_table, prod, cis, CONFIG


def complex_sincd(n, v):
    # same as value encoding state
    N = 2**n
    p = [prod(cos((v-k)*pi/2**(j+1))*cis((v-k)*pi/2**(j+1)) for j in range(n)) for k in range(2**n)]
    c = [prod(cos((v-k)*pi/2**(j+1)) for j in range(n))*cis((N-1)/N * (v-k)*pi) for k in range(2**n)]
    assert all_close(p, c)

    return c


def test_unitary():
    CONFIG.use_mpl()
    n = 3
    theta = 4.7*pi/2**(n-1)

    inverse = True

    import numpy as np

    def gate_to_unitary(gate):
        return np.array(gate)

    N = 2**n

    states = {}
    for unitary in [True, False]:
        q = QuantumRegister(n)
        a = QuantumRegister(1)
        qc = QuantumCircuit(q, a) # ancilla is last qubit

        if not unitary:
            qc.x(a[0])
            qc.rx(-pi/2, a[0])

            for i in range(n):
                qc.h(q[i])

            for i in range(n):
                for _ in range(2**i):
                    qc.cry(2*theta, q[i], a[0])

            if inverse:
                qc.rx(pi/2, a[0])
                qc.x(a[0])

            qc.iqft(q)

            states[unitary] = qc.run()
        else:
            qc.append_u(gate_to_unitary(x), a)
            # qc.unitary(gate_to_unitary(x), a[0])
            qc.unitary(gate_to_unitary(rx(-pi/2)), a[0])

            for i in range(n):
                qc.unitary(gate_to_unitary(h), q[i])

            for i in range(n):
                for _ in range(2**i):
                    # qc.c_unitary(gate_to_unitary(ry(2*theta)), q[i], a[0])
                    qc.c_append_u(gate_to_unitary(ry(2*theta)), q[i], a)

            if inverse:
                qc.unitary(gate_to_unitary(rx(pi/2)), a[0])
                qc.unitary(gate_to_unitary(x), a[0])

            qc.iqft(q)

            states[unitary] = qc.run()

    for unitary in [False, True]:
        print_state_table(states[unitary])

    assert all_close(states[True], states[False])
    state = states[True]
    if inverse:
        s = complex_sincd(n, theta/(2*pi)*N)
        assert all_close(state[:N], s)
    else:
        s = complex_sincd(n, theta/(2*pi)*N)
        assert all_close(state, [1/sqrt(2)*1j*a for a in s] + [1/sqrt(2)*a for a in s])


if __name__ == "__main__":
    CONFIG.use_mpl(True)
    test_unitary()
