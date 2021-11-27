import pytest

from pysegmenttree import QueryFunction
from pysegmenttree.c_extensions import IntSegmentTree
from pysegmenttree.test_utils import VerifySegmentTree


def test_build():
    int_tree = IntSegmentTree([18, 17, 13, 19, 15, 11, 20, 12, 33, 25])


def test_update_wrong_type():
    int_tree = IntSegmentTree([1, 2, 3, 4])
    with pytest.raises(TypeError):
        int_tree.update(0, 10.5)


def test_build_overflow():
    with pytest.raises(OverflowError):
        int_64 = int(2 ** 63 - 2)
        int_tree = IntSegmentTree([int_64, 1, 2])

    with pytest.raises(OverflowError):
        int_64 = int(-(2 ** 63) + 1)
        int_tree = IntSegmentTree([int_64, -1, -1])


def test_update_overflow():
    int_64 = int(2 ** 63 - 3)
    int_tree = IntSegmentTree([int_64, 1, 1])
    with pytest.raises(OverflowError):
        int_tree.update(2, 2)

    int_64 = int(-(2 ** 63) + 2)
    int_tree = IntSegmentTree([int_64, -1, -1])
    with pytest.raises(OverflowError):
        int_tree.update(2, -2)
