import operator
from typing import (
    Callable,
    List,
    Optional,
)

from ._abc import AbstractSegmentTree, T


class PySegmentTree(AbstractSegmentTree):
    def __init__(self, source: List[T], func: Optional[Callable[[T, T], T]] = None):
        self.func = func if func is not None else operator.add
        self.size = len(source)
        self.tree = [*[None] * self.size, *source]
        self._build()

    def _build(self):
        for i in range(self.size - 1, 0, -1):
            # Iteratively construct parent nodes using child ones
            self.tree[i] = self.func(self.tree[i << 1], self.tree[i << 1 | 1])

    def query(self, start: int, end: int) -> T:
        if start > end:
            raise IndexError(f"Invalid interval start > end ({start} > {end})")

        left, right = start + self.size, end + self.size
        res = None
        while left < right:
            if left & 1:
                res = (
                    self.func(res, self.tree[left])
                    if res is not None
                    else self.tree[left]
                )
                left += 1
            if right & 1:
                right -= 1
                res = (
                    self.func(res, self.tree[right])
                    if res is not None
                    else self.tree[right]
                )

            left >>= 1
            right >>= 1
        return res

    def update(self, i: int, value: T):
        if i > self.size - 1 or i < 0:
            raise IndexError("SegmentTree index out of range")

        indx = i + self.size
        self.tree[indx] = value
        parent = indx >> 1

        while parent > 0:
            left_child = self.tree[parent << 1]
            right_child = self.tree[parent << 1 | 1]

            if left_child is not None and right_child is not None:
                self.tree[parent] = self.func(left_child, right_child)
            elif left_child is not None:
                self.tree[parent] = left_child
            else:
                self.tree[parent] = right_child

            parent >>= 1

    def __len__(self):
        return self.size
