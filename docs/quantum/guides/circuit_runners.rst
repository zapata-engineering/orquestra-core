.. _circuit_runners_guide:

=====================
Circuit Runners Guide
=====================

Circuit runners are objects used to run :ref:`Circuits <circuits_guide>` in Orquestra Core. In this guide we'll cover differences between types of circuit runners (generic ``CircuitRunner`` vs ``WavefunctionSimulator``), how to use circuit runners, currently available runners, and creating your own runner (among other topics).


General Circuit Runner Information
==================================

The purpose of a circuit runner is to send instructions to quantum hardware or to a simulator. Since there are various types of quantum hardware and simulators, different sets of instructions need to be written and it can become complex. The :class:`CircuitRunner <orquestra.quantum.api.circuit_runner.CircuitRunner>` interface is an abstraction of object capable of running quantum circuits. For simulators capable of computing whole wavefunction, even richer abstraction :class:`WavefunctionSimulator <orquestra.quantum.api.wavefunction_simulator.WavefunctionSimulator>` is available. Different implementations of :class:`CircuitRunner` are (on the interface level) interchangeable, and thus the user can write their code in a hardware/simulator independent way. Therefore, executing code on various devices becomes easier and more manageable.

CircuitRunner and WavefunctionSimulator
---------------------------------------

:class:`CircuitRunner <orquestra.quantum.api.circuit_runner.CircuitRunner>` is a basic protocol for every class representing circuit runner. :class:`CircuitRunner <orquestra.quantum.api.circuit_runner.CircuitRunner>` s can be used for physical quantum hardware backends as well as shots simulators.

Most often, :class:`CircuitRunner <orquestra.quantum.api.circuit_runner.CircuitRunner>`\s connect to a third-party service to run circuits remotely. The details of how this interaction is performed depends mostly on the parameters used for initializing runner.  For instance, to create runner using IBMQ backend it is necessary to specify API token and backend name:

.. literalinclude:: ../examples/guides/circuit_runners_guide.py
  :start-after: # IBMQ runner creation example
  :end-before: # End IBMQ runner creation example

.. _wavefunction_simulators:

:class:`WavefunctionSimulator <orquestra.quantum.api.wavefunction_simulator.WavefunctionSimulator>` is a special case of ``CircuitRunner``. Runners implementing this protocol can compute coefficients of the wavefunction and exact expectation values. Similarly to other `CircuitRunner``\ s, ``WavefunctionSimulator``\ s may require some parameters to be passed during their initialization.

.. literalinclude:: ../examples/guides/circuit_runners_guide.py
  :start-after: # WavefunctionSimulator creation example
  :end-before: # End WavefunctionSimulator creation example

For more information on how to use each type of circuit runner please refer to the :ref:`section in this guide on various methods <circuit_runner_methods>` or to the :doc:`API documentation </api/orquestra/quantum/api/circuit_runner/index>`.

.. _circuit_runner_methods:

CircuitRunner and WavefunctionSimulator Methods Usage
======================================================

We will demonstrate usage of ``CircuitRunner`` and ``WavefunctionSimulator`` on the example of ``QiskitRunner`` and its extension, ``QiskitWavefunctionSimulator``. The ``QiskitRunner`` class can be used, in principle, with an arbitrary Qiskit backend. In particular, one may use ``IBMQBackend`` for running code on the real hardware. Since creating this backend is more involved, a convenience function ``create_ibmq_runner`` is provided to ease this process. We need to provide an API token used for authentication and an IBMQ device name to be used. Optionally, we might tweak other parameters, such as number of seconds waited between retries.

.. literalinclude:: ../examples/guides/circuit_runners_guide.py
  :start-after: # IBMQ runner creation example
  :end-before: # End IBMQ runner creation example

For an example of direct construction of `QiskitRunner`, we will just wrap an `Aer backend <https://qiskit.org/documentation/tutorials/simulators/1_aer_provider.html#The-Aer-Simulator>`. In a similar fashion, one can construct a ``WavefunctionSimulator``, provided that the passed backend supports computing state vector.

.. literalinclude:: ../examples/guides/circuit_runners_guide.py
  :start-after: # Example Qiskit options
  :end-before: # End WavefunctionSimulator creation example


General CircuitRunner methods
-----------------------------

Once the initialization is done, we can send the ``Circuit`` and number of repetitions to the runner and read the measurements. For more information on creating circuits to send to a circuit runner, refer to the :ref:`Circuits Guide <circuits_guide>`. For a single circuit, that looks like this:

