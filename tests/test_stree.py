import random

import pytest

from pysegmenttree import PySegmentTree, stree
from pysegmenttree.c_extensions import FloatSegmentTree, IntSegmentTree
from pysegmenttree.test_utils import VerifySegmentTree

CLASSES = [PySegmentTree, IntSegmentTree, FloatSegmentTree]


def test_stree():
    tree = stree([18, 17, 13, 19, 15, 11, 20, 12, 33, 25])
    assert isinstance(tree, IntSegmentTree)

    tree = stree([18.5, 17.1, 13.0, 19.2, 15.0, 11.0, 20.0, 12.1, 33.0, 25.0])
    assert isinstance(tree, FloatSegmentTree)

    tree = stree([int(2 ** 63 - 1), 17, 13, 19, 15, 11, 20, 12, 33, 25])
    assert isinstance(tree, PySegmentTree)

    tree = stree([1, 2, 3, 4, 5], min)
    assert isinstance(tree, PySegmentTree)


@pytest.mark.parametrize("cls", CLASSES)
def test_len(cls):
    tree = cls([18, 17, 13, 19])
    assert len(tree) == 4


@pytest.mark.parametrize("cls", CLASSES)
def test_build(cls):
    tree = cls([18, 17, 13, 19, 15, 11, 20, 12, 33, 25])


@pytest.mark.parametrize("cls", CLASSES)
def test_query(cls):
    source = [18, 17, 13, 19, 15, 11, 20, 12, 33, 25]

    tree = cls(source)
    v_tree = VerifySegmentTree(source)

    queries = [[0, 3], [2, 7], [6, 7], [0, len(source)]]
    expected = [48, 78, 20, 183]

    for (start, end), expected in zip(queries, expected):
        assert tree.query(start, end) == expected


@pytest.mark.parametrize("cls", CLASSES)
def test_update(cls):
    source = [18, 17, 13, 19, 15, 11, 20, 12, 33, 25]
    tree = cls(source=source)

    tree.update(0, 20)
    tree.update(3, 14)
    assert tree.query(0, 3) == 50
    assert tree.query(2, 7) == 73
    tree.update(7, -10)

    assert tree.query(5, 9) == 54
    assert tree.query(0, len(source)) == 158


@pytest.mark.parametrize("cls", CLASSES)
def test_query_random(cls):
    random.seed(42)

    size = 500
    rng = 100000
    queries = 1000

    source = [random.randint(-rng, rng) for _ in range(size)]
    tree = cls(source=source)
    verify_tree = VerifySegmentTree(source=source)

    for _ in range(queries):
        left, right = sorted((random.randint(0, size - 1), random.randint(0, size - 1)))
        assert tree.query(left, right) == verify_tree.query(left, right)


@pytest.mark.parametrize("cls", CLASSES)
def test_query_n_update_random(cls):
    random.seed(-42)

    size = 500
    rng = 100000
    queries = 1000

    source = [random.randint(-rng, rng) for _ in range(size)]
    tree = cls(source=source)
    verify_tree = VerifySegmentTree(source=source)

    for _ in range(queries):
        indx = random.randint(0, size - 1)
        value = random.randint(-rng, rng)

        tree.update(indx, value)
        verify_tree.update(indx, value)

        left, right = sorted((random.randint(0, size - 1), random.randint(0, size - 1)))
        assert tree.query(left, right) == verify_tree.query(left, right)
