from pysegmenttree import PySegmentTree
from pysegmenttree.test_utils import Vec2D, VerifySegmentTree


def test_custom_obj():
    src = [
        [14, 5],
        [-5, 0],
        [120, 1],
        [-100, 12],
        [1, 1],
        [0, 0],
        [-20, 1],
        [10, 2],
        [-12, 11],
    ]
    src = [Vec2D(*p) for p in src]

    tree = PySegmentTree(src, func=min)
    verify_tree = VerifySegmentTree(src, func=min)

    queries = [[0, 3], [2, 7], [6, 7], [0, len(src)]]

    for start, end in queries:
        assert tree.query(start, end) == verify_tree.query(start, end)
