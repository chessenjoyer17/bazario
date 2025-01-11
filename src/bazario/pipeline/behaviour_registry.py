from bazario.protocols.pipeline_behaviour import PipelineBehaviour
from bazario.typing.type_vars import TRes_co, TTarget_contra


class PipelineBehaviourRegistry:
    def __init__(self) -> None:
        self._behaviours: dict[
            type[TTarget_contra],
            list[PipelineBehaviour[TTarget_contra, TRes_co]],
        ] = {}

    def add_behaviours(
        self,
        target_type: type[TTarget_contra],
        *behaviours: PipelineBehaviour[TTarget_contra, TRes_co],
    ) -> None:
        self._behaviours.setdefault(target_type, []).extend(behaviours)

    def get_behaviours(
        self,
        target_type: type[TTarget_contra],
    ) -> list[PipelineBehaviour[TTarget_contra, TRes_co]]:
        return [
            behaviour
            for target, behaviours in self._behaviours.items()
            if issubclass(target_type, target)
            for behaviour in behaviours
        ]
