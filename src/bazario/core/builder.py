from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, Self

from bazario.core.dispatcher import DispatcherImpl
from bazario.core.handler_key import NotificationHandlerKey, RequestHandlerKey
from bazario.core.types_extracting import (
    extract_notification_type_from_handler,
    extract_request_type_from_handler,
)
from bazario.protocols.builder import DispatcherBuilder
from bazario.protocols.dispatcher import Dispatcher
from bazario.protocols.handler import NotificationHandler, RequestHandler
from bazario.protocols.resolver import HandlerResolver

P = ParamSpec("P")


def _ensure_resolver_set[R](method: Callable[P, R]) -> Callable[P, R]:
    @wraps(method)
    def wrapper(
        self: "DispatcherBuilderImpl",
        handler: type[RequestHandler] | type[NotificationHandler],
        resolver: HandlerResolver | None = None,
    ) -> R:
        if self._resolver is None and resolver is None:
            raise ValueError("Resolver is not set")

        return method(self, handler, resolver or self._resolver)

    return wrapper


class DispatcherBuilderImpl(DispatcherBuilder):
    def __init__(self) -> None:
        self._resolver = None
        self._request_handlers = {}
        self._notification_handlers = {}

    def with_resolver(self, resolver: HandlerResolver) -> Self:
        self._resolver = resolver
        return self

    @_ensure_resolver_set
    def with_request_handler(
        self,
        handler: type[RequestHandler],
        resolver: HandlerResolver | None = None,
    ) -> Self:
        request_type = extract_request_type_from_handler(handler)
        request_handler_key = RequestHandlerKey(
            handler,
            resolver or self._resolver,
        )
        self._request_handlers[request_type] = request_handler_key

        return self

    @_ensure_resolver_set
    def with_notification_handler(
        self,
        handler: type[NotificationHandler],
        resolver: HandlerResolver | None = None,
    ) -> Self:
        notification_type = extract_notification_type_from_handler(handler)
        notification_handler_key = NotificationHandlerKey(
            handler,
            resolver or self._resolver,
        )
        self._notification_handlers.setdefault(notification_type, []).append(
            notification_handler_key
        )

        return self

    def build(self) -> Dispatcher:
        return DispatcherImpl(self._request_handlers, self._notification_handlers)
