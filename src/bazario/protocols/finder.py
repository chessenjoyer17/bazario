from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from bazario.markers import Notification, Request
from bazario.protocols.handler import NotificationHandler, RequestHandler


@runtime_checkable
class HandlerFinder(Protocol):
    def find_with_request(
        self,
        request_type: type[Request],
    ) -> type[RequestHandler]: ...

    def find_with_notification(
        self,
        notification_type: type[Notification],
    ) -> Iterable[type[NotificationHandler]]: ...
