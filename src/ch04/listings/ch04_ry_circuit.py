q = QuantumRegister(3)
qc = QuantumCircuit(q)

for i in range(len(q)):
    qc.ry(pi/3, q[i])

state = qc.run()