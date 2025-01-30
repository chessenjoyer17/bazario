from bazario.asyncio.abc.publisher import Publisher
from bazario.asyncio.abc.resolver import Resolver
from bazario.asyncio.abc.sender import Sender, TRes
from bazario.asyncio.chain import build_pipeline_behaviors_chain
from bazario.asyncio.registry import Registry
from bazario.exceptions import HandlerNotFoundError
from bazario.markers import Notification, Request


class Dispatcher(Sender, Publisher):
    def __init__(self, resolver: Resolver, registry: Registry) -> None:
        self._resolver = resolver
        self._registry = registry

    async def send(self, request: Request[TRes]) -> TRes:
        request_type = type(request)

        handler_class = self._registry.get_request_handler(request_type)

        if not handler_class:
            raise HandlerNotFoundError(request_type)

        handler = await self._resolver.resolve(handler_class)
        behaviors = [
            await self._resolver.resolve(behavior_type)
            for behavior_type in self._registry.get_pipeline_behaviors(
                request_type,
            )
        ]
        handle_next = build_pipeline_behaviors_chain(handler, behaviors)

        return await handle_next(request)

    async def publish(self, notification: Notification) -> None:
        notification_type = type(notification)

        handler_classes = self._registry.get_notification_handlers(
            notification_type,
        )
        for handler_class in handler_classes:
            handler = await self._resolver.resolve(handler_class)
            behaviors = [
                await self._resolver.resolve(behavior_type)
                for behavior_type in self._registry.get_pipeline_behaviors(
                    notification_type,
                )
            ]
            handle_next = build_pipeline_behaviors_chain(handler, behaviors)

            await handle_next(notification)
