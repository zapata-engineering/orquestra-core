################################################################################
# © Copyright 2022 Zapata Computing Inc.
# modified from tests/qaoa_maxcut_test.py
################################################################################
from collections import Counter

import networkx as nx
import numpy as np
from icecream import ic
from orquestra.integrations.cirq.simulator import CirqSimulator
from orquestra.opt.problems.maxcut import MaxCut
from orquestra.vqa.algorithms import QAOA


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
    qaoa = QAOA.default(cost_hamiltonian=hamiltonian, n_layers=2)

    runner = CirqSimulator()
    opt_results = qaoa.find_optimal_params(runner=runner)
    ic(opt_results)

    circuit = qaoa.get_circuit(opt_results.opt_params)
    measurements = runner.run_and_measure(circuit, n_samples=10000)
    counter = Counter(measurements.bitstrings)
    most_common_string = counter.most_common()[0][0]
    return most_common_string


test_graph = create_harder_graph()
most_common_string = solve_maxcut_qaoa(test_graph)
ic(most_common_string)
