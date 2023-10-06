from math import pi
from sim_circuit import QuantumRegister, QuantumCircuit

def real_valued_sinusoids(n, v):
    N = 2**n
    theta = v*2*pi/N

    q = QuantumRegister(n)
    a = QuantumRegister(1)
    qc = QuantumCircuit(q, a) # ancilla is last qubit

    for j in range(n):
        qc.h(q[j])

    for j in range(n):
        qc.cry(2**(j+1)*theta, q[j], a[0])

    return qc