.. _interfaces:
========================
Interfaces
========================


One of the biggest strengths of Orquestra is its modularity. Integrating new backends, optimizers, ansatzes, etc. does not require changing the core code - it requires only creating a new module that conforms to existing interfaces and therefore can be used across the whole platform. Using our interfaces help you add whatever building blocks you need for your project and ensure that they will work well with other existing elements.

What is an interface?
=====================

Before we get into the details, let's explain what we mean by "interfaces" in this context. We use this word as a shorthand for "a way to implement certain concepts in such a way, that as long as two implementations conform to a particular interface, they can be swapped and the program should still work correctly". Obviously, various implementations might work differently - e.g.: one simulator might be faster than the other - but they should be undistinguishable when it comes to inputs, outputs and how they are being used.



Benefits of interfaces
======================

Interface offers the ability to define behaviour that can be implemented by unrelated classes without forcing them to share a common class hierarchy. This results in code flexibility and faster development with easier testing options. Other benefits include:

* Interoperability
* Modularity
* Dependencies decoupling


Interface implementation
========================

Currently interfaces in Orquestra are defined in the following 3 main libraries:

* `orquestra-quantum <https://github.com/zapatacomputing/orquestra-quantum>`_
* `orquestra-opt <https://github.com/zapatacomputing/orquestra-opt>`_
* `orquestra-vqa <https://github.com/zapatacomputing/orquestra-vqa>`_

The interfaces are located in the ``api`` directory within each packages. They are implemented either as an ``abstract class`` or ``protocols``. `Abstract classes <https://docs.python.org/3/library/abc.html>`_ are classes that contain one or more abstract method. However, they do not contain any implementation. Subclasses are required to provide implementations for abstract methods. Abstract classes can also be considered blueprint classes. 

However, using abstract classes requires using inheritance, which sometimes is undesirable. Therefore, we also make use of `Protocols <https://peps.python.org/pep-0544/>`_ . The main differences are that we don't have to explicitly express that particular implementation conforms to a protocol and that protocols work not just with classes, but also functions. 

Interfaces provided by Orquestra are:

* :class:`QuantumBackend <orquestra.quantum.api.QuantumBackend>` (:ref:`guide <backends_guide>`)
* :class:`QuantumSimulator <orquestra.quantum.api.backend.QuantumSimulator>` (:ref:`guide <backends_guide>`)
* :class:`Optimizer <orquestra.opt.api.Optimizer>` (:ref:`guide <optimizers_guide>`)
* :class:`CostFunction <orquestra.opt.api.CostFunction>` (:ref:`guide <cost_function_guide>`)
* :class:`Ansatz <orquestra.vqa.api.ansatz.Ansatz>` (:ref:`guide <ansatzes_guide>`)
* :class:`Estimators <orquestra.quantum.api.estimation.EstimateExpectationValues>` (:ref:`guide <estimators_guide>`)


Passing parameters
------------------

You might wonder - what if I have two optimizers which take different sets of parameters? For example, you might want to use `L-BFGS-B <https://docs.scipy.org/doc/scipy/reference/optimize.minimize-lbfgsb.html#optimize-minimize-lbfgsb>`_ and `COBYLA <https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cobyla.html#optimize-minimize-cobyla>`_ from `scipy`. This is how you would use them in scipy: 

.. literalinclude:: ../examples/interfaces_guide.py
    :start-after: >> Guide code snippet: script showing scipy optimizers
    :lines: 2-3
    :language: python


`L-BFGS-B` doesn't support argument called `constraints` and `COBYLA` doesn't support `bounds`. So how can you make them fit the same interface, if they have different inputs?

The way we solved this is that in case of Optimizers, we created an interface which has method `minimize`, which requires providing only `cost_function` and `initial_params`. All the extra parameters are passed during the initialization of the Optimizer class, like this:

.. literalinclude:: ../examples/interfaces_guide.py
    :start-after: >> Guide code snippet: script showing passing parameters for optimizers
    :lines: 2-8
    :language: python


We used optimizers here just as an example - this is the pattern that you might see with other interfaces as well. 


Testing
=======

Since some behaviours are impossible to enforce with just abstract class or protocol, in order to make sure that given implementation of an interface meets all the requirements, it should be tested. Every interface comes with a basic set of tests. You can find them in the `<INTERFACE_NAME>_test` directory next to the file where interface itself is implemented. 

In many cases we use so called "contracts". These are specific tests that take an instance of particular interface as input and check if it meets certain "contract". Each contract checks some basic expected behaviour, e.g.: `_validate_gradients_history_is_recorded_if_keep_history_is_true`. They are grouped in a list and can then used in tests in the following way:

.. literalinclude:: ../examples/interfaces_guide.py
    :start-after: >> Guide code snippet: script showing how to use contract tests
    :lines: 2-5
    :language: python

Apart from the contracts, each implementation might have a set of other unit tests which check behavior specific for this implementation. You can find an example of how we test estimators `here <https://github.com/zapatacomputing/orquestra-vqa/blob/977a68202d00f93caa7e89726229c6a8a8bc05b0/tests/orquestra/vqa/estimation/cvar_test.py>`_.

New interface idea
==================
If you have any suggestions for new interfaces, please reach out to `info@zapatacomputing.com <info@zapatacomputing.com>`_
