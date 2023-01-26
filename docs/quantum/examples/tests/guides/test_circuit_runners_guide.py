import os

from orquestra.quantum.circuits import Circuit, X
from orquestra.quantum.runners import SymbolicSimulator

from ...guides.circuit_runners_guide import MyRunner

api_token = os.getenv("ZAPATA_IBMQ_API_TOKEN")


def test_my_simulator_produces_output():
    my_symbolic_sim = SymbolicSimulator()
    my_symbolic_sim.run = lambda x, y: {"0": 1, "1": 1}

    mybackend = MyRunner(my_symbolic_sim, None)
    mybackend.run_and_measure(Circuit([X(0)]), 1000)
