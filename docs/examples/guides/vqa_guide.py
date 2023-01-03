# Default VQE
from orquestra.quantum.operators import PauliTerm
from orquestra.vqa.algorithms import VQE
from orquestra.vqa.ansatz import HEAQuantumCompilingAnsatz

hamiltonian = (
    PauliTerm("X0") +
    PauliTerm("X1") +
    PauliTerm("Z0") * PauliTerm("Z1")
)

ansatz = HEAQuantumCompilingAnsatz(number_of_layers=1, number_of_qubits=hamiltonian.n_qubits)

vqe = VQE.default(
    hamiltonian=hamiltonian,
    ansatz=ansatz,
    use_exact_expectation_values=True,
)
# --- End

# Optimizing default VQE
from orquestra.quantum.runners import SymbolicSimulator

runner = SymbolicSimulator()
result = vqe.find_optimal_params(runner=runner)

print(f"opt_value={result.opt_value}")
print(f"opt_params={result.opt_params}")
# --- End

# Cost function
cost_function = vqe.get_cost_function(runner)
print(cost_function(result.opt_params) == result.opt_value)
# --- End

# VQE initializer
from orquestra.opt.optimizers import ScipyOptimizer
from orquestra.quantum.estimation import estimate_expectation_values_by_averaging
from orquestra.vqa.grouping import group_greedily
from orquestra.vqa.shot_allocation import allocate_shots_uniformly

vqe_2 = VQE(
    hamiltonian=hamiltonian,
    ansatz=ansatz,
    optimizer=ScipyOptimizer(method="L-BFGS-B"),
    estimation_method=estimate_expectation_values_by_averaging,
    grouping=group_greedily,
    shots_allocation=allocate_shots_uniformly,
    n_shots=1000
)

result = vqe_2.find_optimal_params(runner)

print(f"opt_value={result.opt_value}")
print(f"opt_params={result.opt_params}")
# --- End

# replace optimizer
vqe_3 = vqe_2.replace_optimizer(ScipyOptimizer(method="COBYLA"))

print(f"Ansatzes equal? {vqe_3.ansatz == vqe_2.ansatz}")
print(f"Grouping equal? {vqe_3.grouping == vqe_2.grouping}")
print(f"Estimation method equal? {vqe_3.estimation_method == vqe_2.estimation_method}")
print(f"Hamiltonians equal? {vqe_3.hamiltonian == vqe_2.hamiltonian}")
print(f"Optimizers equal? {vqe_3.optimizer == vqe_2.optimizer}")
print(f"First optimization method: {vqe_2.optimizer.method}")
print(f"Second optimization method: {vqe_3.optimizer.method}")
# --- End

# Detailed VQA
# Step 1: initial ingredients
from orquestra.vqa.ansatz import QAOAFarhiAnsatz
# We reuse the the hamiltonian we used in previous examples
cost_hamiltonian = hamiltonian
ansatz = QAOAFarhiAnsatz(
    number_of_layers=3,
    cost_hamiltonian=cost_hamiltonian
)
runner = SymbolicSimulator()
optimizer = ScipyOptimizer(method="L-BFGS-B")

# Step 2: creating estimation_task_factory
from orquestra.vqa.cost_function import substitution_based_estimation_tasks_factory
estimation_task_factory = substitution_based_estimation_tasks_factory(
    target_operator=hamiltonian,
    ansatz=ansatz,
    estimation_preprocessors=[]
)

# Step 3: creating cost function
from orquestra.vqa.cost_function import create_cost_function
from orquestra.quantum.estimation import calculate_exact_expectation_values
cost_function = create_cost_function(
    runner,
    estimation_task_factory,
    calculate_exact_expectation_values
)

# Step 4: optimizing cost function
import numpy as np
optimal_params = optimizer.minimize(
    cost_function, initial_params=0.1 * np.ones(6)
).opt_params

# Step 5: getting executable circuit with optimal parameters
circuit = ansatz.get_executable_circuit(optimal_params)
# --- End
