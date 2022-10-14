from typing import List

from orquestra.quantum.api.backend import QuantumSimulator
from orquestra.quantum.api.estimation import EstimationTask
from orquestra.quantum.measurements import ExpectationValues


def calculate_exact_expectation_values(
    backend: QuantumSimulator,
    estimation_tasks: List[EstimationTask],
) -> List[ExpectationValues]:

    expectation_values_list = [
        backend.get_exact_expectation_values(
            estimation_task.circuit, estimation_task.operator
        )
        for estimation_task in estimation_tasks
    ]
    return expectation_values_list
