################################################################################
# © Copyright 2023 Zapata Computing Inc.
################################################################################
# use for literalinclude start-after >> Start
from workflow_defs import vqe_workflow

my_workflow = vqe_workflow(["ibmq_quito", "ibmq_belem", "ibmq_manila"], n_repetitions=4)
my_workflow_run = my_workflow.run("ray")
print(my_workflow_run.run_id)
