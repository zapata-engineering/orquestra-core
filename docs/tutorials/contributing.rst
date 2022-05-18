==============================
Contributing to Orquestra Core
==============================

Orquestra Core itself doesn't have any source code in it, so the first step is to find which specific package you want to contribute to:

* `orquestra-quantum <https://github.com/zapatacomputing/orquestra-quantum>`_
* `orquestra-opt <https://github.com/zapatacomputing/orquestra-opt>`_
* `orquestra-vqa <https://github.com/zapatacomputing/orquestra-vqa>`_
* `orquestra-qiskit <https://github.com/zapatacomputing/orquestra-qiskit>`_
* `orquestra-cirq <https://github.com/zapatacomputing/orquestra-cirq>`_
* `orquestra-forest <https://github.com/zapatacomputing/orquestra-forest>`_

Now that you've found the repository you want to contribute to, you can fork it and make your edits, or open a new issue for that repo.

If you wanted to make improvements to the code, do that on your fork of the repo. When you're done, make sure your edits actually work, then open up a pull request to merge the changes into the main repo. Fill out any template that comes up for the pull request and send the pull request on its way!

Some best practices for when you're editing the code:

* Use flake8 to make sure your code follows our style conventions

  * We use `Google-style <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_` docstring format. If you'd like to specify types please use `PEP 484 <https://www.python.org/dev/peps/pep-0484/>`_ type hints instead adding them to docstrings.

* When in doubt, add a comment. Better to be over-commented than under-commented
* Try to keep change sets small and easily reviewable. If you can split changes into multiple pull requests, that's probably better