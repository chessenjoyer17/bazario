from bazario.exceptions import HandlerNotFoundError
from bazario.markers import Notification, Request
from bazario.pipeline.behavior_registry import PipelineBehaviorRegistry
from bazario.pipeline.wrap_pipeline_behaviors import wrap_pipeline_behaviors
from bazario.protocols.finder import HandlerFinder
from bazario.protocols.publisher import Publisher
from bazario.protocols.resolver import Resolver
from bazario.protocols.sender import Sender, TRes


class Dispatcher(Sender, Publisher):
    def __init__(
        self,
        resolver: Resolver,
        handler_finder: HandlerFinder,
        pipeline_behavior_registry: PipelineBehaviorRegistry,
    ) -> None:
        self._resolver = resolver
        self._handler_finder = handler_finder
        self._pipeline_behavior_registry = pipeline_behavior_registry

    def send(self, request: Request[TRes]) -> TRes:
        request_type = type(request)
        handler_type = self._handler_finder.find_with_request(request_type)

        if handler_type is None:
            raise HandlerNotFoundError(request_type)

        handler = self._resolver.resolve(handler_type)

        behaviors = self._pipeline_behavior_registry.get_behaviors(
            request_type,
        )

        pipeline = wrap_pipeline_behaviors(behaviors, handler)

        return pipeline(self._resolver, request)

    def publish(self, notification: Notification) -> None:
        notification_type = type(notification)
        handler_types = self._handler_finder.find_with_notification(
            notification_type,
        )
        behaviors = self._pipeline_behavior_registry.get_behaviors(
            notification_type,
        )

        for handler_type in handler_types:
            handler = self._resolver.resolve(handler_type)
            pipeline = wrap_pipeline_behaviors(behaviors, handler)
            pipeline(self._resolver, notification)
