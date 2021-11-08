from typing import Optional, Callable, List

from ._abc import AbstractSegmentTree, T
from ._pysegmenttree_py import PySegmentTree

try:
    from .c_extensions import IntSegmentTree

    C_EXTENSIONS = True
except ImportError:
    C_EXTENSIONS = False


def stree(
    source: List[T], func: Optional[Callable[[T, T], T]] = None
) -> AbstractSegmentTree:
    try:
        if C_EXTENSIONS:
            if source and isinstance(source[0], int) and func is None:
                return IntSegmentTree(source)
    except OverflowError:
        pass

    return PySegmentTree(source=source, func=func)
