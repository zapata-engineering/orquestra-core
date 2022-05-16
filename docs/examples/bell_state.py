################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################

from orquestra.quantum.circuits import CNOT, H, Circuit
from orquestra.integrations.qiskit.simulator import QiskitSimulator
from orquestra.quantum.symbolic_simulator import SymbolicSimulator


bell_circuit = Circuit()
bell_circuit += H(0)
bell_circuit += CNOT(0, 1)
print(bell_circuit)

bell_circuit2 = Circuit([H(0), CNOT(0, 1)])
print(bell_circuit2)

simulator = QiskitSimulator("aer_simulator")
num_samples = 100
measurements = simulator.run_circuit_and_measure(bell_circuit, num_samples)
print(measurements.get_counts())

simulator3 = SymbolicSimulator()
measurements3 = simulator3.run_circuit_and_measure(bell_circuit, num_samples)
print(measurements3.get_counts())

simulator2 = QiskitSimulator("aer_simulator_statevector")
wavefunction = simulator2.get_wavefunction(bell_circuit)
print(wavefunction.amplitudes)
