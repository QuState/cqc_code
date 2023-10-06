q = QuantumRegister(n)
qc = QuantumCircuit(q)

for i in range(len(q)): (1)
    qc.ry(theta, q[i])