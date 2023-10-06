import qiskit
from qiskit import QuantumCircuit, QuantumRegister, execute


def run(self): # Have to add self since this will become a method
    backend = qiskit.Aer.get_backend('statevector_simulator')
    job = execute(self, backend)
    state = job.result().get_statevector()
    return state


setattr(QuantumCircuit, 'run', run)

def test_cx():
    q = QuantumRegister(2)
    qc = QuantumCircuit(q)

    qc.h(q[0])
    qc.cx(q[0], q[1])

    print(qc.run())


def test_uniform_3():
    n = 3

    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    for i in range(len(q)):
        qc.h(q[i])

    print(qc.run())