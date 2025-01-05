from typing import Protocol

from bazario.markers import Notification, Request


class RequestHandler[TReq: Request[TRes], TRes](Protocol):
    def handle(self, request: TReq) -> TRes: ...


class AsyncRequestHandler[TReq: Request[TRes], TRes](Protocol):
    async def handle(self, request: TReq) -> TRes: ...


class NotificationHandler[TNot: Notification](Protocol):
    def handle(self, notification: TNot) -> None: ...


class AsyncNotificationHandler[TNot: Notification](Protocol):
    async def handle(self, notification: TNot) -> None: ...
