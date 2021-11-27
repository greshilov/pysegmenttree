import operator
from typing import Callable, List, Optional, Union

from ._abc import AbstractSegmentTree, Func, QueryFunction, T


class PySegmentTree(AbstractSegmentTree):
    """Pure python segment tree implementation."""

    def __init__(
        self,
        source: List[T],
        func: Optional[Union[Func, QueryFunction]] = QueryFunction.SUM,
    ):
        if isinstance(func, QueryFunction):
            self.func = func.to_python_func()
        else:
            self.func = func
        self._size = len(source)
        self._tree = [*[None] * self._size, *source]
        self._build()

    def _build(self):
        for i in range(self._size - 1, 0, -1):
            # Iteratively construct parent nodes using child ones
            self._tree[i] = self.func(self._tree[i << 1], self._tree[i << 1 | 1])

    def query(self, start: int, end: int) -> Optional[T]:
        """
        Perform a query on the specified interval using func specified in constructor.
        For example, determines the sum of the interval [start, end).

        Computational complexity: O(Log[N])
        """
        if start > end:
            raise IndexError(f"Invalid interval start > end ({start} > {end})")

        left, right = start + self._size, end + self._size
        res = None
        while left < right:
            if left & 1:
                res = (
                    self.func(res, self._tree[left])
                    if res is not None
                    else self._tree[left]
                )
                left += 1
            if right & 1:
                right -= 1
                res = (
                    self.func(res, self._tree[right])
                    if res is not None
                    else self._tree[right]
                )

            left >>= 1
            right >>= 1
        return res

    def update(self, i: int, value: T):
        """
        Set i-th element of the tree to the specified value.

        Computational complexity: O(Log[N])
        """
        if i > self._size - 1 or i < 0:
            raise IndexError("SegmentTree index out of range")

        indx = i + self._size
        self._tree[indx] = value
        parent = indx >> 1

        while parent > 0:
            left_child = self._tree[parent << 1]
            right_child = self._tree[parent << 1 | 1]

            if left_child is not None and right_child is not None:
                self._tree[parent] = self.func(left_child, right_child)
            elif left_child is not None:
                self._tree[parent] = left_child
            else:
                self._tree[parent] = right_child

            parent >>= 1

    def __len__(self):
        return self._size
