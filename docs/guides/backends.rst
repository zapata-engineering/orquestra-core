==============
Backends guide
==============

What this guide covers
======================

* General intro
* In-depth dive in how various methods work, what’s the default etc.
* Zapata's backend – TrackingBackend, SymbolicBackend
* Currently integrated backends
* Conversions to other frameworks
* info on what to do in case where given backend doesn’t use gates that we support (e.g. like https://github.com/zapatacomputing/qe-qhipster/blob/419e36c373442582b8b94933332d54972e9507b8/tests/qeqhipster/simulator_test.py#L27=)


NOTE:
- Refactoring backends is on our radar, though it will probably take us some time before we can do this.


# Guide for backends

## General intro
- Why we have backend interface? @yogi
-- Make implementation easier
-- Make them interchangeable


- Two types of backends:
-- QuantumBackend
-- QuantumSimulator

- Testing
-- We test for general behaviour
-- Also tests for gates – and why they are important (we can use the example of XY gate in various frameworks and their conventions. Or not ¯\_(ツ)_/¯)

## In-depth dive in how various methods work, what's the default etc. @yogi make some examples in examples/backends_guide.py

- run_circuit_and_measure
-- Workhorse of the backends 
-- by default it increases job counts


- run_circuitset_and_measure
- get_measurement_outcome_distribution


Simulator ones:
- get_wavefunction
- get_exact_expectation_values
- get_measurement_outcome_distribution

## Zapata's backend – TrackingBackend, SymbolicBackend

- What they are and why do we need them? -> Athena implemented TrackingBackend, she can answer any questions
- SymbolicBackend is super slow, but helpful for small circuits :) 

## Currently integrated backends

- List all of them
- Maybe some short pros&cons of each?
- GPU stuff as well I think? @yogi

## Conversions to other frameworks

- cirq/pyquil/qiskit
- Mention that it's very fast – the overhead is neglibile, so you can do it back&forth and should be ok :)
- Please double check if we're not changing the values/signs for some gates, e.g. cause we're using different conventions (some gates are in the reverse order, inverted gates)
- If you want to use some specific features from particular framework (e.g. drawing circuits from qiskit) feel free to export/import and do it! super easy :)

## How to integrate your own backend @yogi

- two sections, one for real hardware, one for simulators
-- hardware: credentials
-- simulators: direct

What to pay attention to, what comes out of the box, etc.

## Things I'm not sure where to put but we should put them somewhere:
- Example usage – here's how you change to use various backends.
- Maybe some simple benchmarking 3 backends?