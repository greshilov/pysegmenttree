import segment_tree
import segmenttree
import segtree

import pysegmenttree
from pysegmenttree.test_utils import Vec2D


class ThinWrapper:
    LIB = None
    MAX_CONTAINER_SIZE = float("inf")
    SUPPORTED_TYPES = [int, float, Vec2D]

    def __init__(self, source, function):
        if len(source) > self.MAX_CONTAINER_SIZE:
            raise NotImplementedError()
        if type(source[0]) not in self.SUPPORTED_TYPES:
            raise NotImplementedError()

    def build_tree(self):
        raise NotImplementedError()

    def query(self, start: int, end: int):
        raise NotImplementedError()

    def update(self, index: int, value):
        raise NotImplementedError()


class Segment_TreeWrapper(ThinWrapper):
    LIB = "segment_tree"
    MAX_CONTAINER_SIZE = 100_000
    SUPPORTED_TYPES = [int, float]

    def __init__(self, source, function):
        super().__init__(source, function)
        self.tree = segment_tree.SegmentTree(source)

    def query_sum(self, start: int, end: int):
        return self.tree.query(start, end, "sum")

    def query_min(self, start: int, end: int):
        return self.tree.query(start, end, "max")

    def query_max(self, start: int, end: int):
        return self.tree.query(start, end, "max")

    def update(self, index: int, value):
        return self.tree.update(index, value)


class SegmentTreeWrapper(ThinWrapper):
    LIB = "segmenttree"
    MAX_CONTAINER_SIZE = 100_000
    SUPPORTED_TYPES = [int, float]

    def __init__(self, source, function):
        super().__init__(source, function)
        self.tree = segmenttree.SegmentTree(0, len(source) - 1)
        for i, val in enumerate(source):
            self.tree.add(i, i, val)

    def query_sum(self, start: int, end: int):
        return self.tree.query_sum(start, end)

    def query_min(self, start: int, end: int):
        return self.tree.query_max(start, end)

    def query_max(self, start: int, end: int):
        return self.tree.query_max(start, end)


class CSegmentTreeWrapper(ThinWrapper):
    LIB = "c-segment-tree"
    SUPPORTED_TYPES = [int]

    def __init__(self, source, function: str):
        super().__init__(source, function)
        self.tree = segtree.Segtree(source, function)

    def query_sum(self, start: int, end: int):
        return self.tree.sum(start, end)

    def query_min(self, start: int, end: int):
        return self.tree.min(start, end)

    def query_max(self, start: int, end: int):
        return self.tree.max(start, end)

    def update(self, index: int, value):
        return self.tree.update(index, value)


class PySegmentTreeWrapper(ThinWrapper):
    LIB = "pysegmenttree"

    FUNCTION_TRANSLATOR = {
        "sum": None,
        "min": min,
        "max": max,
    }

    def __init__(self, source, function: str):
        super().__init__(source, function)
        self.tree = pysegmenttree.stree(source, self.FUNCTION_TRANSLATOR[function])

    def query_sum(self, start: int, end: int):
        return self.tree.query(start, end + 1)

    def query_min(self, start: int, end: int):
        return self.tree.query(start, end + 1)

    def query_max(self, start: int, end: int):
        return self.tree.query(start, end + 1)

    def update(self, index: int, value):
        return self.tree.update(index, value)
