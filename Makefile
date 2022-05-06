include subtrees/z_quantum_actions/Makefile


github_actions:
	python3 -m venv ${VENV} && \
		${VENV}/bin/python3 -m pip install --upgrade pip && \
		${VENV}/bin/python3 -m pip install ./orquestra-quantum && \
		${VENV}/bin/python3 -m pip install ./orquestra-opt && \
		${VENV}/bin/python3 -m pip install ./orquestra-vqa && \
		${VENV}/bin/python3 -m pip install ./orquestra-qiskit && \
		${VENV}/bin/python3 -m pip install ./orquestra-cirq
		${VENV}/bin/python3 -m pip install -e '.[dev]'
