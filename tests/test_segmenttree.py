import operator
import random
import functools

from pysegmenttree import SegmentTree


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


def test_build():
    source = [18, 17, 13, 19, 15, 11, 20, 12, 33, 25]
    s_tree = SegmentTree(source=source)
    assert s_tree.tree == [
        None,
        183,
        125,
        58,
        90,
        35,
        32,
        26,
        32,
        58,
        18,
        17,
        13,
        19,
        15,
        11,
        20,
        12,
        33,
        25,
    ]


def test_query():
    source = [18, 17, 13, 19, 15, 11, 20, 12, 33, 25]
    s_tree = SegmentTree(source=source)

    queries = [[0, 3], [2, 7], [6, 7], [0, len(source)]]
    expected = [48, 78, 20, 183]

    for (start, end), expected in zip(queries, expected):
        assert s_tree.query(start, end) == expected


def test_update():
    source = [18, 17, 13, 19, 15, 11, 20, 12, 33, 25]
    s_tree = SegmentTree(source=source)

    s_tree.update(0, 20)
    s_tree.update(3, 14)
    assert s_tree.query(0, 3) == 50
    assert s_tree.query(2, 7) == 73
    s_tree.update(7, -10)

    assert s_tree.query(5, 9) == 54
    assert s_tree.query(0, len(source)) == 158


def test_query_random():
    random.seed(42)

    size = 100
    rng = 100
    queries = 100

    source = [random.randint(-rng, rng) for _ in range(size)]
    s_tree = SegmentTree(source=source)
    verify_tree = VerifySegmentTree(source=source)

    for _ in range(queries):
        left, right = sorted((random.randint(0, size - 1), random.randint(0, size - 1)))
        assert s_tree.query(left, right) == verify_tree.query(left, right)


def test_query_n_update_random():
    random.seed(42)

    size = 100
    rng = 100
    queries = 100

    source = [random.randint(-rng, rng) for _ in range(size)]
    s_tree = SegmentTree(source=source)
    verify_tree = VerifySegmentTree(source=source)

    for _ in range(queries):
        indx = random.randint(0, size - 1)
        value = random.randint(-rng, rng)

        s_tree.update(indx, value)
        verify_tree.update(indx, value)

        left, right = sorted((random.randint(0, size - 1), random.randint(0, size - 1)))
        assert s_tree.query(left, right) == verify_tree.query(left, right)
