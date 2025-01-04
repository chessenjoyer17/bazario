from typing import Protocol

from bazario.markers import Request


class Sender(Protocol):
    def send[TRes](self, request: Request[TRes]) -> TRes: ...
