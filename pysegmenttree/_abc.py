from enum import Enum
from functools import lru_cache
from operator import add
from typing import Callable, Generic, List, Optional, TypeVar, Union

T = TypeVar("T")
Func = Callable[[T, T], T]


class QueryFunction(Enum):
    SUM = "sum"
    MIN = "min"
    MAX = "max"

    @lru_cache()
    def _map(self, value: "QueryFunction"):
        return {
            QueryFunction.SUM: add,
            QueryFunction.MIN: min,
            QueryFunction.MAX: max,
        }[value]

    def to_python_func(self):
        return self._map(self)


class AbstractSegmentTree(Generic[T]):
    def __init__(
        self,
        source: List[T],
        func: Union[Func, QueryFunction] = QueryFunction.SUM,
    ):
        raise NotImplementedError()

    def query(self, start: int, end: int) -> Optional[T]:
        raise NotImplementedError()

    def update(self, i: int, value: T) -> None:
        raise NotImplementedError()

    def __len__(self) -> int:
        raise NotImplementedError()
