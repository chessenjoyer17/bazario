from typing import Protocol, TypeVar

from bazario.asyncio.protocols.handle_next import HandleNext
from bazario.asyncio.protocols.resolver import Resolver
from bazario.typing.aliases import TargetType

TTarget = TypeVar("TTarget", bound=TargetType)
TRes = TypeVar("TRes")


class PipelineBehaviour(Protocol[TTarget, TRes]):
    async def handle(
        self,
        resolver: Resolver,
        target: TTarget,
        handle_next: HandleNext[TTarget, TRes],
    ) -> TRes: ...
