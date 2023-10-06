q = QuantumRegister(1)
qc = QuantumCircuit(q)

theta = pi/3
qc.h(q[0])
qc.p(theta, q[0])
qc.h(q[0])

state = qc.run()