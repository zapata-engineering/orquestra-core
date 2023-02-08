# orquestra-core

## What is it?

Orquestra Core is a set of libraries used for quantum computing developed by [Zapata Computing](https://www.zapatacomputing.com). It's a part of [Orquestra](https://www.zapatacomputing.com/orquestra/) platform, but can be used as standalone Python libraries.
For more details please refer to [the documentation](https://docs.orquestra.io/docs/core/index.html)

Orquestra Core comprises of the following packages:

- [`orquestra-sdk`](https://github.com/zapatacomputing/orquestra-workflow-sdk) provides tools for composing, executing, and managing computational workflows.

- [`orquestra-quantum`](https://github.com/zapatacomputing/orquestra-quantum) provides

  - core functionalities required to run experiments, such as the Circuit class.
  - interfaces for implementing other Orquestra modules, such as quantum backends.
  - basic data structures and functions for quantum computing.

- [`orquestra-opt`](https://github.com/zapatacomputing/orquestra-opt) provides:

  - interfaces for implementing ansatzes including qaoa and qcbm.
  - optimizers and cost functions tailored to opt
  - misc functions such as grouping, qaoa interpolation, and estimators

- [`orquestra-vqa`](https://github.com/zapatacomputing/orquestra-vqa) provides:

  - interfaces for implementing ansatzes including qaoa and qcbm.
  - optimizers and cost functions tailored to vqa
  - misc functions such as grouping, qaoa interpolation, and estimators

- [`orquestra-qiskit`](https://github.com/zapatacomputing/orquestra-qiskit) – integration with [qiskit](https://qiskit.org/).
- [`orquestra-cirq`](https://github.com/zapatacomputing/orquestra-cirq) – integration with [CirQ](https://quantumai.google/cirq).
- [`orquestra-qulacs`](https://github.com/zapatacomputing/orquestra-qulacs) – integration with [Qulacs simulator](http://docs.qulacs.org/en/latest/).
- [`orquestra-braket`](https://github.com/zapatacomputing/orquestra-braket) - integration with [Amazon Braket Python SDK](https://github.com/aws/amazon-braket-sdk-python)

We have temporarily removed [`orquestra-forest`](https://github.com/zapatacomputing/orquestra-forest) (integration with [Forest SDK](https://docs.rigetti.com/qcs/)) due to compatibility issues. It should work in most cases, if you need it feel free to install it manually.

- [`orqviz`](https://github.com/zapatacomputing/orqviz) – Visualization tool for VQA landscapes.

## Installation

To install the latest versions of all of the Orquestra Core packages together run:

`pip install orquestra-core`

Libraries to interact with other frameworks (e.g. qiskit, cirq), simulators or QPU can be installed as optional dependencies, i.e.: `pip install orquestra[cirq]`.

Keep in mind, that some of the packages have extra installation options, so there might be certain features unavailable if installed this way. However, all the components of Orquestra Core can be installed separately as well, e.g.:

```
pip install orquestra-quantum
pip install orquestra-opt[qubo]
```

## Usage

For examples and tutorials please refer to [the documentation](https://docs.orquestra.io/docs/core/index.html).

## Bug Reporting

If you'd like to report a bug/issue please create a new issue in appropriate repository. When in doubt, feel free to create issue in this repo.

## Contributing

Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for more information on contributing to Orquestra Core.
