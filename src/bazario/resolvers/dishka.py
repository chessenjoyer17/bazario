from typing import TypeVar

from dishka import Container

from bazario import Resolver

T = TypeVar("T")


class DishkaResolver(Resolver):
    def __init__(self, container: Container) -> None:
        self._container = container

    def resolve(self, dependency_type: type[T]) -> T:
        return self._container.get(dependency_type)
