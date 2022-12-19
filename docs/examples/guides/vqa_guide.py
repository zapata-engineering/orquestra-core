# Default VQE
from orquestra.quantum.operators import PauliTerm
from orquestra.vqa.algorithms import VQE
from orquestra.vqa.ansatz import HEAQuantumCompilingAnsatz

hamiltonian = (
    PauliTerm("X0") * PauliTerm("Y0")
    + PauliTerm("X0") * PauliTerm("Z0")
    + PauliTerm("X1")
)

ansatz = HEAQuantumCompilingAnsatz(1, hamiltonian.n_qubits)

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
