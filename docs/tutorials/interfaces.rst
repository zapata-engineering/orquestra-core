.. _interfaces:
========================
Interfaces
========================


One of the biggest strengths of Orquestra is its modularity. Integrating new backends, optimizers, ansatzes, etc. does not require changing the core code - it requires only creating a new module that conforms to existing interfaces and therefore can be used across the whole platform. These interfaces allow us to implement various modules and functions.

Benefits of interfaces
~~~~~~~~~~~~~~~~~~~~~~

Interface offers the ability to define behaviour that can be implemented by unrelated classes without forcing them to share a common class hierarchy. This results in code flexibility and faster development with easier testing options. 


Interfaces provided by the Orquestra are:

* ``QuantumBackend``
* ``QuantumSimulator`` (subclass of ``QuantumBackend``)
* ``Optimizer``
* ``CostFunction``
* ``Ansatz``


Interface implementation
========================

Orquestra have 3 main library with interfaces and they are:

* `orquestra-quantum <https://github.com/zapatacomputing/orquestra-quantum>`_
* `orquestra-opt <https://github.com/zapatacomputing/orquestra-opt>`_
* `orquestra-vqa <https://github.com/zapatacomputing/orquestra-vqa>`_

The interfaces are located in the ``api`` directory within each library. They are either used as an ``abstract`` class or ``protocols``. `Abstract classes <https://python-course.eu/oop/the-abc-of-abstract-base-classes.php#:~:text=Abstract%20classes%20are%20classes%20that,implementations%20for%20the%20abstract%20methods.>`_ are classes that contain one or more abstract method. However, they do not contain any implementation. Subclasses are required to provide implementations for abstract methods. Abstract classes can also be considered blueprint classes. Protocols are used to define an interface class that acts as a blueprint for designing other classes. 


Example
~~~~~~~

Here we look at an example of creating a new ansatz class using an interface created for ansatz. The sample code will look as the following:

# QUESTION: is this correct?

.. literalinclude:: ../examples/estimation.py
        :language: python
        :start-at: import numpy as np
        :end-at: return cast(List[ExpectationValues], full_expectation_values)

Once an interface is created, we highly encourage you to create tests and ensure your interfaces are passing. You find some examples in our `tests <https://github.com/zapatacomputing/orquestra-quantum/blob/1d7b437cffb767f9a5caddf824911e13d268eec5/tests/orquestra/quantum/estimation/estimation_test.py>`_ directory. 

New interface idea
~~~~~~~~~~~~~~~~~~
If you have any suggestions for new interfaces, please reach out to `info@zapatacomputing.com <info@zapatacomputing.com>`_
