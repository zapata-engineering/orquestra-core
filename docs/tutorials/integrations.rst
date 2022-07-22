======================================================
Integrations, Modules, and Libraries in Orquestra Core
======================================================

Orquestra Core is made up of multiple packages, each with its own functionality. For more info on how those packages are broken up, check out :ref:`this page <orq_core_structure>`.

Within those packages, there are different options for certain objects (like Backends, Optimizers, etc). This page aims to be an up-to-date list of these options you have so you can choose from what's available. If you notice something that's missing here, or you create your own you want added, open a :ref:`pull request <contributing>` on this repository!


Ansatzes
========

* `XAnsatz <https://github.com/zapatacomputing/orquestra-vqa/blob/main/tests/orquestra/vqa/ansatz/kbody_test.py#L102=>`_
* `XZAnsatz <https://github.com/zapatacomputing/orquestra-vqa/blob/main/tests/orquestra/vqa/ansatz/kbody_test.py#L141=>`_
* `QAOAFarhiAnsatz <https://github.com/zapatacomputing/orquestra-vqa/blob/main/tests/orquestra/vqa/ansatz/qaoa_farhi_test.py>`_
* `WarmStartQAOAAnsatz <https://github.com/zapatacomputing/orquestra-vqa/blob/main/tests/orquestra/vqa/ansatz/qaoa_warm_start_test.py>`_
* `HEAQuantumCompilingAnsatz <https://github.com/zapatacomputing/orquestra-vqa/blob/main/tests/orquestra/vqa/ansatz/quantum_compiling_test.py>`_
* `SingletUCCSDAnsatz <https://github.com/zapatacomputing/orquestra-vqa/blob/main/tests/orquestra/vqa/ansatz/singlet_uccsd_test.py>`_

.. include:: /guides/backends.rst
  :start-after: .. _integrated_backends:
  :end-before: Conversions to other frameworks


Noise Models
============

* `Cirq <https://github.com/zapatacomputing/orquestra-cirq/blob/main/tests/orquestra/integrations/cirq/noise/basic_test.py>`_
* `Qiskit <https://github.com/zapatacomputing/orquestra-qiskit/blob/main/tests/orquestra/integrations/qiskit/noise/basic_test.py>`_


Optimizers
==========

* `BasinHoppingOptimizer <https://github.com/zapatacomputing/orquestra-opt/blob/main/tests/orquestra/opt/optimizers/basin_hopping_test.py>`_
* `CMAESOptimizer <https://github.com/zapatacomputing/orquestra-opt/blob/main/tests/orquestra/opt/optimizers/cma_es_optimizer_test.py>`_
* `QiskitOptimizer <https://github.com/zapatacomputing/orquestra-opt/blob/main/tests/orquestra/opt/optimizers/qiskit_optimizer_test.py>`_
* `ScipyOptimizer <https://github.com/zapatacomputing/orquestra-opt/blob/main/tests/orquestra/opt/optimizers/scipy_optimizer_test.py>`_
* `SearchPointsOptimizer <https://github.com/zapatacomputing/orquestra-opt/blob/main/tests/orquestra/opt/optimizers/search_points_optimizer_test.py>`_
* `SimpleGradientDescent <https://github.com/zapatacomputing/orquestra-opt/blob/main/tests/orquestra/opt/optimizers/simple_gradient_descent_test.py>`_


Problems
========

* `GraphPartitioning <https://github.com/zapatacomputing/orquestra-opt/blob/main/tests/orquestra/opt/problems/graph_partition_test.py>`_
* `MaxIndependentSet <https://github.com/zapatacomputing/orquestra-opt/blob/main/tests/orquestra/opt/problems/max_independent_set_test.py>`_
* `MaxCut <https://github.com/zapatacomputing/orquestra-opt/blob/main/tests/orquestra/opt/problems/maxcut_test.py>`_
* `VertexCover <https://github.com/zapatacomputing/orquestra-opt/blob/main/tests/orquestra/opt/problems/vertex_cover_test.py>`_