from ch04.sim_core import *
from ch03.sim_gates import *


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

    def report(self, name=None):
        if name is None:
            name = len(self.reports)
        report = (self.state.copy(), self.transformations, self.run().copy())
        self.reports[name] = report
        return report

    def compose(self, circuit):
        self.transformations += circuit.transformations

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
        self.transformations.append(QuantumTransformation(x, t, cs))

    def run(self):
        for tr in self.transformations:
            cs = tr.controls
            if len(cs) == 0:
                transform(self.state, tr.target, tr.gate)
            elif len(cs) == 1:
                c_transform(self.state, cs[0], tr.target, tr.gate)
            else:
                mc_transform(self.state, cs, tr.target, tr.gate)
        self.transformations = []
        return self.state

    def measure(self, shots):
        return measure(self.state, shots)
