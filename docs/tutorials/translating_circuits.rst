=======================
Translating Circuits between Libraries
================================================================

If you haven't done the [running circuits tutorial](INSERT LINK HERE), you should do that tutorial first because we'll use the python file from it in this tutorial

Now that we've got this bell state, let's say we want to change it a bit so that instead of the state

.. math::
    | \phi^+ \rangle = \frac{1}{\sqrt{2}}( |00\rangle + |11\rangle )

We instead get the state

.. math::
    | \psi^+ \rangle = \frac{1}{\sqrt{2}}( |01\rangle + |10\rangle )

But we want to do it by editing the circuit in Qiskit, and then visualizing the circuit in Cirq (because why not?) Lucky for us, Orquestra Core allows us to do that readily!

First, we can translate our existing circuit from the current Orquestra Core representation into its Qiskit representation and add an ``X`` gate to the second qubit in Qiskit:

.. literalinclude:: /examples/bell_state.py
    :language: python
    :start-at: qiskit_circuit = export_to_qiskit(bell_circuit)
    :end-at: qiskit_circuit.x(1)

Then, we can re-import the Qiskit version to Orquestra Core and re-export to Cirq:

.. literalinclude:: /examples/bell_state.py
    :language: python
    :start-at: bell_circuit_X = import_from_qiskit(qiskit_circuit)
    :end-at: print(cirq_circuit)

Make sure the output now has an X gate at on qubit 1 after the CNOT gate:

.. code-block::
    0: ───H───@───────
              │
    1: ───────X───X───

Lastly, we can use the Qiskit statevector simulator to make sure we've created the state we want:

.. literalinclude:: /examples/bell_state.py
    :language: python
    :start-at: wavefunction = sv_simulator.get_wavefunction(bell_circuit_X)
    :end-at: print(wavefunction.amplitudes)

And we should get ``[0.        +0.j 0.70710678+0.j 0.70710678+0.j 0.        +0.j]`` if everything went to plan
