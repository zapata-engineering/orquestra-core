=============================
Running Circuits on a Backend
=============================

.. _running_circuits:

If you haven't gone through the :ref:`creating circuits <creating_circuits>` tutorial, do that first because we'll be using the circuit from that tutorial in this one.

Once we have our circuit, the next step is to select what backend to run on and get our measurements. For this run, let's use Qiskit's aer simulator with 100 shots:

.. literalinclude:: /examples/bell_state.py
    :language: python
    :start-at: simulator = QiskitSimulator("aer_simulator")
    :end-at: ic(measurements.get_counts())

It's actually very easy to switch out backends thanks to Orquestra Core's interfaces. Let's say instead of the QiskitSimulator, we want to use Zapata's very own SymbolicSimulator. We can do that by changing just part of one line:

.. literalinclude:: /examples/bell_state.py
    :language: python
    :start-at: sym_simulator = SymbolicSimulator()
    :end-at: ic(measurements3.get_counts())

.. _running_amplitudes:

If we want to get the amplitudes from the wavefunction instead of running measurements, we can do that as well:

.. literalinclude:: /examples/bell_state.py
    :language: python
    :start-at: sv_simulator = QiskitSimulator("aer_simulator_statevector")
    :end-at: ic(wavefunction.amplitudes)

We can also get an expectation value for the circuit given an operator we want to use:

.. literalinclude:: /examples/bell_state.py
    :language: python
    :start-at: ising = 
    :end-at: ic(evals[0].values)

For a full list of backends you can run your circuits on, check :ref:`this page <backends>`