from typing import Optional

import numpy as np
from orquestra.quantum.circuits import RZ, Circuit
from orquestra.vqa.api.ansatz import Ansatz, ansatz_property
from overrides import overrides
from sympy import symbols


class MockAnsatz(Ansatz):

    supports_parametrized_circuits = True
    number_of_qubits = ansatz_property("number_of_qubits")

    def __init__(
        self,
        number_of_layers: int,
        number_of_qubits: int,
    ):
        super().__init__(number_of_layers)
        self.number_of_qubits = number_of_qubits
        self._symbols = ()
        self._circuit = Circuit()
        for i in range(number_of_qubits):
            new_symbol = symbols(f"x{i}")
            self._symbols += (new_symbol,)
            self._circuit += RZ(new_symbol)(i)

    @overrides
    def _generate_circuit(self, params: Optional[np.ndarray] = None) -> Circuit:
        symbols_map = {}
        if params is not None:
            for symbol, param in zip(self._symbols, params):
                symbols_map[symbol] = param
            return self._circuit.bind(symbols_map)
        return self._circuit
