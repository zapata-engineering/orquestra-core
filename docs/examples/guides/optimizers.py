# Definition of cost function
import numpy as np


def f_incorrect(x: float, y: float, z: float) -> float:
    return x ** 2 + y ** 2 + z ** 2


def f_correct(parameters: np.ndarray) -> float:
    x, y, z = parameters
    return x ** 2 + y ** 2 + z ** 2
# --- End


# Cost function with gradient as a class
class SumOfSquaresWithGradient:

    def __call__(self, parameters: np.ndarray) -> float:
        return (parameters ** 2).sum()

    def gradient(self, parameters: np.ndarray) -> np.ndarray:
        return 2 * parameters
# --- End


# FunctionWithGradient
from orquestra.opt.api import FunctionWithGradient


def sum_of_squares(parameters: np.ndarray) -> float:
    return (parameters ** 2).sum()


def sum_of_squares_gradient(parameters: np.ndarray) -> np.ndarray:
    return 2 * parameters


cost_function = FunctionWithGradient(
    sum_of_squares,
    sum_of_squares_gradient
)
# --- End


# finite differences
from orquestra.opt.gradients import finite_differences_gradient

cost_function = FunctionWithGradient(
    sum_of_squares,
    finite_differences_gradient(
        sum_of_squares,
        finite_diff_step_size=1e-4
    )
)
# --- End


# Basic optimization
from orquestra.opt.optimizers import ScipyOptimizer, SimpleGradientDescent


my_optimizers = [
    ScipyOptimizer(method="L-BFGS-B"),
    SimpleGradientDescent(learning_rate=0.1, number_of_iterations=1000)
]

for optimizer in my_optimizers:
    result = optimizer.minimize(cost_function, initial_params=np.array([1.0, -1.0, 0.5]))
    print(result)
# --- End


# Using OptimizeResult
optimizer = ScipyOptimizer(method="L-BFGS-B")
result = optimizer.minimize(cost_function, initial_params=np.array([1.0, -1.0, 0.5]))
print(f"opt_value: {result.opt_value}")
print(f"opt_params: {result.opt_params}")
# --- End