.. literalinclude:: ../examples/guides/circuit_runners_guide.py
  :start-after: # CircuitRunner run and measure circuit
  :end-before: # End CircuitRunner run and measure circuit

If you want to run a batch of multiple circuits, possibly with different number of samples, the code needs to be modified as follows:

.. literalinclude:: ../examples/guides/circuit_runners_guide.py
  :start-after: # CircuitRunner run batch and measure
  :end-before: # End CircuitRunner run batch and measure

``CircuitRunner`` can also provide the distribution of the outcome measurement. It can be extracted using the following approach:

.. literalinclude:: ../examples/guides/circuit_runners_guide.py
  :start-after: # CircuitRunner measurement distribution
  :end-before: # End CircuitRunner measurement distribution

Notice that in all instances, ``CircuitRunner`` automatically adds the measurement operators to the circuit. Therefore, the user is not required to include them in the circuit.

WavefunctionSimulator-specific methods
--------------------------------------

``WavefunctionSimulator`` can be used to extract a wave function and expectation value for a given circuit (or circuit and operator). Below is an example of extracting these values using a ``WavefunctionSimulator`` called :class:`CirqSimulator <orquestra.integrations.cirq.simulator.CirqSimulator>`:

.. literalinclude:: ../examples/guides/circuit_runners_guide.py
  :start-after: # WavefunctionSimulator examples
  :end-before: # End WavefunctionSimulator examples

**Noise Models** can be used on certain simulators (like Qiskit and QSim) to help evaluate a circuit's performance under noisy conditions. For more details how to use that feature, please refer to docs for particular simulator. Note that currently Orquestra does not provide a single abstraction of noise model compatible across multiple runners/simulators.

Zapata's circuit runners
========================

SymbolicSimulator
-----------------

Zapata's :class:`SymbolicSimulator <orquestra.quantum.runners.symbolic_simulator.SymbolicSimulator>` is a type of :ref:`quantum simulator <wavefunction_simulators>` that's built specifically to allow for the evaluation of circuits with :ref:`symbolic gates <symbolic_gates>`. Because there is extra overhead to allow for this broader type of evaluation, :class:`SymbolicSimulator <orquestra.quantum.runners.symbolic_simulator.SymbolicSimulator>` is not the most performant simulator, but it can be useful for deeply understanding small circuits. Additionally, it doesn't require any extra dependencies (apart from ``orquestra-quantum``), making it useful for testing purposes and as a reference implementation of the ``WavefunctionSimulator``.

The :class:`SymbolicSimulator <orquestra.quantum.runners.symbolic_simulator.SymbolicSimulator>` can be used the same way any other simulator can be. To see more usage please refer to the :ref:`section in this guide on various methods <circuit_runner_methods>` or to the :doc:`API documentation </api/orquestra/quantum/api/wavefunction_simulator/index>`

``MeasurementTrackingBackend``
------------------------------

A :class:`MeasurementTrackingBackend <orquestra.quantum.runners.trackers.MeasurementTrackingBackend>` is a circuit runner that tracks and stores data about each run of a circuit. This is accomplished by wrapping pre-existing runner in a :class:`MeasurementTrackingBackend <orquestra.quantum.runners.trackers.MeasurementTrackingBackend>` from :doc:`orquestra.quantum.trackers </api/orquestra/quantum/runners/trackers/index>`.

When :meth:`run_and_measure <orquestra.quantum.api.circuit_runner.CircuitRunner.run_and_measure>` is called, the tracking backend stores the ``data_type`` received from the call (usually a measurement outcome distribution), the wrapped device, the circuit which was run, the distribution of bitstrings which was received, the number of gates in the circuit, and the number of shots run in a JSON file. This is useful when you are paying to run circuits on a machine and you want to be able to re-use the data for different computations.

To create a :class:`MeasurementTrackingBackend <orquestra.quantum.runners.trackers.MeasurementTrackingBackend>` it must be initialized with a runner to be wrapped around, a name for the file you are storing the data in, and an optional boolean indicating whether or not the individual bitstrings should be saved (defaults to `False`)

.. literalinclude:: ../examples/guides/circuit_runners_guide.py
  :start-after: # TrackingBackend creation example
  :end-before: # End TrackingBackend creation example

.. caution::

  If all the bitstrings are saved, it will greatly increase the size of the produced JSON file.

