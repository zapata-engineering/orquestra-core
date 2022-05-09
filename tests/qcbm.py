# need orquestra-quantum, orquestra-opt, orquestra-vqe, orquesta-qulacs
# Generate random parameters for an ansatz
import itertools
import random
from heapq import nlargest
from typing import Optional

import numpy as np
import pytest
from orquestra.integrations.cirq.simulator import CirqSimulator
from orquestra.integrations.qiskit.simulator import QiskitSimulator
from orquestra.opt.api import Optimizer
from orquestra.opt.optimizers import CMAESOptimizer
from orquestra.quantum.api.backend import QuantumSimulator
from orquestra.quantum.distributions import (
    MeasurementOutcomeDistribution,
    compute_clipped_negative_log_likelihood,
)
from orquestra.vqa.ansatz.qcbm import QCBMAnsatz
from orquestra.vqa.cost_function.qcbm_cost_function import create_QCBM_cost_function


def generate_random_ansatz_params(
    number_of_parameters: Optional[int] = None,
    min_value: float = -np.pi * 0.5,
    max_value: float = np.pi * 0.5,
    seed: Optional[int] = None,
):
    if seed is not None:
        np.random.seed(seed)

    return np.random.uniform(min_value, max_value, number_of_parameters)


def get_bars_and_stripes_target_distribution(
    nrows, ncols, fraction=1.0, method="zigzag"
):
    """Generates bars and stripes (BAS) data in zigzag pattern
    Args:
        nrows: number of rows in BAS dataset
        ncols: number of columns in BAS dataset
        fraction: maximum fraction of patterns to include
            (at least one pattern will always be included)
        method: the method to use to label the qubits
    Returns:
        Array of list of BAS pattern.
    """
    if method == "zigzag":
        data = bars_and_stripes_zigzag(nrows, ncols)
    else:
        raise RuntimeError(
            "Method: {} is not supported for generated a target distribution "
            "for bars and stripes".format(method)
        )

    # Remove patterns until left with a subset that has cardinality less than or equal
    # to the percentage * total number of patterns
    num_desired_patterns = int(len(data) * fraction)
    num_desired_patterns = max(num_desired_patterns, 1)
    data = random.sample(list(data), num_desired_patterns)

    distribution_dict = {}
    for pattern in data:
        bitstring = ""
        for qubit in pattern:
            bitstring += str(qubit)

        distribution_dict[bitstring] = 1.0

    return MeasurementOutcomeDistribution(distribution_dict)


# Generate BAS with specified rows and columns in zigzag pattern
def bars_and_stripes_zigzag(nrows, ncols):
    """Generates bars and stripes data in zigzag pattern
    Args:
        nrows: number of rows in BAS dataset
        ncols: number of columns in BAS dataset
    Returns:
        Array of list of BAS pattern.
    """

    data = []

    for h in itertools.product([0, 1], repeat=ncols):
        pic = np.repeat([h], nrows, 0)
        data.append(pic.ravel().tolist())

    for h in itertools.product([0, 1], repeat=nrows):
        pic = np.repeat([h], ncols, 1)
        data.append(pic.ravel().tolist())

    data = np.unique(np.asarray(data), axis=0)

    return data


class TestQCBM:
    @pytest.fixture
    def backend(self):
        return CirqSimulator()

    @pytest.fixture
    def qcbm_ansatz(self):
        return QCBMAnsatz(number_of_layers=4, number_of_qubits=4, topology="all")

    @pytest.fixture
    def target_distribution(self):
        return get_bars_and_stripes_target_distribution(2, 2, 1.0, "zigzag")

    @pytest.fixture
    def optimizer(self):
        return CMAESOptimizer(
            sigma_0=0.1, options={"popsize": 5, "tolx": 1e-6, "seed": 9}
        )

    def test_qcbm_ansatz_optimizes_properly(
        self,
        qcbm_ansatz: QCBMAnsatz,
        backend: QuantumSimulator,
        target_distribution: MeasurementOutcomeDistribution,
        optimizer: Optimizer,
    ):

        cost_function = create_QCBM_cost_function(
            ansatz=qcbm_ansatz,
            backend=backend,
            n_samples=1000,
            distance_measure=compute_clipped_negative_log_likelihood,
            distance_measure_parameters={"epsilon": 1e-6},
            target_distribution=target_distribution,
        )

        initial_params = generate_random_ansatz_params(
            qcbm_ansatz.number_of_params, -1.57, 1.57, 9
        )
        opt_results = optimizer.minimize(cost_function, initial_params, True)

        actual_distribution = backend.get_measurement_outcome_distribution(
            qcbm_ansatz.get_executable_circuit(opt_results.opt_params)
        )

        size_of_bar_and_stripes = len(target_distribution.distribution_dict)
        assert set(
            nlargest(
                size_of_bar_and_stripes,
                actual_distribution.distribution_dict,
                key=actual_distribution.distribution_dict.get,
            )
        ) == set(target_distribution.distribution_dict.keys())
        assert opt_results.opt_value < 1.8
