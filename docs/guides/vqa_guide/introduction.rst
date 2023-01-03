.. _vqa_structure:

=================================
Introduction to VQAs in Orquestra
=================================

.. _vqa_intro:

Introduction to VQAs
=====================

The central idea of VQAs is to use an **optimizer** to find the best quantum circuit to do the job at hand.

We start with an **ansatz** - this is a "template" for generating circuits, which has tunable parameters.

The optimizer selects the parameters by minimizing a **cost function** obtained from the output of the current quantum program.

To **estimate** the value of the cost function for given set of parameters, we need to run (or simulate) the quantum program.


Our :ref:`Optimizers guide <optimizers_guide>` contains introduction to general features of optimization, so this guide focuses on :ref:`ansatzes <ansatzes_guide>` and :ref:`estimators <estimators_guide>`, which are more specific to quantum algorithms. For a more complete, yet approachable discussion, see `Michał's blogpost <https://www.mustythoughts.com/vqas-how-do-they-work>`_.


.. _vqa_basics:

The Basics
==========

Our framework provides a fair amount of flexibility in how one can approach creating and tweaking their own variational algorithm. However, this comes at the price of not being the most intuitive tool to start with. That's why we have introduced simplified interfaces for some of the most commonly used algorithms: Variational Quantum Eigensolver (VQE), Quantum Approximate Optimization Algorithm (QAOA) and Quantum Circuit Born Machine (QCBM). 

They all work similarly, but each is a little bit different - that's why we will describe in details only the first one (VQE) and for QAOA and QCBM just focus on how they're different from VQE.


VQE
---

.. note::

   This guide does not provide any sort of theoretical introduction to VQE. If you are not familiar with the algorithm itself, you might want to start by reading `this blogpost <https://www.mustythoughts.com/variational-quantum-eigensolver-explained>`_. You might also want to read the original `paper introducing VQE <https://arxiv.org/abs/1304.3061>`_

For most scenarios, the easiest way to use VQE with orquestra is via means of the :class:`VQE <orquestra.vqa.algorithms.VQE>` class. Instances of this class group together several different objects needed for running VQE, and expose convenience methods for finding optimal params and constructing cost functions. The :class:`VQE <orquestra.vqa.algorithms.VQE>` class also contains a convenience :meth:`default <orquestra.vqa.algorithms.VQE.default>` method which simplifies creation of its instances even further. Since the :meth:`default` method covers most of the use cases, we'll start by describing its arguments:

- :code:`hamiltonian`: a Hamiltonian of the problem given in :class:`PauliRepresentation <orquestra.quantum.operators.PauliRepresentation>`.
- :code:`ansatz`: ansatz defining how the parametrized circuits should be constructed.
- :code:`use_exact_expectation_values`: boolean determining if computation of expectation values should be done exactly, or estimated using sampling. Exact calculation is only possible when using a simulator!
- :code:`grouping`: optional string determining how grouping of terms in Hamiltonian is done. Either "greedy" or "individual".
- :code:`shots_allocation`: optional string determining how the shots are allocated. Either "uniform" or "proportional".
- :code:`n_shots`: number of shots used when estimating expectation values. Should be provided only if you specified :code:`use_exact_expectation_values=False`.

The :class:`VQE <orquestra.vqa.algorithms.VQE>` objects constructed in this way will use :class:`ScipyOptimizer <orquestra.opt.optimizers.ScipyOptimizer>` with "L-BFGS-B" optimization method.

In the example below, we construct a two-qubit VQE with Hardware Efficient Quantum Compiling Ansatz.

.. literalinclude:: ../../examples/guides/vqa_guide.py
  :language: python
  :start-after: Default VQE
  :end-before: # --- End

Now, in order to optimize it, we need an instance of some :class:`CircuitRunner <orquestra.quantum.api.CircuitRunner>`. For our example, we will construct a :class:`SymbolicSimulator <orquestra.quantum.runners.SymbolicSimulator>`. Finally, we run the :meth:`VQE.find_optimal_params <orquestra.vqa.algorithms.VQE.find_optimal_params>` method to obtain the results.

.. literalinclude:: ../../examples/guides/vqa_guide.py
  :language: python
  :start-after: # Optimizing default VQE
  :end-before: # --- End

.. code-block:: text

   opt_value=-0.9999999903697773
   opt_params=[8.68771769e-01 1.80528665e+00 2.15249204e+00 2.77605314e+00
    1.57081967e+00 3.14161674e+00 1.28392551e+00 1.66060268e+00
    2.34053047e+00 1.66618319e+00 1.40691211e-03 1.66622948e+00]

Notice, that you can obtain raw cost function from :class:`VQE` object. This might be useful for instance if you want to compare the obtained result with some other pre-existing solution that you have. Here we verify that the returned optimal value indeed corresponds to the returned params.

