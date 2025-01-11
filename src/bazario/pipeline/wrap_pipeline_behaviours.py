from functools import partial
from typing import Any, TypeAlias

from bazario.protocols.handle_next import HandleNext
from bazario.protocols.handler import NotificationHandler, RequestHandler
from bazario.protocols.pipeline_behaviour import PipelineBehaviour
from bazario.protocols.resolver import Resolver
from bazario.typing.aliases import TargetType

_HandlerType: TypeAlias = RequestHandler | NotificationHandler


def wrap_pipeline_behaviours(
    behaviours: list[PipelineBehaviour],
    handler: _HandlerType,
) -> HandleNext:
    def process_pipeline(
        resolver: Resolver,
        target: TargetType,
    ) -> Any:
        def handle_next(resolver: Resolver, target: TargetType) -> Any:
            return handler.handle(target)

        for behaviour in reversed(behaviours):
            handle_next = partial(behaviour.handle, handle_next=handle_next)

        return handle_next(resolver, target)

    return process_pipeline
