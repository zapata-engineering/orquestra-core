=========================
Circuits guide
=========================

- have a bit about what sort of things this guide covers


General intro

 - a bit about circuit architecture
   - composed of operations (operations more general than gates)
   - possibly number of qubits
 - show how to create a circuit
 - how to append new operations to the circuit
 - how to convert circuit -> unitary matrix
- how to invert a circuit
 - show how to inspect circuit and components
   - how to iterate over operations
   - get number of qubits in the circuit
   - get info about specific operations (name, qubit indices, etc)
- include power and exponential classes from new unitaryhack work


Symbolic gates

- defining gates with symbolic parameters
- binding parameters
  - there are free parameters that have no values
  - binding parameters assigns them values
  - possible to do a partial binding
  - works on both circuit and operation levels
- circuits with free parameters are suitable for being run on most backends
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
- implemented as subclasses of ``DecompositionRule``
- one rule in ``orquestra-quantum``, other rules are in specific integration repos



We want to implement a circuit
2 ideas from michal:
- 3-qubit qaoa circuit <---
- 2-qubit circuit that allows you to reach every state
