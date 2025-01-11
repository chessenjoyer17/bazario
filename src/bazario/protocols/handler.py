from typing import Protocol, runtime_checkable

from bazario.typing.type_vars import TNot_contra, TReq_contra, TRes_co


@runtime_checkable
class RequestHandler(Protocol[TReq_contra, TRes_co]):
    def handle(self, request: TReq_contra) -> TRes_co: ...


@runtime_checkable
class NotificationHandler(Protocol[TNot_contra]):
    def handle(self, notification: TNot_contra) -> None: ...
