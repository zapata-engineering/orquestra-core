################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################

from icecream import ic

# build the circuit
from orquestra.quantum.circuits import CNOT, Circuit, H

bell_circuit = Circuit()
bell_circuit += H(0)
bell_circuit += CNOT(0, 1)
ic(bell_circuit)

bell_circuit2 = Circuit([H(0), CNOT(0, 1)])
ic(bell_circuit2)


from orquestra.integrations.qiskit.runner import QiskitRunner

# run the circuit
from qiskit import Aer

simulator = QiskitRunner(Aer.get_backend("aer_simulator"))
num_samples = 100
measurements = simulator.run_and_measure(bell_circuit, num_samples)
ic(measurements.get_counts())

from orquestra.quantum.runners.symbolic_simulator import SymbolicSimulator

sym_simulator = SymbolicSimulator()
measurements2 = sym_simulator.run_and_measure(bell_circuit, num_samples)
ic(measurements2.get_counts())

from orquestra.integrations.qiskit.simulator import QiskitWavefunctionSimulator

sv_simulator = QiskitWavefunctionSimulator(Aer.get_backend("statevector_simulator"))
wavefunction = sv_simulator.get_wavefunction(bell_circuit)
ic(wavefunction.amplitudes)

from orquestra.quantum.api.estimation import EstimationTask
from orquestra.quantum.estimation import calculate_exact_expectation_values
from orquestra.quantum.operators import PauliTerm

operator = PauliTerm("Z0") + PauliTerm("Z1")
task = EstimationTask(operator, bell_circuit, None)
evals = calculate_exact_expectation_values(sym_simulator, [task])
ic(evals[0].values)


# translate the circuit
from orquestra.integrations.qiskit.conversions import (
    export_to_qiskit,
    import_from_qiskit,
)

qiskit_circuit = export_to_qiskit(bell_circuit)
qiskit_circuit.x(1)

from orquestra.integrations.cirq.conversions._circuit_conversions import export_to_cirq

bell_circuit_X = import_from_qiskit(qiskit_circuit)
cirq_circuit = export_to_cirq(bell_circuit_X)
print(cirq_circuit)

wavefunction = sv_simulator.get_wavefunction(bell_circuit_X)
ic(wavefunction.amplitudes)

from orquestra.integrations.qulacs.conversions import convert_to_qulacs

qulacs_circuit = convert_to_qulacs(bell_circuit_X)
