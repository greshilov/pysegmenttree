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
