from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from bazario.asyncio.protocols.handler import (
    NotificationHandler,
    RequestHandler,
)
from bazario.markers import Notification, Request


@runtime_checkable
class RequestHandlerFinder(Protocol):
    async def find(
        self,
        request_type: type[Request],
    ) -> type[RequestHandler] | None: ...


@runtime_checkable
class NotificationHandlerFinder(Protocol):
    async def find(
        self,
        notification_type: type[Notification],
    ) -> Iterable[type[NotificationHandler]]: ...
