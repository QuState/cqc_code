from math import log2

from qiskit import QuantumRegister, QuantumCircuit

from ch05.sim_circuit import Swap
from ch07.util import print_state_table, all_close
from ch07.util import CONFIG

from ch04.sim_qiskit import *


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


def show_reports(qc):
    if not CONFIG.get_use_mpl_tables():
        CONFIG.set_use_mpl_tables(True)

    for idx, (name, report) in enumerate(qc.reports.items()):
        print('\n\n' + 50*'-')
        print(f'{idx + 1}. {name}')
        print(50*'-')

        # for tr in report[1]:
        #     print(tr)

        qc_qiskit = hume_to_qiskit(qc.regs, report[1])
        print(qc_qiskit)
        print_state_table(report[2])
        print()


def same_as_qiskit(qc):
    qc_qiskit = hume_to_qiskit(qc.regs, qc.transformations)
    return all_close(qc.run(), qc_qiskit.run())