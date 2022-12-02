################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from functools import partial
from typing import Any, Tuple

import numpy as np
import pytest
from openfermion import (
    get_ground_state,
    get_interaction_operator,
    get_sparse_operator,
    jordan_wigner,
)
from openfermion.hamiltonians import fermi_hubbard
from orquestra.integrations.cirq.conversions import from_openfermion
from orquestra.integrations.qulacs.simulator import QulacsSimulator
from orquestra.opt.optimizers import ScipyOptimizer
from orquestra.quantum.estimation import estimate_expectation_values_by_averaging
from orquestra.quantum.operators import PauliSum
from orquestra.vqa.ansatz.quantum_compiling import HEAQuantumCompilingAnsatz
from orquestra.vqa.cost_function.cost_function import (
    create_cost_function,
    substitution_based_estimation_tasks_factory,
)
from orquestra.vqa.estimation.context_selection import perform_context_selection
from orquestra.vqa.grouping import group_greedily
from orquestra.vqa.shot_allocation import allocate_shots_proportionally


def get_fh_hamiltonian(
    x_dimension: int, y_dimension: int, U: float
) -> Tuple[PauliSum, Any]:
    hamiltonian = fermi_hubbard(
        x_dimension=x_dimension,
        y_dimension=y_dimension,
        tunneling=1,
        coulomb=U,
        chemical_potential=U / 2,
        magnetic_field=0,
        periodic=False,
        spinless=False,
        particle_hole_symmetry=False,
    )
    operator = get_interaction_operator(hamiltonian)
    operator.one_body_tensor = np.real(operator.one_body_tensor)
    operator.two_body_tensor = np.real(operator.two_body_tensor)
    sparse_operator = get_sparse_operator(hamiltonian)
    exact_energy, _ = get_ground_state(sparse_operator)

    jw_hamiltonian = jordan_wigner(operator=hamiltonian)

    return from_openfermion(jw_hamiltonian), exact_energy


class TestVQE:
    def test_solve_fh_with_vqe(self):
        hamiltonian, exact_energy = get_fh_hamiltonian(
            x_dimension=2, y_dimension=1, U=0.5
        )
        backend = QulacsSimulator()

        ansatz = HEAQuantumCompilingAnsatz(2, hamiltonian.n_qubits)
        estimation_method = estimate_expectation_values_by_averaging

        shot_allocation = partial(allocate_shots_proportionally, total_n_shots=50000)
        estimation_preprocessors = [
            group_greedily,
            perform_context_selection,
            shot_allocation,
        ]
        estimation_task_factory = substitution_based_estimation_tasks_factory(
            hamiltonian, ansatz, estimation_preprocessors
        )

        optimizer = ScipyOptimizer(method="COBYLA", options={"maxiter": 250})

        cost_function = create_cost_function(
            backend, estimation_task_factory, estimation_method
        )

        initial_params = np.array(
            [
                0.94557831,
                -1.06991166,
                0.28233565,
                0.47443967,
                0.468148,
                0.5421605,
                0.29240645,
                1.48504768,
                0.48147571,
                0.36578263,
                0.45862184,
                -1.32968834,
                -0.307463,
                0.37939154,
                1.45632776,
                0.09292365,
                0.80710492,
                1.14496005,
                0.65499076,
                -0.06335737,
                0.10678299,
                0.28446654,
                0.5538357,
                0.44774159,
                0.84030601,
                1.77205874,
                0.17598451,
                0.88785342,
                -0.5026344,
                0.72818643,
                -0.00207843,
                0.69474356,
                0.81166782,
                -0.11638733,
                -0.24970387,
                1.02757601,
                0.24950334,
                0.95664434,
                -0.35552715,
                -0.42096424,
                1.30391856,
                0.94936243,
                0.21281127,
                -1.36481705,
                0.37734196,
                0.0475623,
                1.1587143,
                0.9340059,
            ]
        )
        opt_results = optimizer.minimize(cost_function.function, initial_params)
        assert opt_results.opt_value == pytest.approx(exact_energy, rel=2e-2, abs=2e-2)
