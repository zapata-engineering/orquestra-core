################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
include subtrees/z_quantum_actions/Makefile


# The following installation instructions are unconventional.
# This is due to the fact that on the CICD we usually want to test against the latest
# version of the libraries specified from `main`.
# However, in `setup.cfg` those dependencies are pinned using `==`. This is because
# intended usage of `orquestra-core` is to used pinned versions which are
# compatible with each other.
# A solution to that is not to install `orquestra-core` at all, since installing it 
# will force using pinned versions and lead to dependency conflicts.
# Right we runn CI pipeline for `orquestra-core` just to run integration tests, which 
# don't require `orquestra-core` to be installed, just all of its dependencies.
# I'm well aware that there are several problems with this solution:
# 1. It leads to redundancy between options.extras_require in setup.cfg and 
# this makefile.
# 2. It doesn't provide good experience for local development.
# 3. It feels super hacky so probably has plenty of unexpected issues associated
# with it.
# But it's better than tests always failing on the CI ¯\_(ツ)_/¯
github_actions:
	python3 -m venv ${VENV_NAME} && \
		${VENV_NAME}/bin/python3 -m pip install --upgrade pip && \
		${VENV_NAME}/bin/python3 -m pip install orquestra-python-dev && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-quantum && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-opt[all] && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-vqa && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-qiskit && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-cirq[qsim] && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-qulacs && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-braket && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-forest && \
		${VENV_NAME}/bin/python3 -m pip install ./orqviz && \
		${VENV_NAME}/bin/python3 -m pip install -r docs/requirements.txt

coverage:
	$(PYTHON) -m pytest tests/
	$(PYTHON) -m pytest docs/quantum/examples/tests

# Runs tests with the latest dependncies from PyPI
run_tests_before_release:
	python3 -m venv ${VENV_NAME} && \
		${VENV_NAME}/bin/python3 -m pip install --upgrade pip && \
		${VENV_NAME}/bin/python3 -m pip install -e '.[dev]'
		${VENV_NAME}/bin/python3 -m pytest tests/

# We are overwriting the default version as it's using `github_actions`, which does
# not install `orquestra-core` with the right dependencies for the release.
get-next-version: 
	python3 -m venv ${VENV_NAME} && \
		${VENV_NAME}/bin/python3 -m pip install --upgrade pip && \
		${VENV_NAME}/bin/python3 -m pip install -e '.[dev]' && \
		${VENV_NAME}/bin/python3 subtrees/z_quantum_actions/bin/get_next_version.py $(PACKAGE_NAME)
