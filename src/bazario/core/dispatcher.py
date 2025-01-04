from collections.abc import Iterable

from bazario.core.generic_types_extracting import (
    extract_notification_type_from_handler,
    extract_request_type_from_handler,
)
from bazario.markers import Notification, Request
from bazario.protocols.handler import NotificationHandler, RequestHandler
from bazario.protocols.publisher import Publisher
from bazario.protocols.resolver import Resolver
from bazario.protocols.sender import Sender

type TRHandlers = dict[type[Request], type[RequestHandler]]
type TNHandlers = dict[type[Notification], list[type[NotificationHandler]]]


class Dispatcher(Sender, Publisher):
    _request_handlers: TRHandlers
    _notification_handlers: TNHandlers

    def __init__(self, resolver: Resolver) -> None:
        self._resolver = resolver

        self._request_handlers = {}
        self._notification_handlers = {}

    def send[TRes](self, request: Request[TRes]) -> TRes:
        handler = self._find_and_resolve_request_handler(request)

        return handler.handle(request)

    def publish(self, notification: Notification) -> None:
        handlers = self._find_and_resolve_notification_handlers(notification)

        for handler in handlers:
            handler.handle(notification)

    def register_request_handler(self, handler: type[RequestHandler]) -> None:
        request_type = extract_request_type_from_handler(handler)

        self._request_handlers[request_type] = handler

    def register_notification_handler(self, handler: type[NotificationHandler]) -> None:
        notification_type = extract_notification_type_from_handler(handler)

        self._notification_handlers.setdefault(notification_type, []).append(handler)

    def _find_and_resolve_request_handler(self, request: Request) -> RequestHandler:
        request_type = type(request)

        if request_type not in self._request_handlers:
            raise ValueError(f"No handler for {request_type}")

        return self._resolver.resolve(self._request_handlers[request_type])

    def _find_and_resolve_notification_handlers(
        self, notification: Notification
    ) -> Iterable[NotificationHandler]:
        notification_type = type(notification)

        if notification_type not in self._notification_handlers:
            raise ValueError(f"No handler for {notification_type}")

        for handler in self._notification_handlers[notification_type]:
            yield self._resolver.resolve(handler)
