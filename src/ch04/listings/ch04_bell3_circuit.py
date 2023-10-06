q = QuantumRegister(2)
qc = QuantumCircuit(q)

qc.h(q[0])
qc.x(q[1])
qc.cx(q[0], q[1])

state = qc.run()