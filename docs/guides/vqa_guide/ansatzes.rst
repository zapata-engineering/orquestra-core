.. _ansatzes_guide:

========
Ansatzes
========

Usage
=====

In the cotext of VQAs, an ansatz is a parameterized quantum circuit. Given a cost function on the output of the circuit, parameters can be minimized to create a circuit which solves a given problem.

In ``orquestra``, ``Ansatz`` objects are used to construct ``EstimationTaskFactory`` objects which are then used to make a cost function.


Creating Your Own Ansatz
========================

Let's construct a simple example where we only have a single layer of Z rotations in our ansatz. We start by creating a child of the ``Ansatz``` class.

.. literalinclude:: ../../examples/test_ansatz.py
    :language: python
    :start-at: from typing import Optional
    :end-at: class TestAnsatz(Ansatz):

Next, let's define the ``__init__`` method where the ansatz is defined.

.. literalinclude:: ../../examples/test_ansatz.py
    :language: python
    :start-at: def __init__(
    :end-at: self._circuit += RZ(new_symbol)

Finally, we'll define the ``_generate_circuit`` function which substitutes parameters into the circuit.

.. literalinclude:: ../../examples/test_ansatz.py
    :language: python
    :start-at: def _generate_circuit(
    :end-at: return self._circuit.bind(symbols_map)

And that's it! Once the ansatz is defined we can easily subtitute in into an ``EstimationTaskFactory``.