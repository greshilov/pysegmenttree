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
