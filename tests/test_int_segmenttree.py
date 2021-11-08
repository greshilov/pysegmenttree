import pytest

from pysegmenttree.c_extensions import IntSegmentTree
from pysegmenttree.test_utils import VerifySegmentTree


def test_build():
    int_tree = IntSegmentTree([18, 17, 13, 19, 15, 11, 20, 12, 33, 25])


def test_build_overflow():
    with pytest.raises(OverflowError):
        int_64 = int(2 ** 63 - 2)
        int_tree = IntSegmentTree([int_64, 1, 2])


def test_update_overflow():
    with pytest.raises(OverflowError):
        int_64 = int(2 ** 63 - 3)
        int_tree = IntSegmentTree([int_64, 1, 1])
        int_tree.update(2, 2)
