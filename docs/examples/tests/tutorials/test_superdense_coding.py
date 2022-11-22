from orquestra.quantum.circuits import CNOT, Circuit, H, X

from ...tutorials.superdense_coding import measurements, teleport_circuit


def test_teleport_circuit_is_correct():
    assert teleport_circuit == Circuit([H(0), CNOT(0, 1), X(0), CNOT(0, 1), H(0)])


def test_measurements_is_correct():
    assert measurements.get_counts() == {"01": 1}
