from typing import Protocol, runtime_checkable

from bazario.asyncio.type_vars import THandler


@runtime_checkable
class HandlerResolver(Protocol):
    async def resolve(self, handler_type: type[THandler]) -> THandler: ...
