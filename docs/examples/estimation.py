from typing import Dict, List, Optional, Tuple, cast

import numpy as np
from orquestra.quantum.api.backend import QuantumBackend
from orquestra.quantum.api.estimation import EstimationTask
from orquestra.quantum.measurements import ExpectationValues, expectation_values_to_real


def estimate_expectation_values_by_averaging(
    backend: QuantumBackend,
    estimation_tasks: List[EstimationTask],
) -> List[ExpectationValues]:

    (
        estimation_tasks_to_measure,
        estimation_tasks_not_to_measure,
        indices_to_measure,
        indices_not_to_measure,
    ) = split_estimation_tasks_to_measure(estimation_tasks)

    non_measured_expectation_values_list = evaluate_non_measured_estimation_tasks(
        estimation_tasks_not_to_measure
    )

    if estimation_tasks_to_measure == []:
        measured_expectation_values_list = []
    else:
        circuits, operators, shots_per_circuit = zip(
            *[
                (e.circuit, e.operator, e.number_of_shots)
                for e in estimation_tasks_to_measure
            ]
        )
        measurements_list = backend.run_circuitset_and_measure(
            circuits, shots_per_circuit
        )

        measured_expectation_values_list = [
            expectation_values_to_real(
                measurements.get_expectation_values(frame_operator)
            )
            for frame_operator, measurements in zip(operators, measurements_list)
        ]

    full_expectation_values: List[Optional[ExpectationValues]] = [
        None
        for _ in range(
            len(estimation_tasks_not_to_measure) + len(estimation_tasks_to_measure)
        )
    ]

    for ex_val, final_index in zip(
        non_measured_expectation_values_list, indices_not_to_measure
    ):
        full_expectation_values[final_index] = ex_val
    for ex_val, final_index in zip(
        measured_expectation_values_list, indices_to_measure
    ):
        full_expectation_values[final_index] = ex_val

    return cast(List[ExpectationValues], full_expectation_values)
