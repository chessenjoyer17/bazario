from dataclasses import dataclass

from bazario.protocols.handler import NotificationHandler, RequestHandler
from bazario.protocols.resolver import HandlerResolver


@dataclass(frozen=True)
class RequestHandlerKey:
    handler: type[RequestHandler]
    resolver: HandlerResolver


@dataclass(frozen=True)
class NotificationHandlerKey:
    handler: type[NotificationHandler]
    resolver: HandlerResolver
