.. _ansatzes_guide:

========
Ansatzes
========

Usage
=====

In the cotext of VQAs, an ansatz is a template for a parameterized quantum circuit. Given a cost function which depends on the output of the circuit, parameters can be tuned to create a circuit which minimizes the cost function.

In ``orquestra``, ``Ansatz`` objects are used to construct ``EstimationTaskFactory`` objects which are then used to make a cost function.


Available Ansatzes
==================
`orquestra-core` provides several ansatzes. Here we give a list of ansatzes with a breif description of each.

1. kbody ansatzes - ansatzes created to solve maxcut problems. Number of parameters increases exponentially with number of qubits, but these ansaztes avoid local minima. See `the paper <https://arxiv.org/abs/2105.01114>`_ for details.
    a. ``XAnsatz`` - Couples qubits in the X direction. 
    b. ``XZAnsatz`` - Couples qubits in the X and Z directions. 
2. ``QAOAFarhiAnsatz`` - Alternates global cost hamiltons with local mixer hamiltonians. See `the paper <https://arxiv.org/abs/1411.4028>`_ for details.
3. ``WarmStartQAOAAnsatz`` - See `the paper <https://arxiv.org/abs/2009.10095v3>`_ for details.
4. ``HEAQuantumCompilingAnsatz`` - See `the paper <https://arxiv.org/pdf/2011.12245.pdf>`_ for details.
5. ``SingletUCCSDAnsatz`` - Widely used in chemistry problems to estimate the ground state of a molecule's hamiltonian. Parameters control the probability of single an double excitations in your simulated molecule. See `this paper <>`_
6. ``QCBMAnsatz`` - Ansatz for learning distributions. See `this paper <https://arxiv.org/pdf/1801.07686.pdf>`_ for details.


Creating Your Own Ansatz
========================

Let's construct a simple example where we only have a single layer of Z rotations in our ansatz. We start by creating a child of the ``Ansatz``` class.

.. literalinclude:: ../../examples/mock_ansatz.py
    :language: python
    :start-at: from typing import Optional
    :end-at: class MockAnsatz(Ansatz):

Next, let's define the ``__init__`` method where the ansatz is defined.

.. literalinclude:: ../../examples/mock_ansatz.py
    :language: python
    :start-at: def __init__(
    :end-at: self._circuit += RZ(new_symbol)

Finally, we'll define the ``_generate_circuit`` function which substitutes parameters into the circuit.

.. literalinclude:: ../../examples/mock_ansatz.py
    :language: python
    :start-at: def _generate_circuit(
    :end-at: return self._circuit.bind(symbols_map)

And that's it! Once the ansatz is defined we can easily subtitute in into an ``EstimationTaskFactory``.