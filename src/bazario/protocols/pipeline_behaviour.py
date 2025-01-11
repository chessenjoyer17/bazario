from typing import Protocol

from bazario.protocols.handle_next import HandleNext
from bazario.protocols.resolver import Resolver
from bazario.typing.type_vars import TRes_co, TTarget_contra


class PipelineBehaviour(Protocol[TTarget_contra, TRes_co]):
    def handle(
        self,
        resolver: Resolver,
        target: TTarget_contra,
        handle_next: HandleNext[TTarget_contra, TRes_co],
    ) -> TRes_co: ...
