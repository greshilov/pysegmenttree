import dataclasses
import functools
import operator


class VerifySegmentTree:
    def __init__(self, source=None, func=operator.add):
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

    def __add__(self, other: "Vec2D") -> "Vec2D":
        return Vec2D(self.x + other.x, self.y + other.y)

    def __eq__(self, other: "Vec2D"):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: "Vec2D"):
        return self.sqr_length() < other.sqr_length()
