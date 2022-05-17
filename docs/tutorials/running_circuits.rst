=======================
Running Circuits on a Backend
=======================

If you haven't gone through the [creating circuits](INSERT LINK HERE) tutorial, do that first because we'll be using the circuit from that tutorial in this one.

Once we have our circuit, the next step is to select what backend to run on and get our measurements. For this run, let's use Qiskit's aer simulator with 100 shots:

.. literalinclude:: /examples/bell_state.py
    :language: python
    :start-at: simulator = QiskitSimulator("aer_simulator")
    :end-at: print(measurements.get_counts())

It's actually very easy to switch out backends thanks to Orquestra Core's interfaces. Let's say instead of the QiskitSimulator, we want to use Zapata's very own SymbolicSimulator. We can do that by changing just part of one line:

.. literalinclude:: /examples/bell_state.py
    :language: python
    :start-at: sym_simulator = SymbolicSimulator()
    :end-at: print(measurements3.get_counts())

If we want to get the amplitudes from the wavefunction instead of running measurements, we can do that as well:

.. literalinclude:: /examples/bell_state.py
    :language: python
    :start-at: sv_simulator = QiskitSimulator("aer_simulator_statevector")
    :end-at: print(wavefunction.amplitudes)

For a full list of backends you can run your circuits on, check [this](LINK) out (Do we want to do this??)