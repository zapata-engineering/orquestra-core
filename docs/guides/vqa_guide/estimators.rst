.. _estimators_guide:

==========
Estimators
==========


An important part of many quantum algorithms is estimating the expectation value of an observable :math:`O` given the state :math:`|\psi>`: :math:`<\psi| O |\psi>`. There are many methods to achieve this, which might vary depending on the circumstances. 

In this guide, we'll show you the tools to achieve this within Orquestra Core. 

Estimation process
==================

Let's look at the process of estimating expectation values as a black box. What can we say about it? 
We know what the input should be: 

- an observable 
- a quantum state 


And we know what the output should be:

- expectation value


An observable is simple - it can be a Hamiltonian representing our system, consisting of multiple Pauli terms. Expectation value is also straightforward, as it is just a number.

Quantum state, however... Well, this is a little bit more tricky, as we don't have access to the quantum state directly. The most common way of expressing a quantum state is to use a quantum circuit - if you think about it, a quantum circuit is nothing else, but a set of instructions of how to construct a quantum state. 

So we have a circuit, now another thing we need is something to execute the circuit on - a quantum backend. This can be either a real quantum computer or a simulation.

Unfortunately, when you run your circuit on a quantum computer, you don't get a quantum state - you only get a collection of samples. The more samples (shots) you take, the better you will be able to estimate the expectation values (this is the reason why we are talking about "estimating" and not "calculating" expectation values.

Now we have all the components necessary for the estimation process:

- observable
- circuit
- number of shots
- quantum backend

Estimation itself is not specific for variational quantum algorithms. However, many estimation methods have been defined in the context of VQAs, so you can find some of them in `orquestra-quantum <https://github.com/zapatacomputing/orquestra-quantum>`_ and some in `orquestra-vqa <https://github.com/zapatacomputing/orquestra-vqa>`_.

Extra steps
===========

You have all the elements needed to perform estimation, that we just listed above. Unfortunately, this might not be enough to perform the estimation efficiently and there are some extra steps which will ensure that things go smoothly. Here I'll briefly describe three such steps. If you are unfamiliar with these concepts, you can find context selection described in `this blogpost about VQE <https://www.mustythoughts.com/variational-quantum-eigensolver-explained>`_ and shot allocation and grouping in `this one <https://www.mustythoughts.com/vqe-challenges.html>`_.

First, context selection, which is a standard step in VQE. You can only perform measurements in the Z-basis, but your observable might contain terms which require a different basis. In such case, you need to change the basis - you can achieve this by appending an appropriate rotation at the end of your circuits. This is what "context selection" does.

Second, shot allocation. If your Hamiltonian have multiple terms, but you have just a limited number of samples you can take, how do you decide how to distribute them across terms? That's what shot allocation does.

Third, grouping. Instead of running a separate circuit for every term, you might be able to group some of them to get the optimal performance.

Let's look at the software that we built to accomodate all these!

Estimation in Orquestra
=======================

As you can see there are many moving parts in the whole estimation process. Here we'll go through how they are all implemented in software.

Data structures
---------------

There are two main data structures we use here. The first is ``EstimationTask``. It's an object which encapsulates all the data needed to perform estimation:

- ``operator``: a   :class:`PauliSum <orquestra.quantum.operators.PauliSum>` which represents the observable
- ``circuit``: a :class:`Circuit <orquestra.quantum.circuits.Circuit>` object which allow us to get a quantum state
- ``number_of_shots``: ``int`` which specifies how many shots we make. 

Another one is :class:`ExpectationValues <orquestra.quantum.measurements.ExpectationValues>`. Apart from storing the values themselves, if particular estimation method calculates correlations or covariances, it can also store them.

Estimation method
-----------------

Once we have our :class:`EstimationTask <orquestra.quantum.api.estimation.EstimationTask>` defined, we can think about what algorithm for estimation to use. These algorithms are expressed using :class:`EstimateExpectationValues <orquestra.quantum.api.estimation.EstimateExpectationValues>` interface. It is implemented as Python Protocol (you can read more about it in :ref:`interfaces guide <interfaces_guide>`) and it's fairly simple:

.. literalinclude:: ../../examples/guides/estimators_guide.py
    :start-after: >> Tutorial code snippet: estimation protocol
    :lines: 2-6
    :language: python


Let's say you have created a new estimator called ``my_estimator``. In order to use it, you need to call it and provide a backend and a list of estimation_tasks. However, the definition you see above is not enough to make sure all the estimators work reliably. All the implementations of this protocol should also meet the following criteria (which we enforce by a set of contract tests):

1. Return one ExpectationValue for each EstimationTask.
2. The order in which ExpectationValues are returned should match the order in which EstimationTasks were provided.
3. Number of entries in each ExpectationValue is not restricted - if the operator consists of multiple terms, estimator might be contain values for each term.
4. Output ExpectationValue should include coefficients of the terms/operators.
5. ``estimation_tasks`` can include tasks where operator consists of a constant term or contains a constant term. The implemented method should include the contributions of such constant terms in the return value.

