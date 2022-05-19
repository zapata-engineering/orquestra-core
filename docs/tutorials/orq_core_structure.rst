==========================
Orquestra Core's Structure
==========================

.. _orq_core_structure:

Orquestra Core is broken into multiple packages, each with a different purpose

* `orquestra-quantum <https://github.com/zapatacomputing/orquestra-quantum>`_ provides

  * core functionalities required to run experiments, such as the Circuit class.
  * interfaces for implementing other Orquestra modules, such as quantum backends.
  * basic data structures and functions for quantum computing.

* `orquestra-opt <https://github.com/zapatacomputing/orquestra-opt>`_ provides:

  * interfaces for implementing ansatzes including qaoa and qcbm.
  * optimizers and cost functions tailored to opt
  * misc functions such as grouping, qaoa interpolation, and estimators

* `orquestra-vqa <https://github.com/zapatacomputing/orquestra-vqa>`_ provides:

  * interfaces for implementing ansatzes including qaoa and qcbm.
  * optimizers and cost functions tailored to vqa
  * misc functions such as grouping, qaoa interpolation, and estimators

* `orquestra-qiskit <https://github.com/zapatacomputing/orquestra-qiskit>`_ is a `Zapata <https://www.zapatacomputing.com/>`_ library holding modules for integrating qiskit with `Orquestra <https://www.zapatacomputing.com/orquestra/>`_.
* `orquestra-cirq <https://github.com/zapatacomputing/orquestra-cirq>`_ is a `Zapata <https://www.zapatacomputing.com/>`_ library holding modules for integrating cirq with `Orquestra <https://www.zapatacomputing.com/orquestra/>`_.
* `orquestra-forest <https://github.com/zapatacomputing/orquestra-forest>`_ is a `Zapata <https://www.zapatacomputing.com/>`_ library holding modules for integrating forest with `Orquestra <https://www.zapatacomputing.com/orquestra/>`_.

Here is a diagram of which packages import which:

.. image:: images/orquestra_core_connection.png