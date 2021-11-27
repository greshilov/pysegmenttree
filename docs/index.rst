.. pysegmenttree documentation master file, created by
   sphinx-quickstart on Sat Nov 13 22:43:44 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pysegmenttree
=============
**Segment tree** is a data structure to perform efficient range queries over an array.

For example, finding the sum/minimum/maximum of the arbitrary continuous interval in `O(Log[N])` time.
Logariphmic time complexity is achieved by storing the original input data in a tree like data structure with some additional precalculated data.

This library implementation is primarly inspired by this beatiful article_.

.. _article: https://codeforces.com/blog/entry/18051


Library installation
--------------------

.. code-block:: bash

   $ pip install pysegmenttree


Quick Start
-----------

.. code-block:: python

   >> from pysegmenttree import stree

   # Build the tree
   # 'sum' function is used by default
   >> tree = stree([5, 1, 9, 4, 5, 11])

   # Find sum on the interval [1, 4)
   >> tree.query(1, 4)
   14

   # Set element with index 3 to 6
   >> tree.update(3, 6)
   >> tree.query(1, 4)
   16


Advanced usage
--------------
There are three predefined query functions available (:class:`QueryFunction`) that can be used with `int` or `float` trees.

.. code-block:: python

   >> from pysegmenttree import stree, QueryFunction
   >> tree = stree([5, 1, 9, 4, 5, 11], func=QueryFunction.MIN)

   # Find min on the interval [1, 4)
   >> tree.query(1, 4)
   1

Plain python functions are also suitable, but with them c-extensions will **not** be used.

.. code-block:: python

   # Warning! A slow version of segment tree will be used.
   >> tree = stree([5, 1, 9, 4, 5, 11], func=min)
   >> tree.query(1, 4)
   1

Example with user-defined class :class:`Vec2D`.

.. code-block:: python

   >> from pysegmenttree import stree
   >> from pysegmenttree.test_utils import Vec2D
   # List of 2D vectors
   >> tree = stree([Vec2D(0, 1), Vec2D(5, -2), Vec2D(-2, 3)], func=max)
   # Find the vector of maximum length on the interval [0, 2)
   >> tree.query(0, 2)

   Vec2D(x=5, y=-2)


Methods complexity
------------------

Considering that input array has `N` elements.


.. table::
   :widths: auto

   ===========  ===============  ================
   Method       Time complexity  Space complexity
   ===========  ===============  ================
   constructor  O(N)             O(2*N)
   query        O(Log[N])        O(1)
   update       O(Log[N])        O(1)
   ===========  ===============  ================


Source code
-----------

The project is hosted on GitHub_.

.. _GitHub: https://github.com/greshilov/pysegmenttree


.. toctree::
   pysegmenttree
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
