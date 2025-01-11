from typing import Any, TypeVar

from bazario.protocols.pipeline_behavior import PipelineBehavior
from bazario.typing.aliases import TargetType

TTarget = TypeVar("TTarget", bound=TargetType)


class PipelineBehaviorRegistry:
    def __init__(self) -> None:
        self._Behaviors: dict[type, list[PipelineBehavior]] = {}

    def add_behaviors(
        self,
        target_type: type[TTarget],
        *behaviors: PipelineBehavior[TTarget, Any],
    ) -> None:
        self._Behaviors.setdefault(target_type, []).extend(behaviors)

    def get_behaviors(
        self,
        target_type: type[TTarget],
    ) -> list[PipelineBehavior[TTarget, Any]]:
        return [
            Behavior
            for target, Behaviors in self._Behaviors.items()
            if issubclass(target_type, target)
            for Behavior in Behaviors
        ]
