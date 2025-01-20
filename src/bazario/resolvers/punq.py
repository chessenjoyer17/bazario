from typing import TypeVar

from punq import Container

from bazario import Resolver

TDependency = TypeVar("TDependency")


class PunqResolver(Resolver):
    def __init__(self, container: Container) -> None:
        self._container = container

    def resolve(self, dependency_type: type[TDependency]) -> TDependency:
        return self._container.resolve(dependency_type)
