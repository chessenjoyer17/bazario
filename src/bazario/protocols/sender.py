from typing import Protocol

from bazario.markers import Request


class Sender(Protocol):
    def send[TRes](
        self,
        response: Request[TRes],
        component: str | None = None,
    ) -> TRes: ...
