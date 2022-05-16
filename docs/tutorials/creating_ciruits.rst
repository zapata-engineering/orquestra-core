============================
Creating basic circuits
============================

Let's say you want to build a quantu circuit just to build a Bell State and measure it. As a quick reminder, a Bell State is a maximally entangled state with the most well-known form:

.. math::
    | \phi^+ \rangle = \frac{1}{\sqrt{2}}( |00\rangle + |11\rangle)


This state can be created using a Hadamard gate and a CNOT gate:

.. code-block::
         ┌───┐     
    q_0: ┤ H ├──■──
         └───┘┌─┴─┐
    q_1: ─────┤ X ├
              └───┘

Let's create a circuit that does this for us! Create a new file ``bell_state.py`` and follow along

First, we need to import the necessary pieces from Orquestra Core (some of these won't be used here, but rather will be used in future parts of these tutorials):

.. literalinclude:: /docs/examples/bell_state.py
    :language: python
    :start-at: from orquestra.quantum.circuits import CNOT, H, Circuit
    :end-at: import cirq

Next, we can actually build the circuit:

.. literalinclude:: /docs/examples/bell_state.py
    :language: python
    :start-at: bell_circuit = Circuit()
    :end-at: print(bell_circuit)

This will output a text description of the circuit that looks like ``Circuit(operations=[H(0), CNOT(0,1)], n_qubits=2)``

We actually have another option of how to build the circuit by specifying all of the gates at once:

.. literalinclude:: /docs/examples/bell_state.py
    :language: python
    :start-at: bell_circuit2
    :end-at: print(bell_circuit2)

TODO:
This create the exact same circuit as appending the gates one-by-one! Now we can run the circuit on the backend of our choosing.

