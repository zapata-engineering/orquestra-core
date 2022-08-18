.. _backends_guide:

==============
Backends guide
==============

Backends are the interfaces used to run :ref:`Circuits <circuits_guide>` in Orquestra Core. In this guide we'll cover differences between types of backends (``QuantumBackend`` vs ``QuantumSimulator``), how to use backends, currently integrated backends, and creating your own backend (among other topics).


General Backend Information
===========================

The function of a backend is to send instructions to quantum hardware or to a simulator. Since there are various types of quantum hardware and simulators, different sets of instructions needs to be written and it can become complex. ``QuantumBackend`` simplifies this process by enabling the user to deploy a single set of instructions on multiple hardware and simulators simultaneously. Therefore executing code on various devices becomes easier and more manageable.

Two types of backends
---------------------

``QuantumBackend`` is the base class for all backends. ``QuantumBackend``\ s can be used for physical quantum hardware backends as well as simulators.

Because ``QuantumBackend``\ s connect to a cloud provider to run remote circuits, it is necessary to specify which device you want to connect to. For example, the ``QiskitBackend`` takes in a ``device_name`` string:

.. literalinclude:: ../examples/backends_guide.py
  :start-after: # QuantumBackend creation example
  :end-before: # End QuantumBackend creation example

.. _quantum_simulator:

``QuantumSimulator`` is a subclass of ``QuantumBackend`` with added functionality that only simulators can provide, such as getting the wavefunction of a circuit and getting exact expectation values. Unlike ``QuantumBackend``\ s, ``QuantumSimulator``\ s usually do not require a ``device_name`` parameter. One exception to this rule is the ``QiskitSimulator``, which has :ref:`multiple options <integrated_backends>`:

.. literalinclude:: ../examples/backends_guide.py
  :start-after: # QuantumSimulator creation example
  :end-before: # End QuantumSimulator creation example

For more information on how to use each type of backend please refer to the :ref:`section in this guide on various methods <backend_methods>` or to the :doc:`API documentation </api/quantum/api/backend/index>`.

.. _backend_methods:

Backend Methods Usage
=====================

In order to use quantum hardware, the user must use the backend's authentication method to prove that they have the right credentials to send instruction to the hardware. The authentication method is specified by the hardware provider. Providing authentication credentials is the first step in using ``QuantumBackend``. Below is an example of using IBM's hardware through ``QiskitBackend``.

``QuantumSimulator``\ s run in your own environment and therefore can be used without needing authentication credentials.

.. literalinclude:: ../examples/backends_guide.py
  :start-after: # QuantumBackend creation example
  :end-before: # End QuantumBackend creation example

General Backend Methods
-----------------------

After intializing the backend we can send the ``Circuit`` and number of repetitions to the backend and read the measurement. For more information on creating circuits to send to a backend, refer to the :ref:`Circuits Guide <circuits_guide>`. For a single circuit, that looks like this:

.. literalinclude:: ../examples/backends_guide.py
  :start-after: # QuantumBackend run and measure circuit
  :end-before: # End QuantumBackend run and measure circuit

If you want to run multiple circuits with different number of samples, the code needs to be modified as follows:

.. literalinclude:: ../examples/backends_guide.py
  :start-after: # QuantumBackend run and measure circuitset
  :end-before: # End QuantumBackend run and measure circuitset

``QuantumBackend`` can also provide the distribution of the outcome measurement. It can be extracted using the following approach:

.. literalinclude:: ../examples/backends_guide.py
  :start-after: # Quantumbackend measurement distribution
  :end-before: # End Quantumbackend measurement distribution

In all instances, ``QuantumBackend`` automatically adds the measurement operators to the circuit. Therefore, the user is not required to include it in the circuit.

Simulator-specific methods
--------------------------

``QuantumSimulator`` can be used to extract a wave function and expectation value for a given circuit (or circuit and operator). Below is an example of extracting these values using a ``QuantumSimulator`` called ``CirqSimulator``:

.. literalinclude:: ../examples/backends_guide.py
  :start-after: # Quantumsimulator examples
  :end-before: # End Quantumsimulator examples

**Noise Models** can be used on certain simulators (like Qiskit and QSim) to help evaluate a circuit's performance under noisy conditions. For more details how to use that, please refer to docs for particular simulator.

Zapata's backends
=================

SymbolicSimulator
-----------------

Zapata's ``SymbolicSimulator`` is a type of :ref:`quantum simulator <quantum_simulator>` that's built specifically to allow for the evaluation of circuits with :ref:`symbolic gates <symbolic_gates>`. Because there is extra overhead to allow for this broader type of evaluation, ``SymbolicSimulator`` is not the most performant simulator, but it can be useful for deeply understanding small circuits. Additionally, it doesn't require any extra dependencies (apart from ``orquestra-quantum``), making it useful for testing purposes.

The ``SymbolicSimulator`` can be used the same way any other simulator can be. To see more usage please refer to the :ref:`section in this guide on various methods <backend_methods>` or to the :doc:`API documentation </api/quantum/api/backend/index>`

``MeasurementTrackingBackend``
------------------------------

A ``MeasurementTrackingBackend`` is a backend that tracks and stores data about each run of a circuit. This is accomplished by wrapping pre-existing backends in a ``MeasurementTrackingBackend`` from :doc:`orquestra.quantum.trackers </api/quantum/trackers/index>`.

