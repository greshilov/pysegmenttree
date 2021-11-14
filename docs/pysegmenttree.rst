=========
Reference
=========

.. module:: pysegmenttree


stree
=====

.. function:: stree(source: List[T], func: Optional[Callable[[T, T], T]] = None) -> AbstractSegmentTree

    Function that returns a best suitable version of the segment tree for the given input.

    >>> st = stree([0, 1, 2, 3])
    >>> type(st)
    <pysegmenttree.c_extensions.IntSegmentTree object at 0x7f4b0c8dfc50>

    >>> st = stree([0.0, 1.0, 2.0, 3.0])
    >>> type(st)
    <pysegmenttree.c_extensions.FloatSegmentTree object at 0x7f4b0c8dfdb0>

    >>> st = stree([0, 1, 2, 3], func=min)
    >>> type(st)
    <pysegmenttree._pysegmenttree_py.PySegmentTree object at 0x7f4b0c9a18e0>


PySegmentTree
=============

.. class:: PySegmentTree(source: List[T], func: Optional[Func] = None)

    Creates a segment tree instance.

    **func** is a function that will be used in `query` method.
    Must be a function with two arguments `T`, returning `T`(Type interface is `Callable[[T, T], T]`).

    >>> st = PySegmentTree([1.5, 1, 0, 2], func=min)

    .. method:: len(st)

       Return the number of items in segment tree *st*.

       >>> len(st)
       4


    .. method:: query(start: int, end: int) -> Optional[T]

       Performs a query operation on the interval [**start**, **end**) with the function chosen during the creation.
       Note, that **end** is not included. Behaviour is replicated from the python slice operator.

       >>> st.query(0, 2)
       1
       >>> st.query(0, 4)
       0


    .. method:: update(i: int, value: T)

       Set i-th element of the tree to the specified value **value**.

       >>> st.update(0, -100)
       >>> st.query(0, 2)
       -100


IntSegmentTree
==============

.. class:: IntSegmentTree(source: List[int], func: Optional[str] = None)

    Typed version of the :class:`PySegmentTree` implemented in C using `long long int` type.
    The behavior is the same as for :class:`PySegmentTree` except few moments:

    - **func** argument in the constructor has `str` type and currently doesn't affect anything. This type of tree is always `sum` tree.
    - Raises :exc:`OverflowError` if any element exceeds `long long` type range.
    - Much faster than :class:`PySegmentTree`.


FloatSegmentTree
================

.. class:: FloatSegmentTree(source: List[float], func: Optional[str] = None)

    Same as :class:`IntSegmentTree`, except it uses `double` C-type under the hood.
