try:
    from ._pysegmenttree import SegmentTree
except ImportError:  # pragma: no cover
    from ._pysegmenttree_py import SegmentTree

__version__ = "0.1.0"
__all__ = ["SegmentTree"]
