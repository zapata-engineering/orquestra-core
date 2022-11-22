################################################################################
# © Copyright 2022 Zapata Computing Inc.
# modified from tests/qaoa_maxcut_test.py
################################################################################
from collections import Counter

import networkx as nx
import numpy as np

from orquestra.integrations.cirq.simulator import CirqSimulator
from orquestra.opt.optimizers import ScipyOptimizer
from orquestra.opt.problems.maxcut import MaxCut
from orquestra.quantum.estimation import calculate_exact_expectation_values
from orquestra.vqa.ansatz.qaoa_farhi import QAOAFarhiAnsatz
from orquestra.vqa.cost_function.cost_function import (
    create_cost_function,
    substitution_based_estimation_tasks_factory,
)

from icecream import ic


def create_simple_graph():
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


def create_harder_graph():
    graph = nx.Graph()
    graph.add_nodes_from([0, 1, 2, 3, 4, 5])
    graph.add_edge(0, 1, weight=10)
    graph.add_edge(0, 3, weight=5)
    graph.add_edge(1, 2, weight=1)
    graph.add_edge(2, 3, weight=1)

    # YOUR CODE HERE

    graph.add_edge(0, 4, weight=10)
    graph.add_edge(0, 5, weight=5)
    graph.add_edge(1, 4, weight=1)
    graph.add_edge(2, 4, weight=5)
    graph.add_edge(1, 5, weight=5)
    return graph


def solve_maxcut_qaoa(test_graph):

    hamiltonian = MaxCut().get_hamiltonian(test_graph)
    ansatz = QAOAFarhiAnsatz(2, cost_hamiltonian=hamiltonian)

    estimation_method = calculate_exact_expectation_values
    estimation_task_factory = substitution_based_estimation_tasks_factory(
        hamiltonian, ansatz
    )

    backend = CirqSimulator()
    optimizer = ScipyOptimizer(method="L-BFGS-B")

    cost_function = create_cost_function(
        backend,
        estimation_task_factory,
        estimation_method,
    )
    initial_params = np.ones(ansatz.number_of_params) * np.pi / 5
    opt_results = optimizer.minimize(cost_function, initial_params)

    circuit = ansatz.get_executable_circuit(opt_results.opt_params)
    measurements = backend.run_circuit_and_measure(circuit, n_samples=10000)
    counter = Counter(measurements.bitstrings)
    most_common_string = counter.most_common()[0][0]
    return most_common_string


test_graph = create_harder_graph()
most_common_string = solve_maxcut_qaoa(test_graph)
ic(most_common_string)
