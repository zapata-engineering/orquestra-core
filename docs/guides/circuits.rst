=========================
Circuits guide
=========================


What this guide covers
======================

This guide is an in-depth dive into the ``Circuit`` class within Orquestra Core. In it, we'll cover advanced capabilities that can be performed using ``Circuit`` s like using symbolic gates, creating your own gates, and building decomposition rules. If you're looking for a place to get started, please see :ref:`the basics tutorial <creating_circuits>` before diving into the advanced capabilities here.


The Problem
===========

In this guide we want to create a QAOA circuit to solve a 3-node, fully-connected maxcut problem. Our :ref:`Basic QAOA Tutorial <qaoa>` walks through using Orquestra Core's built-in QAOA functionality to solve the problem from circuit creation through to a final result. Here, to demonstrate capabilities of ``Circuit`` s, we'll do a simple example and just build the circuit we can use to solve the problem later.

TODO: diagram of the graph we want to to maxcut on w/ short explainer including circuit diagram

General intro
=============

Circuit Architecture
--------------------

Orquestra Core represents quantum circuits with the ``Circuit`` class, which is in turn composed of ``Operation`` s. The most common operation type is a ``GateOperation``, which we'll focus on here. Circuits also have a number of qubits property, but users don't have to define that themselves.

If you would like to follow along with this guide, please create a new python file and start it with the imports we'll need to ensure the rest of the code examples can be run:

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: from orquestra.quantum.circuits import (
  :end-at: N_QUBITS =

Notice we also defined the number of qubits we'll be working with. This will make some list comprehensions easier later.

Creating a circuit
------------------

For this QAOA problem, the first part of the circuit we need to create is the initial state preparation circuit. That can be done by putting a Hadamard gate on each qubit. In the end we want the initial state preparation circuit to look like this:

.. code-block:: text
  TODO

We do this in our example using a `list comprehension <https://www.w3schools.com/python/python_lists_comprehension.asp>`_:

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: state_prep_circ = Circuit(
  :end-at: state_prep_circ = Circuit(

We could have also explicitly put a Hadamard gate on each qubit index too, as we will see later.

.. _getting_unitary:

Getting the unitary matrix of a circuit
---------------------------------------

Now let's inspect some aspects of the unitary of the circuit, just as a sanity check to see that everything makes sense. We can convert our circuit to a unitary matrix with the ``.to_unitary()`` method. In this case, we should see that the shape of the unitary is an 8x8 matrix (because we have a circuit that operates on 3 qubits) and the type should be a numpy ndarray.

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: unitary = state_prep_circ.to_unitary()
  :end-at: ic(type(unitary))

.. include:: /tutorials/beginner_tutorial.rst
    :start-after: icecream-note:
    :end-before: This will output a text description of the circuit

The output we get from those two ``icecream`` statements should be

.. code-block:: text

  ic| unitary.shape: (8, 8)
  ic| type(unitary): <class 'numpy.ndarray'>

Inverting a circuit
-------------------

**TODO**

Appending operations to a circuit
---------------------------------

You don't have to build a whole circuit all at once! Let's see how to append operations to an existing circuit by constructing the next part of our QAOA circuit, the problem hamiltonian circuit. This problem hamiltonian circuit gives a quantum description of the problem and shows how the nodes are connected. In this case, the 3 nodes are all-to-all connected, so our circuit should look like this:

.. code-block:: text
  TODO

We'll build up this circuit one connection at a time:

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: problem_hamiltonian_circ = Circuit(
  :end-before: unitary = problem_hamiltonian_circ.to_unitary()

For now, don't worry about what the ``beta`` variables mean in these circuits. We'll cover that later when we talk about :ref:`symbolic gates <symbolic_gates>`. For now, just notice that we started with an initial circuit and we were able to append other circuits to it using ``+=``

Let's get the :ref:`unitary matrix <getting_unitary>` again and see if it makes sense for this circuit

.. literalinclude:: /examples/circuits_guide.py
  :language: python
  :start-at: unitary = problem_hamiltonian_circ.to_unitary()
  :end-at: ic(type(unitary))

The output should look like this:

.. code-block:: text

  ic| unitary.shape: (8, 8)
  ic| type(unitary): <class 'sympy.matrices.immutable.ImmutableDenseMatrix'>

Notice the type is different from earlier (sympy matrix vs numpy matrix). This is because we have symbols in the ``RZ`` gates.

We don't have to append full circuits to append to an existing circuit, we can also append individual gates. Let's use that fact to create the last part of the circuit we need. 





 - show how to inspect circuit and components
   - how to iterate over operations
   - get number of qubits in the circuit
   - get info about specific operations (name, qubit indices, etc)
- TODO: include power and exponential classes from new unitaryhack work


Symbolic gates

- defining gates with symbolic parameters
- binding parameters
  - there are free parameters that have no values
  - binding parameters assigns them values
  - possible to do a partial binding
- circuits with free parameters aren't suitable for being run on most backends
  - some backends allow this (list which ones)

Using custom gates

- defining custom gates
- instantiating custom gates
- parameterized custom gates
  - using symbols in a custom gate
  - parameter ordering (defining which parameters are first to be filled during instantiating)
- defining custom circuits operations

Decompositions

- explaining decomposition is representing a gate operation in terms of ?simpler? operations
- 2 things needed for decomposition are
  - predicate (tells you what should be decomposed)
  - production (tells you how it should be decomposed)
- should implement protocol ``DecompositionRule``
- one rule in ``orquestra-quantum``, other rules are in specific integration repos
