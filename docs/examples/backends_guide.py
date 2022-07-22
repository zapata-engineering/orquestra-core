# QuantumBackend creation example
from orquestra.integrations.qiskit.backend import QiskitBackend

backend = QiskitBackend(
    "ibm_oslo", api_token="LOOKMORTYITURNEDMYSELFINTOANAPITOKEN!I'MAPIRICK"
)
# End QuantumBackend creation example


# QuantumSimulator creation example
# Example of simulator with no arguments
from orquestra.integrations.cirq.simulator import CirqSimulator

simulator = CirqSimulator()

# Example QiskitSimulator options
from orquestra.integrations.qiskit.simulator import QiskitSimulator

simulator = QiskitSimulator("aer_simulator")
simulator = QiskitSimulator("aer_simulator_statevector")
# End QuantumSimulator creation example


# TrackingBackend creation example
from orquestra.quantum.symbolic_simulator import SymbolicSimulator
from orquestra.quantum.trackers import MeasurementTrackingBackend

backend = MeasurementTrackingBackend(SymbolicSimulator(), "tracker_example")
# End TrackingBackend creation example


# Importng and Exporting with different frameworks
from orquestra.integrations.forest.conversions import (
    export_to_pyquil,
    import_from_pyquil,
)
from orquestra.integrations.cirq.conversions._circuit_conversions import (
    export_to_cirq,
    import_from_cirq,
)
from orquestra.integrations.qulacs.conversions import convert_to_qulacs
from orquestra.integrations.qiskit.conversions import (
    export_to_qiskit,
    import_from_qiskit,
)

# end importing/exporting examples
