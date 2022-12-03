################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from collections import Counter

import networkx as nx
import numpy as np
import pytest
from orquestra.integrations.cirq.simulator import CirqSimulator
from orquestra.integrations.qiskit.simulator import QiskitWavefunctionSimulator
from orquestra.integrations.qulacs.simulator import QulacsSimulator
from orquestra.opt.optimizers import ScipyOptimizer
from orquestra.opt.problems.maxcut import MaxCut
from orquestra.quantum.estimation import calculate_exact_expectation_values
from orquestra.vqa.ansatz.qaoa_farhi import QAOAFarhiAnsatz
from orquestra.vqa.cost_function.cost_function import (
    create_cost_function,
    substitution_based_estimation_tasks_factory,
)
from qiskit import Aer


@pytest.fixture
def test_graph():
    """
    [0] --10-- [1]
    |           |
    10          1
    |           |
    [3] --1 -- [2]
    """
    graph = nx.Graph()
    graph.add_nodes_from([0, 1, 2, 3])
    graph.add_edge(0, 1, weight=10)
    graph.add_edge(0, 3, weight=10)
    graph.add_edge(1, 2, weight=1)
    graph.add_edge(2, 3, weight=1)
    return graph


@pytest.fixture(
    params=[
        CirqSimulator(),
        QulacsSimulator(),
        QiskitWavefunctionSimulator(Aer.get_backend("aer_simulator_statevector")),
    ]
)
def backend(request):
    return request.param


class TestMaxcut:
    def test_solve_maxcut_qaoa(self, test_graph, backend):

        hamiltonian = MaxCut().get_hamiltonian(test_graph)

        ansatz = QAOAFarhiAnsatz(2, cost_hamiltonian=hamiltonian)
        # 1000 and 0111 are not really optimal solutions, but they're close enough,
        # so that optimization might also end up in this local minimum,
        # and hence it's ok for us to accept it.
        correct_solutions = [
            (1, 0, 1, 0),  # Cost: 22
            (0, 1, 0, 1),  # Cost: 22
            (1, 0, 0, 0),  # Cost: 20
            (0, 1, 1, 1),  # Cost: 20
        ]

        estimation_method = calculate_exact_expectation_values
        estimation_task_factory = substitution_based_estimation_tasks_factory(
            hamiltonian, ansatz
        )

        optimizer = ScipyOptimizer(method="L-BFGS-B")

        cost_function = create_cost_function(
            backend,
            estimation_task_factory,
            estimation_method,
        )
        initial_params = np.ones(ansatz.number_of_params) * np.pi / 5

        opt_results = optimizer.minimize(cost_function, initial_params)
        circuit = ansatz.get_executable_circuit(opt_results.opt_params)
        measurements = backend.run_and_measure(circuit, n_samples=10000)

        counter = Counter(measurements.bitstrings)
        most_common_string = counter.most_common()[0][0]
        assert most_common_string in correct_solutions
