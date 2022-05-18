################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################

from orquestra.quantum.circuits import CNOT, H, Circuit

from orquestra.quantum.symbolic_simulator import SymbolicSimulator
from orquestra.quantum.api.estimation import EstimationTask
from orquestra.integrations.qiskit.simulator import QiskitSimulator
from orquestra.quantum.openfermion import IsingOperator
from orquestra.quantum.estimation import calculate_exact_expectation_values

from orquestra.integrations.qiskit.conversions import (
    export_to_qiskit,
    import_from_qiskit,
)
from orquestra.integrations.cirq.conversions._circuit_conversions import export_to_cirq

from icecream import ic

# build the circuit
bell_circuit = Circuit()
bell_circuit += H(0)
bell_circuit += CNOT(0, 1)
ic(bell_circuit)

bell_circuit2 = Circuit([H(0), CNOT(0, 1)])
ic(bell_circuit2)

# run the circuit
simulator = QiskitSimulator("aer_simulator")
num_samples = 100
measurements = simulator.run_circuit_and_measure(bell_circuit, num_samples)
ic(measurements.get_counts())

sym_simulator = SymbolicSimulator()
measurements3 = sym_simulator.run_circuit_and_measure(bell_circuit, num_samples)
ic(measurements3.get_counts())

sv_simulator = QiskitSimulator("aer_simulator_statevector")
wavefunction = sv_simulator.get_wavefunction(bell_circuit)
ic(wavefunction.amplitudes)

ising = IsingOperator("[Z0] + [Z1]")
task = EstimationTask(ising, bell_circuit, None)
evals = calculate_exact_expectation_values(sym_simulator, [task])
ic(evals[0].values)

# translate the circuit
qiskit_circuit = export_to_qiskit(bell_circuit)
qiskit_circuit.x(1)

bell_circuit_X = import_from_qiskit(qiskit_circuit)
cirq_circuit = export_to_cirq(bell_circuit_X)
print(cirq_circuit)

wavefunction = sv_simulator.get_wavefunction(bell_circuit_X)
ic(wavefunction.amplitudes)
