def geometric_sequence_circuit(n, v):
    theta = v*2*pi/N

    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    for j in range(n):
        qc.h(q[j])

    for j in range(n):
        qc.p(2 ** j * theta, q[j])

    assert all_close(qc.run(), [sqrt(1/N) * cis(k*theta) for k in range(N)])