.. _estimators_guide:

==========
Estimators
==========

Estimators abstract away the method which is used to estimate a quantity. ``orquestra-vqa``provides 2 main estimator tools ``EstimationMethod`` and ``EstimationTaskFactory``.

``EstimationMethod``
====================

A ``QuantumBackend`` object can be either a simulator or hardware. On a simulator, we have direct access to the wavefunction so we can simply extract the expectation value of an observable :math:`O` by calculating :math:`<\psi| O |\psi>`.

In addition to this this, ``orquestra`` provides several separate ways of obtaining expectation values:
- ``calculate_exact_expectation_values``
- ``estimate_expectation_values_by_averaging``
- ``perform_context_selection``
- ``CvarEstimator``
- ``GibbsObjectiveEstimator``


``EstimationTaskFactory``
=========================

In VQA, a quantum computer is used to estimate the cost function of an optimization problem (see :ref:`Introduction to VQAs <vqa_intro>`). In orquestra, the ``EstimationTaskFactory`` object tells the quantum computer which circuits to run when calculating the cost function. Specifically, it takes the parameters being optimized and turns them into a circuit.

When defining a VQA in orquestra, ``CostFunction`` :ref:`objects <cost_function>` typically take an ``EstimationTaskFactory`` as an argument. See :ref:`the VQA basics <vqa_basics>` for an example.

``EstimationTaskFactory`` Factory
=================================

- We have seen a great prolifereation of ``EstimationTaskFactory`` objects for our many VQAs. So we have implemented a methods to quickly construct ``EstimationTaskFactory`` objects, known as ``EstimationTaskFactory`` factories.

- The simplest example of this is ``evaluate_estimation_circuits``, which simply takes in a parameterized circuit (in an ``EstimationTask`` object) and a symbols map and substitutes those symbols into the circuit.

- The most common example of an ``EstimationTaskFactory`` factory in VQAs is the ``expectation_value_estimation_tasks_factory`` `method <https://github.com/zapatacomputing/orquestra-vqa/blob/c6ddc3ecba726a092126277e5d04c5076741be65/src/orquestra/vqa/cost_function/cost_function.py#:~:text=def%20expectation_value_estimation_tasks_factory>`_. When called, this method returns an ``EstimationTaskFactory`` which generates circuits for a given observable.

- We recognize this is confusing and plan on refactoring ``EstimationTaskFactory`` soon to make up for this.


``EstimationPreprocessors``
===========================

Say you are tasked with a VQA which requires substituting your parameters into more than one circuit. You can use ``EstimationPreprocessors`` to acheive this. A list of preprocessors is given as follows:
1. shot allocation - allows one to dynamically allocate shots to estimation tasks.
2. grouping - combine EstimationTasks which can be done simultaneously to save computation resources. Comes in 3 types:
    a. group_individually
    b. group_greedily
    c. group_comeasureable_terms_greedy
