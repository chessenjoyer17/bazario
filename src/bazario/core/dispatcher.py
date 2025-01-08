from bazario.core.exceptions import HandlerNotFoundError
from bazario.markers import Notification, Request
from bazario.protocols.finder import (
    NotificationHandlerFinder,
    RequestHandlerFinder,
)
from bazario.protocols.publisher import Publisher
from bazario.protocols.resolver import HandlerResolver
from bazario.protocols.sender import Sender, TRes


class Dispatcher(Sender, Publisher):
    def __init__(
        self,
        handler_resolver: HandlerResolver,
        request_handler_finder: RequestHandlerFinder,
        notification_handler_finder: NotificationHandlerFinder,
    ) -> None:
        self._handler_resolver = handler_resolver
        self._request_handler_finder = request_handler_finder
        self._notification_handler_finder = notification_handler_finder

    def send(self, request: Request[TRes]) -> TRes:
        handler_type = self._request_handler_finder.find(request)

        if handler_type is None:
            raise HandlerNotFoundError(type(request))

        handler = self._handler_resolver.resolve(handler_type)

        return handler.handle(request)

    def publish(self, notification: Notification) -> None:
        handler_types = self._notification_handler_finder.find(notification)

        for handler_type in handler_types:
            handler = self._handler_resolver.resolve(handler_type)
            handler.handle(notification)
