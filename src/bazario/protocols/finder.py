from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from bazario.markers import Notification, Request
from bazario.protocols.handler import NotificationHandler, RequestHandler


@runtime_checkable
class RequestHandlerFinder(Protocol):
    def find(self, request: Request) -> type[RequestHandler] | None: ...


@runtime_checkable
class NotificationHandlerFinder(Protocol):
    def find(
        self,
        notification: Notification,
    ) -> Iterable[type[NotificationHandler]]: ...
