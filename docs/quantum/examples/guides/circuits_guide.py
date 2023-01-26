################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
import numpy as np
import sympy
from icecream import ic
from orquestra.quantum.circuits import (
    CNOT,
    CZ,
    RX,
    RZ,
    Circuit,
    CustomGateDefinition,
    H,
)
from orquestra.quantum.decompositions import decompose_operations

N_QUBITS = 3

beta = sympy.symbols("beta_0:3", real=True)
gamma = sympy.symbols("gamma_0:3", real=True)
theta = sympy.Symbol("theta", real=True)

# State Preparation Circuit
state_prep_circ = Circuit([H(i) for i in range(N_QUBITS)])
unitary = state_prep_circ.to_unitary()
ic(unitary.shape)  # should be 8x8 matrix
ic(type(unitary))  # will be numpy ndarray, later see sympy matrix

# Inverting the circuit
inverse_state_prep_circ = state_prep_circ.inverse()
ic(inverse_state_prep_circ)
combined_circ = state_prep_circ + inverse_state_prep_circ
combined_unitary = combined_circ.to_unitary()
ic(np.allclose(combined_unitary, np.eye(8)))

# Problem Hamiltonian Circuit
problem_hamiltonian_circ = Circuit([CNOT(0, 1), RZ(beta[0])(1), CNOT(0, 1)])
problem_hamiltonian_circ += Circuit([CNOT(0, 2), RZ(beta[1])(2), CNOT(0, 2)])
problem_hamiltonian_circ += Circuit([CNOT(1, 2), RZ(beta[2])(2), CNOT(1, 2)])
unitary = problem_hamiltonian_circ.to_unitary()
ic(unitary.shape)  # should be 8x8 matrix
ic(type(unitary))  # sympy matrix

# Mixing Hamiltonian Circuit
mixing_circ = Circuit()
for i in range(N_QUBITS):
    mixing_circ += RX(gamma[i])(i)
ic(mixing_circ)

# Combine the circuit
qaoa_circ = state_prep_circ + problem_hamiltonian_circ + mixing_circ
ic(qaoa_circ)
ic(qaoa_circ.n_qubits)
ic(len(qaoa_circ.operations))
for op in qaoa_circ.operations:
    ic(op.gate.name, op.qubit_indices, op.params)
ic(qaoa_circ.free_symbols)

# Binding Beta Circuit
bound_beta_circ = qaoa_circ.bind({beta[0]: 0.1, beta[1]: 0.1, beta[2]: 0.1})
ic(bound_beta_circ.free_symbols)

# Binding Gammas in Circuit
bound_all_circ = bound_beta_circ.bind({gamma[0]: 0.2, gamma[1]: 0.2, gamma[2]: 0.2})
ic(bound_all_circ.free_symbols)
unitary = bound_all_circ.to_unitary()
ic(type(unitary))

# Non-parametrized mixing circuit for comparison
new_mixing_circ = Circuit([RX(0.2)(0), RX(0.2)(1), RX(0.2)(2)])
ic(new_mixing_circ == mixing_circ.bind({gamma[0]: 0.2, gamma[1]: 0.2, gamma[2]: 0.2}))

# Custom Gates
custom_matrix = sympy.Matrix(
    [
        [1.0 * sympy.exp(-sympy.I * theta / 2), 0, 0, 0],
        [0, 1.0 * sympy.exp(sympy.I * theta / 2), 0, 0],
        [0, 0, 1.0 * sympy.exp(sympy.I * theta / 2), 0],
        [0, 0, 0, 1.0 * sympy.exp(-sympy.I * theta / 2)],
    ]
)
ZZ = CustomGateDefinition(
    gate_name="ZZ", matrix=custom_matrix, params_ordering=(theta,)
)
new_problem_ham_circ = Circuit(
    [ZZ(beta[0])(0, 1), ZZ(beta[1])(0, 2), ZZ(beta[2])(1, 2)]
)
ic(new_problem_ham_circ.to_unitary() == problem_hamiltonian_circ.to_unitary())
ic(new_problem_ham_circ.collect_custom_gate_definitions())


# Decomposing Gates
class CNOTDecompositionRule:
    def production(self, operation):
        q0, q1 = operation.qubit_indices
        return [H(q1), CZ(q0, q1), H(q1)]

    def predicate(self, operation):
        return operation.gate.name == "CNOT"


decomposed_circ = Circuit(
    decompose_operations(bound_all_circ.operations, [CNOTDecompositionRule()])
)
ic(np.allclose(decomposed_circ.to_unitary(), bound_all_circ.to_unitary()))


# Exponential and power gates
ic(H.power(2).matrix == sympy.eye(2))

# exponential example
ic(sympy.simplify(H.exp.matrix))
