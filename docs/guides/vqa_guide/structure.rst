.. _vqa_structure:

=================
Structure of VQAs
=================

.. _vqa_intro:

Introduction to VQAs
=====================

The central idea of VQA is to use an **optimizer** to program a quantum computer.

In VQA, the optimizer selects a quantum program from a landscape of possible programs defined by an **ansatz**.

The optimizer selects a program by minimizing a **cost function** obtained from the output of the current quantum program.

To **estimate** the cost function, we need to run (or simulate) the quantum program.

Optimizers and cost functions are general features of optimization problems, so this guide focuses on ansatzes and estimators. For a more complete, yet approachable discussion, see `Michal's blogpost <https://www.mustythoughts.com/vqas-how-do-they-work>`_


.. _vqa_basics:

The Basics
==========

The process for running a VQA algorithm can be outlined in 5 steps:

1. Define initial ingredients ``Ansatz``, ``QuantumBackend`` and ``Optimizer``.
2. Call an ``EstimationTaskFactory`` factory using ``Ansatz``.
3. Call ``create_cost_function`` using the ``EstimationTaskFactory`` and ``Backend``.
4. Call ``optimizer.minimize`` using the ``CostFunction`` to get optimized parameters.
5. Call ``ansatz.get_executable_circuit`` with optimized parameters to get the quantum program.


Let's go through an example where a vqa is used to solve the maxcut problem. See the full program guide :ref:`qaoa tutorial <qaoa>` for a more in-depth look at this particular algorithm.

The main body of the program is this:

.. literalinclude:: ../../examples/qaoa_maxcut.py
    :language: python
    :start-at: def solve_maxcut_qaoa(test_graph):
    :end-at: return most_common_string

We'll go through the steps as they were outlined above:

1. The ``Ansatz``, ``Backend`` and ``Optimizer`` can be defined independently of one another.
2. As explained in :ref:`estimators guide <estimators>`, the ``EstimationTaskFactory`` tells the quantum computer how to construct a circuit. It therefore will always take an ``Ansatz`` as an argument.
3. As explained briefly above, VQA uses a quantum computer to estimate the cost function. So it is sensible that to create our cost function we would need the method of costructing circuits for our cost function (``EstimationTask``) and the quantum computer to run them on (``QuantumBackend``). See the :ref:`cost function <cost_function>` guide for details.
4. Now that we have the , we minimize if using the optimizer. This step generally takes the longest to run.
5. Obtain the final circuit by substituting the optimized parameters into the ansatz.

And that's it! once these steps are completed we have now finished our variational quantum algorithm in ``orquestra``!



