from functools import partial
from typing import TypeAlias

from bazario.asyncio.protocols.handle_next import HandleNext
from bazario.asyncio.protocols.handler import (
    NotificationHandler,
    RequestHandler,
)
from bazario.asyncio.protocols.pipeline_behaviour import PipelineBehaviour
from bazario.asyncio.protocols.resolver import Resolver
from bazario.typing.type_vars import TRes_co, TTarget_contra

_HandlerType: TypeAlias = (
    RequestHandler[TTarget_contra, TRes_co]
    | NotificationHandler[TTarget_contra]
)


def wrap_pipeline_behaviours(
    behaviours: list[PipelineBehaviour[TTarget_contra, TRes_co]],
    handler: _HandlerType,
) -> HandleNext[TTarget_contra, TRes_co]:
    async def process_pipeline(
        resolver: Resolver,
        target: TTarget_contra,
    ) -> TRes_co:
        async def handle_next(
            resolver: Resolver,
            target: TTarget_contra,
        ) -> TRes_co:
            return await handler.handle(target)

        for behaviour in reversed(behaviours):
            handle_next = partial(behaviour.handle, handle_next=handle_next)

        return await handle_next(resolver, target)

    return process_pipeline
