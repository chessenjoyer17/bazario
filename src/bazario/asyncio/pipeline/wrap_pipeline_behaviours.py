from functools import partial
from typing import Any, TypeAlias

from bazario.asyncio.protocols.handle_next import HandleNext
from bazario.asyncio.protocols.handler import (
    NotificationHandler,
    RequestHandler,
)
from bazario.asyncio.protocols.pipeline_behaviour import PipelineBehaviour
from bazario.asyncio.protocols.resolver import Resolver
from bazario.typing.aliases import TargetType

_HandlerType: TypeAlias = RequestHandler | NotificationHandler


def wrap_pipeline_behaviours(
    behaviours: list[PipelineBehaviour],
    handler: _HandlerType,
) -> HandleNext:
    async def process_pipeline(resolver: Resolver, target: TargetType) -> Any:
        async def handle_next(resolver: Resolver, target: TargetType) -> Any:
            return await handler.handle(target)

        for behaviour in reversed(behaviours):
            handle_next = partial(behaviour.handle, handle_next=handle_next)

        return await handle_next(resolver, target)

    return process_pipeline
