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


# keep_history
result = optimizer.minimize(
    cost_function,
    initial_params=np.array([1.0, -1.0, 0.5]),
    keep_history=True
)
print(result.history)
# --- End

# history_entry
print([entry.value for entry in result.history])
# --- End

# basic recorder
from orquestra.opt.history import recorder

wrapped_cost_function = recorder(cost_function)
parameters = np.random.rand(3)
# Check that we get the same results
assert cost_function(parameters) == wrapped_cost_function(parameters)
print(parameters)
print(wrapped_cost_function.history)
# --- End

# recording gradient
print(wrapped_cost_function.gradient(np.array([1, 2, 3])))
print(wrapped_cost_function.gradient.history)
# --- End

# every nth
from orquestra.opt.api.save_conditions import every_nth

# Create fresh recorder
wrapped_cost_function = recorder(cost_function, save_condition=every_nth(4))

for i in range(20):
    wrapped_cost_function(i * np.ones(3))

print([entry.value for entry in wrapped_cost_function.history])
# --- End

# custom save condition
def my_save_condition(value, parameters, call_number) -> bool:
    return parameters[1] > parameters[0]


wrapped_cost_function = recorder(cost_function, save_condition=my_save_condition)
wrapped_cost_function(np.array([1, 2, 0]))  # Should be saved
wrapped_cost_function(np.array([2, 1, 0]))  # Should not be saved

print(wrapped_cost_function.history)
# --- End


# storing artifacts
def sum_of_squares_with_artifacts(parameters: np.ndarray, store_artifact=None) -> float:
    if store_artifact:
        store_artifact("order", np.argsort(parameters))
    return (parameters ** 2).sum()

wrapped_cost_function = recorder(sum_of_squares_with_artifacts)

for i in range(4):
    wrapped_cost_function(np.random.rand(3))

print(wrapped_cost_function.history[0])
for entry in wrapped_cost_function.history:
    print(f"parameters: {entry.params}, order: {entry.artifacts['order']}")
# --- End
