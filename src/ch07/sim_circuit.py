from ch07.sim_core import *
from ch07.sim_core import measure
from ch03.sim_gates import *


from ch06.sim_circuit import QuantumRegister as QuantumRegister6
from ch06.sim_circuit import QuantumTransformation as QuantumTransformation6
from ch06.sim_circuit import QuantumCircuit as QuantumCircuit6
from ch05.sim_circuit import Swap

import numpy as np


class QuantumRegister(QuantumRegister6):
    pass


class QuantumTransformation(QuantumTransformation6):
    pass


class QuantumCircuit(QuantumCircuit6):
    def measure(self, shots = 0):
        state = self.run()
        samples = measure(state, shots)
        return {'state vector': state, 'counts': samples}

    def append(self, circuit, reg):
        assert(reg.size == sum(circuit.regs))
        for tr in circuit.transformations:
            self.transformations.append(QuantumTransformation(tr.gate, reg.shift + tr.target, tr.controls, tr.name, tr.arg))

    def c_append(self, circuit, c, reg):
        assert(c not in range(reg.shift, reg.shift + reg.size))
        for tr in circuit.transformations:
            self.transformations.append(QuantumTransformation(tr.gate, reg.shift + tr.target, [c] + [reg.shift + t for t in tr.controls], 'c' + tr.name, tr.arg))

    def mc_append(self, circuit, cs, reg):
        assert(len(cs) == len(set(cs)))
        for c in cs:
            assert(c not in range(reg.shift, reg.shift + reg.size))
        for tr in circuit.transformations:
            self.transformations.append(QuantumTransformation(tr.gate, reg.shift + tr.target, cs + [reg.shift + t for t in tr.controls], 'mc' + tr.name, tr.arg))

    def unitary(self, U, t):
        self.transformations.append(QuantumTransformation(U, t, [], 'unitary'))

    def append_u(self, U, q):
        assert(U.shape[0] == U.shape[1] == 2**q.size)
        self.unitary(U, q.shift)

    def c_unitary(self, U, c, t):
        self.transformations.append(QuantumTransformation(U, t, [c], 'unitary'))

    def c_append_u(self, U, c, q):
        assert(U.shape[0] == U.shape[1] == 2**q.size)
        self.c_unitary(U, c, q.shift)


    def inverse(self):
        qs = [QuantumRegister(size, 'q' if len(self.regs) == 1 else None) for size in self.regs]
        qc = QuantumCircuit(*qs)

        for tr in self.transformations[::-1]:
            if isinstance(tr, Swap):
                qc.swap(tr.i, tr.j)
                continue

            if tr.name == 'unitary':
                cs = tr.controls
                if len(cs) == 0:
                    qc.unitary(np.conj(tr.gate.transpose()), tr.target)
                    continue
                elif len(cs) == 1:
                    qc.c_unitary(np.conj(tr.gate.transpose()), cs[0], tr.target)
                    continue

            m = getattr(qc, tr.name)
            cs = tr.controls

            t = tr.target
            reg = 0
            while t >= self.regs[reg]:
                t = t - self.regs[reg]
                reg = reg + 1

            if len(cs) == 0:
                if tr.arg:
                    m(-tr.arg, qs[reg][t])
                else:
                    m(qs[reg][t])
            elif len(cs) == 1:
                if tr.arg:
                    m(-tr.arg, cs[0], qs[reg][t])
                else:
                    m(cs[0], qs[reg][t])

        return qc

    def run(self):
        for tr in self.transformations:
            if tr.name == 'unitary':
                cs = tr.controls
                if len(cs) == 0:
                    transform_u(self.state, tr.gate, tr.target)
                elif len(cs) == 1:
                    c_transform_u(self.state, tr.gate, cs[0], tr.target)

            elif isinstance(tr, Swap):
                c_transform(self.state, tr.i, tr.j, x)
                c_transform(self.state, tr.j, tr.i, x)
                c_transform(self.state, tr.i, tr.j, x)
            else:
                cs = tr.controls
                if len(cs) == 0:
                    transform(self.state, tr.target, tr.gate)
                elif len(cs) == 1:
                    c_transform(self.state, cs[0], tr.target, tr.gate)
                else:
                    mc_transform(self.state, cs, tr.target, tr.gate)
        self.transformations = []
        return self.state