from bazario.asyncio.protocols.finder import HandlerFinder
from bazario.asyncio.protocols.publisher import Publisher
from bazario.asyncio.protocols.resolver import HandlerResolver
from bazario.asyncio.protocols.sender import Sender, TRes
from bazario.exceptions import HandlerNotFoundError
from bazario.markers import Notification, Request


class Dispatcher(Sender, Publisher):
    def __init__(
        self,
        handler_finder: HandlerFinder,
        handler_resolver: HandlerResolver,
    ) -> None:
        self._handler_finder = handler_finder
        self._handler_resolver = handler_resolver

    async def send(self, request: Request[TRes]) -> TRes:
        request_type = type(request)
        handler_type = await self._handler_finder.find_with_request(
            request_type,
        )

        if handler_type is None:
            raise HandlerNotFoundError(request_type)

        handler = await self._handler_resolver.resolve(handler_type)

        return await handler.handle(request)

    async def publish(self, notification: Notification) -> None:
        notification_type = type(notification)
        handler_types = await self._handler_finder.find_with_notification(
            notification_type,
        )

        for handler_type in handler_types:
            handler = await self._handler_resolver.resolve(handler_type)
            await handler.handle(notification)
