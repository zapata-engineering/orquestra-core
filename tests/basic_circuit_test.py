################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################

from orquestra.quantum.circuits import CNOT, H, Circuit
from orquestra.integrations.qiskit.simulator import QiskitSimulator


# just want to have example code for 'building basic circuit' tutorial
class TestQCBM:
    def test_build_basic_circuit(self):
        bell_circuit = Circuit()
        bell_circuit += H(0)
        bell_circuit += CNOT(0, 1)
        print(bell_circuit)
        bell_circuit2 = Circuit([H(0), CNOT(0, 1)])

        simulator = QiskitSimulator("aer_simulator")
        num_samples = 100
        measurements = simulator.run_circuit_and_measure(bell_circuit, num_samples)
        print(measurements.bitstrings)

        simulator2 = QiskitSimulator("aer_simulator_statevector")
        wavefunction = simulator2.get_wavefunction(bell_circuit)
        print(wavefunction.amplitudes)

        assert bell_circuit.operations == bell_circuit2.operations

# assert circuit.operations == [H(0), CNOT(0, 1)]
# assert circuit.n_qubits == 2

