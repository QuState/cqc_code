from math import pi

from ch04.sim_core import *
from ch03.sim_gates import *

from ch04.sim_circuit import QuantumCircuit as QuantumCircuit4
from ch04.sim_circuit import QuantumRegister as QuantumRegister4


class QuantumRegister(QuantumRegister4):
    def __init__(self, size, shift=0):
        self.size = size
        self.shift = shift


class Swap:
    def __init__(self, i, j):
        self.i = i
        self.j = j


class QuantumCircuit(QuantumCircuit4):

    def run(self):
        for tr in self.transformations:
            if isinstance(tr, Swap):
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
