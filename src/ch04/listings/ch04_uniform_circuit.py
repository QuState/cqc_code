q = QuantumRegister(3)
qc = QuantumCircuit(q)

for i in range(len(q)):
    qc.h(q[i])

state = qc.run()