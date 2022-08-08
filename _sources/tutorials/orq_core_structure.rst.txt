.. _orq_core_structure:

=================
Package Structure
=================

As shown in the diagram below, Orquestra Core is broken into multiple packages, each with a different purpose.

* `orquestra-quantum <https://github.com/zapatacomputing/orquestra-quantum>`_ provides

  * core functionalities required to run experiments, such as the Circuit class.
  * interfaces for implementing other Orquestra modules, such as quantum backends.
  * basic data structures and functions for quantum computing.

* `orquestra-opt <https://github.com/zapatacomputing/orquestra-opt>`_ provides

  * interfaces for implementing ansatzes including qaoa and qcbm.
  * optimizers and cost functions tailored to opt
  * misc functions such as grouping, qaoa interpolation, and estimators

* `orquestra-vqa <https://github.com/zapatacomputing/orquestra-vqa>`_ provides

  * interfaces for implementing ansatzes including qaoa and qcbm.
  * optimizers and cost functions tailored to vqa
  * misc functions such as grouping, qaoa interpolation, and estimators

* `orquestra-qiskit <https://github.com/zapatacomputing/orquestra-qiskit>`_ provides an integration with `Qiskit <https://qiskit.org/>`_.
* `orquestra-cirq <https://github.com/zapatacomputing/orquestra-cirq>`_ provides an integration with `Cirq <https://quantumai.google/cirq>`_ as well as :ref:`Nvidia's custatevec backend <backends>`.
* `orquestra-forest <https://github.com/zapatacomputing/orquestra-forest>`_ provides an integration with `Rigetti Forest <https://pyquil-docs.rigetti.com/en/stable/>`_.
* `orquestra-qulacs <https://github.com/zapatacomputing/orquestra-qulacs>`_ provides an integration with the `Qulacs simulator <https://github.com/qulacs/qulacs>`_.

.. image:: images/orquestra_core_connection.excalidraw.png

Dividing Orquestra core into multiple packages creates provides a number of benefits:

* It makes the code more modular and helps creating clear boundaries between the libraries.
* A lot of packages that we rely on are unstable - by dividing code into multiple separate packages, we reduce the risk of one unstable dependency breaking all of them.
* Users have more control over what they want and need to install.
* Both points above reduce the risk that the user will end up with conflicting dependencies with some other packages they might be using.
* It is easier to develop them separately.
