from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from bazario.asyncio.protocols.handler import (
    NotificationHandler,
    RequestHandler,
)
from bazario.markers import Notification, Request


@runtime_checkable
class HandlerFinder(Protocol):
    async def find_with_request(
        self,
        request_type: type[Request],
    ) -> type[RequestHandler] | None: ...
    async def find_with_notification(
        self,
        notification_type: type[Notification],
    ) -> Iterable[type[NotificationHandler]]: ...
