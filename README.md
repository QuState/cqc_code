## About the code in this repository

> [!NOTE]
> This repository is a work in progress--more comments and notes will be added

* The code uses minimal dependencies, in order to facilitate learning and ensure longevity
* The code behind notebooks is built incrementally in each chapter following sound dependency management principles
* The notebooks only use code dependencies in the chapter they belong to
* There will be a simulator, called Hume, that will put together all pieces, and will be usable as a standalone simulator


#### Overview of contents and structure 


<pre>
├── README.md
├── src                            # notebooks are designed to run from the src directory
│   ├── chXX
│   │   ├── chXX.ipynb             # notebook with chapter code that can be used for experimentation
│   │   ├── chXX_output.ipynb      # notebook that includes the output of chXX.ipynb after being run (can be used for comparison)
│   │   ├── chXX_exercises.ipynb   # notebook with chapter exercises and solutions
│   │   └── x.py                   # the source code introduced in each chapter
│   ├── ...
</pre>


#### Qiskit notebooks

The Python simulator implemented in the book uses identical syntax to Qiskit so that it can be used to run on Qiskit backends/real computers.
We include notebooks called `chXX_qiskit.ipynb` with examples from each chapter to demonstrate how to easily use the code from the book to experiment with Qiskit.

We use a small adapter to ensure that identical syntax can be used with Qiskit.
For example, the `run` method on a circuit works the same way.

Running an example circuit using our Python simulator:

```
from sim_circuit import QuantumRegister, QuantumCircuit

q = QuantumRegister(3)
qc = QuantumCircuit(q)

qc.h(q[0])
qc.h(q[1])
qc.mcx([q[0], q[1]], q[2])

state = qc.run()
```

Output:

![Example state table](images/ex_state_table.png)

Running an exampy circuit using Qiskit:

```
import qiskit
from qiskit import QuantumCircuit, QuantumRegister, transpile

def run(self):
    backend = qiskit.Aer.get_backend('statevector_simulator')
    circ = transpile(self, backend)
    job = backend.run(circ)
    state = job.result().get_statevector()
    return state

setattr(QuantumCircuit, 'run', run)

q = QuantumRegister(3)
qc = QuantumCircuit(q)

qc.h(q[0])
qc.h(q[1])
qc.mcx([q[0], q[1]], q[2])

state = qc.run()
```

Output:

![Example state table qiskit](images/ex_state_table_qiskit.png)