import random
from typing import List, Union

import pytest

from pysegmenttree import PySegmentTree, QueryFunction, stree
from pysegmenttree._abc import T
from pysegmenttree.c_extensions import FloatSegmentTree, IntSegmentTree
from pysegmenttree.test_utils import VerifySegmentTree

CLASSES = [PySegmentTree, IntSegmentTree, FloatSegmentTree]
SUPPORTED_FUNCTIONS = [f for f in QueryFunction]


def construct_tree(
    kls: Union[PySegmentTree, IntSegmentTree, FloatSegmentTree],
    source: List[T],
    func: QueryFunction,
):
    if kls is PySegmentTree:
        return kls(source=source, func=func)
    elif kls in (IntSegmentTree, FloatSegmentTree):
        return kls(source=source, func=func.value)
    else:
        raise RuntimeError(f"Unexpected tree class {kls}")


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.parametrize("func", SUPPORTED_FUNCTIONS)
def test_len(cls: type, func: QueryFunction):
    tree = construct_tree(cls, [18, 17, 13, 19], func)
    assert len(tree) == 4


@pytest.mark.parametrize("cls", CLASSES)
def test_query(cls: type):
    source = [18, 17, 13, 19, 15, 11, 20, 12, 33, 25]

    tree = construct_tree(cls, source, func=QueryFunction.SUM)
    v_tree = VerifySegmentTree(source, func=QueryFunction.SUM)

    queries = [[0, 3], [2, 7], [6, 7], [0, len(source)]]
    expected = [48, 78, 20, 183]

    for (start, end), expected in zip(queries, expected):
        assert tree.query(start, end) == expected


@pytest.mark.parametrize("cls", CLASSES)
def test_update(cls: type):
    source = [18, 17, 13, 19, 15, 11, 20, 12, 33, 25]
    tree = construct_tree(cls, source, func=QueryFunction.SUM)

    tree.update(0, 20)
    tree.update(3, 14)
    assert tree.query(0, 3) == 50
    assert tree.query(2, 7) == 73
    tree.update(7, -10)

    assert tree.query(5, 9) == 54
    assert tree.query(0, len(source)) == 158


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.parametrize("func", SUPPORTED_FUNCTIONS)
def test_query_random(cls: type, func: QueryFunction):
    random.seed(42)

    size = 500
    rng = 100000
    queries = 1000

    source = [random.randint(-rng, rng) for _ in range(size)]
    tree = construct_tree(cls, source, func=func)
    verify_tree = VerifySegmentTree(
        source=source,
        func=func,
    )

    for _ in range(queries):
        left, right = sorted((random.randint(0, size - 1), random.randint(0, size - 1)))
        assert tree.query(left, right) == verify_tree.query(left, right)


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.parametrize("func", SUPPORTED_FUNCTIONS)
def test_query_n_update_random(cls: type, func: QueryFunction):
    random.seed(-42)

    size = 500
    rng = 100000
    queries = 1000

    source = [random.randint(-rng, rng) for _ in range(size)]
    tree = construct_tree(cls, source, func=func)
    verify_tree = VerifySegmentTree(source=source, func=func)

    for _ in range(queries):
        indx = random.randint(0, size - 1)
        value = random.randint(-rng, rng)

        tree.update(indx, value)
        verify_tree.update(indx, value)

        left, right = sorted((random.randint(0, size - 1), random.randint(0, size - 1)))
        assert tree.query(left, right) == verify_tree.query(left, right)
