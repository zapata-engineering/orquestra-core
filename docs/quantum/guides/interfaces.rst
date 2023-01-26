.. _interfaces:
==========
Interfaces
==========


One of the biggest strengths of Orquestra is its modularity. Integrating new backends, optimizers, ansatzes, etc. does not require changing the core code - it requires only creating a new module that conforms to existing interfaces and therefore can be used across the whole platform. Using our interfaces helps you add whatever building blocks you need for your project and ensure that they will work well with other existing elements.

What is an interface?
=====================

Before we get into the details, let's explain what we mean by "interfaces" in this context. We use this word as a shorthand for "a way to implement certain concepts in such a way, that as long as two implementations conform to a particular interface, they can be swapped and the program should still work correctly". Obviously, various implementations might work differently - e.g.: one simulator might be faster than the other - but they should be indistinguishable when it comes to inputs, outputs and how they are being used.



Benefits of interfaces
======================

Interface offers the ability to define behaviour that can be implemented by unrelated classes without forcing them to share a common class hierarchy. This results in code flexibility and faster development with easier testing options. Other benefits include greater interoperability, modularity, and decoupling of dependencies.


Interface implementation
========================

Currently interfaces in Orquestra are defined in the following 3 main libraries:

* `orquestra-quantum <https://github.com/zapatacomputing/orquestra-quantum>`_
* `orquestra-opt <https://github.com/zapatacomputing/orquestra-opt>`_
* `orquestra-vqa <https://github.com/zapatacomputing/orquestra-vqa>`_

The interfaces are located in the ``api`` directory within each packages. They are implemented either as an ``abstract class`` or ``protocols``. `Abstract classes <https://docs.python.org/3/library/abc.html>`_ are classes that contain one or more abstract methods and thus cannot be instantiated. Concrete implementations (subclasses) of a given abstract base class have to override all of the abstract methods. Abstract base classes often serve as blueprint classes, defining common behaviours in terms of some specialized method(s) that has to be implemented in child classes.

However, using abstract classes requires using inheritance, which sometimes is undesirable. Therefore, we also make use of `Protocols <https://peps.python.org/pep-0544/>`_ . The main differences are that we don't have to explicitly express that particular implementation conforms to a protocol and that protocols work not just with classes, but also functions. 

Orquestra provides the following interfaces:


.. list-table::
    :align: left

    * - :class:`CircuitRunner <orquestra.quantum.api.circuit_runner.CircuitRunner>` (:ref:`guide <backends_guide>`)
    * - :class:`WavefunctionSimulator <orquestra.quantum.api.wavefunction_simulator.WavefunctionSimulator>` (:ref:`guide <backends_guide>`)
    * - :class:`Optimizer <orquestra.opt.api.Optimizer>` (:ref:`guide <optimizers_guide>`)
    * - :class:`CostFunction <orquestra.opt.api.CostFunction>`
    * - :class:`Ansatz <orquestra.vqa.api.ansatz.Ansatz>` (:ref:`guide <ansatzes_guide>`)
    * - :class:`Estimators <orquestra.quantum.api.estimation.EstimateExpectationValues>` (:ref:`guide <estimators_guide>`)


Passing parameters
------------------

You might wonder - what if I have two optimizers which take different sets of parameters? For example, you might want to use `L-BFGS-B <https://docs.scipy.org/doc/scipy/reference/optimize.minimize-lbfgsb.html#optimize-minimize-lbfgsb>`_ and `COBYLA <https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cobyla.html#optimize-minimize-cobyla>`_ from ``scipy``. This is how you would use them in scipy: 

.. literalinclude:: ../examples/guides/interfaces_guide.py
    :start-after: >> Guide code snippet: script showing scipy optimizers
    :lines: 2-3
    :language: python


``L-BFGS-B`` doesn't support argument called ``constraints`` and ``COBYLA`` doesn't support ``bounds``. So how can you make them fit the same interface, if they have different inputs?

In the case of optimizers, Orquestra solves this problem by moving differing parameters into object initialization. Constructed optimizers provide :meth:`minimize <orquestra.opt.api.Optimizer.minimize>` method that always accepts only :func:`create_cost_function <orquestra.vqa.cost_function.cost_function.create_cost_function>` and ``initial_params`` arguments. Once constructed, optimizers are fully interchangeable.

.. literalinclude:: ../examples/guides/interfaces_guide.py
    :start-after: >> Guide code snippet: script showing passing parameters for optimizers
    :lines: 2-8
    :language: python


We used optimizers here just as an example - this is the pattern that you might see with other interfaces as well. 


Testing
=======

Not every requirement can be expressed and enforced by using an abstract base class or a combination of static typing and protocols. For instance, there might be some nontrivial relationships between inputs and outputs that need to hold, or there might be some necessary side effects. Such requirements need to be verified by additional tests, as their violation cannot be caught by tools like mypy or Flake8. In Orquestra, every interface comes with a basic set of tests. You can find them in the ``<INTERFACE_NAME>_test`` directory next to the file where the interface itself is implemented. 

In many cases, Orquestra captures additional requirements as so-called "contracts". They are specific test functions that take an instance of the particular interface as input and check if it meets a certain "contract". Each contract checks some basic expected behaviour typically described by its name, e.g.: ``_validate_gradients_history_is_recorded_if_keep_history_is_true``. They are grouped in a list and can then be used in tests in the following way:

.. literalinclude:: ../examples/guides/interfaces_guide.py
    :start-after: >> Guide code snippet: script showing how to use contract tests
    :lines: 2-5
    :language: python

Apart from the contracts, each implementation might have a set of other unit tests which check behaviour specific to this implementation. You can find an example of how we test estimators `here <https://github.com/zapatacomputing/orquestra-vqa/blob/977a68202d00f93caa7e89726229c6a8a8bc05b0/tests/orquestra/vqa/estimation/cvar_test.py>`_.