We hope points 1-3 are not controversial for you. Points 4-5 define a conventions that we have decided to follow - we know that in some circles people like using other conventions, which might be confusing. So we want to be clear about the conventions that we follow.

``orquestra`` provides several separate ways of obtaining expectation values:

- :func:`calculate_exact_expectation_values <orquestra.quantum.estimation.calculate_exact_expectation_values>`
- :func:`estimate_expectation_values_by_averaging <orquestra.quantum.estimation.estimate_expectation_values_by_averaging>`
- :class:`CvarEstimator <orquestra.vqa.estimation.cvar.CvarEstimator>`
- :class:`GibbsObjectiveEstimator <orquestra.vqa.estimation.gibbs_objective.GibbsObjectiveEstimator>`


Preprocessors
-------------

We have also introduced a concept of :class:`EstimationPreprocessor <orquestra.quantum.api.estimation.EstimationPreprocessor>`. EstimationPreprocessors is a function which takes in a list of estimation tasks and returns a new list of estimation tasks. It's a simple abstraction, but allows to express some of those "extra steps" that we described later. For example, if we want to perform grouping, we will provide a list containing one estimation task with a big operator and then get back multiple tasks each with an operator representing one group.


In Orquestra Core we have implemented the following preprocessors:


- shot allocation:
    - :func:`allocate_shots_proportionally <orquestra.vqa.shot_allocation.allocate_shots_proportionally>`
    - :func:`allocate_shots_uniformly <orquestra.vqa.shot_allocation.allocate_shots_uniformly>`
- grouping:
    - :func:`group_individually <orquestra.vqa.grouping.group_individually>`
    - :func:`group_greedily <orquestra.vqa.grouping.group_greedily>`
    - :func:`group_comeasureable_terms_greedy <orquestra.vqa.grouping.group_comeasureable_terms_greedy>`
- :func:`perform_context_selection <orquestra.vqa.estimation.context_selection.perform_context_selection>`


If you look closely, you might notice that some of these methods do not actually follow the preprocessor interface. Let's take a look at `allocate_shots_proportionally`. It takes two things as input - list of estimation tasks and total number of shots. So why do we say it's kindof a preprocessor? Cause it's easy to make it into a preprocessor using `partial`:


.. literalinclude:: ../../examples/guides/estimators_guide.py
    :start-after: >> Tutorial code snippet: script showing how to use partials
    :lines: 2-4
    :language: python


Utility functions
-----------------

We have also created a couple of methods which make working with estimators easier, here's a brief overview:

Let's start with factories of estimation tasks. What is a factory? Factory is a method which creates some objects according to a particular recipe, given the inputs. It's useful when you don't know ahead of time exactly what the parameters of your object should be. In case of variational algorithms we can't create circuits ahead, as we don't know what their parameters will be - they are updated on the fly. If we don't know what the circuis are, we also can't create our estimation tasks. But we can create an object (factory), which will generate those estimation tasks. This all happens inside the cost function and fortunately you don't have worry too much about how exactly. Two most important factories are :func:`substitution_based_estimation_tasks_factory <orquestra.vqa.cost_function.cost_function.substitution_based_estimation_tasks_factory>` and :func:`dynamic_circuit_estimation_tasks_factory <orquestra.vqa.cost_function.cost_function.dynamic_circuit_estimation_tasks_factory>`. The main difference between them is that the first one creates a circuit once and then just subtitutes symbols with parameters, while the other one creates circuits on the fly.

Some other tools:

- :func:`evaluate_estimation_circuits <orquestra.quantum.estimation.evaluate_estimation_circuits>` - substitutes symbols with numerical parameters for all the circuits in the estimation tasks 
- :func:`split_estimation_tasks_to_measure <orquestra.quantum.estimation.split_estimation_tasks_to_measure>` - this function splits a given list of EstimationTask into two: one that contains EstimationTasks that should be measured, and one that contains EstimationTasks with constants or with 0 shots.
- :func:`evaluate_non_measured_estimation_tasks <orquestra.quantum.estimation.evaluate_non_measured_estimation_tasks>` - this returns the expectation value for the tasks which don't need to be measured

Example
=======

Let's see how this plays out in an actual example. For example, let's say we want to run VQE using the following techniques:
- greedy grouping algorithm
- proportional shot allocation with total 50000 shots per iteration
- CVaR estimation method with alpha equal to 0.1

Here's a snippet of code which shows how to do this:

.. literalinclude:: ../../examples/guides/estimators_guide.py
    :start-after: >> Tutorial code snippet: script for running VQE
    :lines: 16-40
    :language: python


And if you would like to run and play with this code, here is the whole script:


.. literalinclude:: ../../examples/guides/estimators_guide.py
    :start-after: >> Tutorial code snippet: script for running VQE
    :lines: 2-46
    :language: python