To use the :class:`MeasurementTrackingBackend <orquestra.quantum.runners.trackers.MeasurementTrackingBackend>` you can call :meth:`run_and_measure <orquestra.quantum.api.circuit_runner.CircuitRunner.run_and_measure>` or :meth:`run_batch_and_measure <orquestra.quantum.api.circuit_runner.CircuitRunner.run_batch_and_measure>` :ref:`just like with all other CircuitRunners <circuit_runner_methods>`. There is also the option to manually append measurement information to the data in a :class:`MeasurementTrackingBackend <orquestra.quantum.runners.trackers.MeasurementTrackingBackend>` using :meth:`record_raw_measurement_data <<orquestra.quantum.runners.trackers.MeasurementTrackingBackend.record_raw_measurement_data>`. This is usually not necessary, but if your use case requires it, please see the :doc:`API documentation </api/orquestra/quantum/runners/trackers/index>` for more information.

For more examples of using the :class:`MeasurementTrackingBackend <orquestra.quantum.runners.trackers.MeasurementTrackingBackend>`, refer to the `tracking backend tests <https://github.com/zapatacomputing/orquestra-quantum/blob/main/tests/orquestra/quantum/trackers_test.py>`_

.. _integrated_circuit_runners:

Currently integrated backends
=============================

Hardware backends
-----------------


.. list-table::

  * - :class:`QiskitRunner <orquestra.integrations.qiskit.runner.QiskitRunner>`
    - Can wrap any Qiskit backend, including ones using physical hardware.
  * - :class:`create_ibmq_runner <orquestra.integrations.qiskit.runner.create_ibmq_runner>`
    - Runner for `IBM Quantum <https://quantum-computing.ibm.com/>`_.
  * - :class:`aws_runner <orquestra.integrations.braket.runner.aws_runner>`
    - Runner for `Amazon Braket <https://aws.amazon.com/braket/>`_.

Simulators
----------

.. list-table::

  * - :class:`SymbolicSimulator <orquestra.quantum.runners.symbolic_simulator.SymbolicSimulator>`
    - Built-in simulator providing by the Orquestra Quantum SDK for simulating small circuits. 
  * - :class:`CirqSimulator <orquestra.integrations.cirq.simulator.CirqSimulator>`
    - Integration with the `Cirq simulator <https://quantumai.google/cirq/simulate/simulation>`_.
  * - :class:`QiskitWavefunctionSimulator <orquestra.integrations.qiskit.simulator._qiskit_wavefunction_simulator.QiskitWavefunctionSimulator>`
    - Can wrap any Qiskit backend supporting ``save_statevector`` instruction.
  * - :class:`QulacsSimulator <orquestra.integrations.qulacs.simulator.QulacsSimulator>`
    - Integration with the `Qulacs simulator <https://github.com/qulacs/qulacs>`_.
  * - :class:`QSimSimulator <orquestra.integrations.cirq.simulator._qsim_simulator.QSimSimulator>`
    - Integration with the `qsim simulator <https://github.com/quantumlib/qsim>`_.
  * - :class:`CuStateVecSimulator <orquestra.integrations.custatevec.simulator.CuStateVecSimulator>`
    - A simulator for running circuits on a GPU using Nvidia's `CuStateVec library <https://docs.nvidia.com/cuda/cuquantum/custatevec/>`_.
  * - :class:`braket_local_simulator <orquestra.integrations.braket.simulator.braket_local_simulator>`
    - Function for initializing Braket's local simulator.

Conversions to other frameworks
===============================

The integrations Orquestra Core has with :ref:`many other frameworks <orq_core_structure>` not only allows for running on Orquestra-supported backends, but also allows for converting circuits to and from those frameworks.

There are slightly different ways to import the conversions from the integrations for different frameworks, so here's examples for all of them:

.. literalinclude:: ../examples/guides/circuit_runners_guide.py
  :start-after: # Importing and Exporting with different frameworks
  :end-before: # end importing/exporting examples

If you want to use some specific features from a particular framework (e.g. drawing circuits from qiskit) feel free to export/import and do it! Examples of using the import and export functions for this purpose can be found in the :ref:`getting started tutorial <beginner_translating_circuits>`.


How to create your own CircuitRunner
====================================

We have a very simple way of creating new implementations of ``CircuitRunner`` protocol. Before you start working on one, you need to answer the following questions:

* Will my runner use external, already existing backend/simulator/service?
   * If so, what kind of circuits does this third-party software/hardware use? Is there already a function that can convert Orquestra circuit to the one native for the service we are integrating with?

We will further assume that the runner being created will use an existing shots based simulator that uses circuits in some format that is not native to Orquestra. Furthermore, we assume that there exist no conversion routine between Orquestra and the circuits needed for our backend. However, if any of those assumptions do not hold, your job does not get more complicated and it should be trivial to adapt the below example to your use case.

