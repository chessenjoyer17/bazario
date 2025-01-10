from bazario.exceptions import HandlerNotFoundError
from bazario.markers import Notification, Request
from bazario.protocols.finder import HandlerFinder
from bazario.protocols.publisher import Publisher
from bazario.protocols.resolver import HandlerResolver
from bazario.protocols.sender import Sender, TRes


class Dispatcher(Sender, Publisher):
    def __init__(
        self,
        handler_finder: HandlerFinder,
        handler_resolver: HandlerResolver,
    ) -> None:
        self._handler_finder = handler_finder
        self._handler_resolver = handler_resolver

    def send(self, request: Request[TRes]) -> TRes:
        request_type = type(request)
        handler_type = self._handler_finder.find_with_request(request_type)

        if handler_type is None:
            raise HandlerNotFoundError(request_type)

        handler = self._handler_resolver.resolve(handler_type)

        return handler.handle(request)

    def publish(self, notification: Notification) -> None:
        notification_type = type(notification)
        handler_types = self._handler_finder.find_with_notification(
            notification_type,
        )

        for handler_type in handler_types:
            handler = self._handler_resolver.resolve(handler_type)
            handler.handle(notification)
