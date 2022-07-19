==============
Backends guide
==============

TODO: prose here about backends and this guide

What this guide covers
======================

* General intro
* In-depth dive in how various methods work, what’s the default etc.
* Zapata's backend – TrackingBackend, SymbolicBackend
* Currently integrated backends
* Conversions to other frameworks
* info on what to do in case where given backend doesn’t use gates that we support (e.g. like https://github.com/zapatacomputing/qe-qhipster/blob/419e36c373442582b8b94933332d54972e9507b8/tests/qeqhipster/simulator_test.py#L27=)


General intro
=============

- Why we have backend interface? @yogi
-- Make implementation easier
-- Make them interchangeable


Two types of backends
---------------------

``QuantumBackend`` is the base class for all backends. ``QuantumBackend``\ s are used for physical quantum hardware backends.

.. _quantum_simulator:

``QuantumSimulator`` is a subclass of ``QuantumBackend`` with added functionality that only simulators can provide, such as getting the wavefunction of a circuit and getting the exact expectation values.

For more information on how to use each type of backend please refer to the :ref:`section in this guide on various methods <backend_methods>` or to the :doc:`API documentation </api/quantum/api/backend/index>`.

Testing the Backends
--------------------

The `backend tests <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/api/backend_test.py>`_ cover both general behaviors we want to make sure the ``Backend``\ s follow and specific gate tests. For instance, a common "general behavior" test across multiple backends is the ``run_circuitset_and_measure`` test. Here are examples in the `Cirq tests <https://github.com/zapatacomputing/orquestra-cirq/blob/main/tests/orquestra/integrations/cirq/simulator/simulator_test.py#L52=>`_ and the `Qiskit tests <https://github.com/zapatacomputing/orquestra-qiskit/blob/main/tests/orquestra/integrations/qiskit/backend/backend_test.py#L162=>`_.

.. note::

    Because tests are often specific to their ``Backend``, there are only prototype backend tests in `orquestra-quantum <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/api/backend_test.py>`_. Implementations of these tests are in the integrations that house specific backends. Please refer to the section on :ref:`currently integrated backends <integrated_backends>` for a complete list of backends

For gates tests, the goal is to ensure it is properly implemented. @yogi I'm going to need some help here because all the examples I can find just say "pass" (https://github.com/zapatacomputing/orquestra-forest/blob/main/tests/orquestra/integrations/forest/simulator_test.py and https://github.com/zapatacomputing/orquestra-cirq/blob/main/tests/orquestra/integrations/cirq/simulator/simulator_test.py and https://github.com/zapatacomputing/orquestra-quantum/blob/main/tests/orquestra/quantum/symbolic_simulator_test.py and etc)

-- Also tests for gates – and why they are important (we can use the example of XY gate in various frameworks and their conventions. Or not ¯\_(ツ)_/¯)

.. _backend_methods:

In-depth dive in how various methods work, what's the default etc. @yogi make some examples in examples/backends_guide.py
================================================

- run_circuit_and_measure
-- Workhorse of the backends 
-- by default it increases job counts


- run_circuitset_and_measure
- get_measurement_outcome_distribution


Simulator ones:
- get_wavefunction
- get_exact_expectation_values
- get_measurement_outcome_distribution

Zapata's backends
=================

SymbolicSimulator
-----------------

Zapata's ``SymbolicSimulator`` is a type of :ref:`quantum simulator <quantum_simulator>` that's built specifically to allow for the evaluation of circuits with :ref:`symbolic gates <symbolic_gates>`. Because there is extra overhead to allow for this broader type of evaluation, ``SymbolicSimulator`` is not the most performant simulator, but it can be useful for deeply understanding small circuits.

The ``SymbolicSimulator`` can be used the same way any other simulator can be. To see more usage please refer to the :ref:`section in this guide on various methods <backend_methods>` or to the :doc:`API documentation </api/quantum/api/backend/index>`

TrackingBackend
---------------

TODO

.. _integrated_backends:

Currently integrated backends
=============================

Hardware backends
-----------------

* `QiskitBackend <https://github.com/zapatacomputing/orquestra-qiskit/blob/main/tests/orquestra/integrations/qiskit/backend/backend_test.py>`_

Simulators
----------

* `SymbolicSimulator <https://github.com/zapatacomputing/orquestra-quantum/blob/main/tests/orquestra/quantum/symbolic_simulator_test.py>`_
* `ForestSimulator <https://github.com/zapatacomputing/orquestra-forest/blob/main/tests/orquestra/integrations/forest/simulator_test.py>`_
* `CirqSimulator <https://github.com/zapatacomputing/orquestra-cirq/blob/main/tests/orquestra/integrations/cirq/simulator/simulator_test.py>`_
* `QiskitSimulator <https://github.com/zapatacomputing/orquestra-qiskit/blob/main/tests/orquestra/integrations/qiskit/simulator/simulator_test.py>`_ has multiple options

  * ``aer_simulator``
  * ``aer_simulator_statevector``

* `QulacsSimulator <https://github.com/zapatacomputing/orquestra-qulacs/blob/main/tests/orquestra/integrations/qulacs/simulator_test.py>`_


- Maybe some short pros&cons of each?
- GPU stuff as well I think? @yogi

Conversions to other frameworks
===============================

- cirq/pyquil/qiskit
- Mention that it's very fast - the overhead is neglibile, so you can do it back&forth and should be ok :)
- Please double check if we're not changing the values/signs for some gates, e.g. cause we're using different conventions (some gates are in the reverse order, inverted gates)
- If you want to use some specific features from particular framework (e.g. drawing circuits from qiskit) feel free to export/import and do it! super easy :)

How to integrate your own backend @yogi
=================================

- two sections, one for real hardware, one for simulators
-- hardware: credentials
-- simulators: direct

What to pay attention to, what comes out of the box, etc.




## Things I'm not sure where to put but we should put them somewhere:
- Example usage – here's how you change to use various backends.
- Maybe some simple benchmarking 3 backends?

NOTE:
- Refactoring backends is on our radar, though it will probably take us some time before we can do this.