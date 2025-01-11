from typing import Protocol, TypeVar

from bazario.protocols.handle_next import HandleNext
from bazario.protocols.resolver import Resolver
from bazario.typing.aliases import TargetType

TRes = TypeVar("TRes")
TTarget = TypeVar("TTarget", bound=TargetType)


class PipelineBehaviour(Protocol[TTarget, TRes]):
    def handle(
        self,
        resolver: Resolver,
        target: TTarget,
        handle_next: HandleNext[TTarget, TRes],
    ) -> TRes: ...
