from orquestra.quantum.circuits import CNOT, H, Circuit, X, Z

from orquestra.quantum.symbolic_simulator import SymbolicSimulator

from icecream import ic

teleport_circuit = Circuit()

# prepare entanglement
teleport_circuit += H(0)
teleport_circuit += CNOT(0, 1)

# alice encodes bits into her qubit
# comment and uncomment these lines to send 00, 01, 10, and 11
teleport_circuit += X(0)
# teleport_circuit += Z(0)

# bob decodes the qubits
teleport_circuit += CNOT(0, 1)
teleport_circuit += H(0)

# bob runs and measures the qubits
backend = SymbolicSimulator()
measurements = backend.run_circuit_and_measure(teleport_circuit, 1)
ic(measurements.get_counts())
