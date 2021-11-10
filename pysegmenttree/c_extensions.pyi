from typing import List, Optional

from ._abc import AbstractSegmentTree, T

class IntSegmentTree(AbstractSegmentTree):
    def __init__(self, source: List[T], func: Optional[str] = None):
        pass

class FloatSegmentTree(AbstractSegmentTree):
    def __init__(self, source: List[T], func: Optional[str] = None):
        pass
