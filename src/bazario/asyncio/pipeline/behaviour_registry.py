from typing import Any, TypeVar

from bazario.asyncio.protocols.pipeline_behaviour import PipelineBehaviour
from bazario.typing.aliases import TargetType

TTarget = TypeVar("TTarget", bound=TargetType)


class PipelineBehaviourRegistry:
    def __init__(self) -> None:
        self._behaviours: dict[type, list[PipelineBehaviour]] = {}

    def add_behaviours(
        self,
        target_type: type[TTarget],
        *behaviours: PipelineBehaviour[TTarget, Any],
    ) -> None:
        self._behaviours.setdefault(target_type, []).extend(behaviours)

    def get_behaviours(
        self,
        target_type: type[TTarget],
    ) -> list[PipelineBehaviour[TTarget, Any]]:
        return [
            behaviour
            for target, behaviours in self._behaviours.items()
            if issubclass(target_type, target)
            for behaviour in behaviours
        ]
