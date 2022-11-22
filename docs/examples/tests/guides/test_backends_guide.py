import os

from orquestra.integrations.qiskit.backend import QiskitBackend
from orquestra.quantum.backends import SymbolicSimulator
from orquestra.quantum.circuits import Circuit, X

from ...guides.backends_guide import MyBackend

api_token = os.getenv("ZAPATA_IBMQ_API_TOKEN")


def test_my_simulator_produces_output():
    my_symbolic_sim = SymbolicSimulator()
    my_symbolic_sim.run = lambda x, y: {"0": 1, "1": 1}

    mybackend = MyBackend(my_symbolic_sim, None)
    mybackend.run_circuit_and_measure(Circuit([X(0)]), 1000)


def test_qiskit_backend_initialization():
    QiskitBackend("ibmq_lima", api_token=api_token)
