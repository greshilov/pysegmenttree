import operator
import random
import statistics
import timeit

from typing import Type, List

import pysegmenttree._pysegmenttree_py
import pysegmenttree.c_extensions


IMPLEMENTATIONS = {
    "PySegmentTree": pysegmenttree._pysegmenttree_py.SegmentTree,
    "CSegmentTree": pysegmenttree.c_extensions.IntSegmentTree,
}


def get_random_query(start: int, end: int):
    query = [random.randint(start, end), random.randint(start, end)]
    query.sort()
    return query


def print_stats(timeit_results: List[float]):
    print(
        f"""
min: {min(timeit_results)}
max: {max(timeit_results)}
mean: {statistics.mean(timeit_results)}""".strip()
    )


def bench_build(tree_cls_name: str, tree_cls: Type, size: int = 1_000_000):
    print(f"\n{tree_cls_name}: build")
    print(f"Tree size: {size}")

    random.seed(42)
    container = [random.randint(-100, 100) for _ in range(size)]

    context = {**globals(), **locals()}
    print_stats(
        timeit.repeat(
            f"{tree_cls.__module__}.{tree_cls.__name__}(container)",
            globals=context,
            number=1,
            repeat=5,
        )
    )


def bench_query(
    tree_cls_name: str, tree_cls, size: int = 100_000, queries: int = 10000
):
    print(f"\n{tree_cls_name}: query")
    print(f"Tree size: {size}, queries count: {queries}")

    random.seed(42)
    container = [random.randint(-100, 100) for _ in range(size)]

    tree = tree_cls(container)
    prepared_queries = [get_random_query(0, size - 1) for _ in range(queries)]

    context = {**globals(), **locals()}
    print_stats(
        timeit.repeat(
            "for query in prepared_queries: tree.query(*query)",
            globals=context,
            number=1,
            repeat=5,
        )
    )


def bench_update(
    tree_cls_name: str, tree_cls, size: int = 100_000, queries: int = 10000
):
    print(f"\n{tree_cls_name}: update")
    print(f"Tree size: {size}, queries count: {queries}")

    random.seed(42)
    container = [random.randint(-100, 100) for _ in range(size)]

    tree = tree_cls(container)
    prepared_queries = [
        [random.randint(0, size - 1), random.randint(-100, 100)] for _ in range(queries)
    ]

    context = {**globals(), **locals()}
    print_stats(
        timeit.repeat(
            "for query in prepared_queries: tree.update(*query)",
            globals=context,
            number=1,
            repeat=5,
        )
    )


if __name__ == "__main__":
    for tree_cls_name, tree_cls in IMPLEMENTATIONS.items():
        bench_build(tree_cls_name, tree_cls)
        bench_query(tree_cls_name, tree_cls)
        # bench_update(tree_cls_name, tree_cls)
