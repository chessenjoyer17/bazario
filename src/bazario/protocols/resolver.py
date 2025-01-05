from typing import Protocol

from bazario.protocols.handler import NotificationHandler, RequestHandler

type HandlerType = RequestHandler | NotificationHandler


class HandlerResolver(Protocol):
    def resolve[T: HandlerType](self, key: type[T]) -> T: ...
