from bazario.exceptions import HandlerNotFoundError
from bazario.markers import Notification, Request
from bazario.pipeline.behaviour_registry import PipelineBehaviourRegistry
from bazario.pipeline.wrap_pipeline_behaviours import wrap_pipeline_behaviours
from bazario.protocols.finder import HandlerFinder
from bazario.protocols.publisher import Publisher
from bazario.protocols.resolver import Resolver
from bazario.protocols.sender import Sender, TRes


class Dispatcher(Sender, Publisher):
    def __init__(
        self,
        resolver: Resolver,
        handler_finder: HandlerFinder,
        pipeline_behaviour_registry: PipelineBehaviourRegistry,
    ) -> None:
        self._resolver = resolver
        self._handler_finder = handler_finder
        self._pipeline_behaviour_registry = pipeline_behaviour_registry

    def send(self, request: Request[TRes]) -> TRes:
        request_type = type(request)
        handler_type = self._handler_finder.find_with_request(request_type)

        if handler_type is None:
            raise HandlerNotFoundError(request_type)

        handler = self._resolver.resolve(handler_type)

        behaviours = self._pipeline_behaviour_registry.get_behaviours(
            request_type,
        )

        pipeline = wrap_pipeline_behaviours(behaviours, handler)

        return pipeline(self._resolver, request)

    def publish(self, notification: Notification) -> None:
        notification_type = type(notification)
        handler_types = self._handler_finder.find_with_notification(
            notification_type,
        )
        behaviours = self._pipeline_behaviour_registry.get_behaviours(
            notification_type,
        )

        for handler_type in handler_types:
            handler = self._resolver.resolve(handler_type)
            pipeline = wrap_pipeline_behaviours(behaviours, handler)
            pipeline(self._resolver, notification)
