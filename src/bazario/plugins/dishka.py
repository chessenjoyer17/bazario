__all__ = (
    "DishkaHandlerResolver",
    "DishkaNotificationHandlerFinder",
    "DishkaRequestHandlerFinder",
    "bazario_provider",
)

from collections.abc import Iterable

from dishka import Container, Provider, Scope, WithParents

from bazario.core.dispatcher import Dispatcher
from bazario.core.type_inspection import (
    extract_base_generic_type,
    matches_generic_type,
)
from bazario.markers import Notification, Request
from bazario.protocols.finder import (
    NotificationHandlerFinder,
    RequestHandlerFinder,
)
from bazario.protocols.handler import NotificationHandler, RequestHandler
from bazario.protocols.resolver import HandlerResolver


class DishkaHandlerResolver(HandlerResolver):
    def __init__(self, container: Container) -> None:
        self._container = container

    def resolve[T](self, key: type[T]) -> T:
        return self._container.get(key)


class DishkaRequestHandlerFinder(RequestHandlerFinder):
    def __init__(self, container: Container) -> None:
        self._container = container

    def find(self, request: Request) -> type[RequestHandler] | None:
        keys = self._container.registry.factories.keys()

        for key in keys:
            generic_type = extract_base_generic_type(key.type_hint)

            if generic_type and matches_generic_type(
                generic_type,
                RequestHandler,
                type(request),
            ):
                return key.type_hint

        return None


class DishkaNotificationHandlerFinder(NotificationHandlerFinder):
    def __init__(self, container: Container) -> None:
        self._container = container

    def find(
        self,
        notification: Notification,
    ) -> Iterable[type[NotificationHandler]]:
        keys = self._container.registry.factories.keys()

        for key in keys:
            generic_type = extract_base_generic_type(key.type_hint)

            if generic_type and matches_generic_type(
                generic_type,
                NotificationHandler,
                type(notification),
            ):
                yield key.type_hint


def bazario_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)

    provider.provide(WithParents[Dispatcher])
    provider.provide(WithParents[DishkaHandlerResolver])
    provider.provide(WithParents[DishkaRequestHandlerFinder])
    provider.provide(WithParents[DishkaNotificationHandlerFinder])

    return provider
