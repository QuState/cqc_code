import numpy as np

from math import pi

from hume.simulator.gates import *
from hume.simulator.core import transform, init_state, c_transform, mc_transform, measure, transform_u, c_transform_u


# CHAPTER 5 ------------------------------------------------------------------------------------------------------------
class Swap:
    def __init__(self, i, j):
        self.name = 'swap'
        self.i = i
        self.j = j

    def __str__(self):
        return f'swap {self.i} {self.j}'


# CHAPTER 4 ------------------------------------------------------------------------------------------------------------
class QuantumRegister:
    def __init__(self, size, shift=0):
        self.size = size
        self.shift = shift

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[ii] for ii in range(*key.indices(len(self)))]
        elif isinstance(key, int):
            if key < 0:
                key += len(self)
            assert(0 <= key < self.size)
            return self.shift + key

    def __len__(self):
        return self.size

    def __iter__(self):
        return list([self.shift + i for i in range(self.size)])

    def __reversed__(self):
        return list([self.shift + i for i in range(self.size)[::-1]])


class QuantumTransformation:
    def __init__(self, gate, target, controls=[], name=None, arg=None):
        self.gate = gate
        self.target = target
        self.controls = controls
        self.name = name
        self.arg = arg

    def __str__(self):
            return rf'{self.name} {round(self.arg, 2) if self.arg is not None else ""} {self.controls} {self.target}'

    def __copy__(self):
        return QuantumTransformation(self.gate, self.target, self.controls, self.name, self.arg)


class QuantumCircuit:
    def __init__(self, *args):
        bits = 0
        regs = []
        for register in args:
            register.shift = bits
            bits += register.size
            regs.append(register.size)

        self.state = init_state(bits)
        self.transformations = []
        self.regs = regs
        self.reports = {}

    def initialize(self, state):
        self.state = state

    def x(self, t):
        self.transformations.append(QuantumTransformation(x, t, [], 'x'))

    def y(self, t):
        self.transformations.append(QuantumTransformation(y, t, [], 'y'))

    def z(self, t):
        self.transformations.append(QuantumTransformation(z, t, [], 'z'))

    def h(self, t):
        self.transformations.append(QuantumTransformation(h, t, [], 'h'))

    def p(self, theta, t):
        self.transformations.append(QuantumTransformation(phase(theta), t, [], 'p', theta))

    def rx(self, theta, t):
        self.transformations.append(QuantumTransformation(rx(theta), t, [], 'rx', theta))

    def ry(self, theta, t):
        self.transformations.append(QuantumTransformation(ry(theta), t, [], 'ry', theta))

    def rz(self, theta, t):
        self.transformations.append(QuantumTransformation(rz(theta), t, [], 'rz', theta))

    def cx(self, c, t):
        self.transformations.append(QuantumTransformation(x, t, [c], 'cx'))

    def cy(self, c, t):
        self.transformations.append(QuantumTransformation(y, t, [c], 'cy'))

    def cz(self, c, t):
        self.transformations.append(QuantumTransformation(z, t, [c], 'cz'))

    def cp(self, theta, c, t):
        self.transformations.append(QuantumTransformation(phase(theta), t, [c], 'cp', theta))

    def cry(self, theta, c, t):
        self.transformations.append(QuantumTransformation(ry(theta), t, [c], 'cry', theta))

    def mcx(self, cs, t):
        self.transformations.append(QuantumTransformation(x, t, cs, 'mcx'))

    def mcp(self, theta, cs, t):
        self.transformations.append(QuantumTransformation(phase(theta), t, cs, 'mcp', theta))

    def measure(self, shots):
        return measure(self.state, shots)

    # CHAPTER 5 EXTENSION:
    def report(self, name=None):
        start_state = init_state(sum(self.regs))
        tr_count = 0
        for report in self.reports.values():
            if report[3] > tr_count:
                tr_count = report[3]
                start_state = report[2]

        qc = QuantumCircuit()
        qc.regs = self.regs.copy()
        qc.initialize(start_state.copy())
        qc.transformations = self.transformations[tr_count:].copy()
        end_state = qc.run()

        if name is None:
            name = len(self.reports)
        report = (start_state, self.transformations[tr_count:len(self.transformations)].copy(), end_state,
                  len(self.transformations))
        self.reports[name] = report
        return report

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

    def swap(self, i, j):
        self.transformations.append(Swap(i, j))

    def mswap(self, targets):
        for j in range(len(targets) // 2):
            self.swap(targets[j], targets[len(targets)-1-j])

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

    def qft(self, targets, swap=True):
        for j in range(len(targets))[::-1]:
            self.h(targets[j])
            for k in range(j)[::-1]:
                self.cp(pi * 2.0 ** (k - j), targets[j], targets[k])

        if swap:
            self.mswap(targets)

    def iqft(self, targets, swap=True):
        for j in range(len(targets))[::-1]:
            self.h(targets[j])
            for k in range(j)[::-1]:
                self.cp(-pi * 2 ** (k - j), targets[j], targets[k])

        if swap:
            self.mswap(targets)

    # CHAPTER 7 EXTENSION:
    def append(self, circuit, reg):
        assert(reg.size == sum(circuit.regs))
        for tr in circuit.transformations:
            if isinstance(tr, Swap):
                self.transformations.append(Swap(tr.i, tr.j))
                continue
            self.transformations.append(QuantumTransformation(tr.gate, reg.shift + tr.target,
                                                              tr.controls, tr.name, tr.arg))

    def c_append(self, circuit, c, reg):
        assert(c not in range(reg.shift, reg.shift + reg.size))
        for tr in circuit.transformations:
            self.transformations.append(QuantumTransformation(tr.gate, reg.shift + tr.target,
                                                              [c] + [reg.shift + t for t in tr.controls],
                                                              'c' + tr.name, tr.arg))

    def mc_append(self, circuit, cs, reg):
        assert(len(cs) == len(set(cs)))
        for c in cs:
            assert(c not in range(reg.shift, reg.shift + reg.size))
        for tr in circuit.transformations:
            self.transformations.append(QuantumTransformation(tr.gate, reg.shift + tr.target,
                                                              cs + [reg.shift + t for t in tr.controls],
                                                              'mc' + tr.name, tr.arg))

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

