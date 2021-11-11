import operator
import random
import statistics
import timeit
from typing import Any, List, Type

import tabulate

import pysegmenttree._pysegmenttree_py
import pysegmenttree.c_extensions


def get_random_query(start: int, end: int):
    query = [random.randint(start, end), random.randint(start, end)]
    query.sort()
    return query


def bench_build(tree_cls: Type, size: int = 1_000_000):
    print(f"\n{tree_cls.__name__}: build")
    print(f"Tree size: {size}")

    random.seed(42)
    container = [random.randint(-100, 100) for _ in range(size)]

    context = {**globals(), **locals()}
    return timeit.repeat(
        f"{tree_cls.__module__}.{tree_cls.__name__}(container)",
        globals=context,
        number=1,
        repeat=5,
    )


def bench_query(tree_cls: Type, size: int = 100_000, queries: int = 10000):
    print(f"\n{tree_cls.__name__}: query")
    print(f"Tree size: {size}, queries count: {queries}")

    random.seed(42)
    container = [random.randint(-100, 100) for _ in range(size)]

    tree = tree_cls(container)
    prepared_queries = [get_random_query(0, size - 1) for _ in range(queries)]

    context = {**globals(), **locals()}
    return timeit.repeat(
        "for query in prepared_queries: tree.query(*query)",
        globals=context,
        number=1,
        repeat=5,
    )


def bench_update(tree_cls: Type, size: int = 100_000, queries: int = 10000):
    print(f"\n{tree_cls.__name__}: update")
    print(f"Tree size: {size}, queries count: {queries}")

    random.seed(42)
    container = [random.randint(-100, 100) for _ in range(size)]

    tree = tree_cls(container)
    prepared_queries = [
        [random.randint(0, size - 1), random.randint(-100, 100)] for _ in range(queries)
    ]

    context = {**globals(), **locals()}
    return timeit.repeat(
        "for query in prepared_queries: tree.update(*query)",
        globals=context,
        number=1,
        repeat=5,
    )


IMPLEMENTATIONS = [
    pysegmenttree._pysegmenttree_py.PySegmentTree,
    pysegmenttree.c_extensions.IntSegmentTree,
    pysegmenttree.c_extensions.FloatSegmentTree,
]

BENCHES = {
    "build": bench_build,
    "query": bench_query,
    "update": bench_query,
}


if __name__ == "__main__":
    results_table = [["-", *(impl.__name__ for impl in IMPLEMENTATIONS)]]
    for bench, func in BENCHES.items():
        results_table.append([bench])
        for tree_cls in IMPLEMENTATIONS:
            timeit_results = func(tree_cls)
            mean = statistics.mean(timeit_results)
            results_table[-1].append(mean)
    print(tabulate.tabulate(results_table, headers="firstrow", tablefmt="grid"))
