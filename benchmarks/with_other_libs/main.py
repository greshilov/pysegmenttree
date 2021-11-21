import collections
import functools
import json
import pathlib
import random
import timeit

from benchmarks.with_other_libs.wrappers import *
from pysegmenttree.test_utils import Vec2D

DATA_DIR = pathlib.Path(__file__).parent / "data"
RESULT_FILE_NAME = DATA_DIR / "bench_results.json"

LIBS = [
    Segment_TreeWrapper,
    SegmentTreeWrapper,
    CSegmentTreeWrapper,
    PySegmentTreeWrapper,
]
REFRENCE_SIZE = 100_000
TYPES = [int, float, Vec2D]
QUERY_COUNT = 10_000
DEF_RANGE = 10_000


def typ_random(typ: type):
    if typ is int:
        return random.randint(-DEF_RANGE, DEF_RANGE)
    elif typ is float:
        return random.randint(-DEF_RANGE, DEF_RANGE) * random.random()
    elif typ is Vec2D:
        return Vec2D(
            random.randint(-DEF_RANGE, DEF_RANGE), random.randint(-DEF_RANGE, DEF_RANGE)
        )


@functools.lru_cache
def generate_data(typ: type, size: int):
    random.seed(42)
    return [typ_random(typ) for _ in range(size)]


@functools.lru_cache
def generate_sum_queries(size: int):
    random.seed(42)
    return [
        sorted([random.randint(0, size - 1), random.randint(0, size - 1)])
        for _ in range(size)
    ]


@functools.lru_cache
def generate_update_queries(typ: type, size: int):
    random.seed(42)
    return [[random.randint(0, size - 1), typ_random(typ)] for _ in range(size)]


def bench_init(kls: type, source: list):
    def func():
        return kls(source, "sum")

    context = {**globals(), **locals()}
    try:
        return timeit.repeat(
            "func()",
            globals=context,
            number=1,
            repeat=5,
        )
    except NotImplementedError:
        return


def bench_query_sum(kls: type, source: list, queries: list):
    random.seed(42)

    def func(tree):
        for left, right in queries:
            tree.query_sum(left, right)

    context = {**globals(), **locals()}
    try:
        return timeit.repeat(
            "func(tree)",
            setup="tree = kls(source, 'sum')",
            globals=context,
            number=1,
            repeat=5,
        )
    except NotImplementedError:
        return


def bench_update_sum(kls: type, source: list, queries: list):
    random.seed(42)

    def func(tree):
        for i, el in queries:
            tree.update(i, el)

    context = {**globals(), **locals()}
    try:
        return timeit.repeat(
            "func(tree)",
            setup="tree = kls(source, 'sum')",
            globals=context,
            number=1,
            repeat=5,
        )
    except NotImplementedError:
        return


def main():
    results = collections.defaultdict(list)
    for kls in LIBS:
        lib = kls.LIB
        print(f"Testing {lib}")

        for typ in TYPES:
            source = generate_data(typ, REFRENCE_SIZE)
            results["init"].append(
                {
                    "lib": lib,
                    "type": typ.__name__,
                    "size": REFRENCE_SIZE,
                    "result": bench_init(kls, source),
                }
            )

            sum_queries = generate_sum_queries(REFRENCE_SIZE)
            results["query"].append(
                {
                    "lib": lib,
                    "type": typ.__name__,
                    "size": REFRENCE_SIZE,
                    "result": bench_query_sum(kls, source, sum_queries),
                }
            )

            update_queries = generate_update_queries(typ, REFRENCE_SIZE)
            results["update"].append(
                {
                    "lib": lib,
                    "type": typ.__name__,
                    "size": REFRENCE_SIZE,
                    "result": bench_update_sum(kls, source, update_queries),
                }
            )

    with open(RESULT_FILE_NAME, "w") as f:
        json.dump(results, f)


if __name__ == "__main__":
    main()
