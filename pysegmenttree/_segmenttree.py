from typing import List, Optional, Union

from ._abc import AbstractSegmentTree, Func, QueryFunction, T
from ._pysegmenttree_py import PySegmentTree

try:
    from .c_extensions import FloatSegmentTree, IntSegmentTree

    C_EXTENSIONS = True
except ImportError:
    C_EXTENSIONS = False


def stree(
    source: List[T], func: Union[Func, QueryFunction] = QueryFunction.SUM
) -> AbstractSegmentTree:
    """
    Automatically detects the type of input container, and uses the
    fastest possible segment tree implementation.
    """
    try:
        if C_EXTENSIONS and isinstance(func, QueryFunction):
            if source and isinstance(source[0], int):
                return IntSegmentTree(source, func=func.value)
            if source and isinstance(source[0], float):
                return FloatSegmentTree(source, func=func.value)
    except OverflowError:
        pass

    return PySegmentTree(source=source, func=func)
