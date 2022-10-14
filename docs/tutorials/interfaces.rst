.. _interfaces:
========================
Interfaces
========================


One of the biggest strengths of Orquestra is its modularity. Integrating new backends, optimizers, ansatzes, etc. does not require changing the core code - it requires only creating a new module that conforms to existing interfaces and therefore can be used across the whole platform. 
Benefits of interfaces
~~~~~~~~~~~~~~~~~~~~~~

Interface offers the ability to define behaviour that can be implemented by unrelated classes without forcing them to share a common class hierarchy. This results in code flexibility and faster development with easier testing options. Other benefits include:

* Interoperability
* Modularity
* Dependencies decoupling

Some relevant contents regarding these can be found `here <https://www.zapatacomputing.com/we-felt-your-pain-and-built-orquestra/>`_.


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

Here we look at an example of creating a new expectation class using an interface created for expectation values. The sample code will look as the following:


.. literalinclude:: ../examples/expectation_values.py
        :language: python
        :start-at: from typing import List
        :end-at: return expectation_values_list


Testing
~~~~~~~~

Since behaviours are impossible to enforce with just abstract class or protocol, in order to make sure that your implementation of an interface meets all the requirements, you should add tests for it. Every interface comes with basic set of tests. For a reference usage of these tests we recommend looking at code `test <https://github.com/zapatacomputing/orquestra-quantum/blob/1d7b437cffb767f9a5caddf824911e13d268eec5/tests/orquestra/quantum/estimation/estimation_test.py>`_ for particular interface implementations.

New interface idea
~~~~~~~~~~~~~~~~~~
If you have any suggestions for new interfaces, please reach out to `info@zapatacomputing.com <info@zapatacomputing.com>`_
