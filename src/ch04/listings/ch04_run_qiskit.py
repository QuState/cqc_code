import qiskit
from qiskit import QuantumCircuit, QuantumRegister, execute

def run(self):
    backend = qiskit.Aer.get_backend('statevector_simulator')
    job = execute(self, backend)
    state = job.result().get_statevector()
    return state


setattr(QuantumCircuit, 'run', run)