from abc import ABC, abstractmethod
from typing import TypeVar

TDependency = TypeVar("TDependency")


class Resolver(ABC):
    @abstractmethod
    async def resolve(
        self,
        dependency_type: type[TDependency],
    ) -> TDependency: ...
