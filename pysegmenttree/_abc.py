from typing import Callable, Generic, List, Optional, TypeVar, Union

T = TypeVar("T")
Func = Callable[[T, T], T]


class AbstractSegmentTree(Generic[T]):
    def __init__(self, source: List[T], func: Optional[Union[Func, str]] = None):
        raise NotImplementedError()

    def query(self, start: int, end: int) -> Optional[T]:
        raise NotImplementedError()

    def update(self, i: int, value: T) -> None:
        raise NotImplementedError()

    def __len__(self) -> int:
        raise NotImplementedError()
