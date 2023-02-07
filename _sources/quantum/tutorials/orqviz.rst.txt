======
Orqviz
======

To aid in the development of variational quantum algorithms, we have developed a visualization tool called orqviz. It is a Python package that allows users to visualize high dimensional cost function landscapes. It is designed to be used in Jupyter notebooks, and can be installed via pip.

Orqviz provides a collection of tools which quantum researchers and enthusiasts alike can use for their simulations. It works with any framework for running quantum circuits, for example Qiskit, Cirq, PennyLane, and the Orquestra Quantum SDK. The package contains functions to generate data, as well as a range of flexible plotting and helper functions.

Visualizing a Cost Function Landscape
=====================================

In this tutorial we will use orqviz to visualize a simple sinusoidal cost function landscape using orqviz.

Let's start by importing the necessary packages and seed the random number generator for reproducibility:

.. literalinclude:: ../examples/tutorials/orqviz.py
    :language: python
    :start-at: import orqviz
    :end-at: np.random.seed(42)

Next, we define our cost function. In this case, we will use a simple sinusoidal function:

.. literalinclude:: ../examples/tutorials/orqviz.py
    :language: python
    :start-at: def cost_Function(pars):
    :end-at: n_params = 42

As you can see, the above function has many parameters, too many to display in a single plot. Orqviz can visualize this higher dimensional landscape by taking 2d slice of it in a region of interest. The orientation of this 2d slice is defined by two orthonormal vectors. As an example, let's choose them randomly and display a square of size :math:`[-\pi, \pi]`.

.. literalinclude:: ../examples/tutorials/orqviz.py
    :language: python
    :start-at: params = np
    :end-at: get_random_orthonormal_vector(dir1)

Finally, let's generate the data for this particular slice and plot it.

.. literalinclude:: ../examples/tutorials/orqviz.py
    :language: python
    :start-at: scan2D_result =
    :end-at: scan_result(scan2D_result)

This code results in the following plot:

.. image:: images/cost_function_landscape.png
    :width: 50%
    :align: center

The plot shows the cost function landscape in the region of interest. The color of each point corresponds to the value of the cost function at that point. The colorbar on the right shows the range of values of the cost function.

FAQ
===

**What are the expected type and shape for the parameters?**
Parameters should be of type ``numpy.ndarray`` filled with real numbers. The shape of the parameters can be arbitrary, as long as ``numpy`` allows it, i.e., you cannot have inconsistent sizes per dimension.

**What is the format of the loss_function that most orqviz methods expect?**
We define a ``loss_function`` as a function which receives only the parameters of the model and returns a floating point number. That value could for example be the cost function of an optimization problem, the prediction of a classifier, or the fidelity with respect to a fixed quantum state. All the calculation that needs to be performed to get to these values needs to happen in your function. Check out the above code as a minimal example.

**What can I do if my loss function requires additional arguments?**
In that case you need to wrap the function into another function such that it again receives only the parameters of the model. We built a wrapper class called ``LossFunctionWrapper`` that you can import from ``orqviz.loss_function``. It is a thin wrapper with helpful perks such as measuring the average evaluation time of a single loss function call, and the total number of calls.


Other Tutorials
===============

For more in-depth tutorials on using orqviz with different quantum libraries, check out the Jupyter notebooks in the `orqviz repository <https://github.com/zapatacomputing/orqviz/tree/main/docs/examples>`_.