First you need to create a function that can translate circuits between your library and `Orquestra's circuits <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/circuits/_circuit.py>`_. Once that's done, you need to create an actual class implementing ``CircuitRunner`` protocol. However, it doesn't have to be that hard! In most cases, it is sufficient to inherit a ``BaseCircuitRunner`` class and implement its ``_run_and_measure(circuit, n_samples)`` method.

Here is an example of a (fake) simulator integrated using this process:

.. literalinclude:: ../examples/guides/circuit_runners_guide.py
  :start-after: # Inherit BaseCircuitRunner
  :end-before: # End Inherit BaseCircuitRunner

Testing the Circuit Runners
---------------------------

One of our goals with the ``CircuitRunner``\ s and ``WavefunctionSimulator``\ s was to make sure that all implementations of a given protocol behave in a uniform way. In order to ensure that, we have developed a common suite of tests which all runners and simulators need to pass. Those tests are implemented in the form of *contracts*, i.e. collections of boolean functions accepting runner as a single argument. A runner (or wavefunction simulator) is said to fulfill given contract iff for this runner it evaluates to ``True``. Contracts can be used to effortlessly construct tests for your new runner, but they have additional purpose. They document properties of a given protocols that cannot be captured via type system. For instance, suppose you run a 5-qubit circuit using some runner.  Independently of runner used, you expected returned measurements ot have samples of length 5, right? This requirement is uncapturable by the type system, but there's' a contract that ensures that.

.. note::

   Contracts are great when you are developing your own ``CircuitRunner`` or a ``WavefunctionSimulator``. However, if you are only using the existing ones, you probably won't need to look too much into the contracts.

Let's first discuss contracts for a generic ``CircuitRunner``,
`residing here <https://github.com/zapatacomputing/orquestra-quantum/blob/main/src/orquestra/quantum/api/circuit_runner_contracts.py>`_. The basic mandatory contracts are called ``CIRCUIT_RUNNER_CONTRACTS``, to be a valid implementation of ``CircuitRunner``, an object has to pass all of the contracts in this list. Another list of contracts, ``STRICT_CIRCUIT_RUNNER_CONTRACTS``, is designed for runners that guarantee that number of samples they return is the same as the requested number (in general, backends need to return *at least* as many samples as requested).

For ``WavefunctionSimulator``\s the situation is (slightly) more complicated. Some contracts ensure that the computed wavefunction is correct we cannot just compare the computed wavefunction to the expected one and expect an exact equality. That's because we are using floating point numbers. Furthermore, some simulators may trade off precision for performance. which also excludes possibility of exact comparison. Since the precision is always simulator-dependent, the contract tests for ``WavefunctionSimulator``\s are parametrized with absolute tolerance value (*atol*).

The first, mandatory list of for all ``WavefunctionSimulators`` is constructed by calling ``simulator_contracts_for_tolerance(atol=some_tolerance)`` function, with the default for ``atol`` being 1e-7. For simulators capable of starting from an arbitrary initial state, you should also include contracts returned by the ``simulator_contracts_with_nontrivial_initial_state`` function.

Lastly, there are some lists of contracts ensuring that our runners use definitions of quantum gates compatible with rest of the Orquestra. While most libraries agree on the definition of most gates, there might be some differences. For instance, angles in rotations may differ by the factor of 2, or the order of qubits in two-qubit gates may be reversed. To ensure that runners use the compatible definition of gates, we first construct vast family of circuits (such that given gate appears in multiple circuits) and some set of operators. We choose the operators so that their expected value is easy to compute by hand. By sampling the circuits and comparing computed expectation values, we may judge if the gates that we think we submitted match the ones that were actually executed. Additionally, for ``WavefunctionSimulator``\s, we may just compute the wavefunction instead of computing expectation values. The functions for constructing gate compatibility contracts are called ``circuit_runner_gate_compatibility_contracts`` and ``simulator_gate_compatibility_contracts``.

.. note::

  Simulator gate compatibility tests *DO NOT* replace circuit runner gate compatibility tests. If you are implementing a ``WavefunctionSimulator``, you should make sure both lists of contracts are satisfied.

.. caution::

  Contracts checking gate compatibility require running many circuits with large numbers of samples. Thus, they might incur large penalty hit and additional costs if the third party service you are integrating is paid. Be mindful of that, and if needed implement flag in your tests to allow you for skipping the gate compatibility contracts for quick unit tests.
