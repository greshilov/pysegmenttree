from typing import Callable, List, Optional

from ._abc import AbstractSegmentTree, T
from ._pysegmenttree_py import PySegmentTree

try:
    from .c_extensions import FloatSegmentTree, IntSegmentTree

    C_EXTENSIONS = True
except ImportError:
    C_EXTENSIONS = False


def stree(
    source: List[T], func: Optional[Callable[[T, T], T]] = None
) -> AbstractSegmentTree:
    """
    Automatically detects the type of input container, and uses the
    fastest possible segment tree implementation.
    """
    try:
        if C_EXTENSIONS:
            if source and isinstance(source[0], int) and func is None:
                return IntSegmentTree(source)
            if source and isinstance(source[0], float) and func is None:
                return FloatSegmentTree(source)
    except OverflowError:
        pass

    return PySegmentTree(source=source, func=func)
