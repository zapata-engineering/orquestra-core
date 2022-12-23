.. _optimizers_guide:

================
Optimizers guide
================

Optimization (i.e. ability to minimize a scalar function) lies at the heart of scientific computing
and its applications. For instance, being able to minimize a cost function is crucial for
Variational Quantum Algorithms (VQAs).

Optimization is nothing new, and there exists plethora of ready to use libraries with various
optimizers. So what new can Orquestra bring to the table? The answer, as usually with Orquestra,
is unification. The `orquestra-opt` package defines interfaces for all things related to
optimization and provides implementation of many existing optimizers.


What this guide covers
======================
This guide will introduce you to everything you need to know to optimize scalar functions using
`orquestra-opt` package. In particular we'll discuss:

- What functions can be minimized? Definition of cost function.
- Gradients, and how to add them to your cost function.
- Orquestra's approach for implementing optimization algorithms - the
  :class:`Optimizer <orquestra.opt.api.Optimizer>` interface.
- How to record history of evaluation of the cost function.
- List of currently available optimizers.


Cost functions
==============

Before we start optimizing, we need to know what can be optimized. In Orquestra, we deal only with
minimization of functions of the form :math:`f:\mathbb{R}^N \to \mathbb{R}`. Throughout the
codebase, such functions are called the *cost functions*.

All optimizers expect that the arguments to cost functions are stored as a single vector in a 1-D
numpy arrays. Suppose you want to create the following cost function:
:math:`f(x, y, z) = x^2 + y^2 + z^2`. Out of the two natural ways of defining it in Python, the
second one is the one expected by Optimizers:

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # Definition of cost function
  :end-before: # --- End

.. note::
   Remember that the argument to your cost function should be called `parameters`. While
   it makes no difference for most optimizers at runtime, it makes your function match
   structurally to the :class:`CostFunction <orquestra.opt.api.CostFunction>` protocol expected
   by Optimizers.

Adding gradients
================
Some optimization methods use gradients to move across the optimization landscape in the
correct direction. You can enrich your cost function with gradient in several ways.

To start with, cost function with gradients are just normal cost functions having additional
`gradient` attribute. This attribute should also be a callable returning gradient
of you function at a given point. Hence, one possible way of defining a cost function with
gradient is to just write a class with `__call__` method and a gradient attribute.

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # Cost function with gradient as a class
  :end-before: # --- End

For some cases, like in the example above, defining a whole class just to add a gradient
to your function is an overkill. There has to be a simpler way, right? Right. You can use
a :class:`FunctionWithGradient <orquestra.opt.api.FunctionWithGradient>` wrapper to combine
your cost function and another function defining its gradient.

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # FunctionWithGradient
  :end-before: # --- End

There are some cases when you can't define the gradient analytically. In such cases, it is
possible to use some approximation methods to compute it. One possibility is to use
finite differences method as demonstrated in the example below.

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # finite difference
  :end-before: # --- End

The :func:`finite_differences_gradient <orquestra.opt.gradients.finite_differences_gradient>`
function itself returns a function that approximates its input gradient. The second parameter
controls the step size in the approximation.

The optimizers
==============

Knowing what functions can be minimized, let us now take a closer look at how to minimize them.
The objects responsible for the whole process are implementations of the :class:`Optimizer`
interface. Every Optimizer implements the :meth:`minimize <orquestra.opt.api.Optimizer.minimize>`
method that accepts the following parameters:

- `cost_function`: the cost function to be optimized.
- `initial_params`:  the initial guess for the optimal parameters. Its dimension should
  match the dimension of the first argument of the `cost_function`.
- `keep_history`: a boolean determining if history of function evaluations should be kept or
  not. The default is :code:`False`, as storage of evaluation history might eat up a lot of
  memory.

Of course, optimizers have other methods as well. Those methods are relevant mainly when we
are implementing our own optimizers, and hence we defer discussing them until later.

But wait, surely some optimization methods require additional parameters and some fine tuning.
Where do those parameters go, if `minimize` only accepts the arguments listed above?
That's a very good question. Similarly as we have done with other interfaces, we moved all
optimizer-specific parametrization into Optimizers'
:meth:`__init__ <orquestra.opt.api.Optimizer.__init__>` method. This way, once the
optimizers are constructed, they can be used interchangeably with one another.

Let us illustrate how the optimizers work. In the example below, we construct two optimizers
and we use them to optimize our sum of squares. We then print the results.

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # Basic optimization
  :end-before: # --- End

The results might differ slightly, but here is what we got when running the example.

.. code-block:: text

        history: []
           nfev: 3
            nit: 2
     opt_params: array([0., 0., 0.])
      opt_value: 0.0

.. code-block:: text

        history: []
           nfev: None
            nit: 1000
     opt_params: array([ 5.11528491e-21, -5.11528491e-21,  5.38660015e-21])
      opt_value: 8.134774054521418e-41


As we can see, once constructed, :class:`ScipyOptimizer <orquestra.opt.optimizers.ScipyOptimizer>` and :class:`SimpleGradientDescent <orquestra.opt.optimizers.SimpleGradientDescent>` optimizer could be used in the same way. The output of the :meth:`minimize` method is a Scipy `OptimizeResult <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html>`_ object containing the following fields:

