################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
from functools import partial

import numpy as np
from orquestra.integrations.qiskit.simulator import QiskitSimulator
from orquestra.opt.gradients import finite_differences_gradient
from orquestra.opt.optimizers import ScipyOptimizer
from orquestra.quantum.estimation import (
    calculate_exact_expectation_values,
    estimate_expectation_values_by_averaging,
)
from orquestra.quantum.openfermion import (
    count_qubits,
    get_ground_state,
    get_interaction_operator,
    get_sparse_operator,
    jordan_wigner,
)
from orquestra.quantum.openfermion.hamiltonians import fermi_hubbard
from orquestra.vqa.ansatz.quantum_compiling import HEAQuantumCompilingAnsatz
from orquestra.vqa.cost_function.cost_function import (
    create_cost_function,
    substitution_based_estimation_tasks_factory,
)
from orquestra.vqa.estimation.context_selection import perform_context_selection
from orquestra.vqa.grouping import group_greedily
from orquestra.vqa.shot_allocation import allocate_shots_proportionally


def get_fh_hamiltonian(x_dimension, y_dimension, U):
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
    return operator


class TestVQE:
    def test_solve_fh_with_vqe(self):
        hamiltonian = get_fh_hamiltonian(x_dimension=2, y_dimension=1, U=0.5)
        sparse_operator = get_sparse_operator(hamiltonian)
        exact_energy, _ = get_ground_state(sparse_operator)

        jw_hamiltonian = jordan_wigner(operator=hamiltonian)
        backend = QiskitSimulator("aer_simulator_statevector")

        ansatz = HEAQuantumCompilingAnsatz(1, count_qubits(jw_hamiltonian))
        estimation_method = estimate_expectation_values_by_averaging

        shot_allocation = partial(allocate_shots_proportionally, total_n_shots=10000)
        estimation_preprocessors = [
            group_greedily,
            perform_context_selection,
            shot_allocation,
        ]
        estimation_task_factory = substitution_based_estimation_tasks_factory(
            jw_hamiltonian, ansatz, estimation_preprocessors
        )

        optimizer = ScipyOptimizer(method="L-BFGS-B")

        cost_function = create_cost_function(
            backend,
            estimation_task_factory,
            estimation_method,
            gradient_function=partial(
                finite_differences_gradient, finite_diff_step_size=1e-3
            ),
        )

        # TODO: find good initial parameters for this test
        initial_params = np.random.random(ansatz.number_of_params)
        _ = optimizer.minimize(cost_function, initial_params)
        # assert opt_results.opt_value == pytest.approx(exact_energy)
