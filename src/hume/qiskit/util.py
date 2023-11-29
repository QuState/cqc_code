from math import log2

import qiskit
from qiskit import QuantumRegister, QuantumCircuit, execute

from hume.simulator.circuit import Swap
from hume.utils.common import print_state_table, all_close, CONFIG


def run(self):
    backend = qiskit.Aer.get_backend('statevector_simulator')
    job = execute(self, backend)
    state = job.result().get_statevector()
    return state


setattr(QuantumCircuit, 'run', run)


def hume_to_qiskit(regs, transformations):
    qs = [QuantumRegister(size, 'q' if len(regs) == 1 else None) for size in regs]
    qc = QuantumCircuit(*qs)

    for tr in transformations:
        if isinstance(tr, Swap):
            qc.swap(tr.i, tr.j)
            continue
        if tr.name == 'unitary':
            U = tr.gate
            assert(U.shape[0] == U.shape[1])
            m = int(log2(U.shape[0]))
            qc.unitary(U, [i + tr.target for i in range(m)])
            continue

        m = getattr(qc, tr.name)
        cs = tr.controls

        t = tr.target
        reg = 0
        while t >= regs[reg]:
            t = t - regs[reg]
            reg = reg + 1

        if len(cs) == 0:
            if tr.arg is None:
                m(qs[reg][t])
            else:
                m(tr.arg, qs[reg][t])
        elif len(cs) == 1:
            if tr.arg:
                m(tr.arg, cs[0], qs[reg][t])
            else:
                m(cs[0], qs[reg][t])
        else:
            if tr.arg:
                m(tr.arg, cs, qs[reg][t])
            else:
                m(cs, qs[reg][t])

    return qc



def print_circuit(qc):
    qc_qiskit = hume_to_qiskit(qc.regs, qc.transformations)
    print(qc_qiskit)


def draw_circuit(qc, format='mpl'):
    qc_qiskit = hume_to_qiskit(qc.regs, qc.transformations)
    return qc_qiskit.draw(format)


def show_reports(qc):
    if not CONFIG.get_use_mpl():
        CONFIG.use_mpl()

    reports = []

    for (name, report) in qc.reports.items():
        reports.append((name, report))

    for idx, (name, report) in enumerate(reports[::-1]):
        print('\n\n' + 50*'-')
        print(f'{len(reports) - idx}. {name}')
        print(50*'-')

        qc_qiskit = hume_to_qiskit(qc.regs, report[1])
        print(qc_qiskit)
        print_state_table(report[2])
        print()


def same_as_qiskit(qc):
    qc_qiskit = hume_to_qiskit(qc.regs, qc.transformations)
    return all_close(qc.run(), qc_qiskit.run())


