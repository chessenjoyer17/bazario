__all__ = (
    "DishkaHandlerFinder",
    "DishkaResolver",
)

from collections.abc import Iterable

from dishka import AsyncContainer

from bazario import Notification, Request
from bazario.asyncio import (
    NotificationHandler,
    RequestHandler,
    Resolver,
)
from bazario.asyncio.protocols.finder import HandlerFinder
from bazario.typing.type_inspection import (
    extract_base_generic_type,
    matches_generic_type,
)
from bazario.typing.type_vars import TDependency


class DishkaResolver(Resolver):
    def __init__(self, container: AsyncContainer) -> None:
        self._container = container

    async def resolve(self, dependency_type: type[TDependency]) -> TDependency:
        return await self._container.get(dependency_type)


class DishkaHandlerFinder(HandlerFinder):
    def __init__(self, container: AsyncContainer) -> None:
        self._factories = container.registry.factories

    async def find_with_request(
        self,
        request_type: type[Request],
    ) -> type[RequestHandler] | None:
        for key in self._factories:
            generic_type = extract_base_generic_type(key.type_hint)

            matches = matches_generic_type(
                generic_type,
                RequestHandler,
                request_type,
            )

            if generic_type and matches:
                return key.type_hint

        return None

    async def find_with_notification(
        self,
        notification_type: type[Notification],
    ) -> Iterable[type[NotificationHandler]]:
        handler_types = []
        for key in self._factories:
            generic_type = extract_base_generic_type(key.type_hint)

            matches = matches_generic_type(
                generic_type,
                NotificationHandler,
                notification_type,
            )

            if generic_type and matches:
                handler_types.append(key.type_hint)

        return handler_types
