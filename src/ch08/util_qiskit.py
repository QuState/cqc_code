from ch07.util_qiskit import *


def print_circuit(qc):
    qc_qiskit = hume_to_qiskit(qc.regs, qc.transformations)
    print(qc_qiskit)


def draw_circuit(qc, format='text'):
    qc_qiskit = hume_to_qiskit(qc.regs, qc.transformations)
    return qc_qiskit.draw(format)
