.. _interfaces:
========================
Interfaces
========================


One of the biggest strengths of Orquestra is its modularity. Integrating new backends, optimizers, ansatzes, etc. does not require changing the core code - it requires only creating a new module that conforms to existing interfaces and therefore can be used across the whole platform. These interfaces allow us to implement various modules and functions.

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

The intrefaces are located in the ``src/orquestra/api`` folder within each library. They are either used as an ``abstract`` class or ``protocols``. 

Example
~~~~~~~

Here we look at an example of creating a new ansatz class using an interface created for ansatz. The sample code will look as the following:

.. literalinclude:: ..//examples/mock_ansatz.py
    :language: python
    :start-at: from typing import Optional
    :end-at: class MockAnsatz(Ansatz):



.. literalinclude:: ../examples/circuits_guide.py
  :language: python
  :start-at: unitary = problem_hamiltonian_circ.to_unitary()
  :end-at: ic(type(unitary))
