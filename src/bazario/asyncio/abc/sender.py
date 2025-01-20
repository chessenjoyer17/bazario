from typing import Protocol, TypeVar

from bazario.markers import Request

TRes = TypeVar("TRes")


class Sender(Protocol):
    async def send(self, request: Request[TRes]) -> TRes: ...
