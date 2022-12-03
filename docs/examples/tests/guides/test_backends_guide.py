import os

from orquestra.integrations.qiskit.runner import create_ibmq_runner
from orquestra.quantum.circuits import Circuit, X
from orquestra.quantum.runners import SymbolicSimulator

from ...guides.backends_guide import MyRunner

api_token = os.getenv("ZAPATA_IBMQ_API_TOKEN")


def test_my_simulator_produces_output():
    my_symbolic_sim = SymbolicSimulator()
    my_symbolic_sim.run = lambda x, y: {"0": 1, "1": 1}

    mybackend = MyRunner(my_symbolic_sim, None)
    mybackend.run_and_measure(Circuit([X(0)]), 1000)


def test_qiskit_backend_initialization():
    create_ibmq_runner(api_token, "ibmq_lima")
