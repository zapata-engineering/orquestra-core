################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################

from heapq import nlargest
from numbers import Number
from typing import Callable, cast

import numpy as np
import pytest
from orquestra.integrations.qulacs.simulator import QulacsSimulator
from orquestra.opt.api import Optimizer
from orquestra.opt.optimizers import CMAESOptimizer
from orquestra.quantum.api.wavefunction_simulator import WavefunctionSimulator
from orquestra.quantum.distributions import (
    MeasurementOutcomeDistribution,
    compute_clipped_negative_log_likelihood,
)
from orquestra.quantum.distributions.BAS_dataset import (
    get_bars_and_stripes_target_distribution,
)
from orquestra.vqa.ansatz import QCBMAnsatz
from orquestra.vqa.cost_function.qcbm_cost_function import create_QCBM_cost_function


class TestQCBM:
    @pytest.fixture
    def simulator(self):
        return QulacsSimulator()

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
        simulator: WavefunctionSimulator,
        target_distribution: MeasurementOutcomeDistribution,
        optimizer: Optimizer,
    ):

        cost_function = create_QCBM_cost_function(
            ansatz=qcbm_ansatz,
            runner=simulator,
            n_samples=1000,
            distance_measure=cast(
                Callable[..., Number], compute_clipped_negative_log_likelihood
            ),
            distance_measure_parameters={"epsilon": 1e-6},
            target_distribution=target_distribution,
        )

        np.random.seed(9)
        initial_params = np.random.uniform(-1.57, 1.57, qcbm_ansatz.number_of_params)

        opt_results = optimizer.minimize(cost_function, initial_params, True)

        actual_distribution = simulator.get_measurement_outcome_distribution(
            qcbm_ansatz.get_executable_circuit(opt_results.opt_params), n_samples=None
        )

        size_of_bar_and_stripes = len(target_distribution.distribution_dict)
        assert set(
            nlargest(
                size_of_bar_and_stripes,
                actual_distribution.distribution_dict,
                key=actual_distribution.distribution_dict.get,  # type: ignore
            )
        ) == set(target_distribution.distribution_dict.keys())
        assert opt_results.opt_value < 1.8
