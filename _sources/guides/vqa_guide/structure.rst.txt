.. _vqa_structure:

=================
Structure of VQAs
=================

.. _vqa_intro:

Introduction to VQAs
=====================

The central idea of VQAs is to use an **optimizer** to find the best quantum circuit to do the job at hand.

We start with an **ansatz** - this is a "template" for generating circuits, which has tunable parameters.

The optimizer selects the parameters by minimizing a **cost function** obtained from the output of the current quantum program.

To **estimate** the value of the cost function for given set of parameters, we need to run (or simulate) the quantum program.

:ref:`Optimizers <optimizers_guide>` and :ref:`cost functions <cost_function_guide>` are general features of optimization problems, so this guide focuses on ansatzes and estimators. For a more complete, yet approachable discussion, see `Michał's blogpost <https://www.mustythoughts.com/vqas-how-do-they-work>`_.


.. _vqa_basics:

The Basics
==========

The process for running a VQA algorithm can be outlined in 5 steps:

1. Define initial ingredients: :class:`Ansatz <orquestra.vqa.api.ansatz.Ansatz>`, :class:`WavefunctionSimulator <orquestra.quantum.api.wavefunction_simulator.WavefunctionSimulator>` or :class:`CircuitRunner <orquestra.quantum.api.circuit_runner.CircuitRunner>` and :class:`Optimizer <orquestra.opt.api.Optimizer>`.
2. Create an :class:`EstimationTaskFactory <orquestra.quantum.api.estimation.EstimationTasksFactory>` factory using :class:`Ansatz <orquestra.vqa.api.ansatz.Ansatz>`.
3. Call :func:`create_cost_function <orquestra.vqa.cost_function.cost_function.create_cost_function>` using the :class:`EstimationTaskFactory <orquestra.quantum.api.estimation.EstimationTasksFactory>`  and :class:`WavefunctionSimulator <orquestra.quantum.api.wavefunction_simulator.WavefunctionSimulator>` or :class:`CircuitRunner <orquestra.quantum.api.circuit_runner.CircuitRunner>`.
4. Call :meth:`optimizer.minimize <orquestra.opt.api.Optimizer.minimize>` using the :class:`CostFunction <orquestra.opt.api.cost_function.CostFunction>` to get optimized parameters.
5. Call :meth:`ansatz.get_executable_circuit <orquestra.vqa.api.ansatz.Ansatz.get_executable_circuit>` with optimized parameters to get the quantum program.


Let's go through an example where a vqa is used to solve the maxcut problem. See the :ref:`qaoa tutorial <qaoa_tutorial>` for a more hands-on example how to use VQAs with Orquestra Core

.. literalinclude:: ../../examples/tutorials/qaoa_maxcut.py
    :language: python
    :start-at: def solve_maxcut_qaoa(test_graph):
    :end-at: return most_common_string

We'll go through the steps as they were outlined above:

1. The :class:`Ansatz <orquestra.vqa.api.ansatz.Ansatz>`, :class:`WavefunctionSimulator <orquestra.quantum.api.wavefunction_simulator.WavefunctionSimulator>` or :class:`CircuitRunner <orquestra.quantum.api.circuit_runner.CircuitRunner>` and :class:`Optimizer <orquestra.opt.api.Optimizer>` can be defined independently of one another.
2. As explained in :ref:`estimators guide <estimators>`, the :class:`EstimationTaskFactory <orquestra.quantum.api.estimation.EstimationTasksFactory>` tells the quantum computer how to construct a circuit. It therefore will always take an :class:`Ansatz <orquestra.vqa.api.ansatz.Ansatz>` as an argument.
3. As explained briefly above, VQA uses a quantum computer to estimate the value of the cost function. So to create our cost function we would need the method of constructing circuits for our cost function (``estimation_task_factory``) and a simulator or runner to execute them. See the :ref:`cost function <cost_function_guide>` guide for details.
4. Now that we have the cost function, we minimize if using the optimizer. This step generally takes the longest to run.
5. Obtain the final circuit by substituting the optimized parameters into the ansatz.

And that's it! once these steps are completed we have now finished our variational quantum algorithm in ``orquestra``!



Libraries structure
===================

Most of the code associated directly with VQAs lives in the `orquestra-vqa <https://github.com/zapatacomputing/orquestra-vqa>`_ repository. Some of these are not worth separate guides, but it might be useful for you to know what we have.

So here's a short list of what's in `orquestra-vqa`:

- ansatzes - see :ref:`ansatzes guide <_ansatzes_guide>`
- cost functions - see: :ref:`cost functions guide <cost_function_guide>`
- estimation - see: :ref:`estimation guide <estimators_guide>`
- grouping - see: :ref:`estimation guide <estimators_guide>`
- openfermion - some utility tools to make it easier to work with `OpenFermion <https://quantumai.google/openfermion>`_ within Orquestra.
- optimizers - we have some VQA-specific optimizers such as Layer-by-layer optimizer, `Fourier <https://journals.aps.org/prx/abstract/10.1103/PhysRevX.10.021067>`_ or `R-QAOA <https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.125.260505>`_ . See: :ref:`optimizers guide <optimizers_guide>` for more details.
- parameter initialization - `Interp method <https://journals.aps.org/prx/abstract/10.1103/PhysRevX.10.021067>`_
- shot allocation - see: :ref:`estimation guide <estimators_guide>`