.. note::
   This example only works because we opted for exact computation of expectation values. Obviously,
   if the cost function requires sampling, the results might differ even for the same params.

.. literalinclude:: ../../examples/guides/vqa_guide.py
  :language: python
  :start-after: # Cost function
  :end-before: # --- End

.. code:: text

   True

As already stated, the default method of constructing :class:`VQE` objects is sufficient for most use cases. Let us now describe how to deal with those cases where the :meth:`default` method is not sufficient.

First of all, there are two ways of customizing the :class:`VQE` objects. You can either construct a new instance using normal initializer of :class:`VQE` object, or start with a default implementation, and then customize it using one of the :meth:`replace_xyz` methods. We start with the first method. But before we do, let us explain some simplifications made by the :meth:`default` method.

As you probably guessed, the "uniform" and "proportional" are not the only possible methods of allocating shots. Similarly, there might be other ways of grouping not covered by the :meth:`default` method. Of course, one could think we can extend the :meth:`default` method to accept more and more options. However, such code would be rather unpleasant to maintain and confusing to use. And what about your custom methods of allocating shots or grouping? In Orquestra, both of those tasks are implemented as :class:`orquestra.quantum.api.EstimationPreprocessor` and under the hood, the :meth:`default` method constructed them for you.

When using the :meth:`__init__` method of :class:`VQE`, you need to specify the preprocessors yourself. The preprocessors already available in Orquestra are available in :mod:`orquestra.vqa.grouping` and :mod:`orquestra.vqa.shot_allocation`. Another difference is that you need to specify the optimizer explicitly. In the example below, we construct a :class:`VQE` object with the same ansatz and hamiltonian as previously, but this time we choose to estimate expectation values by averaging. We then optimize it using the same runner as before.

.. literalinclude:: ../../examples/guides/vqa_guide.py
  :language: python
  :start-after: # VQE initializer
  :end-before: # --- End

One can also construct new VQE objects based off the already existing ones. To do so, one can use one of the :meth:`replace_xyz` methods, where :code:`xyz` stands for an attribute you want to replace. The important thing to notice is that all those methods are not mutating an existing object, but creating a new one with one attribute replaced and the others preserved.

We can verify this is indeed the case by inspecting objects returned by :meth:`replace_xyz` methods and comparing them to the original objects. for instance:

.. literalinclude:: ../../examples/guides/vqa_guide.py
  :language: python
  :start-after: # replace optimizer
  :end-before: # --- End

.. code:: text

    Ansatzes equal? True
    Grouping equal? True
    Estimation method equal? True
    Hamiltonians equal? True
    Optimizers equal? False
    First optimization method: L-BFGS-B
    Second optimization method: COBYLA

..  note::

   Arguments to :meth:`replace_xyz` follow the same semantics as the arguments to :code:`orquestra.vqa.algorithms.vqe.VQE.__init__` method. In particular, all preprocessors has to be passed as callables and not strings.

To find all the attributes of :class:`VQE <orquestra.vqa.algorithms.vqe.VQE>` that can be replaced in this way, refer to the class documentation.

Implementations of QAOA and QCBM algorithms follow the same design principles as VQE. In particular:

* Their instances can be constructed using either simplified :meth:`default` method, or with more control using their initializer
* They store optimizer as one of the attributes. The optimization is done by calling
  :meth:`find_optimal_params`
* The instances are supposed to be treated as immutable, but new instances can be constructed by replacing respective attributes using :meth:`replace_xyz` methods.

Knowing those similarities, in the rest of the introduction we will only highlight differences between Orquestra's implementation of VQE and QAOA/QCBM.

QAOA
----

.. note::

   The QAOA algorithm was introduced in `this <https://arxiv.org/abs/1411.4028>`_ papier. If you are not familiar with the algorithm, there is a lot of introductory texts available online, e.g. `here <https://www.mustythoughts.com/quantum-approximate-optimization-algorithm-explained>`_

The Quantum Approximate Optimization Algorithm is implemented by the :class:`QAOA <orquestra.vqa.algorithms.QAOA>` class. The  :meth:`default <orquestra.vqa.algorithms.QAOA.default>` method constructs :class:`QAOA` object using Fahri ansatz with specified number of layers. An important detail differing :class:`QAOA` from :class:`VQE` is lack of :code:`grouping` or :code:`shot_allocation` parameters, which just don't make sense for QAOA algorithm. Using class' initializer directly, one can further customize what ansatz is used.


QCBM
----

.. note::

   See `here <https://arxiv.org/abs/1804.04168>`_ or `here <https://arxiv.org/abs/1801.07686>`_ for papers describing QCBM.

