################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
# use for literalinclude start-after >> Start
import matplotlib.pyplot as plt
import pandas as pd

import orquestra.sdk as sdk

# Get the results of the workflow run
workflow_run = sdk.WorkflowRun.by_id("wf.vqe_workflow.661d935")

# Transform the results into a pandas DataFrame
backend_names = []
cost_function_values = []
for task in workflow_run.get_tasks():
    if task.fn_name == "evaluate_cost_function":
        backend_names.append(task.get_inputs().kwargs["backend_name"])
        cost_function_values.append(task.get_outputs())
    if task.fn_name == "find_optimal_params":
        optimal_value = task.get_outputs()[1]

results = pd.DataFrame(
    {"Backend": backend_names, "Cost function value": cost_function_values}
)

# Plot the results
results["Error"] = results["Cost function value"] - optimal_value
results.plot(x="Backend", y="Error", kind="scatter")
plt.tight_layout()
plt.show()
