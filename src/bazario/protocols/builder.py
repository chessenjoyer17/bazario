from typing import Protocol, Self

from bazario.protocols.dispatcher import Dispatcher
from bazario.protocols.handler import RequestHandler
from bazario.protocols.resolver import HandlerResolver


class DispatcherBuilder(Protocol):
    def with_resolver(self, resolver: HandlerResolver) -> Self: ...
    def with_request_handler(
        self,
        handler: type[RequestHandler],
        resolver: HandlerResolver | None = None,
    ) -> Self: ...
    def with_notification_handler(
        self,
        handler: type[RequestHandler],
        resolver: HandlerResolver | None = None,
    ) -> Self: ...
    def build(self) -> Dispatcher: ...
