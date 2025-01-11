from typing import Protocol, runtime_checkable

from bazario.typing.type_vars import TDependency


@runtime_checkable
class Resolver(Protocol):
    async def resolve(
        self,
        dependency_type: type[TDependency],
    ) -> TDependency: ...
