=========
Reference
=========

.. module:: pysegmenttree


stree
=====

.. function:: stree(source: List[T], func: Union[Callable[[T, T], T]], QueryFunction] = QueryFunction.SUM) -> AbstractSegmentTree

    Function that returns the best suitable version of the segment tree for the given input.

    .. note::
        To use all advantages of c-api extensions, you should use :class:`QueryFunction` enum memeber in `func` argument.

    >>> st = stree([0, 1, 2, 3], func=QueryFunction.MIN)
    >>> type(st)
    <class 'pysegmenttree.c_extensions.IntSegmentTree'>

    But if you pass :func:`min` the slower version of the tree will be used, so be careful.

    >>> st = stree([0, 1, 2, 3], func=min)
    >>> type(st)
    <class 'pysegmenttree._pysegmenttree_py.PySegmentTree'>

    The same is true for the `float` trees.

    >>> st = stree([0.0, 1.0, 2.0, 3.0])
    >>> type(st)
    <class 'pysegmenttree.c_extensions.FloatSegmentTree'>



QueryFunction
=============
.. class:: QueryFunction

    .. autoattribute:: SUM
    .. autoattribute:: MIN
    .. autoattribute:: MAX

    Enum representing query functions that can be used to build segment trees using c-api extensions.



PySegmentTree
=============

.. class:: PySegmentTree(source: List[T], func: Union[Callable[[T, T], T]], QueryFunction] = QueryFunction.SUM)

    Creates a pure python segment tree instance.

    **func** is a function that will be used in `query` method.
    Must be either a function with two arguments `T`, returning `T` or the :class:`QueryFunction` enum member.

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

    - **func** argument in the constructor has `str` type and must be one of the :class:`QueryFunction` enum values ('sum', 'min', ...).
    - Raises :exc:`OverflowError` if any element exceeds `long long` type range.
    - Much faster than :class:`PySegmentTree`.


FloatSegmentTree
================

.. class:: FloatSegmentTree(source: List[float], func: Optional[str] = None)

    Same as :class:`IntSegmentTree`, except it uses `double` C-type under the hood.
