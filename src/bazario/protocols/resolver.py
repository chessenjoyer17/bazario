from typing import Protocol, runtime_checkable

from bazario.type_vars import THandler


@runtime_checkable
class HandlerResolver(Protocol):
    def resolve(self, handler_type: type[THandler]) -> THandler: ...
