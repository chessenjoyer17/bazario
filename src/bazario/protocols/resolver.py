from typing import Protocol, TypeVar, runtime_checkable

from bazario.aliases import HandlerType

T = TypeVar("T", bound=HandlerType)


@runtime_checkable
class HandlerResolver(Protocol):
    def resolve(self, handler_type: type[T]) -> T: ...
