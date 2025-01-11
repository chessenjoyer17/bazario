from bazario.asyncio.pipeline.behavior_registry import (
    PipelineBehaviorRegistry,
)
from bazario.asyncio.pipeline.wrap_pipeline_behaviors import (
    wrap_pipeline_behaviors,
)
from bazario.asyncio.protocols.finder import HandlerFinder
from bazario.asyncio.protocols.publisher import Publisher
from bazario.asyncio.protocols.resolver import Resolver
from bazario.asyncio.protocols.sender import Sender, TRes
from bazario.exceptions import HandlerNotFoundError
from bazario.markers import Notification, Request


class Dispatcher(Sender, Publisher):
    def __init__(
        self,
        resolver: Resolver,
        handler_finder: HandlerFinder,
        pipeline_behaviorregistry: PipelineBehaviorRegistry,
    ) -> None:
        self._resolver = resolver
        self._handler_finder = handler_finder
        self._pipeline_behaviorregistry = pipeline_behaviorregistry

    async def send(self, request: Request[TRes]) -> TRes:
        request_type = type(request)
        handler_type = await self._handler_finder.find_with_request(
            request_type,
        )

        if handler_type is None:
            raise HandlerNotFoundError(request_type)

        handler = await self._resolver.resolve(handler_type)
        behaviors = self._pipeline_behaviorregistry.get_behaviors(
            request_type,
        )
        pipeline = wrap_pipeline_behaviors(behaviors, handler)

        return await pipeline(self._resolver, request)

    async def publish(self, notification: Notification) -> None:
        notification_type = type(notification)
        handler_types = await self._handler_finder.find_with_notification(
            notification_type,
        )
        behaviors = self._pipeline_behaviorregistry.get_behaviors(
            notification_type,
        )

        for handler_type in handler_types:
            handler = await self._resolver.resolve(handler_type)
            pipeline = wrap_pipeline_behaviors(behaviors, handler)

            await pipeline(self._resolver, notification)