The Quantum Circuit Born Machine algorithm is implemented by the :class:`QCBM <orquestra.vqa.algorithms.QCBM>` class. Contrary  to the previously discussed algorithms, in QCBM one cannot customize what ansatz is used. The :meth:`default <orquestra.vqa.algorithms.QAOA.default>` allows for configuring target measurement distribution and number of layers. One can also configure estimation method, just like in case of QAOA and VQE. Using :class:`QAOA <orquestra.vqa.algorithms.QCBM>` initializer allows for more advanced customization of estimation method, but otherwise doesn't differ from the :meth:`default` method.

Details of running VQAs
=======================

Honestly, most of the time you would only need the default classes - as you have seen above, there's plenty you can do with those pre-built templates. However, in case you want to really experiment with the details of these algorithms configuration or just are curious how we've built them, please keep reading.

The process for running a VQA algorithm can be outlined in 5 steps:

1. Define initial ingredients: :class:`Ansatz <orquestra.vqa.api.ansatz.Ansatz>`, :class:`WavefunctionSimulator <orquestra.quantum.api.wavefunction_simulator.WavefunctionSimulator>` or :class:`CircuitRunner <orquestra.quantum.api.circuit_runner.CircuitRunner>` and :class:`Optimizer <orquestra.opt.api.Optimizer>`.
2. Create an :class:`EstimationTaskFactory <orquestra.quantum.api.estimation.EstimationTasksFactory>` factory using :class:`Ansatz <orquestra.vqa.api.ansatz.Ansatz>`.
3. Call :func:`create_cost_function <orquestra.vqa.cost_function.cost_function.create_cost_function>` using the :class:`EstimationTaskFactory <orquestra.quantum.api.estimation.EstimationTasksFactory>`  and :class:`WavefunctionSimulator <orquestra.quantum.api.wavefunction_simulator.WavefunctionSimulator>` or :class:`CircuitRunner <orquestra.quantum.api.circuit_runner.CircuitRunner>`.
4. Call :meth:`optimizer.minimize <orquestra.opt.api.Optimizer.minimize>` using the :class:`CostFunction <orquestra.opt.api.cost_function.CostFunction>` to get optimized parameters.
5. Call :meth:`ansatz.get_executable_circuit <orquestra.vqa.api.ansatz.Ansatz.get_executable_circuit>` with optimized parameters to get the quantum program.


Let's go through an example where a vqa is used to solve the maxcut problem. See the :ref:`qaoa tutorial <qaoa_tutorial>` for a more hands-on example how to use VQAs with Orquestra Core

.. literalinclude:: ../../examples/guides/vqa_guide.py
  :language: python
  :start-after: # Detailed VQA
  :end-before: # --- End

We'll go through the steps as they were outlined above:

1. The :class:`Ansatz <orquestra.vqa.api.ansatz.Ansatz>`, :class:`WavefunctionSimulator <orquestra.quantum.api.wavefunction_simulator.WavefunctionSimulator>` or :class:`CircuitRunner <orquestra.quantum.api.circuit_runner.CircuitRunner>` and :class:`Optimizer <orquestra.opt.api.Optimizer>` can be defined independently of one another.
2. As explained in :ref:`estimators guide <estimators_guide>`, the :class:`EstimationTaskFactory <orquestra.quantum.api.estimation.EstimationTasksFactory>` tells the quantum computer how to construct a circuit. It therefore will always take an :class:`Ansatz <orquestra.vqa.api.ansatz.Ansatz>` as an argument.
3. As explained briefly above, VQA uses a quantum computer to estimate the value of the cost function. So to create our cost function we would need the method of constructing circuits for our cost function (``estimation_task_factory``) and a simulator or runner to execute them.
4. Now that we have the cost function, we minimize if using the optimizer. This step generally takes the longest to run.
5. Obtain the final circuit by substituting the optimized parameters into the ansatz.

And that's it! once these steps are completed we have now finished our variational quantum algorithm in ``orquestra``!



Libraries structure
===================

Most of the code associated directly with VQAs lives in the `orquestra-vqa <https://github.com/zapatacomputing/orquestra-vqa>`_ repository. Some of these are not worth separate guides, but it might be useful for you to know what we have.

So here's a short list of what's in `orquestra-vqa`:

- ansatzes - see :ref:`ansatzes guide <ansatzes_guide>`
- estimation - see: :ref:`estimation guide <estimators_guide>`
- grouping - see: :ref:`estimation guide <estimators_guide>`
- openfermion - some utility tools to make it easier to work with `OpenFermion <https://quantumai.google/openfermion>`_ within Orquestra.
- optimizers - we have some VQA-specific optimizers such as Layer-by-layer optimizer, `Fourier <https://journals.aps.org/prx/abstract/10.1103/PhysRevX.10.021067>`_ or `R-QAOA <https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.125.260505>`_ . See: :ref:`optimizers guide <optimizers_guide>` for more details.
- parameter initialization - `Interp method <https://journals.aps.org/prx/abstract/10.1103/PhysRevX.10.021067>`_
- shot allocation - see: :ref:`estimation guide <estimators_guide>`