When ``run_circuit_and_measure`` is called, the tracking backend stores the ``data_type`` received from the call (usually a measurement outcome distribution), the wrapped device, the circuit which was run, the distribution of bitstrings which was received, the number of gates in the circuit, and the number of shots run in a JSON file. This is useful when you are paying to run circuits on a machine and you want to be able to re-use the data for different computations.

To create a ``MeasurementTrackingBackend`` it must be initialized with a backend to be wrapped around, a name for the file you are storing the data in, and an optional boolean indicating whether or not the individual bitstrings should be saved (defaults to `False`)

.. literalinclude:: ../examples/backends_guide.py
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
* `QSimSimulator <https://github.com/zapatacomputing/orquestra-cirq/blob/main/tests/orquestra/integrations/cirq/simulator/qsimsimulator_test.py>`_
* `CuStateVecSimulator <https://github.com/zapatacomputing/orquestra-cirq/tree/main/src/orquestra/integrations/custatevec/simulator>`_

Conversions to other frameworks
===============================

The integrations Orquestra Core has with :ref:`many other frameworks <orq_core_structure>` not only allows for running on Orquestra-supported backends, but also allows for converting circuits to and from those frameworks. This process is very fast so converting to and from different frameworks can be done multiple times with negligible overhead.

There are slightly different ways to import the conversions from the integrations for different frameworks, so here's examples for all of them:

.. literalinclude:: ../examples/backends_guide.py
  :start-after: # Importng and Exporting with different frameworks
  :end-before: # end importing/exporting examples

If you want to use some specific features from a particular framework (e.g. drawing circuits from qiskit) feel free to export/import and do it! Examples of using the import and export functions for this purpose can be found in the :ref:`getting started tutorial <beginner_translating_circuits>`.


How to integrate your own backend
=================================

We have simplified the process of integrating any simulator into Orquestra Core. First you need to create a function that can translate gates between your library and `Orquestra's gates <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/circuits/_builtin_gates.py>`_. Then create a class method that inherits from ``QuantumSimulator`` and overrides the needed abstract methods (like ``run_circuit_and_measure``). In order for integration to work properly, the signature of all the methods needs to be exactly the same as in the abstract class. If your simulator requires some extra arguments (e.g. whether to use a noise model), please provide it in the ``__init__`` method.

Here is an example of a (fake) simulator integrated using this process:

.. literalinclude:: ../examples/backends_guide.py
  :start-after: # Inherit QuantumSimulator
  :end-before: # End Inherit QuantumSimulator


If you have credentials to access hardware, you can provide this to ``QuantumBackend`` when you initialize it. The process might vary between each backend. Check the ``QuantumBackend`` documentation for your hardware to find the credentials it accepts. If no credentials were provided, ``QuantumBackend`` will fail when you try to execute a function as you do not have permission to access the hardware. ``QuantumSimulator``\ s do not require any credentials as they are executed on a local environment.

Testing the Backends
--------------------

One of our goals with the ``QuantumBackend``\ s was to make sure that all the backends behave in a uniform way. In order to ensure that, we have developed a suite of tests which all backends need to pass.

.. note::

  This suite of tests is needed when integrating your own backend, but to just use already-integrated backends the end user likely won't need to directly work with these tests.

The `backend tests <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/api/backend_test.py>`_ cover both general behaviors we want to make sure the ``Backend``\ s follow and specific gate tests. For instance, a common "general behavior" test across multiple backends is the ``run_circuitset_and_measure`` test. Here are examples in the `Cirq tests <https://github.com/zapatacomputing/orquestra-cirq/blob/main/tests/orquestra/integrations/cirq/simulator/simulator_test.py#L52=>`_ and the `Qiskit tests <https://github.com/zapatacomputing/orquestra-qiskit/blob/main/tests/orquestra/integrations/qiskit/backend/backend_test.py#L162=>`_.

.. note::

    Because tests are often specific to their ``Backend``, there are only prototype backend tests in `orquestra-quantum <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/api/backend_test.py>`_. Implementations of these tests are in the integrations that house specific backends. Please refer to the section on :ref:`currently integrated backends <integrated_backends>` for a complete list of backends

For gates tests, the goal is to ensure gates are properly implemented. Sometimes gate operations in certain simulators are in reverse order (compared to Orquestra Core and other frameworks). When you use a gate operation in Orquestra, it's important to make sure it's represented correctly in the simulator and/or backend. In order to do that, Orquestra Core has a `suite of gate operations <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/testing/test_cases_for_backend_tests.py>`_ that should be tested on each backend and simulator. This is done with `QuantumBackendGateTests <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/api/backend_test.py#L193=>`_ and `QuantumSimulatorGateTests <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/api/backend_test.py#L432=>`_

.. TODO: updating the link to the backend test excluding RH gates to braket when public

There is also the case where a certain backend doesn't use some gates that we support. When this happens, in the backend test, a list of excluded gates will be used in the ``QuantumSimulatorGatesTest`` like in `TestCirqSimulatorGates <https://github.com/zapatacomputing/orquestra-cirq/blob/main/tests/orquestra/integrations/cirq/simulator/simulator_test.py#L147>`_. For example, that might look something like this:

.. code-block:: python

  class TestCirqSimulatorGates(QuantumSimulatorGatesTest):
      gates_to_exclude = ["RH"]
      pass

.. NOTE: Refactoring backends is on our radar, though it will probably take us some time before we can do this.

.. TODO: add information on benchmarking backends once that functionality is implemented