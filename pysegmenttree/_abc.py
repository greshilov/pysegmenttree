from typing import (
    Callable,
    Generic,
    List,
    Optional,
    TypeVar,
)

T = TypeVar("T")


class AbstractSegmentTree(Generic[T]):
    def __init__(self, source: List[T], func: Optional[Callable[[T, T], T]] = None):
        raise NotImplementedError()

    def query(self, start: int, end: int) -> T:
        raise NotImplementedError()

    def update(self, i: int, value: T) -> None:
        raise NotImplementedError()

    def __len__(self) -> int:
        raise NotImplementedError()