- `opt_params`: optimal parameters found
- `opt_value`: value of the cost function at the optimal point (i.e.
  :code:`cost_function(opt_params)`
- `nfev`: number of function evaluation during the optimization process
- `nit`: number of iterations
- `history`: history of evaluation of our cost function.

The `history` field is empty in both cases, since we haven't passed :code:`keep_history=True`.
Both optimizers did well and found optimal or near-optimal solution, although we have to admit
that the optimization task we gave them wasn't too hard. The
:class:`SimpleGradientDescent` haven't evaluated our function even once during the
optimization, which is expected - it only uses gradient to guide the optimization.
The :class:`ScipyOptimizer` used two iterations to reach the global minimum, while the second
optimizer used 1000 which is expected, as it was explicitly instructed to do so.

Of course, all of the fields discussed above can be accessed programmatically during program
execution, for instance:

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # Using OptimizeResult
  :end-before: # --- End

Storing evaluation history
==========================

In the simplest case, the evaluation history can be kept by passing :code:`keep_history=True`.
Let us first see how this history info is stored.

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # keep_history
  :end-before: # --- End

The output could look as follows

.. code:: text

   [HistoryEntry(call_number=0, params=array([ 1. , -1. ,  0.5]), value=2.25), HistoryEntry(call_number=1, params=array([ 0.33333333, -0.33333333,  0.16666667]), value=0.2499999999999999), HistoryEntry(call_number=2, params=array([0., 0., 0.]), value=0.0)]

We can observe that:

- Stored history info is a list.
- This list contains items of type :class:`HistoryEntry`
- Each such entry contains the following:

  - call number: sequential number of call to the cost function
  - params: parameters with which the cost function was called
  - value: current value of the cost function

Of course, as usually, we can access all these info programmatically. For instance, this
is how you can extract only the sequence of values of the cost function:

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # history_entry
  :end-before: # --- End

.. code:: text

   [2.25, 0.2499999999999999, 0.0]

For many applications, this is everything that you need to know. However, there are some caveats.

- What if I want only *some* evaluations to be saved? For instance, if we suspect there will be
  one million calls, maybe it is enough to save memory and save only every tenth entry?
- What if I want to store some more info? Maybe our cust function produces some other artifacts
  that are worth saving for the purpose of further analysis?

The :code:`orquestra-opt` package contains everything you need to accomplish those goals. To
properly discuss how to do this, we need to introduce a new concept. Enter *recorders*.

Recorders
---------

Simply put, recorders are callable objects that wrap the cost function and pass through
all calls. However, they also store the history of invocations.

Recorder for a given function is created by calling a :func:`recorder` function on it.
This function chooses the appropriate recorder type and returns its instance. Before going any
further, let us check on some simple function that recorder created in this way indeed
behaves as expected.

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # basic recorder
  :end-before: # --- End

Looking at the output we see that the recorder correctly stored the call that we made.

.. code:: text

   [0.93765228 0.69672247 0.68539876]
   [HistoryEntry(call_number=0, params=array([0.93765228, 0.69672247, 0.68539876]), value=1.8343854651854021)]

Ok, what about gradient? It turns out that if your cost function has a gradient it will be
recorder as well.

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # recording gradient
  :end-before: # --- End

.. code:: text

   [2. 4. 6.]
   [HistoryEntry(call_number=0, params=array([1, 2, 3]), value=array([2., 4., 6.]))]

As you can see from the output, the recorder successfully captured evaluation of the
gradient.

The next thing we need to learn is how to conditionally store only selected evaluations.
All recorders have an attribute called :code:`save_condition`. It is a boolean function that
accepts value, parameters and call number and returns :code:`True` if and only
if it this particular evaluation should be saved. The default save condition is a dummy
function called :func:`always <orquestra.opt.api.always>` which always returns true. Another function,
:func:`every_nth <orquestra.opt.api.every_nth>`, saves only every nth evaluation. Here's how it works:

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # every nth
  :end-before: # --- End

.. code:: text

   [0.0, 48.0, 192.0, 432.0, 768.0]

As can bee seen, the recorder saved only every 4-th evaluation of the cost function.

Let's conclude this part by demonstrating custom save conditions. In this, rather artificial,
scenario, we save only these evaluations for which second coordinate is greater than the first one.

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # custom save condition
  :end-before: # --- End

.. code:: text

   [HistoryEntry(call_number=0, params=array([1, 2, 0]), value=5)]


Saving artifacts
----------------

There is even more advanced usage of the recorders. As already stated we can store arbitrary
artifacts. But how does the recorder know what to save? Well it doesn't, but it exposes
a callback for your cost function that can be used to store anything it wants.

To illustrate, let us modify our sum of squares so that it saves the indices sorting its
input. E.g. if the input was [3, 5, 0] it should save vector [2, 0, 1]).


.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # storing artifacts
  :end-before: # --- End

