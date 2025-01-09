__all__ = (
    "DishkaHandlerResolver",
    "DishkaNotificationHandlerFinder",
    "DishkaRequestHandlerFinder",
)

from collections.abc import Iterable

from dishka import AsyncContainer, WithParents

from bazario import Notification, Request
from bazario.asyncio import (
    Dispatcher,
    HandlerResolver,
    NotificationHandler,
    NotificationHandlerFinder,
    RequestHandler,
    RequestHandlerFinder,
    THandler,
)
from bazario.type_inspection import (
    extract_base_generic_type,
    matches_generic_type,
)


class DishkaHandlerResolver(HandlerResolver):
    def __init__(self, container: AsyncContainer) -> None:
        self._container = container

    async def resolve(self, handler_type: type[THandler]) -> THandler:
        return await self._container.get(handler_type)


class DishkaRequestHandlerFinder(RequestHandlerFinder):
    def __init__(self, container: AsyncContainer) -> None:
        self._container = container

    async def find(
        self,
        request_type: type[Request],
    ) -> type[RequestHandler] | None:
        for key in self._container.registry.factories:
            generic_type = extract_base_generic_type(key.type_hint)

            if generic_type and matches_generic_type(
                generic_type,
                RequestHandler,
                request_type,
            ):
                return key.type_hint

        return None


class DishkaNotificationHandlerFinder(NotificationHandlerFinder):
    def __init__(self, container: AsyncContainer) -> None:
        self._container = container

    async def find(
        self,
        notification_type: type[Notification],
    ) -> Iterable[type[NotificationHandler]]:
        handlers_types = []
        for key in self._container.registry.factories:
            generic_type = extract_base_generic_type(key.type_hint)

            if generic_type and matches_generic_type(
                generic_type,
                NotificationHandler,
                notification_type,
            ):
                handlers_types.append(key.type_hint)

        return handlers_types


def dispatcher_factory(
    handler_resolver: DishkaHandlerResolver,
    request_handler_finder: DishkaRequestHandlerFinder,
    notification_handler_finder: DishkaNotificationHandlerFinder,
) -> WithParents[Dispatcher]:
    return Dispatcher(
        handler_resolver,
        request_handler_finder,
        notification_handler_finder,
    )
