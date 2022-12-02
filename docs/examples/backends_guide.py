# QuantumSimulator creation example
# Example of simulator with no arguments
from orquestra.integrations.cirq.simulator import CirqSimulator

simulator = CirqSimulator()

# Example Qiskit options
from orquestra.integrations.qiskit.runner import QiskitRunner
from orquestra.integrations.qiskit.simulator import QiskitWavefunctionSimulator
from qiskit import Aer

runner = QiskitRunner(Aer.get_backend("aer_simulator"))
simulator = QiskitWavefunctionSimulator(Aer.get_backend("aer_simulator_statevector"))
# End QuantumSimulator creation example


import numpy as np

# Quantumsimulator examples
from orquestra.integrations.cirq.simulator import CirqSimulator
from orquestra.quantum.circuits import CNOT, Circuit, H, X
from orquestra.quantum.operators import PauliTerm

initial_state = np.array([0, 1, 0, 0])
circuit = Circuit([H(0), X(1)])

simulator = CirqSimulator()

# wave function
wave_function = simulator.get_wavefunction(circuit, initial_state)

# expectation values

operator = PauliTerm("Z0") + PauliTerm("Z1")

expectation_values = simulator.get_exact_expectation_values(circuit, operator)
# End Quantumsimulator examples


# QuantumBackend creation example
from orquestra.integrations.qiskit.runner import create_ibmq_runner

runner = create_ibmq_runner(
    #api_token="LOOKMORTYITURNEDMYSELFINTOANAPITOKEN!I'MAPIRICK",
    api_token="7e82270032e2a395fb069c793113ac7156c7f0b546f27869e5407e57f4b57435fdc3f3b76df178bb3e89464cf1a76642d6e9ff0887a3d203b7ea6951ed707855",
    backend_name="ibm_oslo",
    retry_delay_seconds=1,
)

# End QuantumBackend creation example


# QuantumBackend run and measure circuit
circuit = Circuit() + X(0) + X(1)
number_of_samples = 1024

measurements = simulator.run_and_measure(circuit, number_of_samples)
# End QuantumBackend run and measure circuit

# QuantumBackend run and measure circuitset
circuit1 = Circuit() + X(0) + X(1)
circuit2 = Circuit() + H(0) + CNOT(0, 1)
circuit3 = Circuit() + X(0) + H(0) + CNOT(0, 1)

circuit_set = [circuit1, circuit2, circuit3]
number_of_samples_set = [10, 90, 100]

measurements_set = simulator.run_batch_and_measure(circuit_set, number_of_samples_set)
# End QuantumBackend run and measure circuitset


# Quantumbackend measurement distribution
measurement_distribution = simulator.get_measurement_outcome_distribution(
    circuit, n_samples=1000
)
# End Quantumbackend measurement distribution


# TrackingBackend creation example
from orquestra.quantum.runners.symbolic_simulator import SymbolicSimulator
from orquestra.quantum.runners.trackers import MeasurementTrackingBackend

backend = MeasurementTrackingBackend(SymbolicSimulator(), "tracker_example")
# End TrackingBackend creation example


from orquestra.integrations.cirq.conversions._circuit_conversions import (
    export_to_cirq,
    import_from_cirq,
)

# Importng and Exporting with different frameworks
from orquestra.integrations.forest.conversions import (
    export_to_pyquil,
    import_from_pyquil,
)
from orquestra.integrations.qiskit.conversions import (
    export_to_qiskit,
    import_from_qiskit,
)
from orquestra.integrations.qulacs.conversions import convert_to_qulacs

# Inherit QuantumSimulator
from orquestra.quantum.api.circuit_runner import BaseCircuitRunner
from orquestra.quantum.measurements import Measurements
# end importing/exporting examples


class MyRunner(BaseCircuitRunner):
    def __init__(self, simulator_name, noise_model):
        super().__init__()
        self.noise_model = noise_model
        self.simulator = create_simulator(simulator_name) # function to c

    def run_and_measure(self, circuit, n_samples):
        my_circ = export_to_my_circ(circuit)  # function to translate circuits
        result = self.simulator.run(
            circuit, n_samples
        )  # assumption that your simulator uses the method .run to execute and measure. Also it takes circuit and shots as the only params
        samples = convert_the_results_to_samples(result)

        return Measurements(samples)

# End Inherit QuantumSimulator
