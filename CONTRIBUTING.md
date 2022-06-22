# Contributing to Orquestra

🎶 Thanks so much for your interest in contributing to Orquestra! 🎶

We at Zapata's quantum software team value contributions to orquestra, so we created this document to guide you from planning your code all the way to making a PR. But if you have more questions, please feel free to email our engineers [michal](mailto:michal.stechly@zapatacomputing.com) of [athena](mailto:athena.caesura@zapatacomputing.com) for some guidance. 

## Code of Conduct

Contributors to the orquestra project are expected to follow the orquestra [code of conduct](CODE_OF_CONDUCT.md). Please report violations to either of our engineers listed above.

## How to Contribute

### Choosing an Issue

For new contributors, the good-first-issue tag is usually a great place to start!

### Installation

After cloning the repository, run `pip install -e .[dev]` from the main directory to install the development version. Note that in certain environments you might need to add quotes: `pip install -e '.[dev]'`. This install will ensure you have all the dependencies you need in order to contribute to Orquestra.

### Commits

Zapata's QS team uses the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/#specification) style for commit messages so that we can automatically generate release notes.

### Comments

We use [Google-style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) docstring format. If you'd like to specify types please use [PEP 484](https://www.python.org/dev/peps/pep-0484/) type hints instead adding them to docstrings.

### Style

Orquestra contributors are required to use black, flake8, mypy and isort to run automated checks for code style. Make sure to install the development version (described above) so you can run these commands using the `make style` command or [pre-commit hooks](https://pre-commit.com/).

### Tests

All new contributions to Orquestra should be accompanied by deterministic unit tests. This means each test should focus on a specific aspect of the new code and shouldn't include any probabilistic elements. If you are unsure how to remove randomness in your tests, mention it in your PR and we'll be happy to assist. 💪

Tests for this project can be run using the `make coverage` or `pytest tests` commands from the main directory.

### Making a PR

Before submitting your PR, run `make muster` from the main directory. This ensures your code will pass tests and style once submitted.

When your code passes muster, ensure your changes are on a new branch whose name describes the issue you are solving.

Then you can make a PR directly to the `main` branch by filling out the PR submission template and clicking create pull request.

When you make your PR, github will automatically run style and test checks on python 3.8, 3.9, and 3.10 using [Github Actions](.github/workflows/style.yml). While tests are running, request that `quantum-software` to review your code.

Once you have made the requested changes and your PR is approved, you can click merge and delete your branch. 🎉

### CLA

After making your PR, send an email to Michal or Athena (emails above) so that we can send you a copy of our CLA. If you wish to view the CLA before contributing, our you can find [here](docs/_static/ZapataCLA.pdf).

### Bug Reporting

If you'd like to report a bug/issue please create a new issue in this repository.

## Tips

### Modular Design

Here at Zapata's QS team we're all about connecting computers. Our Orquestra software is intended to act as a bridge between others including pyquil, cirq, qiskit, and qulacs. This flexibility gives our scientists access to a wide variety of platforms from which to conduct experiments.

As a result, we make extensive use of modular interfaces such as [protocols](https://peps.python.org/pep-0544/) in our codebase. Familiarizing yourself with protocols will greatly enhance your understanding of our design and improve the your contributions.

### Tests

If you implement an interface, chances are we have already written some tests for it. For instance if you were to implement a new `QuantumBackend`, you should take advantage of the tests in `QuantumBackendTests`. This means that the tests you write can be specific to your new implementation and can save a lot of time!

Tests not only to ensure the code is functional, but will also tells us a lot about your implementation. Don't let your code go in alone! Give it some nice tests to keep it company! 👭

Most importantly, don't be afraid to use our tests as inspiration for your own!

## Ending Note 🎵

Thanks again for contributing!

We're hiring! So check out our job listings on our [website](https://www.zapatacomputing.com/quantum-computing-careers/)!

🔥 Can't wait to see your PRs 🔥
