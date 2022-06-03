################################################################################
# © Copyright 2022 Zapata Computing Inc.
################################################################################
include subtrees/z_quantum_actions/Makefile


github_actions:
	python3 -m venv ${VENV_NAME} && \
		${VENV_NAME}/bin/python3 -m pip install --upgrade pip && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-quantum && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-opt && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-vqa && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-qiskit && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-forest && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-cirq && \
		${VENV_NAME}/bin/python3 -m pip install ./orquestra-qulacs && \
		${VENV_NAME}/bin/python3 -m pip install -e '.[dev]'

coverage:
	$(PYTHON) -m pytest tests/
