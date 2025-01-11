from typing import Protocol

from bazario.protocols.resolver import Resolver
from bazario.typing.type_vars import TRes_co, TTarget_contra


class HandleNext(Protocol[TTarget_contra, TRes_co]):
    async def __call__(
        self,
        resolver: Resolver,
        target: TTarget_contra,
    ) -> TRes_co: ...