.. code:: text

   HistoryEntryWithArtifacts(call_number=0, params=array([0.83539053, 0.60336326, 0.68849924]), value=1.5359557618364512, artifacts={'order': array([1, 2, 0])})
   parameters: [0.83539053 0.60336326 0.68849924], order: [1 2 0]
   parameters: [0.77104168 0.88808436 0.82558708], order: [0 2 1]
   parameters: [0.45159923 0.5376592  0.14075176], order: [2 0 1]
   parameters: [0.93415374 0.78783696 0.35753713], order: [2 1 0]

We see that if our function stores artifacts, the entries stored in recorder's :code:`history`
attribute are of :class:`HistoryEntryWithArtifacts <orquestra.opt.history.recorder.HistoryEntryWithArtifacts>`
type, which has additional field called :code:`artifacts`. This field stores a dictionary of the
artifacts that your cost function saved for given evaluation.

Of course, there's no need for your cost function to store the same artifacts for each evaluation.
The stored dictionary is completely free-form, and you can store whatever you want.

.. note::

   This guide primarily focuses on optimization, and hence we only used recorders on
   cost functions. However, they work just as fine for arbitrary functions.

Using recorders with optimizers
-------------------------------

The previous section focused on using recorders as a standalone feature. We will now explore
how recorders can be used with optimizers.

If you take a closer look at the initializer of base :class:`Optimizer` class, you'll see
that it accepts a `recorder` argument. This argument is a factory, which means it should be a
callable that, when provided a cost function, returns a recorder. It defaults to
the :func:`recorder <orquestra.opt.history.recorder>` that we just discussed. We can replace it with
our own factory. The example below shows how to minimize the Rosenbrock function,
and record its evaluation using both the default :func:`recorder` and the custom one provided by us.

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # custom recorder
  :end-before: # --- End

.. code:: text

   [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76]

As can be seen, our optimizer saved only every second evaluation of the cost function when
we passed :code:`keep_history=True`. Under the hood, the optimizer constructed an instance
of the recorder according to the recipe that we specified.

The information presented so far should be enough for optimizing arbitrary cost function
and control how its evaluation history is stored. Let us now move to more advanced topics.

Creating your own optimizer
===========================

So far we only discussed using already existing optimizers. However, you might want to implement
an optimizer using some fancy optimization method that is not yet available in Orquestra.

The way it is done is by subclassing the :class:`Optimizer` class. At bare minimum,
your implementation has to include the :meth:`_minimize` method that implements the actual
minimization algorithm.

Optionally, you may also override the :meth:`_preprocess_cost_function` method. This method
is responsible for two things:

- validating the passed cost function, and raising an error if some problems are detected.
- wrapping/modifying the cost function to adapt it to use with the given optimizer.

For instance, the :meth:`_preprocess_cost_function` can make sure that the function has
a gradient if the optimizer requires it. Or it can add an approximate gradient, if the
cost function doesn't have one.

The following snippet may serve as a template for implementing your own optimizer.

.. literalinclude:: ../examples/guides/optimizers.py
  :language: python
  :start-after: # custom optimizer
  :end-before: # --- End


List of currently available optimizers
======================================

The table below lists the optimizers currently available in orquestra-opt.
Note that some optimizers are only available when the appropriate install extra is used, e.g. ``pip install orquestra-opt[qiskit]``.

.. list-table::
  :header-rows: 1
  :widths: 30 50 20
  
  * - Optimizer
    - Description
    - Install extra
  * - :class:`BasinHoppingOptimizer <orquestra.opt.optimizers.BasinHoppingOptimizer>`
    - An optimizer utilizing the `scipy.optimize.basinhopping <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.basinhopping.html>`_ method.
    -
  * - :class:`ScipyOptimizer <orquestra.opt.optimizers.ScipyOptimizer>`
    - Wrapper around `scipy.optimize.minimize <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html>`_ module. Provides optimizers such as Nelder-Mead, COBYLA, BFGS, and SLSQP.
    -
  * - :class:`SearchPointOptimizer <orquestra.opt.optimizers.SearchPointsOptimizer>`
    - An optimizer performing brute-force search over specified grid.
    -
  * - :class:`PSOOptimizer <orquestra.opt.optimizers.pso.PSOOptimizer>`
    - `Particle swarm <https://en.wikipedia.org/wiki/Particle_swarm_optimization>`_ optimizer.
    -
  * - :class:`QiskitOptimizer <orquestra.opt.optimizers.qiskit_optimizer.QiskitOptimizer>`
    - A wrapper around optimizers available in Qiskit, including ADAM, AMSGRAD, SPSA, and NFT.
    - :code:`qiskit`
  * - :class:`CMAESOptimizer <orquestra.opt.optimizers.cma_es_optimizer.CMAESOptimizer>`
    - A wrapper around the `Covariance Matrix Adaptation Evolution Strategy (CMA-ES) <https://cma-es.github.io/>`_ optimizer.
    - :code:`cma`
  * - :class:`ScikitQuantOptimizer <orquestra.opt.optimizers.scikit_quant_optimizer.ScikitQuantOptimizer>`
    - A wrapper around `scikit-quant <https://scikit-quant.readthedocs.io/en/latest/>`_ optimizers.
    - :code:`scikit-quant`