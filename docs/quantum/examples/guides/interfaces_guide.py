import numpy as np
import scipy
from scipy.optimize.bounds import Bounds


def cost_function(self, x: np.ndarray) -> float:
    w = 1 + (x - 1) * 0.25
    return (
        np.sin(np.pi * x[0]) ** 2
        + np.sum((w[:-1] - 1) ** 2 * (1 + 10 * np.sin(np.pi * w[:-1]) ** 2))
        + (w[-1] - 1) ** 2 * (1 + np.sin(2 * np.pi * w[-1]) ** 2)
    )


initial_params = np.random.uniform(-600, 600, 3)
bounds = Bounds()
constraints = ()

# >> Guide code snippet: script showing scipy optimizers
# >> Start
scipy.optimize.minimize(cost_function, initial_params, method="L-BFGS-B", bounds=bounds)
scipy.optimize.minimize(cost_function, initial_params, method="COBYLA", constraints=constraints)
# >> End


# >> Guide code snippet: script showing passing parameters for optimizers
# >> Start
from orquestra.opt.optimizers.scipy_optimizer import ScipyOptimizer

optimizer_1 = ScipyOptimizer(method="L-BFGS-B", bounds=bounds)
optimizer_2 = ScipyOptimizer(method="COBYLA", constraints=constraints)

optimizer_1.minimize(cost_function, initial_params)
optimizer_2.minimize(cost_function, initial_params)
# >> End


import pytest
from orquestra.quantum.api.estimator_contract import ESTIMATOR_CONTRACTS
from orquestra.vqa.estimation.cvar import CvarEstimator


# >> Guide code snippet: script showing how to use contract tests
# >> Start
@pytest.mark.parametrize("contract", ESTIMATOR_CONTRACTS)
def test_estimator_contract(contract):
    estimator = CvarEstimator(alpha=0.2)
    assert contract(estimator)


# >> End
