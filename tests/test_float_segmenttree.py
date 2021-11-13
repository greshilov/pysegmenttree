import random

import pytest

from pysegmenttree.c_extensions import FloatSegmentTree
from pysegmenttree.test_utils import VerifySegmentTree


def test_update_wrong_type():
    float_tree = FloatSegmentTree([1.0, 2.0, 3.0, 4.0])

    float_tree.update(0, 2)
    assert float_tree.query(0, 2) == 4.0

    with pytest.raises(TypeError):
        float_tree.update(0, None)


def test_float_query_n_update_random():
    random.seed(-42)

    size = 500
    rng = 100000
    queries = 1000

    source = [random.randint(-rng, rng) * random.random() for _ in range(size)]
    tree = FloatSegmentTree(source=source)
    verify_tree = VerifySegmentTree(source=source)

    for _ in range(queries):
        indx = random.randint(0, size - 1)
        value = random.randint(-rng, rng) * random.random()

        tree.update(indx, value)
        verify_tree.update(indx, value)

        left, right = sorted((random.randint(0, size - 1), random.randint(0, size - 1)))
        assert pytest.approx(tree.query(left, right)) == pytest.approx(
            verify_tree.query(left, right)
        )
