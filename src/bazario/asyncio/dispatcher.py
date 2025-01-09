from bazario.asyncio.protocols.finder import (
    NotificationHandlerFinder,
    RequestHandlerFinder,
)
from bazario.asyncio.protocols.publisher import Publisher
from bazario.asyncio.protocols.resolver import HandlerResolver
from bazario.asyncio.protocols.sender import Sender, TRes
from bazario.exceptions import (
    HandlerNotFoundError,
    NotificationHandlerNotSetError,
)
from bazario.markers import Notification, Request


class Dispatcher(Sender, Publisher):
    def __init__(
        self,
        handler_resolver: HandlerResolver,
        request_handler_finder: RequestHandlerFinder,
        notification_handler_finder: NotificationHandlerFinder | None = None,
    ) -> None:
        self._handler_resolver = handler_resolver
        self._request_handler_finder = request_handler_finder
        self._notification_handler_finder = notification_handler_finder

    async def send(self, request: Request[TRes]) -> TRes:
        request_type = type(request)
        handler_type = await self._request_handler_finder.find(request_type)

        if handler_type is None:
            raise HandlerNotFoundError(request_type)

        handler = await self._handler_resolver.resolve(handler_type)

        return await handler.handle(request)

    async def publish(self, notification: Notification) -> None:
        if self._notification_handler_finder is None:
            raise NotificationHandlerNotSetError

        notification_type = type(notification)
        handler_types = await self._notification_handler_finder.find(
            notification_type,
        )

        for handler_type in handler_types:
            handler = await self._handler_resolver.resolve(handler_type)
            await handler.handle(notification)
