================
Quantum Circuits
================

This tutorial explains how to use the Orquestra Quantum SDK to define and run quantum circuits, as well as translate between frameworks such as Qiskit and Cirq. 

.. _creating_basic_circuits:

Creating basic circuits
=======================

Let's say you want to build a quantum circuit just to build a Bell State and measure it. As a quick reminder, a Bell State is a maximally entangled state with the most well-known form:

.. math::
    | \phi^+ \rangle = \frac{1}{\sqrt{2}}( |00\rangle + |11\rangle)


This state can be created using a Hadamard gate and a CNOT gate:

.. code-block:: text

         ┌───┐     
    q_0: ┤ H ├──■──
         └───┘┌─┴─┐
    q_1: ─────┤ X ├
              └───┘

Let's create a circuit that does this for us! Create a new file ``bell_state.py`` and follow along

This circuit can be created in a few lines. First, we import the needed gate and circuit classes, then create a new ``Circuit`` object, and finally add the gates we want.

.. literalinclude:: ../examples/tutorials/bell_state.py
    :language: python
    :start-at: from orquestra.quantum.circuits import CNOT, H, Circuit
    :end-at: ic(bell_circuit)

.. _icecream-note:

.. note::
    ``icecream`` (and ``ic``) is like ``print``, but offers more information about what is being printed. It's great for debugging! Just install it with ``pip install icecream``

    If you would rather just use ``print``, everything in this tutorial should still work! Just replace ``ic()`` with ``print()`` and all will be well.

This will output a text description of the circuit that looks like ``bell_circuit: Circuit(operations=[H(0), CNOT(0,1)], n_qubits=2)``

We actually have another option of how to build the circuit by specifying all of the gates at once:

.. literalinclude:: ../examples/tutorials/bell_state.py
    :language: python
    :start-at: bell_circuit2
    :end-at: ic(bell_circuit2)

This creates the exact same circuit as appending the gates one-by-one! Now we can run the circuit on the backend of our choosing.

.. _superdense_coding:

**Your turn!**

`Superdense coding <https://www.qutube.nl/courses-10/fundamentals-11/superdense-coding-326>`_ is one of those incredible results of quantum computing where we're able to transmit two bits of information using just one qubit (as long as that qubit's entangled with another qubit). It also uses a bell state, so let's try to make a circuit that implements superdense coding with Orquestra Core! You might want to make a new file for this and call it something like ``superdense_coding.py``. 

.. hint::

    If you need a refresher on superdense coding, watch `this video <https://www.qutube.nl/courses-10/fundamentals-11/superdense-coding-326>`_ from QuTech Academy

Got your circuit? Compare it with ours:

.. hint::
    :class: dropdown

    .. literalinclude:: ../examples/tutorials/superdense_coding.py
        :language: python
        :start-at: from orquestra.quantum.circuits import
        :end-before: # bob runs and measures the qubits


Running Circuits on a Backend
=============================

.. _running_circuits:

Once we have our circuit, the next step is to select what backend to run on and get our measurements. For this run, let's use Qiskit's aer simulator with 100 shots:

.. literalinclude:: ../examples/tutorials/bell_state.py
    :language: python
    :start-at: import QiskitSimulator
    :end-at: ic(measurements.get_counts())

It's actually very easy to switch out backends thanks to Orquestra Core's interfaces. Let's say instead of the QiskitSimulator, we want to use Zapata's very own :class:`SymbolicSimulator <orquestra.quantum.runners.symbolic_simulator.SymbolicSimulator>` . We can do that by changing just part of one line:

.. literalinclude:: ../examples/tutorials/bell_state.py
    :language: python
    :start-at: import SymbolicSimulator
    :end-at: ic(measurements2.get_counts())

.. _running_amplitudes:

If we want to get the amplitudes from the wavefunction instead of running measurements, we can do that as well:

.. literalinclude:: ../examples/tutorials/bell_state.py
    :language: python
    :start-at: sv_simulator = QiskitSimulator("aer_simulator_statevector")
    :end-at: ic(wavefunction.amplitudes)

We can also get an expectation value for the circuit given an operator we want to use:

.. literalinclude:: ../examples/tutorials/bell_state.py
    :language: python
    :start-at: import EstimationTask
    :end-at: ic(evals[0].values)

For a full list of backends you can run your circuits on, refer to the :doc:`Circuit Runners guide <../guides/circuit_runners>`.

**Your turn!**

For the superdense coding example we made in the last section, run the circuit on a backend of your choosing (our ``SymbolicSimulator`` works well ;) ). When you're done, check how we did it below!

.. hint::
    :class: dropdown

    .. literalinclude:: ../examples/tutorials/superdense_coding.py
        :language: python
        :start-at: # bob runs and measures the qubits
        :end-at: ic(measurements.get_counts())

.. _beginner_translating_circuits:

Translating Circuits between Libraries
======================================

Now that we've got this bell state, let's say we want to change it a bit so that instead of the state

.. math::
    | \phi^+ \rangle = \frac{1}{\sqrt{2}}( |00\rangle + |11\rangle )

We instead get the state

.. math::
    | \psi^+ \rangle = \frac{1}{\sqrt{2}}( |01\rangle + |10\rangle )

But we want to do it by editing the circuit in Qiskit, and then visualizing the circuit in Cirq (because why not?) Lucky for us, Orquestra Core allows us to do that readily!

First, we can translate our existing circuit from the current Orquestra Core representation into its Qiskit representation and add an ``X`` gate to the second qubit in Qiskit:

.. literalinclude:: ../examples/tutorials/bell_state.py
    :language: python
    :start-at: qiskit.conversions import
    :end-at: qiskit_circuit.x(1)

Then, we can re-import the Qiskit version to Orquestra Core and re-export to Cirq:

.. literalinclude:: ../examples/tutorials/bell_state.py
    :language: python
    :start-at: import export_to_cirq
    :end-at: print(cirq_circuit)

Make sure the output now has an X gate at on qubit 1 after the CNOT gate:

.. code-block:: text

    0: ───H───@───────
              │
    1: ───────X───X───

Lastly, we can use the Qiskit statevector simulator to make sure we've created the state we want. Try to write that line yourself (potentially reminding yourself what we did in the previous section) then look at the answer below

.. hint::
    :class: dropdown

    .. literalinclude:: ../examples/tutorials/bell_state.py
        :language: python
        :start-at: wavefunction = sv_simulator.get_wavefunction(bell_circuit_X)
        :end-at: ic(wavefunction.amplitudes)

And we should get ``wavefunction.amplitudes: array([0.70710678+0.j, 0.+0.j, 0.+0.j, 0.70710678+0.j])`` if everything went according to plan.

**Your turn!**

Try to export our new ``bell_circuit_X`` to Qulacs!

.. hint::
    :class: dropdown

    .. literalinclude:: ../examples/tutorials/bell_state.py
        :language: python
        :start-at: import export_to_qulacs
        :end-at: qulacs_circuit = 

Ready for something a bit more interesting? Try the :ref:`qaoa tutorial <qaoa>`!