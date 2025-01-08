from typing import Protocol, TypeVar, runtime_checkable

from bazario.markers import Request

TRes = TypeVar("TRes")


@runtime_checkable
class Sender(Protocol):
    def send(self, request: Request[TRes]) -> TRes: ...
