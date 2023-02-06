Getting Started
###############

There are two ways to get started with Orquestra Core: by installing the packages locally or by using the Orquestra Portal cloud environment.

.. tab-set::

    .. tab-item:: Start Locally

        **Quick Installation**

        To install all of the Orquestra Core packages needed for the tutorials and recipes, run the following command:

        .. code-block:: bash

            pip install orquestra-core[all]
        
        You can now begin with the first :doc:`Workflow SDK<sdk/tutorials/quickstart>` and :doc:`Quantum SDK<quantum/tutorials/beginner_tutorial>` tutorials.

        .. note
            
            If you are using Windows, you may need to :doc:`follow additional steps <sdk/tutorials/installing-windows>` in order to correctly install Orquestra Core's Workflow SDK.

        **Custom Installation**

        Note that you can also install the Orquestra Core packages individually.
        For example, to install the Orquestra Core package for the Workflow SDK, run the following command:

        .. code-block:: bash

            pip install orquestra-sdk[all]
        
        The table below lists the packages within Orquestra Core.


        .. list-table::
            :widths: 30 70

            * - `orquestra-sdk <https://github.com/zapatacomputing/orquestra-workflow-sdk>`_
              - Tools for composing, executing, and managing computational workflows.
            * - `orquestra-quantum <https://github.com/zapatacomputing/orquestra-quantum>`_
              - Data structures and interfaces describing fundamental concepts in quantum computing such as circuits and backends.
            * - `orquestra-opt <https://github.com/zapatacomputing/orquestra-opt>`_
              - Data structures, interfaces, and utilities related to continuous and discrete optimization.
            * - `orquestra-vqa <https://github.com/zapatacomputing/orquestra-vqa>`_
              - Implementations of common variational quantum algorithms including VQE, QAOA, and QCBM.
            * - `orqviz <https://github.com/zapatacomputing/orqviz>`_
              - Tools for visualizing the loss landscape of parameterized quantum algorithms.
            * - `orquestra-qiskit <https://github.com/zapatacomputing/orquestra-qiskit>`_
              - Integration with `Qiskit <https://qiskit.org/>`_.
            * - `orquestra-cirq <https://github.com/zapatacomputing/orquestra-cirq>`_
              - Integration with `Cirq <https://quantumai.google/cirq>`_ and :ref:`Nvidia's custatevec backend <backends>`.
            * - `orquestra-forest <https://github.com/zapatacomputing/orquestra-forest>`_
              - Integration with `Rigetti Forest <https://pyquil-docs.rigetti.com/en/stable/>`_.
            * - `orquestra-qulacs <https://github.com/zapatacomputing/orquestra-qulacs>`_
              - Integration with the `Qulacs simulator <https://github.com/qulacs/qulacs>`_.
            * - `orquestra-braket <https://github.com/zapatacomputing/orquestra-braket>`_
              - Integration with `Amazon Braket <https://aws.amazon.com/braket/>`_.


    .. tab-item:: Start on the Cloud

        When running in the Orquestra Portal cloud environment, the Orquestra Core packages packages required for the tutorials and recipes will already be installed.
        Orquestra Portal users can begin directly with the first :doc:`Workflow SDK<sdk/tutorials/quickstart>` and :doc:`Quantum SDK<quantum/tutorials/beginner_tutorial>` or browse the example notebooks contained in your Portal environment.
        To learn more about Orquestra Portal, `contact Zapata Computing <https://www.zapatacomputing.com/contact/>`_.
