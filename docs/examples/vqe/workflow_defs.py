################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
# use for literalinclude start-after >> Start
from orquestra.integrations.qiskit.runner import QiskitRunner
from orquestra.quantum.operators import PauliTerm
from orquestra.quantum.runners import SymbolicSimulator
from orquestra.vqa.algorithms import VQE
from orquestra.vqa.ansatz import HEAQuantumCompilingAnsatz

import orquestra.sdk as sdk

# Create a two-qubit transverse field Ising Hamiltonian
g = 0.1
hamiltonian = PauliTerm("Z0") * PauliTerm("Z1") + g * (
    PauliTerm("X0") + PauliTerm("X1")
)

# Define the VQE ansatz and algorithm
ansatz = HEAQuantumCompilingAnsatz(
    number_of_layers=1, number_of_qubits=hamiltonian.n_qubits
)

vqe = VQE.default(
    hamiltonian=hamiltonian,
    ansatz=ansatz,
    use_exact_expectation_values=False,
    n_shots=8000,
    grouping="greedy",
)


@sdk.task
def find_optimal_params():
    optimization_result = vqe.find_optimal_params(runner=SymbolicSimulator())
    return optimization_result.opt_params, optimization_result.opt_value


@sdk.task
def evaluate_cost_function(params, backend_name):
    from qiskit import IBMQ

    IBMQ.load_account()
    runner = QiskitRunner(IBMQ.get_provider().get_backend(name=backend_name))
    return vqe.get_cost_function(runner)(params)


@sdk.workflow
def vqe_workflow(backend_names, n_repetitions):
    """Execute VQE n_repetitions times on each backend in backend_names."""
    params, value = find_optimal_params()
    return [
        evaluate_cost_function(params=params, backend_name=backend_name)
        for backend_name in backend_names
        for _ in range(n_repetitions)
    ]
