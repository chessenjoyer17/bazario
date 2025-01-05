from bazario.core.aliases import NotificationHandlers, RequestHandlers
from bazario.core.handler_key import NotificationHandlerKey, RequestHandlerKey
from bazario.markers import Notification, Request
from bazario.protocols.dispatcher import Dispatcher


class DispatcherImpl(Dispatcher):
    def __init__(
        self,
        request_handlers: RequestHandlers,
        notification_handlers: NotificationHandlers,
    ) -> None:
        self._request_handlers = request_handlers
        self._notification_handlers = notification_handlers

    def send[TRes](self, request: Request[TRes]) -> TRes:
        key = self._find_request_handler_key(request)

        handler = key.resolver.resolve(key.handler)

        return handler.handle(request)

    def publish(self, notification: Notification) -> None:
        keys = self._find_notification_handler_keys(notification)

        for key in keys:
            handler = key.resolver.resolve(key.handler)

            handler.handle(notification)

    def _find_request_handler_key(self, request: Request) -> RequestHandlerKey:
        request_type = type(request)

        if request_type not in self._request_handlers:
            raise ValueError(f"No request handler for {request_type}")

        return self._request_handlers[request_type]

    def _find_notification_handler_keys(
        self, notification: Notification
    ) -> list[NotificationHandlerKey]:
        notification_type = type(notification)

        if notification_type not in self._notification_handlers:
            raise ValueError(f"No notification handlers for {notification_type}")

        return self._notification_handlers[notification_type]
