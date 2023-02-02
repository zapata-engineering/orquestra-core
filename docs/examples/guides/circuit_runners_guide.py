# WavefunctionSimulator creation example
# Example of simulator with no arguments
from orquestra.integrations.cirq.simulator import CirqSimulator

simulator = CirqSimulator()

# Example Qiskit options
from orquestra.integrations.qiskit.runner import QiskitRunner
from orquestra.integrations.qiskit.simulator import QiskitWavefunctionSimulator
from qiskit import Aer

runner = QiskitRunner(Aer.get_backend("aer_simulator"))
simulator = QiskitWavefunctionSimulator(Aer.get_backend("aer_simulator_statevector"))
# End WavefunctionSimulator creation example


import numpy as np

# WavefunctionSimulator examples
from orquestra.integrations.cirq.simulator import CirqSimulator
from orquestra.quantum.circuits import CNOT, Circuit, H, X
from orquestra.quantum.operators import PauliSum

initial_state = np.array([0, 1, 0, 0])
circuit = Circuit([H(0), X(1)])

simulator = CirqSimulator()

# wave function
wave_function = simulator.get_wavefunction(circuit, initial_state)

# expectation values

operator = PauliSum("Z0 + 2*Z1")

expectation_values = simulator.get_exact_expectation_values(circuit, operator)

# End QuantumSimulator examples

import os

LOOKMORTYITURNEDMYSELFINTOANAPITOKENIMAPIRICK = os.getenv("ZAPATA_IBMQ_API_TOKEN")

# Inherit BaseCircuitRunner
from orquestra.integrations.qiskit.runner import create_ibmq_runner

backend = create_ibmq_runner(LOOKMORTYITURNEDMYSELFINTOANAPITOKENIMAPIRICK, "ibmq_lima")
# End Inherit BaseCircuitRunner

# CircuitRunner run and measure circuit
circuit = Circuit() + X(0) + X(1)
number_of_samples = 1024

measurements = simulator.run_and_measure(circuit, number_of_samples)
# End CircuitRunner run and measure circuit

# CircuitRunner run batch and measure
circuit1 = Circuit() + X(0) + X(1)
circuit2 = Circuit() + H(0) + CNOT(0, 1)
circuit3 = Circuit() + X(0) + H(0) + CNOT(0, 1)

circuit_set = [circuit1, circuit2, circuit3]
number_of_samples_set = [10, 90, 100]

measurements_set = simulator.run_batch_and_measure(circuit_set, number_of_samples_set)
# End CircuitRunner run batch and measure


# CircuitRunner measurement distribution
measurement_distribution = simulator.get_measurement_outcome_distribution(
    circuit, n_samples=1000
)
# End CircuitRunner measurement distribution


# TrackingBackend creation example
from orquestra.quantum.runners.symbolic_simulator import SymbolicSimulator
from orquestra.quantum.runners.trackers import MeasurementTrackingBackend

backend = MeasurementTrackingBackend(SymbolicSimulator(), "tracker_example")
# End TrackingBackend creation example


from orquestra.integrations.cirq.conversions._circuit_conversions import (
    export_to_cirq,
    import_from_cirq,
)

# Importing and Exporting with different frameworks
from orquestra.integrations.cirq.conversions import (
    export_to_cirq,
    import_from_cirq,
)
from orquestra.integrations.qiskit.conversions import (
    export_to_qiskit,
    import_from_qiskit,
)
from orquestra.integrations.qulacs.conversions import convert_to_qulacs

# Inherit BaseCircuitRunner
from orquestra.quantum.api.circuit_runner import BaseCircuitRunner
from orquestra.quantum.measurements import Measurements

# end importing/exporting examples


class MyRunner(BaseCircuitRunner):
    def __init__(self, simulator_name, noise_model):
        super().__init__()
        self.noise_model = noise_model
        self.simulator = create_simulator(simulator_name)  # function to c

    def _run_and_measure(self, circuit, n_samples):
        my_circ = export_to_my_circ(circuit)  # function to translate circuits
        # Here we assume your simulator uses the method run() to execute and measure.
        result = self.simulator.run(my_circ, n_samples, self.noise_model)
        samples = convert_the_results_to_samples(result)

        return Measurements(samples)


# End Inherit QuantumSimulator


def export_to_my_circ(circuit):
    # mock function to translate circuits
    return circuit


def convert_the_results_to_samples(result):
    # mock function to convert the results of your simulator to samples
    return result


def create_simulator(simulator_name):
    # mock function to create your simulator
    class Simulator:
        def run(self, circuit, n_samples, noise_model):
            return circuit

    return Simulator()
