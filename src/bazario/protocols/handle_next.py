from typing import Protocol, TypeVar

from bazario.protocols.resolver import Resolver
from bazario.typing.aliases import TargetType

TRes_co = TypeVar("TRes_co", covariant=True)
TTarget_contra = TypeVar(
    "TTarget_contra",
    bound=TargetType,
    contravariant=True,
)


class HandleNext(Protocol[TTarget_contra, TRes_co]):
    def __call__(
        self,
        resolver: Resolver,
        target: TTarget_contra,
    ) -> TRes_co: ...
