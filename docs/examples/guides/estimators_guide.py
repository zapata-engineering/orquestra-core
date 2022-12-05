from typing import List, Protocol

from orquestra.quantum.api.circuit_runner import BaseCircuitRunner
from orquestra.quantum.api.estimation import EstimationTask, ExpectationValues


# >> Tutorial code snippet: estimation protocol
# >> Start
class EstimateExpectationValues(Protocol):
    def __call__(
        self, backend: BaseCircuitRunner, estimation_tasks: List[EstimationTask]
    ) -> List[ExpectationValues]:
        """Estimate expectation values using given backend."""


# >> End


# >> Tutorial code snippet: script showing how to use partials
# >> Start
from functools import partial

from orquestra.vqa.shot_allocation import allocate_shots_proportionally

shot_allocation_preprocessor = partial(
    allocate_shots_proportionally, total_n_shots=50000
)
# >> End


# >> Tutorial code snippet: script for running VQE
# >> Start
from functools import partial

import numpy as np
from orquestra.integrations.qulacs.simulator import QulacsSimulator
from orquestra.opt.optimizers import ScipyOptimizer
from orquestra.quantum.operators import PauliSum
from orquestra.vqa.ansatz.quantum_compiling import HEAQuantumCompilingAnsatz
from orquestra.vqa.cost_function.cost_function import (
    create_cost_function,
    substitution_based_estimation_tasks_factory,
)
from orquestra.vqa.estimation.context_selection import perform_context_selection
from orquestra.vqa.estimation.cvar import CvarEstimator
from orquestra.vqa.grouping import group_greedily
from orquestra.vqa.shot_allocation import allocate_shots_proportionally

# We define all the other components necessary to define the cost function
hamiltonian = PauliSum("Z0*X1*Z2 + Z0*Z2*Y3 + X3")
backend = QulacsSimulator()
ansatz = HEAQuantumCompilingAnsatz(2, hamiltonian.n_qubits)

# And now we get to estimation methods
estimation_method = CvarEstimator(alpha=0.1)
shot_allocation = partial(allocate_shots_proportionally, total_n_shots=50000)

# Order matters - context selection needs to happen after the grouping!
estimation_preprocessors = [
    group_greedily,
    perform_context_selection,  # This is required for VQE measurements to be done in the right way
    shot_allocation,
]

estimation_task_factory = substitution_based_estimation_tasks_factory(
    hamiltonian, ansatz, estimation_preprocessors
)

# And here is finally the cost function we will be minimizing
cost_function = create_cost_function(
    backend, estimation_task_factory, estimation_method
)

optimizer = ScipyOptimizer(method="COBYLA", options={"maxiter": 250})
initial_params = np.random.random(ansatz.number_of_params)
opt_results = optimizer.minimize(cost_function.function, initial_params)
# >> End
