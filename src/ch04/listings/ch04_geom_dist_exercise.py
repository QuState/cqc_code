q = QuantumRegister(n)
qc = QuantumCircuit(q)

for i in range(len(q)):
    qc.ry(theta, q[k])

for i in range(len(q) - 1):
    qc.cry(pi - theta, q[k], q[k+1])

z = qc.run()