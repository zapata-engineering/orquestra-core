.. _backends_guide:

==============
Backends guide
==============

Backends are the interfaces used to run :ref:`Circuits <circuits_guide>` in Orquestra Core. In this guide we'll cover differences between types of backends (``QuantumBackend`` vs ``QuantumSimulator``, ``TrackingBackend``, ``SymbolicSimulator``), how to use backends, currently integrated backends, and creating your own backend (among other topics).


General Backend Information
===========================

- Why we have backend interface? @yogi
-- Make implementation easier
-- Make them interchangeable


Two types of backends
---------------------

``QuantumBackend`` is the base class for all backends. ``QuantumBackend``\ s are used for physical quantum hardware backends.

Because ``QuantumBackend``\ s connect to a cloud provider to run remote circuits, it is necessary to specify which device you want to connect to. For example, the ``QiskitBackend`` takes in a ``device_name`` string:

.. literalinclude:: /examples/backends_guide.py
  :start-after: # QuantumBackend creation example
  :end-before: # End QuantumBackend creation example

.. _quantum_simulator:

``QuantumSimulator`` is a subclass of ``QuantumBackend`` with added functionality that only simulators can provide, such as getting the wavefunction of a circuit and getting exact expectation values. Unlike ``QuantumBackend``\ s, ``QuantumSimulator``\ s usually do not require a ``device_name`` parameter. One exception to this rule is the ``QiskitSimulator``, which has :ref:`multiple options <integrated_backends>`:

.. literalinclude:: /examples/backends_guide.py
  :start-after: # QuantumSimulator creation example
  :end-before: # End QuantumSimulator creation example

For more information on how to use each type of backend please refer to the :ref:`section in this guide on various methods <backend_methods>` or to the :doc:`API documentation </api/quantum/api/backend/index>`.

Testing the Backends
--------------------

The `backend tests <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/api/backend_test.py>`_ cover both general behaviors we want to make sure the ``Backend``\ s follow and specific gate tests. For instance, a common "general behavior" test across multiple backends is the ``run_circuitset_and_measure`` test. Here are examples in the `Cirq tests <https://github.com/zapatacomputing/orquestra-cirq/blob/main/tests/orquestra/integrations/cirq/simulator/simulator_test.py#L52=>`_ and the `Qiskit tests <https://github.com/zapatacomputing/orquestra-qiskit/blob/main/tests/orquestra/integrations/qiskit/backend/backend_test.py#L162=>`_.

.. note::

    Because tests are often specific to their ``Backend``, there are only prototype backend tests in `orquestra-quantum <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/api/backend_test.py>`_. Implementations of these tests are in the integrations that house specific backends. Please refer to the section on :ref:`currently integrated backends <integrated_backends>` for a complete list of backends

For gates tests, the goal is to ensure gates are properly implemented. Sometimes gate operations in certain simulators are in reverse order (compared to Orquestra Core and other frameworks). When you use a gate operation in Orquestra, it's important to make sure it's represented correctly in the simulator and/or backend. In order to do that, Orquestra Core has a `suite of gate operations <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/testing/test_cases_for_backend_tests.py>`_ that should be tested on each backend and simulator. This is done with `QuantumBackendGateTests <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/api/backend_test.py#L193=>`_ and `QuantumSimulatorGateTests <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/api/backend_test.py#L432=>`_

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

A ``TrackingBackend`` is a backend that tracks and stores data about each run of a circuit. This is accomplished by wrapping pre-existing backends in a ``TrackingBackend``. Currently the ``MeasurementTrackingBackend`` in :doc:`orquestra.quantum.trackers </api/quantum/trackers/index>` is the only implemented ``TrackingBackend``

When ``run_circuit_and_measure`` is called, the tracking backend stores the ``data_type`` recieved from the call (usually a measurement outcome distribution), the wrapped device, the circuit which was run, the disribution of bitstrings which was recieved, the number of gates in the circuit, and the number of shots run in a JSON file. This is useful when you are paying to run circuits on a machine and you want to be able to re-use the data in a different workflow.

To create a ``MeasurementTrackingBackend`` it must be initialized with a backend to be wrapped around, a name for the file you are storing the data in, and a boolean indicating whether or not the individual bitstrings should be saved. 

.. literalinclude:: /examples/backends_guide.py
  :start-after: # TrackingBackend creation example
  :end-before: # End TrackingBackend creation example

.. caution:: 
  
  If all the bitstrings are saved, it will greatly increase the size of the produced JSON file.

To use the ``MeasurementTrackingBackend`` you can call ``run_circuit_and_measure`` or ``run_circuitset_and_measure`` :ref:`just like with all other QuantumBackends <backend_methods>`. There is also the option to manually append measurement information to the data in a ``MeasurementTrackingBackend`` using ``record_raw_measurement_data``. This is not usually necessary, but if your use case requires it, please see the :doc:`API documentation </api/quantum/trackers/index>` for more information. 

For more examples of using the ``MeasurementTrackingBackend``, refer to the `tracking backend tests <https://github.com/zapatacomputing/orquestra-quantum/blob/main/tests/orquestra/quantum/trackers_test.py>`_

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


- GPU stuff as well I think? @yogi

Conversions to other frameworks
===============================

The integrations Orquestra Core has with :ref:`many other frameworks <orq_core_structure>` not only allows for running on Orquestra-supported backends, but also allows for converting circuits to and from those frameworks. This process is very fast so converting to and from different frameworks can be done multiple times with negligible overhead.

There are slightly different ways to import the conversions from the integrations for different frameworks, so here's examples for all of them:

.. literalinclude:: /examples/backends_guide.py
  :start-after: # Importng and Exporting with different frameworks
  :end-before: # end importing/exporting examples

If you want to use some specific features from a particular framework (e.g. drawing circuits from qiskit) feel free to export/import and do it! Examples of using the import and export functions for this purpose can be found in the :ref:`getting started tutorial <beginner_translating_circuits>`.

- Please double check if we're not changing the values/signs for some gates, e.g. cause we're using different conventions (some gates are in the reverse order, inverted gates) @yogi you said you might know what this is about? (@yogi to ask Michal on monday morning)

How to integrate your own backend @yogi
=================================

- two sections, one for real hardware, one for simulators
-- hardware: credentials
-- simulators: direct

What to pay attention to, what comes out of the box, etc.




## Things I'm not sure where to put but we should put them somewhere:
- Example usage – here's how you change to use various backends.
- Maybe some simple benchmarking 3 backends?  (from ethan: my vote is hold off on this until we actually have benchmarking tooling)
- info on what to do in case where given backend doesn’t use gates that we support (e.g. like https://github.com/zapatacomputing/qe-qhipster/blob/419e36c373442582b8b94933332d54972e9507b8/tests/qeqhipster/simulator_test.py#L27=)

NOTE:
- Refactoring backends is on our radar, though it will probably take us some time before we can do this.