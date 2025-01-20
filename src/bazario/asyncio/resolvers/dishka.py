from typing import TypeVar

from dishka import AsyncContainer

from bazario.asyncio.abc.resolver import Resolver

T = TypeVar("T")


class DishkaResolver(Resolver):
    def __init__(self, container: AsyncContainer) -> None:
        self._container = container

    async def resolve(self, dependency_type: type[T]) -> T:
        return await self._container.get(dependency_type)
