def uniform(n):
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    for i in range(len(q)):
        qc.h(q[i])

    return qc