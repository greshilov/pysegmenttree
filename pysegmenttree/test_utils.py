import dataclasses
import functools
import operator
from typing import List, Union

from ._abc import AbstractSegmentTree, Func, QueryFunction, T


class VerifySegmentTree(AbstractSegmentTree):
    def __init__(
        self,
        source: List[T],
        func: Union[Func, QueryFunction] = QueryFunction.SUM,
    ):
        if isinstance(func, QueryFunction):
            self.func = func.to_python_func()
        else:
            self.func = func

        self.source = source[:]

    def query(self, start: int, end: int):
        if not start < end:
            return None
        return functools.reduce(self.func, self.source[start:end])

    def update(self, i: int, value):
        self.source[i] = value


@dataclasses.dataclass
@functools.total_ordering
class Vec2D:
    x: float
    y: float

    def sqr_length(self):
        return self.x * self.x + self.y * self.y

    def __add__(self, other: object) -> "Vec2D":
        if not isinstance(other, Vec2D):
            return NotImplemented
        return Vec2D(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object):
        if not isinstance(other, Vec2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: object):
        if not isinstance(other, Vec2D):
            return NotImplemented
        return self.sqr_length() < other.sqr_length()
