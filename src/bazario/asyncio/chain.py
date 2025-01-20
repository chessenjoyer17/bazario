from collections.abc import Reversible
from typing import Any

from bazario.asyncio.abc.handler import NotificationHandler, RequestHandler
from bazario.asyncio.abc.pipeline_behavior import (
    HandleNext,
    PipelineBehavior,
)


def build_pipeline_behaviors_chain(
    handler: RequestHandler | NotificationHandler,
    behaviors: Reversible[PipelineBehavior],
) -> HandleNext:
    current_behavior: HandleNext = handler.handle

    for behavior in reversed(behaviors):
        current_behavior = _wrap_with_behavior(behavior, current_behavior)

    return current_behavior


def _wrap_with_behavior(
    behavior: PipelineBehavior,
    handle_next: HandleNext,
) -> HandleNext:
    async def wrapped_handler(request: Any) -> Any:
        return await behavior.handle(request, handle_next)

    return wrapped_handler
