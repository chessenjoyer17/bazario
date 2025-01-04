from typing import Protocol, TypeVar

T = TypeVar("T")


class Resolver(Protocol):
    def resolve(self, key: type[T]) -> T: ...
