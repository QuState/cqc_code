from ch07.sim_core import *
from ch07.sim_core import measure
from ch03.sim_gates import *


from ch06.sim_circuit import QuantumRegister as QuantumRegister6
from ch06.sim_circuit import QuantumTransformation as QuantumTransformation6
from ch06.sim_circuit import QuantumCircuit as QuantumCircuit6


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
