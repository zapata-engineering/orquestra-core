=================================================
Designing Proteins with a D-Wave Quantum Annealer
=================================================

.. _d_wave_qubo-label:

This tutorial presents a protein design problem, whose goal is to optimize the
energy of conformation for optimal protein folding.

D-Wave quantum computers accept unconstrained models (Binary Quadratic Models,
BQM). It is named binary because variables are represented by qubits that return two
states and quadratic because you can configure coupling strengths between pairs
of qubits. More details can be found in the `D-Wave documentation <https://docs.ocean.dwavesys.com/en/stable/index.html>`_.


Introduction
------------

Proteins
~~~~~~~~

Proteins are usually described at `four levels of detail <https://en.wikipedia.org/wiki/Protein_structure>`_. We will briefly
review them and point out where our tutorial fits into these structures.

These are the four basic levels of detail:

1. Primary Structure: This refers to a sequence of amino acids bonded into a
   polypeptide chain. This structure is often described by a simple list of
   amino acids like *Tyr-Lys-Ala-Asp-Phe...*

2. Secondary Structure: The highly regular local sub-structures on the actual
   polypeptide backbone chain. For our purposes, the backbone structure is
   fixed.

3. Tertiary Structure: The three-dimensional structure created by a single
   protein molecule (a single polypeptide chain). Such structure is often
   referred to as "folding".

4. Quaternary Structure: the three-dimensional structure consisting of the
   aggregation of two or more individual polypeptide chains.

Rotamers
~~~~~~~~

Once a protein backbone is defined by the peptide chain, there are still
internal rotational degrees of freedom in the amino acid that are not part of
the backbone bonds. Amino acid structures that differ by rotational degrees of
freedom are called "rotamers". These are relevant to our tutorial because we search
for optimal rotamers (in addition to amino acids) that provide the lowest
energy contributions to the protein.


Protein Problem Workflow
------------------------

Representation
~~~~~~~~~~~~~~

In the first step, we need to represent a protein problem in a form of
Quadratic Unconstrained Binary Optimization (QUBO)
model. This model is capable of interacting with D-Wave quantum hardwave using
Binary Quadratic Model (BQM) class from D-Wave's SDK.

In the next example we use D-Wave's Simulated Annealing Sampler, Leap Hybrid
Sampler and DWave Sampler (Quantum).

.. Note::
   To run hybrid and quantum samplers user need to have an
   access to D-Wave quantum hardware.

In the problem considered herein, we have protein with 3 aminoacids in chain, and for each
position we have available rotamers:

1. 3 rotamers - for aminoacid at position 1
2. 4 rotamers - for aminoacid at position 2
3. 3 rotamers - for aminoacid at position 3

The upper triangular matrix in the example below represents interaction energies
in the QUBO model. The Main diagonal in this representation stores 1-body energies,
e.g. particular rotamer self-energy. Other cells represent the energy
between a pair, 2-bodies energies, e.g., rotamer 1 at position 1 and rotamer 3
at position 2, for example. Note: computers index starting with "0".
So for example above we may say (0, 0) <-> (1, 2) energy,
where the **(a, b)** notation represents (position, rotamer).

.. code-block:: python

    import numpy as np
    import dimod
    from hybrid.reference.kerberos import KerberosSampler
    from dwave.system import LeapHybridSampler, DWaveSampler

    energy_matrix = np.array(
        [[-100.0,   50000,  50000,  -1121.0,    1122.0, 1123.0, -1124.0, 1131.0, 1132.0, -1133.0],
        [0,         200.0,  50000,  1221.0,     1222.0, 1223.0, 1224.0, 1231.0,  1232.0, -1233.0],
        [0,         0,      -300.0, -1321.0,    1322.0, -1323.0, 1324.0, 1331.0, 1332.0, 1333.0],
        [0,         0,      0,      400.0,      50000,  50000,  50000,  -2131.0, 2132.0, -2133.0],
        [0,         0,      0,      0,          -500.0, 50000,  50000,  2231.0,  -2232.0, 2233.0],
        [0,         0,      0,      0,          0,      600.0,  50000,  -2331.0, 2332.0, -2333.0],
        [0,         0,      0,      0,          0,      0,      -700.0, 2431.0,  -2432.0, 2433.0],
        [0,         0,      0,      0,          0,      0,      0,      800.0,   50000,   50000 ],
        [0,         0,      0,      0,          0,      0,      0,      0,       -900.0,  50000 ],
        [0,         0,      0,      0,          0,      0,      0,      0,       0,       10.0  ]])

    variables = [
        (0, 0), (0, 1), (0, 2),          # aminoacid 1 - has 3 possible rotamers
        (1, 0), (1, 1), (1, 2), (1, 3),  # aminoacid 2 - has 4 possible rotamers
        (2, 0), (2, 1), (2, 2)           # aminoacid 3 - has 3 possible rotamers
    ]

    bqm = dimod.BinaryQuadraticModel.from_numpy_matrix(energy_matrix, variables)


Workflow Definition
~~~~~~~~~~~~~~~~~~~

In order to run BQM/QUBO model on Orquestra, a workflow definition should have
a task. The task below uses a randomly generated energy matrix.
In a real protein design problem, the energy matrix contains interactions between pairs of
the protein. This interactions energy matrix may be obtained from the tools
like Rosetta.

.. code-block:: python

    @sdk.task
    def protein_optimization() -> float:
        logging.debug("Generating example protein problem")
        logging.debug(energy_matrix)

        simanneal = dimod.SimulatedAnnealingSampler()
        sa_solution = simanneal.sample(bqm)
        logging.debug("[SimulatedAnnealingSampler] Energy:", sa_solution.first.energy)
        logging.debug("[SimulatedAnnealingSampler] Solution:", sa_solution.first)

        # NOTE: In order to run these user need to have an access to D-Wave quantum hardware
        #       Access should be configured here in workflow or in environment.
        hybrid_solution = LeapHybridSampler().sample(bqm)
        logging.debug("[HYBRID] Energy:", hybrid.first.energy)
        logging.debug("[HYBRID] Solution:", hybrid.first)

        quantum_solution = DWaveSampler().sample(bqm)
        logging.debug("[Quantum] Energy:", dwave.first.energy)
        logging.debug("[Quantum] Solution:", dwave.first)

        return sa_solution


    @sdk.workflow
    def protein_workflow():
        return [
            protein_optimization()
        ]


Conclusion
----------

This class of protein design problem can be executed on the Orquestra Platform
using the Orquestra Workflow SDK. These problems should be formulated in a QUBO format, so the
energy matrix should contain both one body and two body interaction energies.
