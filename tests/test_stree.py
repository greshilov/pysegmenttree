from pysegmenttree import PySegmentTree, QueryFunction, stree
from pysegmenttree.c_extensions import FloatSegmentTree, IntSegmentTree


def test_stree():
    tree = stree([18, 17, 13, 19, 15, 11, 20, 12, 33, 25])
    assert isinstance(tree, IntSegmentTree)

    tree = stree(
        [18.5, 17.1, 13.0, 19.2, 15.0, 11.0, 20.0, 12.1, 33.0, 25.0],
        func=QueryFunction.MAX,
    )
    assert isinstance(tree, FloatSegmentTree)

    tree = stree([int(2 ** 63 - 1), 17, 13, 19, 15, 11, 20, 12, 33, 25])
    assert isinstance(tree, PySegmentTree)

    tree = stree(
        [int(2 ** 63 - 1), 17, 13, 19, 15, 11, 20, 12, 33, 25],
        func=QueryFunction.MIN,
    )
    assert isinstance(tree, IntSegmentTree)

    tree = stree([1, 2, 3, 4, 5], func=min)
    assert isinstance(tree, PySegmentTree)
